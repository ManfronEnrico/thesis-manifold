"""
UserPromptSubmit hook: branch guard
- If on main: extract topic from prompt, suggest branch name, inject interactive choice
- If on feature branch: inject short confirmation
- Output: JSON with assistantResponse or empty (pass-through)
"""
import sys
import json
import subprocess
import re

STOPWORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "is","are","was","were","be","been","being","have","has","had","do","does",
    "did","will","would","could","should","may","might","shall","can","need",
    "i","we","you","he","she","they","it","this","that","these","those",
    "my","our","your","his","her","their","its","me","us","him","them",
    "what","how","why","when","where","which","who","please","just","also",
    "want","like","going","work","make","get","let","now","new","about",
    "some","any","all","not","no","so","then","than","there","here","up",
    "im","ive","id","ill","dont","cant","wont","isnt","arent","wasnt",
}

PREFIX_KEYWORDS = {
    "thesis":   {"thesis","chapter","section","writing","draft","outline","introduction",
                 "conclusion","abstract","literature","review","srq","rq","argument","claim"},
    "data":     {"data","dataset","pipeline","script","analysis","preprocess","clean",
                 "feature","model","train","evaluate","nielsen","indeks","spss","csv"},
    "config":   {"config","settings","hook","skill","rule","integration","setup","install",
                 "zotero","notebooklm","gdrive","tooling","claude","branch"},
    "chore":    {"refactor","rename","reorganize","cleanup","hygiene","move","delete",
                 "remove","fix","update","docs","readme","map","structure"},
    "session":  set(),  # fallback
}

def get_branch():
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""

def extract_keywords(prompt: str, n: int = 4) -> list[str]:
    words = re.findall(r"[a-z]+", prompt.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 3][:n]

def pick_prefix(keywords: list[str]) -> str:
    for prefix, vocab in PREFIX_KEYWORDS.items():
        if prefix == "session":
            continue
        if any(k in vocab for k in keywords):
            return prefix
    return "session"

def slugify(keywords: list[str], max_words: int = 3) -> str:
    slug_words = [w for w in keywords if len(w) > 3][:max_words]
    return "-".join(slug_words) if slug_words else "work"

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    prompt = data.get("prompt", "") or ""
    branch = get_branch()

    # Already on a feature branch — brief confirmation, pass through
    if branch and branch != "main":
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "suppressedSystemPrompt": False,
                "additionalSystemPrompt": f"Git branch: ✓ {branch} — proceed normally."
            }
        }))
        sys.exit(0)

    # Detached HEAD or no git repo — pass through silently
    if not branch:
        sys.exit(0)

    # On main — build suggestion
    keywords = extract_keywords(prompt)
    prefix = pick_prefix(keywords)
    slug = slugify(keywords)
    suggested = f"{prefix}/{slug}"

    injection = f"""
BRANCH_GUARD TRIGGERED — respond to this BEFORE answering the user's question.

The user (and any collaborator reading this) is currently on the `main` branch.
`main` is reserved for stable, merged work. Active development should happen on a feature branch so that:
- Work can be reviewed before merging
- `main` stays clean and deployable at all times
- Collaborators can work in parallel without stepping on each other

Suggested branch based on the user's prompt:
  → {suggested}

Present the user with this exact interactive choice (keep it brief and friendly):

---
You're on `main`. Before we start, let's move to a branch.

Suggested: `{suggested}`

  [1] Create and switch to `{suggested}`  →  `git checkout -b {suggested}`
  [2] Use a different name (type it)
  [3] Stay on `main` (only if you're merging completed work)

Which would you like?
---

After the user responds:
- If [1]: run `git checkout -b {suggested}` via Bash and confirm success, then answer their question
- If [2]: use the name they provide, run `git checkout -b <name>`, confirm, then answer
- If [3]: ask "Are you sure? This is only recommended for merge/integration work." — if confirmed, proceed and note you're on main
"""

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "suppressedSystemPrompt": False,
            "additionalSystemPrompt": injection.strip()
        }
    }))

if __name__ == "__main__":
    main()
