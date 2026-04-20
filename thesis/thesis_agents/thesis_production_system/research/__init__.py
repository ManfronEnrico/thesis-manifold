"""Research layer — NotebookLM integration for thesis support."""

from .notebooklm_access import NotebookLMAccess, QuestionResult, ResearchResult
from .citation_confidence import CitationConfidence, ConfidenceLevel

__all__ = [
    "NotebookLMAccess",
    "CitationConfidence",
    "QuestionResult",
    "ResearchResult",
    "ConfidenceLevel",
]
