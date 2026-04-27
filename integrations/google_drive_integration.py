"""
Google Drive integration for thesis paper management.

Provides two access patterns:
1. MCP (OAuth) - for interactive queries via Claude
2. Service Account (JSON key) - for programmatic access, automation, and team sharing

Usage:
    # With OAuth token (MCP - already authenticated)
    from src.google_drive_integration import GoogleDriveAPI
    api = GoogleDriveAPI()
    papers = api.list_papers_with_metadata()

    # With Service Account - Option A: file path
    api = GoogleDriveAPI(service_account_key="/path/to/service-account.json")

    # With Service Account - Option B: env var (JSON string)
    api = GoogleDriveAPI(service_account_key_json=os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY"))

    papers = api.list_papers_with_metadata()  # Includes importance classification
    new_files = api.detect_new_papers()
"""

import os
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from pathlib import Path


class GoogleDriveAPI:
    """Unified interface for Google Drive paper management."""

    def __init__(
        self,
        service_account_key: Optional[str] = None,
        service_account_key_json: Optional[str] = None,
        papers_folder_id: str = "1cwK41FAJM_3WlpO-_9cOYMF04cjhV_LD",
    ):
        """
        Initialize Google Drive API client.

        Args:
            service_account_key: Path to service account JSON file.
            service_account_key_json: JSON string (from env var). Takes precedence over service_account_key.
            papers_folder_id: Google Drive folder ID for papers root.
        """
        self.papers_folder_id = papers_folder_id
        self.service_account_key = service_account_key
        self.service_account_key_json = service_account_key_json
        self.client = None
        self.importance_levels = {
            "0_not_relevant": "not_relevant",
            "1_essential": "essential",
            "2_high": "high",
            "UNSURE": "unsure",
        }

        if service_account_key_json or service_account_key:
            self._init_service_account()

    def _init_service_account(self):
        """Initialize service account client from file or env var."""
        try:
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build

            if self.service_account_key_json:
                if isinstance(self.service_account_key_json, str):
                    service_account_info = json.loads(self.service_account_key_json)
                else:
                    service_account_info = self.service_account_key_json
            elif self.service_account_key:
                with open(self.service_account_key, "r") as f:
                    service_account_info = json.load(f)
            else:
                raise RuntimeError("No service account credentials provided")

            credentials = Credentials.from_service_account_info(
                service_account_info,
                scopes=["https://www.googleapis.com/auth/drive.readonly"]
            )
            self.client = build("drive", "v3", credentials=credentials)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize service account: {e}")

    def list_papers_with_metadata(self) -> List[Dict[str, Any]]:
        """
        List all papers in the papers folder with metadata and importance classification.

        Recursively searches through importance folders (0_not_relevant, 1_essential, 2_high, UNSURE)
        and returns PDFs with importance level attached.

        Returns:
            List of dicts with keys: name, id, mimeType, createdTime, modifiedTime, size,
                                     webViewLink, importance, folder_path
        """
        if not self.client:
            raise RuntimeError(
                "Service account not initialized. "
                "Use GoogleDriveAPI(service_account_key='...') or "
                "GoogleDriveAPI(service_account_key_json=os.getenv('GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY'))"
            )

        all_papers = []

        try:
            # Get direct children of papers folder (importance level folders)
            results = self.client.files().list(
                q=f"'{self.papers_folder_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'",
                spaces="drive",
                fields="files(id, name)",
                pageSize=100
            ).execute()

            importance_folders = results.get("files", [])

            # For each importance folder, list all PDFs
            for folder in importance_folders:
                folder_name = folder.get("name", "")
                folder_id = folder.get("id")

                # Map folder name to importance level
                importance = self.importance_levels.get(folder_name, "unknown")

                # List files in this importance folder
                paper_results = self.client.files().list(
                    q=f"'{folder_id}' in parents and trashed=false",
                    spaces="drive",
                    fields="files(id, name, mimeType, createdTime, modifiedTime, size, webViewLink)",
                    pageSize=100
                ).execute()

                papers = paper_results.get("files", [])
                enriched = self._enrich_metadata(papers, importance, folder_name)
                all_papers.extend(enriched)

            return all_papers

        except Exception as e:
            raise RuntimeError(f"Failed to list papers: {e}")

    def detect_new_papers(
        self,
        minutes_since: int = 60,
        cached: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Detect papers uploaded or modified in the last N minutes.

        Args:
            minutes_since: Look back this many minutes (default 60).
            cached: Use cached metadata if available (faster, less API calls).

        Returns:
            List of new/modified papers with metadata and importance.
        """
        from datetime import timedelta

        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes_since)
        cutoff_iso = cutoff_time.isoformat() + "Z"

        if not self.client:
            raise RuntimeError("Service account not initialized.")

        all_new = []

        try:
            # Get importance folders
            results = self.client.files().list(
                q=f"'{self.papers_folder_id}' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'",
                spaces="drive",
                fields="files(id, name)",
                pageSize=100
            ).execute()

            importance_folders = results.get("files", [])

            # Search for new files in each folder
            for folder in importance_folders:
                folder_name = folder.get("name", "")
                folder_id = folder.get("id")
                importance = self.importance_levels.get(folder_name, "unknown")

                paper_results = self.client.files().list(
                    q=(
                        f"'{folder_id}' in parents and "
                        f"(createdTime > '{cutoff_iso}' or modifiedTime > '{cutoff_iso}') and "
                        f"trashed=false"
                    ),
                    spaces="drive",
                    fields="files(id, name, mimeType, createdTime, modifiedTime, size, webViewLink)",
                    pageSize=50
                ).execute()

                papers = paper_results.get("files", [])
                enriched = self._enrich_metadata(papers, importance, folder_name)
                all_new.extend(enriched)

            return all_new

        except Exception as e:
            raise RuntimeError(f"Failed to detect new papers: {e}")

    def _enrich_metadata(
        self,
        files: List[Dict],
        importance: str,
        folder_path: str
    ) -> List[Dict[str, Any]]:
        """Add computed fields to file metadata."""
        for f in files:
            f["created_datetime"] = datetime.fromisoformat(f["createdTime"].replace("Z", "+00:00"))
            f["modified_datetime"] = datetime.fromisoformat(f["modifiedTime"].replace("Z", "+00:00"))

            if "size" in f:
                size_bytes = int(f["size"])
                f["size_mb"] = round(size_bytes / (1024 * 1024), 2)
            else:
                f["size_mb"] = None

            f["extension"] = Path(f["name"]).suffix.lower() if "." in f["name"] else None
            f["importance"] = importance
            f["folder_path"] = folder_path

        return files

    def get_folder_stats(self) -> Dict[str, Any]:
        """Get summary statistics about papers by importance level."""
        papers = self.list_papers_with_metadata()

        stats_by_importance = {}
        for importance in set(p.get("importance") for p in papers):
            papers_in_level = [p for p in papers if p.get("importance") == importance]
            pdf_count = sum(1 for p in papers_in_level if p.get("extension") == ".pdf")
            total_size = sum(p.get("size_mb", 0) for p in papers_in_level if p.get("size_mb"))

            stats_by_importance[importance] = {
                "count": len(papers_in_level),
                "pdf_count": pdf_count,
                "total_size_mb": round(total_size, 2),
            }

        return {
            "total_files": len(papers),
            "pdf_count": sum(1 for p in papers if p.get("extension") == ".pdf"),
            "total_size_mb": round(sum(p.get("size_mb", 0) for p in papers if p.get("size_mb")), 2),
            "by_importance": stats_by_importance,
            "oldest_file": min(papers, key=lambda p: p["created_datetime"])["name"] if papers else None,
            "newest_file": max(papers, key=lambda p: p["created_datetime"])["name"] if papers else None,
        }

    def get_file_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a paper by name."""
        papers = self.list_papers_with_metadata()
        for p in papers:
            if p["name"].lower() == name.lower():
                return p
        return None

    def get_papers_by_importance(self, importance: str) -> List[Dict[str, Any]]:
        """Get all papers at a specific importance level."""
        papers = self.list_papers_with_metadata()
        return [p for p in papers if p.get("importance") == importance]


def quick_list_papers() -> List[Dict[str, Any]]:
    """Quick way to list papers (uses GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY env var)."""
    key_json = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY")
    if not key_json:
        raise ValueError("Set GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY env var")

    api = GoogleDriveAPI(service_account_key_json=key_json)
    return api.list_papers_with_metadata()


def quick_detect_new(minutes: int = 60) -> List[Dict[str, Any]]:
    """Quick way to detect new papers (uses GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY env var)."""
    key_json = os.getenv("GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY")
    if not key_json:
        raise ValueError("Set GOOGLE_DRIVE_SERVICE_ACCOUNT_KEY env var")

    api = GoogleDriveAPI(service_account_key_json=key_json)
    return api.detect_new_papers(minutes_since=minutes)


if __name__ == "__main__":
    papers = quick_list_papers()
    print(f"Found {len(papers)} papers:")
    for p in papers:
        print(f"  [{p['importance']:12}] {p['name']} ({p['size_mb']} MB, modified {p['modified_datetime']})")
