"""
Biweekly Report Generator - FastAPI Backend
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
import os
import re
from collections import defaultdict
from typing import Optional, Tuple, List, Dict, Set, Any, TypedDict
from datetime import datetime

try:
    import anthropic  # type: ignore
    HAS_ANTHROPIC = True
except ImportError:
    anthropic = None  # type: ignore
    HAS_ANTHROPIC = False

try:
    from openai import OpenAI  # type: ignore
    HAS_OPENAI = True
except ImportError:
    OpenAI = None  # type: ignore
    HAS_OPENAI = False

app = FastAPI(title="Biweekly Report Generator API")

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project to Repository Mapping
PROJECT_REPOS = {
    "Ooo": [
        "Tokamak-zk-EVM", "Tokamak-zk-EVM-contracts", "private-app-channel-manager",
        "tokamak-zkp-channel-manager-new", "TokamakL2JS", "Tokamak-zk-EVM-landing-page",
    ],
    "Eco": [
        "ton-staking-v2", "tokamak-economics-whitepaper-v2", "RAT-frontend",
        "staking-community-version", "tokamak-dao-v2", "tokamak-landing-page",
    ],
    "TRH": [
        "trh-sdk", "trh-backend", "trh-platform-ui", "DRB-node",
        "tokamak-thanos", "tokamak-rollup-hub-v2", "tokamak-thanos-stack", "tokamak-thanos-geth",
    ],
}

SECTION_INFO_TECHNICAL = {
    "Ooo": {
        "number": "2.2",
        "title": "Zero-Knowledge Proof-Based Private App Channels",
        "overview_url": "https://medium.com/tokamak-network/project-tokamak-zk-evm-67483656fd21",
        "context": "Tokamak Private App Channels enable users to create private channels for ZK-based transactions.",
    },
    "Eco": {
        "number": "2.3",
        "title": "Developing Decentralized Staking and Governance",
        "overview_url": "https://tokamak.notion.site/49e44e989c514bd683e077c01cc8f143?pvs=25",
        "context": "This team handles TON staking economics, whitepaper development, RAT verification system, and DAO governance.",
    },
    "TRH": {
        "number": "2.4",
        "title": "Advancing Developer-Centric Appchain Infrastructure",
        "overview_url": "https://tokamak.notion.site/1433390669554ae5b09e400f4c9c0fd4?pvs=25",
        "context": "Tokamak Rollup Hub provides on-demand L2 deployment infrastructure.",
    },
}

SECTION_INFO_PUBLIC = {
    "Ooo": {
        "number": "2.2",
        "title": "Zero-Knowledge Proof-Based Private App Channels",
        "context": "Revolutionary privacy technology that keeps your transactions completely confidential while maintaining full security on Ethereum. Users can conduct private DeFi transactions without revealing sensitive financial data.",
        "business_focus": "privacy technology, user experience, DeFi integration, data protection",
    },
    "Eco": {
        "number": "2.3",
        "title": "TON Staking & Governance: Building a Sustainable Token Economy",
        "context": "Staking rewards for TON holders, transparent governance, economic security.",
        "business_focus": "staking rewards, governance participation, tokenomics",
    },
    "TRH": {
        "number": "2.4",
        "title": "Tokamak Rollup Hub: One-Click Layer 2 Deployment",
        "context": "Rapid L2 deployment, cost-effective scaling, enterprise-ready infrastructure.",
        "business_focus": "ease of deployment, enterprise adoption, scalability",
    },
}

SECTION_INFO_INDIVIDUAL_TECHNICAL = {
    "number": "2.5",
    "title": "Individual Contributions",
    "context": "Individual project work outside the three core initiatives.",
}

SECTION_INFO_INDIVIDUAL_PUBLIC = {
    "number": "2.5",
    "title": "Individual Contributions",
    "context": "Individual project progress that complements the main initiatives.",
}


TOKAMAK_BASE_URL = os.environ.get("TOKAMAK_BASE_URL", "https://api.ai.tokamak.network")
TOKAMAK_API_KEY = os.environ.get("TOKAMAK_API_KEY", "")
TOKAMAK_MODEL = os.environ.get("TOKAMAK_MODEL", "gpt-5.2-pro")


def has_tokamak_client() -> bool:
    return bool(TOKAMAK_API_KEY) and HAS_OPENAI and OpenAI is not None


def generate_with_tokamak(prompt: str, max_tokens: int) -> Optional[str]:
    if not has_tokamak_client() or OpenAI is None:
        return None
    client = OpenAI(base_url=TOKAMAK_BASE_URL, api_key=TOKAMAK_API_KEY)
    try:
        response = client.chat.completions.create(
            model=TOKAMAK_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.4,
        )
        content = response.choices[0].message.content if response.choices else None
        return content.strip() if content else None
    except Exception:
        return None


def generate_with_anthropic(prompt: str, max_tokens: int) -> Optional[str]:
    if not HAS_ANTHROPIC or not os.environ.get('ANTHROPIC_API_KEY') or anthropic is None:
        return None
    client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))
    try:
        response = client.messages.create(
            model="claude-sonnet-4.5",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        text = getattr(response.content[0], "text", "").strip()
        return text or None
    except Exception:
        return None


def generate_with_llm(prompt: str, max_tokens: int) -> Optional[str]:
    tokamak_response = generate_with_tokamak(prompt, max_tokens)
    if tokamak_response:
        return tokamak_response
    return generate_with_anthropic(prompt, max_tokens)


def get_project_for_repo(repo_name: str) -> Optional[str]:
    for project, repos in PROJECT_REPOS.items():
        if repo_name in repos:
            return project
    return None


def parse_timestamp(timestamp: str) -> Optional[datetime]:
    if not timestamp:
        return None
    try:
        return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def normalize_member_identity(member_name: str, member_email: str) -> Tuple[str, str]:
    name = (member_name or "").strip('"').strip()
    email = (member_email or "").strip('"').strip()
    email_local = email.split("@")[0] if "@" in email else ""

    use_name = bool(name) and name.isascii() and re.search(r"[A-Za-z]", name)
    label = name if use_name else (email_local or name)
    member_id = (email_local or label).lower().replace(" ", "-")
    return member_id, label


class ActivityGroup(TypedDict):
    commits: List[Dict[str, Any]]
    prs: List[Dict[str, Any]]
    repos: Set[str]


def parse_csv_content(content: str) -> dict:
    """Parse CSV content and return GitHub activities grouped by project, repo, and member."""
    project_data: defaultdict[str, ActivityGroup] = defaultdict(lambda: {"commits": [], "prs": [], "repos": set()})
    repo_data: defaultdict[str, ActivityGroup] = defaultdict(lambda: {"commits": [], "prs": [], "repos": set()})
    individual_data: defaultdict[str, ActivityGroup] = defaultdict(lambda: {"commits": [], "prs": [], "repos": set()})
    members: Dict[str, Dict[str, str]] = {}
    timestamps: List[datetime] = []

    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        if row.get('source') != 'github':
            continue

        repo = row.get('repository', '').strip('"')
        if not repo:
            continue

        timestamp = row.get('timestamp', '')
        parsed_time = parse_timestamp(timestamp)
        if parsed_time:
            timestamps.append(parsed_time)

        member_name = row.get('member_name', '').strip('"')
        member_email = row.get('member_email', '').strip('"')
        member_id, member_label = normalize_member_identity(member_name, member_email)
        if member_id and member_id not in members:
            members[member_id] = {
                "id": member_id,
                "label": member_label,
                "name": member_name,
                "email": member_email,
            }

        project = get_project_for_repo(repo)

        entry_type = row.get('type', '')
        message = row.get('message', '').strip('"')
        title = row.get('title', '').strip('"')
        sha = row.get('sha', '').strip('"')
        pr_number = row.get('pr_number', '').strip('"')
        additions = row.get('additions', '0') or '0'
        deletions = row.get('deletions', '0') or '0'
        state = row.get('state', '').strip('"')

        repo_target = repo_data[repo]
        repo_target["repos"].add(repo)

        if project:
            target = project_data[project]
        else:
            if not member_id:
                continue
            target = individual_data[member_id]

        target["repos"].add(repo)

        if entry_type == 'commit' and message:
            if message.lower().startswith('merge '):
                continue
            entry = {
                "repo": repo,
                "message": message.split('\n')[0][:200],
                "sha": sha[:8] if sha else "",
                "timestamp": timestamp,
                "additions": int(additions),
                "deletions": int(deletions),
                "member_id": member_id,
            }
            target["commits"].append(entry)
            repo_target["commits"].append(entry)
        elif entry_type == 'pull_request' and title:
            entry = {
                "repo": repo,
                "title": title,
                "pr_number": pr_number,
                "state": state,
                "timestamp": timestamp,
                "member_id": member_id,
            }
            target["prs"].append(entry)
            repo_target["prs"].append(entry)

    def serialize_group(data_map: Dict[str, ActivityGroup]) -> Dict[str, Dict[str, Any]]:
        result: Dict[str, Dict[str, Any]] = {}
        for key, data in data_map.items():
            result[key] = {
                "commits": data["commits"],
                "prs": data["prs"],
                "repos": list(data["repos"]),
            }
        return result

    return {
        "projects": serialize_group(project_data),
        "repos": serialize_group(repo_data),
        "individuals": serialize_group(individual_data),
        "members": list(members.values()),
        "timestamps": timestamps,
    }


def detect_scope_from_timestamps(timestamps: List[datetime]) -> Tuple[str, Optional[str], Optional[str], Optional[int]]:
    if not timestamps:
        return "biweekly", None, None, None
    start = min(timestamps)
    end = max(timestamps)
    days = (end.date() - start.date()).days + 1
    if days <= 16:
        scope = "biweekly"
    elif days <= 45:
        scope = "monthly"
    elif days <= 110:
        scope = "quarterly"
    else:
        scope = "quarterly"
    return scope, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), days


def format_period_label(scope: str, days: Optional[int]) -> str:
    if scope == "biweekly":
        return "Bi-Weekly"
    if scope == "monthly":
        return "Monthly"
    if scope == "quarterly":
        return "Quarterly"
    if scope == "weekly":
        return "Weekly"
    if days:
        return f"{days}-Day"
    return "Custom"


def format_date_label(date_str: Optional[str]) -> str:
    if not date_str:
        return ""
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d")
        return parsed.strftime("%b %d")
    except ValueError:
        return date_str


def build_report_title(scope: str, start_date: Optional[str], end_date: Optional[str], days: Optional[int]) -> str:
    period_label = format_period_label(scope, days)
    start_label = format_date_label(start_date)
    end_label = format_date_label(end_date)
    date_range = f"{start_label} – {end_label}" if start_label and end_label else ""
    if date_range:
        return f"Tokamak Network {period_label} Report: {date_range}"
    return f"Tokamak Network {period_label} Report"


def headline_phrase(text: str) -> str:
    cleaned = re.sub(r"\.+$", "", text.strip())
    cleaned = re.sub(
        r"^(Launched|Improved|Delivered|Integrated|Strengthened|Updated|Added|Implemented|Built)\s+",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    words = cleaned.split()
    if not words:
        return ""
    return " ".join(words[:4])


def build_report_headline(summaries: Dict[str, Dict[str, Any]], report_type: str) -> str:
    themes = {
        "Ooo": "Privacy",
        "Eco": "Staking & Governance",
        "TRH": "Rollup Infrastructure",
    }

    keyword_patterns = {
        "Ooo": [
            ("Private Transactions", ["private", "channel", "proof", "zk", "confidential"]),
            ("Secure Wallet Experiences", ["wallet", "snap", "extension", "menu"]),
            ("Proof Performance", ["prove", "prover", "sigma", "optimiz", "cache"]),
        ],
        "Eco": [
            ("Fast Withdrawal", ["withdrawal", "fast withdrawal", "rat"]),
            ("Staking Infrastructure", ["staking", "validator", "seig", "delegate"]),
            ("Governance UX", ["dao", "governance", "delegate", "voting"]),
        ],
        "TRH": [
            ("Mainnet Readiness", ["mainnet", "pre-deployment", "safety", "validation"]),
            ("Operational Tooling", ["backup", "monitor", "dashboard", "logs"]),
            ("Deployment Experience", ["deploy", "sdk", "rollup", "hub"]),
        ],
    }

    def pick_keyword(project: str, deliverables: List[str]) -> str:
        patterns = keyword_patterns.get(project, [])
        joined = " ".join(deliverables).lower()
        for keyword, needles in patterns:
            if any(needle in joined for needle in needles):
                return keyword
        return themes.get(project, project)

    keywords = []
    for project in ["Ooo", "Eco", "TRH"]:
        summary = summaries.get(project)
        if not summary:
            continue

        if report_type == "public":
            deliverables = extract_public_pr_deliverables(summary.get("merged_pr_list", []), 2)
            if not deliverables:
                deliverables = extract_public_deliverables(summary.get("top_commits", []), 2)
        else:
            deliverables = extract_deliverables(summary.get("top_commits", []), 2, public=False, with_links=False)

        keywords.append(pick_keyword(project, deliverables))

    if keywords:
        unique = []
        for keyword in keywords:
            if keyword not in unique:
                unique.append(keyword)
        return f"{', '.join(unique)} Progress"
    return f"{themes['Ooo']}, {themes['Eco']}, and {themes['TRH']} Progress"


def prepare_summary(project: str, data: Dict[str, Any]) -> dict:
    """Prepare summary for a project or repository."""
    commits = data['commits']
    prs = data['prs']
    repos = data['repos']
    if isinstance(repos, set):
        repos = list(repos)

    commits_sorted = sorted(commits, key=lambda x: x['additions'] + x['deletions'], reverse=True)

    seen = set()
    top_commits = []
    for c in commits_sorted:
        key = c['message'][:50].lower()
        if key not in seen:
            seen.add(key)
            top_commits.append(c)
        if len(top_commits) >= 30:
            break

    merged_prs = [p for p in prs if p['state'] == 'MERGED']

    return {
        "project": project,
        "repos": repos,
        "total_commits": len(commits),
        "total_prs": len(prs),
        "merged_prs": len(merged_prs),
        "top_commits": top_commits,
        "merged_pr_list": merged_prs[:15],
    }


def repo_sort_key(summary: dict) -> tuple:
    return (summary.get("total_commits", 0), summary.get("merged_prs", 0), len(summary.get("repos", [])))


def simplify_message(message: str) -> str:
    cleaned = re.sub(r"^(feat|fix|refactor|test|docs|chore|ci|merge)(\([^)]+\))?:\s*", "", message, flags=re.IGNORECASE)
    cleaned = re.sub(r"^\[[^\]]+\]\s*", "", cleaned)
    cleaned = cleaned.strip()
    return cleaned[:140]


def initial_commit_replacement(repo: Optional[str], technical: bool) -> str:
    module_hint = repo.replace("-", "/") if repo else "the project"
    if technical:
        return f"Established the foundation for {module_hint}"
    return "Launched the first architectural draft"


def sanitize_initial_commit(text: str, repo: Optional[str], technical: bool) -> str:
    if "initial commit" in text.lower():
        return initial_commit_replacement(repo, technical)
    return text


def sentence_case(text: str) -> str:
    if not text:
        return text
    cleaned = text.strip()
    if not cleaned:
        return cleaned
    return cleaned[0].upper() + cleaned[1:]


def normalize_technical_highlight_phrase(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(
        r"^(add|adds|added)\s+",
        "Added ",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"^(integrate|integrates|integrated)\s+",
        "Integrated ",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"^(remove|removes|removed)\s+",
        "Removed ",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"^(update|updates|updated)\s+",
        "Updated ",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"^(fix|fixed|fixes)\s+",
        "Fixed ",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(
        r"^(implement|implements|implemented)\s+",
        "Implemented ",
        cleaned,
        flags=re.IGNORECASE,
    )
    return cleaned


def normalize_public_deliverable(message: str) -> str:
    cleaned = simplify_message(message)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return ""

    cleaned = re.sub(r"^(feature|feat)\s*:\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*\(?#?\d+\)?$", "", cleaned).strip()

    replacements = [
        (r"^(add|added)\s+", "Launched "),
        (r"^(update|updated|improve|improved)\s+", "Improved "),
        (r"^(fix|fixed|resolve|resolved)\s+", "Strengthened "),
        (r"^(integrate|integrated)\s+", "Integrated "),
        (r"^(implement|implemented|build|built)\s+", "Delivered "),
    ]

    for pattern, replacement in replacements:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

    return sentence_case(cleaned)


def is_public_deliverable(text: str) -> bool:
    if not text:
        return False

    lower = text.lower()
    if len(text.split()) < 3:
        return False
    if lower.startswith(("with ", "and ", "for ", "to ")):
        return False
    if re.search(r"[a-z][A-Z]", text):
        return False

    skip_terms = [
        "playwright",
        "debugger",
        "timing",
        "instrument",
        "benchmark",
        "profile",
        "test",
        "e2e",
        "ci",
        "refactor",
        "chore",
        "merge",
        "conflict",
        "submodule",
        "branch",
        "json",
        "config",
        "script",
        "plan",
        "roadmap",
        "delete",
        "deleted",
        "remove",
        "removed",
        "cleanup",
        "docs",
        "documentation",
        "readme",
        "guide",
        "sdk",
        "api",
        "rpc",
        "contract",
        "contracts",
    ]
    return not any(term in lower for term in skip_terms)


def extract_public_deliverables(commits: List[Dict[str, Any]], limit: int) -> List[str]:
    seen: Set[str] = set()
    deliverables: List[str] = []
    for commit in commits:
        msg = commit.get("message", "")
        if not msg:
            continue
        msg = sanitize_initial_commit(msg, commit.get("repo"), technical=False)
        if msg.lower().startswith("launched the first architectural draft"):
            key = msg.lower()
            if key not in seen:
                seen.add(key)
                deliverables.append(msg)
            if len(deliverables) >= limit:
                break
            continue
        cleaned = normalize_public_deliverable(msg)
        if not is_public_deliverable(cleaned):
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        deliverables.append(cleaned)
        if len(deliverables) >= limit:
            break
    return deliverables


def normalize_pr_title(title: str) -> str:
    cleaned = title.strip()
    cleaned = re.sub(
        r"^(feat|feature|fix|refactor|docs|chore|ci)(\([^)]+\))?:\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s*\(?#?\d+\)?$", "", cleaned).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return sentence_case(cleaned)


def normalize_public_phrase(text: str) -> str:
    cleaned = normalize_pr_title(text)
    cleaned = re.sub(r"\b(merge|chore|refactor|ci|tests?|docs?|documentation)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return sentence_case(cleaned)


def choose_public_verb(text: str) -> str:
    lower = text.lower()
    if any(keyword in lower for keyword in ["launch", "release", "introduce"]):
        return "Launched"
    if any(keyword in lower for keyword in ["secure", "safety", "guard", "validation"]):
        return "Secured"
    if any(keyword in lower for keyword in ["expand", "scale", "increase"]):
        return "Expanded"
    if any(keyword in lower for keyword in ["optimize", "streamline", "refine"]):
        return "Streamlined"
    if any(keyword in lower for keyword in ["improve", "update", "upgrade", "enhance"]):
        return "Improved"

    verbs = ["Improved", "Launched", "Secured", "Expanded", "Streamlined"]
    return verbs[sum(ord(c) for c in text) % len(verbs)]


def target_from_repo(repo_name: str) -> str:
    name = repo_name.lower()
    if "staking" in name:
        return "staking experience"
    if "dao" in name or "governance" in name:
        return "governance workflows"
    if "rollup" in name or "hub" in name:
        return "rollup deployment flows"
    if "wallet" in name or "snap" in name:
        return "wallet experience"
    if "sdk" in name:
        return "developer tooling"
    if "infra" in name or "node" in name:
        return "infrastructure reliability"
    return "user experience"


def rewrite_public_jargon(text: str, repo_name: str = "") -> str:
    replacements = [
        (r"\b(ui fixes?|translations?)\b", "Improved user accessibility and localization"),
        (r"\bbug fixes?\b|\brefactor(ing)?\b", "Enhanced system stability and code reliability"),
        (r"\bbackend updates?\b", "Strengthened core infrastructure for better performance"),
        (r"\bwallet experience\b", "Refined secure transaction workflows for users"),
        (r"\bfiles? via upload\b", "Archived historical records"),
        (r"\babis? files?\b", "contract interfaces"),
        (r"restructure to pnpm|pnpm monorepo", "optimized development environment"),
    ]
    updated = text
    for pattern, replacement in replacements:
        updated = re.sub(pattern, replacement, updated, flags=re.IGNORECASE)
    if repo_name:
        updated = re.sub(
            r"Improved user-facing experience",
            f"Improved {target_from_repo(repo_name)}",
            updated,
            flags=re.IGNORECASE,
        )
    return updated


def publicize_deliverable(text: str) -> str:
    cleaned = normalize_public_phrase(text)
    lower = cleaned.lower()
    if not cleaned:
        return ""

    if any(keyword in lower for keyword in ["mainnet", "pre-deployment", "safety", "validation"]):
        return "Improved mainnet readiness and deployment safety"
    if any(keyword in lower for keyword in ["monitor", "dashboard", "observability", "logs"]):
        return "Improved operational visibility with monitoring tools"
    if any(keyword in lower for keyword in ["staking", "validator", "delegate", "reward"]):
        return "Improved staking experience and validator operations"
    if any(keyword in lower for keyword in ["withdrawal", "fast withdrawal"]):
        return "Improved fast withdrawal reliability and speed"
    if any(keyword in lower for keyword in ["wallet", "snap", "extension"]):
        return "Launched safer wallet experiences for private transactions"
    if any(keyword in lower for keyword in ["privacy", "zk", "proof", "channel"]):
        return "Improved privacy tooling for secure transactions"
    if any(keyword in lower for keyword in ["rollup", "deploy", "hub", "sdk"]):
        return "Improved rollup deployment experience"

    if cleaned.lower().startswith(("add ", "added ", "implement ", "implemented ", "build ", "built ")):
        return f"Launched {cleaned.lower().split(' ', 1)[1]}"
    if cleaned.lower().startswith(("update ", "updated ", "improve ", "improved ", "enhance ", "enhanced ")):
        return f"Improved {cleaned.lower().split(' ', 1)[1]}"
    if cleaned.lower().startswith(("fix ", "fixed ", "resolve ", "resolved ")):
        return f"Secured {cleaned.lower().split(' ', 1)[1]}"

    verb = choose_public_verb(cleaned)
    return f"{verb} {cleaned[0].lower() + cleaned[1:]}"


def ensure_public_verb(text: str) -> str:
    if not text:
        return text
    lower = text.lower()
    if lower.startswith(("launched ", "improved ", "secured ", "expanded ", "streamlined ", "delivered ")):
        return text
    return f"Improved {text[0].lower() + text[1:]}"


def diversify_public_verb(text: str, repo_name: str = "") -> str:
    if not text or not repo_name:
        return text
    match = re.match(r"^Improved\s+(.+)$", text, flags=re.IGNORECASE)
    if not match:
        return text
    lower = text.lower()
    if any(keyword in lower for keyword in ["launch", "release", "introduce"]):
        return text

    preferred = None
    if any(keyword in lower for keyword in ["security", "secure", "safety", "validation", "hardening"]):
        preferred = "Secured"
    elif any(keyword in lower for keyword in ["deployment", "rollup", "pipeline", "workflow", "tooling"]):
        preferred = "Streamlined"
    elif any(keyword in lower for keyword in ["staking", "governance", "delegate", "reward"]):
        preferred = "Strengthened"
    elif any(keyword in lower for keyword in ["support", "coverage", "compatibility", "integration"]):
        preferred = "Expanded"

    verbs = ["Improved", "Strengthened", "Expanded", "Streamlined", "Secured"]
    verb = preferred or verbs[sum(ord(c) for c in repo_name) % len(verbs)]
    if verb == "Improved":
        return text
    return f"{verb} {match.group(1)}"


def enrich_public_deliverable(text: str, project: str, repo_name: str = "") -> str:
    if not text:
        return text

    lower = text.lower()
    if "setup" in lower and "bug" in lower:
        return "Secured the setup flow to reduce onboarding friction"
    if all(token in lower for token in ["usdt", "usdc", "ton"]):
        return "Expanded supported assets (USDT, USDC, TON) for private transfers"

    if len(text.split()) < 4:
        fallback = {
            "Ooo": "Improved privacy and transaction safety for users",
            "Eco": "Improved staking and governance experience for participants",
            "TRH": "Improved deployment reliability for rollup builders",
        }
        if repo_name:
            return f"Improved {target_from_repo(repo_name)}"
        return fallback.get(project, "Improved user-facing experience")

    return text


def derive_public_theme(summaries: Dict[str, Dict[str, Any]]) -> str:
    keyword_patterns = [
        ("Staking", ["staking", "validator", "delegate", "seig", "reward", "vton"]),
        ("Governance", ["governance", "dao", "voting", "proposal"]),
        ("Privacy", ["privacy", "zk", "proof", "confidential", "private"]),
        ("Wallet", ["wallet", "snap", "extension"]),
        ("Infrastructure", ["infrastructure", "node", "deployment", "rollup", "hub", "sdk"]),
        ("Performance", ["optimiz", "performance", "throughput", "latency"]),
        ("Security", ["security", "secure", "harden", "safety", "validation"]),
    ]

    deliverables: List[str] = []
    entries = sorted(summaries.items(), key=lambda item: repo_sort_key(item[1]), reverse=True)
    for _, summary in entries[:3]:
        deliverables.extend(extract_public_pr_deliverables(summary.get("merged_pr_list", []), 2))
        if len(deliverables) < 4:
            deliverables.extend(extract_public_commit_deliverables(summary.get("top_commits", []), 2))

    joined = " ".join(deliverables).lower()
    themes = []
    for label, needles in keyword_patterns:
        if any(needle in joined for needle in needles):
            themes.append(label)

    if themes:
        unique = []
        for theme in themes:
            if theme not in unique:
                unique.append(theme)
        return ", ".join(unique[:3])
    return "Ecosystem Progress"


def pick_public_achievement(summaries: Dict[str, Dict[str, Any]]) -> str:
    entries = sorted(summaries.items(), key=lambda item: repo_sort_key(item[1]), reverse=True)
    for _, summary in entries[:3]:
        deliverables = extract_public_pr_deliverables(summary.get("merged_pr_list", []), 1)
        if not deliverables:
            deliverables = extract_public_commit_deliverables(summary.get("top_commits", []), 1)
        if deliverables:
            item = ensure_public_verb(enrich_public_deliverable(deliverables[0], ""))
            item = rewrite_public_jargon(item)
            return item
    return "Strengthened the ecosystem through focused delivery"


def strip_verb(text: str) -> str:
    return re.sub(
        r"^(Launched|Released|Secured|Hardened|Optimized|Streamlined|Integrated|Improved)\s+",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()


def resolve_verb_conflicts(text: str) -> str:
    if not text:
        return text
    improved_fix = re.match(r"^Improved\s+(.+?)\s+fix(?:ing|ed)?\s+(.+)$", text, flags=re.IGNORECASE)
    if improved_fix:
        subject = improved_fix.group(1).strip()
        cause = improved_fix.group(2).strip()
        return f"Improved {subject} by resolving {cause}"
    match = re.match(r"^(Launched|Released|Secured|Hardened|Optimized|Streamlined|Integrated|Improved)\b", text, flags=re.IGNORECASE)
    if not match:
        return text
    verb = match.group(1)
    remainder = re.sub(
        r"\b(Launched|Released|Secured|Hardened|Optimized|Streamlined|Integrated|Improved)\b\s+",
        "",
        text[len(verb):],
        flags=re.IGNORECASE,
    ).strip()
    return f"{verb} {remainder}".strip()


def format_public_highlight_items(items: List[str]) -> str:
    cleaned_items = []
    for item in items:
        text = rewrite_public_jargon(item)
        text = ensure_public_verb(text)
        text = re.sub(r"^(Improved|Launched|Secured|Expanded|Streamlined)\s+\1\b", r"\1", text, flags=re.IGNORECASE)
        text = resolve_verb_conflicts(text)
        cleaned_items.append(text)
    return ", ".join(cleaned_items)


def extract_technical_highlight_items(commits: List[Dict[str, Any]], limit: int) -> List[str]:
    seen: Set[str] = set()
    items: List[str] = []
    for commit in commits:
        msg = commit.get("message", "")
        if not msg:
            continue
        msg = sanitize_initial_commit(msg, commit.get("repo"), True)
        cleaned = simplify_message(msg)
        if not cleaned:
            continue
        if not is_public_deliverable(cleaned):
            continue
        cleaned = sentence_case(cleaned)
        cleaned = normalize_technical_highlight_phrase(cleaned)
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append(cleaned)
        if len(items) >= limit:
            break
    return items


def generate_technical_highlight(
    summaries: Dict[str, Dict[str, Any]],
    total_commits: int,
    total_prs: int,
    total_repos: int,
) -> str:
    entries = sorted(summaries.items(), key=lambda item: repo_sort_key(item[1]), reverse=True)
    focus: List[Tuple[str, str]] = []
    for repo_name, summary in entries:
        if repo_name == "Other repos":
            continue
        items = extract_technical_highlight_items(summary.get("top_commits", []), 1)
        if items:
            focus.append((repo_name, items[0]))
        if len(focus) >= 3:
            break

    if not focus:
        return f"Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories."

    if len(focus) == 1:
        sentence_one = f"Key engineering progress centered on {focus[0][0]}, including {focus[0][1]}."
        sentence_two = ""
    else:
        sentence_one = (
            f"Key engineering progress landed in {focus[0][0]} and {focus[1][0]}, "
            f"including {focus[0][1]} and {focus[1][1]}."
        )
        sentence_two = (
            f"Additional work advanced {focus[2][0]} with {focus[2][1]}."
            if len(focus) >= 3
            else ""
        )

    sentences = " ".join(sentence for sentence in [sentence_one, sentence_two] if sentence)
    stats = f"Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories."
    return f"{sentences} {stats}".strip()


def highlight_focus_count(scope: str) -> int:
    return {
        "biweekly": 3,
        "monthly": 4,
        "quarterly": 5,
    }.get(scope, 3)


def generate_public_highlight(
    summaries: Dict[str, Dict[str, Any]],
    total_commits: int,
    total_prs: int,
    scope: str,
) -> str:
    entries = sorted(summaries.items(), key=lambda item: repo_sort_key(item[1]), reverse=True)
    highlights: List[Tuple[str, str]] = []
    focus_count = highlight_focus_count(scope)
    narrative_limit = max(4, focus_count + 1)
    for repo_name, summary in entries[:max(6, narrative_limit + 1)]:
        deliverables = extract_public_pr_deliverables(summary.get("merged_pr_list", []), 1)
        if not deliverables:
            deliverables = extract_public_commit_deliverables(summary.get("top_commits", []), 1)
        if deliverables:
            highlights.append((repo_name, deliverables[0]))
        if len(highlights) >= narrative_limit:
            break

    if not highlights:
        return (
            f"이번 기간 동안 토카막 네트워크는 **{total_commits}**개의 기여와 "
            f"**{total_prs}**개의 병합된 제안을 통해 핵심 생태계 역량을 강화했습니다."
        )

    narrative = format_public_highlight_items([item for _, item in highlights])
    focus_pairs = []
    for repo_name, item in highlights[:focus_count]:
        cleaned = rewrite_public_jargon(item, repo_name)
        cleaned = ensure_public_verb(enrich_public_deliverable(cleaned, "", repo_name))
        focus_pairs.append((repo_name, strip_verb(cleaned)))
    focus_sentence = ", ".join(f"{repo}의 {phrase}" for repo, phrase in focus_pairs)
    return (
        f"이번 기간 동안 토카막은 {narrative}를 달성하며 다음 단계로 나아갔습니다. "
        f"특히 {focus_sentence}에서 드러난 진전이 이번 회차의 방향성을 보여줍니다. "
        f"이번 회차의 핵심은 {focus_sentence}로 요약됩니다."
    )


def extract_public_pr_deliverables(prs: List[Dict[str, Any]], limit: int) -> List[str]:
    seen: Set[str] = set()
    deliverables: List[str] = []
    for pr in prs:
        title = pr.get("title", "")
        if not title:
            continue
        title = sanitize_initial_commit(title, pr.get("repo"), technical=False)
        if title.lower().startswith("launched the first architectural draft"):
            key = title.lower()
            if key not in seen:
                seen.add(key)
                deliverables.append(title)
            if len(deliverables) >= limit:
                break
            continue
        cleaned = publicize_deliverable(title)
        if not is_public_deliverable(cleaned):
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        deliverables.append(cleaned)
        if len(deliverables) >= limit:
            break
    return deliverables


def extract_public_commit_deliverables(commits: List[Dict[str, Any]], limit: int) -> List[str]:
    seen: Set[str] = set()
    deliverables: List[str] = []
    for commit in commits:
        msg = commit.get("message", "")
        if not msg:
            continue
        msg = sanitize_initial_commit(msg, commit.get("repo"), technical=False)
        if msg.lower().startswith("launched the first architectural draft"):
            key = msg.lower()
            if key not in seen:
                seen.add(key)
                deliverables.append(msg)
            if len(deliverables) >= limit:
                break
            continue
        cleaned = publicize_deliverable(msg)
        if not is_public_deliverable(cleaned):
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        deliverables.append(cleaned)
        if len(deliverables) >= limit:
            break
    return deliverables


def dedupe_prefixes(items: List[str]) -> List[str]:
    results: List[str] = []
    seen: Set[str] = set()
    for item in items:
        lower = item.lower()
        lower = re.sub(r"^(launched|improved|secured|expanded|streamlined)\s+", "", lower)
        if lower in seen:
            continue
        seen.add(lower)
        results.append(item)
    return results


def extract_technical_deliverables(commits: List[Dict[str, Any]], limit: int) -> List[str]:
    deliverables: List[str] = []
    seen: Set[str] = set()
    for commit in commits:
        msg = simplify_message(commit.get("message", ""))
        if not msg:
            continue
        repo = commit.get("repo")
        module_hint = repo.replace("-", "/") if repo else "module"
        lower_msg = msg.strip().lower()
        if "initial commit" in lower_msg:
            cleaned = initial_commit_replacement(repo, technical=True)
        elif re.fullmatch(r"(fix|fixed)", lower_msg):
            cleaned = f"Fixed stability issues in {module_hint}"
        elif re.fullmatch(r"(update|updated)", lower_msg):
            cleaned = f"Updated core logic in {module_hint}"
        else:
            cleaned = f"{msg} in {module_hint}"
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        link = None
        if commit.get("repo") and commit.get("sha"):
            link = f"https://github.com/tokamak-network/{commit['repo']}/commit/{commit['sha']}"
        if link:
            deliverables.append(f"{cleaned} ([Commit]({link}))")
        else:
            deliverables.append(cleaned)
        if len(deliverables) >= limit:
            break
    return deliverables


def build_raw_data_input(
    summaries: Dict[str, Dict[str, Any]],
    individual_summaries: Dict[str, Dict[str, Any]],
    report_type: str,
    report_grouping: str,
) -> str:
    technical = report_type == "technical"
    lines: List[str] = []

    if report_grouping == "repository":
        entries = sorted(summaries.items(), key=lambda item: repo_sort_key(item[1]), reverse=True)
        for repo_name, summary in entries[:12]:
            lines.append(f"Repository: {repo_name}")
            lines.append("Top commits:")
            for commit in summary.get("top_commits", [])[:12]:
                repo = commit.get("repo", "")
                msg = sanitize_initial_commit(commit.get("message", ""), repo, technical)
                sha = commit.get("sha", "")
                lines.append(f"- [{repo}] {msg} (sha: {sha})")
            lines.append("Merged PRs:")
            for pr in summary.get("merged_pr_list", [])[:8]:
                repo = pr.get("repo", "")
                number = pr.get("pr_number", "")
                title = sanitize_initial_commit(pr.get("title", ""), repo, technical)
                lines.append(f"- [{repo}] PR#{number}: {title}")
            lines.append("")
    else:
        for project_key in ["Ooo", "Eco", "TRH"]:
            summary = summaries.get(project_key)
            if not summary:
                continue
            lines.append(f"Project: {project_key}")
            lines.append(f"Repositories: {', '.join(summary.get('repos', []))}")
            lines.append("Top commits:")
            for commit in summary.get("top_commits", [])[:15]:
                repo = commit.get("repo", "")
                msg = sanitize_initial_commit(commit.get("message", ""), repo, technical)
                sha = commit.get("sha", "")
                lines.append(f"- [{repo}] {msg} (sha: {sha})")
            lines.append("Merged PRs:")
            for pr in summary.get("merged_pr_list", [])[:10]:
                repo = pr.get("repo", "")
                number = pr.get("pr_number", "")
                title = sanitize_initial_commit(pr.get("title", ""), repo, technical)
                lines.append(f"- [{repo}] PR#{number}: {title}")
            lines.append("")

    if individual_summaries:
        lines.append("Contributors:")
        for payload in individual_summaries.values():
            label = payload.get("label", "")
            summary = payload.get("summary", {})
            commits = summary.get("top_commits", [])[:3]
            commit_snippets = "; ".join(
                sanitize_initial_commit(c.get("message", ""), c.get("repo"), technical)
                for c in commits
                if c.get("message")
            )
            lines.append(f"- {label}: {commit_snippets}")

    return "\n".join(lines).strip()


def generate_full_report_with_ai(
    report_type: str,
    summaries: Dict[str, Dict[str, Any]],
    individual_summaries: Dict[str, Dict[str, Any]],
    date_range: Dict[str, Optional[str]],
    total_commits: int,
    total_prs: int,
    total_repos: int,
    report_grouping: str,
) -> Optional[str]:
    if not has_tokamak_client() and (not HAS_ANTHROPIC or not os.environ.get('ANTHROPIC_API_KEY') or anthropic is None):
        return None

    start = date_range.get("start") or "N/A"
    end = date_range.get("end") or "N/A"
    raw_data = build_raw_data_input(summaries, individual_summaries, report_type, report_grouping)

    if report_type == "technical":
        prompt = f"""[Role]
You are a Senior Software Architect at Tokamak Network. Your task is to generate a highly detailed Technical Development Report based on the provided activity data.

[Team & Project Context]
- 2.2 (Ooo): Zero-Knowledge Proof-Based Private App Channels.
- 2.3 (Eco): Decentralized Staking and Governance.
- 2.4 (TRH): Tokamak Rollup Hub (Infrastructure).

[Constraints]
1. Header: "Tokamak Network Technical Report: [Date Range]"
2. Summary: Display "Total: X commits, Y merged PRs across Z repositories" only ONCE at the top.
3. Bullets: Every bullet point must follow this strict format:
   - "* [Action Verb] [Specific Function/Feature] in [Repository Directory Path] ([Commit](URL))"
   - Example: "* Implemented updateUserStorageSlot in Tokamak/zk/EVM/contracts ([Commit](https://...))"
4. Detail: Do not use vague words like "fixed" or "updated" alone. If the data is sparse, infer the technical context from the directory path or commit message to be as descriptive as possible.
5. Contributors: For each main contributor, summarize their primary technical achievement during this period.

[Data Input]
Date Range: {start} to {end}
Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories

{raw_data}
"""
    else:
        prompt = f"""[Role]
You are a Visionary Tech Evangelist at Tokamak Network. Your task is to generate an engaging Public Ecosystem Update based on the provided activity data.

[Team & Project Context]
- 2.2 (Ooo): Private Transactions & Secure Channels.
- 2.3 (Eco): Staking Rewards & Community Governance.
- 2.4 (TRH): One-Click Layer 2 Deployment Infrastructure.

[Constraints]
1. Header: "Tokamak Network Bi-Weekly Report: [Date Range]"
2. Highlight Section: Write a 3-sentence opening that connects the technical progress to user benefits (e.g., increased privacy, faster withdrawals, easier deployment).
3. Grouping: Use engaging titles:
   - "Private & Secure Transactions (Ooo)"
   - "Staking & Economic Security (Eco)"
   - "Scalable Infrastructure (TRH)"
4. Jargon Filter: Translate all technical terms into "User Impact" language.
   - Example: Instead of "NFT-based registry", use "Secured ownership through digital asset architecture."
   - Example: Instead of "pnpm monorepo", use "Optimized system structure for faster development."
5. Formatting: Focus on "Results" (Launched, Secured, Improved). Do not show commit links or raw file paths in this version.
6. Contributors: Focus on how each person's work improved the overall project mission.

[Data Input]
Date Range: {start} to {end}
Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories

{raw_data}
"""

    return generate_with_llm(prompt, max_tokens=2000)


def simplify_message_public(message: str) -> str:
    cleaned = simplify_message(message)
    cleaned = re.sub(
        r"\b(ci|api|sdk|contract|contracts|refactor|test|tests|doc|docs|chore|merge|pr|rpc|zk|zkp|l1|l2|e2e)\b",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\b(add|added|update|updated|fix|fixed|refactor|remove|removed|chore|feat|feature)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned[:140]


def classify_commits(commits: List[Dict[str, Any]]) -> Dict[str, int]:
    categories = {"feature": 0, "fix": 0, "refactor": 0, "test": 0, "docs": 0, "other": 0}
    for commit in commits:
        msg = commit.get("message", "").lower()
        if any(key in msg for key in ["feat", "add", "implement", "launch", "introduce"]):
            categories["feature"] += 1
        elif any(key in msg for key in ["fix", "bug", "issue", "error", "hotfix"]):
            categories["fix"] += 1
        elif any(key in msg for key in ["refactor", "optimiz", "perf", "cleanup", "simplify"]):
            categories["refactor"] += 1
        elif "test" in msg:
            categories["test"] += 1
        elif "doc" in msg:
            categories["docs"] += 1
        else:
            categories["other"] += 1
    return categories


def top_repos_from_commits(commits: List[Dict[str, Any]], limit: int = 3) -> List[str]:
    counts: Dict[str, int] = defaultdict(int)
    for commit in commits:
        repo = commit.get("repo")
        if repo:
            counts[repo] += 1
    return [repo for repo, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit]]


def extract_deliverables(
    commits: List[Dict[str, Any]],
    limit: int,
    public: bool,
    with_links: bool = False,
) -> List[str]:
    seen: Set[str] = set()
    deliverables: List[str] = []
    for commit in commits:
        msg = commit.get("message", "")
        if not msg:
            continue
        cleaned = simplify_message_public(msg) if public else simplify_message(msg)
        key = cleaned.lower()
        if not cleaned or key in seen:
            continue
        seen.add(key)
        if public:
            cleaned = sentence_case(cleaned)
        if with_links and commit.get("repo") and commit.get("sha"):
            link = f"https://github.com/tokamak-network/{commit['repo']}/commit/{commit['sha']}"
            deliverables.append(f"{cleaned} ([Commit]({link}))")
        else:
            deliverables.append(cleaned)
        if len(deliverables) >= limit:
            break
    return deliverables


def generate_technical_section(project: str, summary: dict, use_ai: bool = True) -> str:
    """Generate technical report section."""
    info = SECTION_INFO_TECHNICAL[project]

    if use_ai and HAS_ANTHROPIC and os.environ.get('ANTHROPIC_API_KEY'):
        return generate_with_ai_technical(project, summary, info)

    return generate_basic_technical(project, summary, info)


def generate_public_section(project: str, summary: dict, use_ai: bool = True) -> str:
    """Generate public report section."""
    info = SECTION_INFO_PUBLIC[project]

    if use_ai and HAS_ANTHROPIC and os.environ.get('ANTHROPIC_API_KEY'):
        return generate_with_ai_public(project, summary, info)

    return generate_basic_public(project, summary, info)


def generate_repo_technical_section(repo_name: str, summary: dict, use_ai: bool = True) -> str:
    info = {
        "number": "",
        "title": repo_name,
        "context": f"Repository activity summary for {repo_name}.",
        "overview_url": f"https://github.com/tokamak-network/{repo_name}",
    }
    if use_ai and (has_tokamak_client() or (HAS_ANTHROPIC and os.environ.get('ANTHROPIC_API_KEY'))):
        return generate_with_ai_technical(repo_name, summary, info)
    return generate_basic_technical(repo_name, summary, info)


def generate_repo_public_section(repo_name: str, summary: dict, use_ai: bool = True) -> str:
    if repo_name == "Other repos":
        remaining = len(summary.get("repos", []))
        return (
            f"* Other Active Developments: Managed consistent updates across {remaining} other repositories, "
            "focusing on continuous maintenance, documentation, and automated testing to ensure a robust ecosystem.\n"
        )

    total_commits = summary.get("total_commits", 0)
    merged_prs = summary.get("merged_prs", 0)
    if total_commits >= 40 or merged_prs >= 6:
        limit = 5
    elif total_commits >= 25 or merged_prs >= 4:
        limit = 4
    elif total_commits >= 12 or merged_prs >= 2:
        limit = 3
    else:
        limit = 2

    deliverables = extract_public_pr_deliverables(summary.get("merged_pr_list", []), limit)
    if len(deliverables) < limit:
        deliverables.extend(
            extract_public_commit_deliverables(summary.get("top_commits", []), limit - len(deliverables))
        )
    deliverables = dedupe_prefixes(deliverables)
    if not deliverables:
        deliverables = ["Improved core infrastructure for better performance"]

    cleaned_items = []
    for item in deliverables[:limit]:
        cleaned = ensure_public_verb(enrich_public_deliverable(item, "", repo_name))
        cleaned = rewrite_public_jargon(cleaned, repo_name)
        cleaned = diversify_public_verb(cleaned, repo_name)
        cleaned_items.append(cleaned)

    if not cleaned_items:
        return ""

    summary_sentence = f"{cleaned_items[0]}."
    bullets = [f"* {item}." for item in cleaned_items[1:]]
    if bullets:
        return summary_sentence + "\n" + "\n".join(bullets) + "\n"
    return summary_sentence + "\n"


def generate_with_ai_technical(project: str, summary: dict, info: dict) -> str:
    """Generate technical section using Claude API."""
    if not has_tokamak_client() and anthropic is None:
        return generate_basic_technical(project, summary, info)

    commit_list = "\n".join([
        f"- [{c['repo']}] {sanitize_initial_commit(c['message'], c.get('repo'), True)} (sha: {c['sha']})"
        for c in summary['top_commits'][:20]
    ])

    pr_list = "\n".join([
        f"- [{p['repo']}] PR#{p['pr_number']}: {sanitize_initial_commit(p['title'], p.get('repo'), True)}"
        for p in summary['merged_pr_list'][:10]
    ])

    prompt = f"""[Role]
You are a Senior Software Architect at Tokamak Network. Your task is to generate a highly detailed Technical Development Report based on the provided activity data.

[Team & Project Context]
- 2.2 (Ooo): Zero-Knowledge Proof-Based Private App Channels.
- 2.3 (Eco): Decentralized Staking and Governance.
- 2.4 (TRH): Tokamak Rollup Hub (Infrastructure).

[Constraints]
1. Header: "Tokamak Network Technical Report: [Date Range]"
2. Summary: Display "Total: X commits, Y merged PRs across Z repositories" only ONCE at the top.
3. Bullets: Every bullet point must follow this strict format:
   - "* [Action Verb] [Specific Function/Feature] in [Repository Directory Path] ([Commit](URL))"
   - Example: "* Implemented updateUserStorageSlot in Tokamak/zk/EVM/contracts ([Commit](https://...))"
4. Detail: Do not use vague words like "fixed" or "updated" alone. If the data is sparse, infer the technical context from the directory path or commit message to be as descriptive as possible.
5. Contributors: For each main contributor, summarize their primary technical achievement during this period.

[Data Input]
Project: {info['title']}
Date Range: {summary.get('start_date', 'N/A')} to {summary.get('end_date', 'N/A')}
Project Context: {info['context']}
Total commits: {summary['total_commits']}
Merged PRs: {summary['merged_prs']}

Top commits:
{commit_list}

Merged PRs:
{pr_list}
"""

    bullets = generate_with_llm(prompt, max_tokens=1500)
    if not bullets:
        return generate_basic_technical(project, summary, info)
    return f"{bullets}\n"


def generate_with_ai_public(project: str, summary: dict, info: dict) -> str:
    """Generate public section using Claude API."""
    if not has_tokamak_client() and anthropic is None:
        return generate_basic_public(project, summary, info)

    commit_list = "\n".join([
        f"- [{c['repo']}] {sanitize_initial_commit(c['message'], c.get('repo'), False)}"
        for c in summary['top_commits'][:20]
    ])

    prompt = f"""[Role]
You are a Visionary Tech Evangelist at Tokamak Network. Your task is to generate an engaging Public Ecosystem Update based on the provided activity data.

[Team & Project Context]
- 2.2 (Ooo): Private Transactions & Secure Channels.
- 2.3 (Eco): Staking Rewards & Community Governance.
- 2.4 (TRH): One-Click Layer 2 Deployment Infrastructure.

[Constraints]
1. Header: "Tokamak Network Bi-Weekly Report: [Date Range]"
2. Highlight Section: Write a 3-sentence opening that connects the technical progress to user benefits (e.g., increased privacy, faster withdrawals, easier deployment).
3. Grouping: Use engaging titles:
   - "Private & Secure Transactions (Ooo)"
   - "Staking & Economic Security (Eco)"
   - "Scalable Infrastructure (TRH)"
4. Jargon Filter: Translate all technical terms into "User Impact" language.
   - Example: Instead of "NFT-based registry", use "Secured ownership through digital asset architecture."
   - Example: Instead of "pnpm monorepo", use "Optimized system structure for faster development."
5. Formatting: Focus on "Results" (Launched, Secured, Improved). Do not show commit links or raw file paths in this version.
6. Contributors: Focus on how each person's work improved the overall project mission.

[Data Input]
Project: {info['title']}
Date Range: {summary.get('start_date', 'N/A')} to {summary.get('end_date', 'N/A')}
Context: {info['context']}
Business Focus: {info['business_focus']}
Total improvements: {summary['total_commits']}

Recent commits (for context only):
{commit_list}
"""

    bullets = generate_with_llm(prompt, max_tokens=1000)
    if not bullets:
        return generate_basic_public(project, summary, info)
    return f"{bullets}\n"


def generate_basic_technical(project: str, summary: dict, info: dict) -> str:
    """Generate basic technical section without AI."""
    commits = summary['top_commits']
    top_repos = top_repos_from_commits(commits)
    repo_list = ", ".join(top_repos) if top_repos else "core repositories"

    deliverables = extract_technical_deliverables(commits, 5)
    if not deliverables:
        deliverables = ["Maintenance and reliability updates across core systems."]

    bullets = [f"* Delivered updates across {repo_list}."]
    bullets.extend([f"* {item}." if not item.endswith(")") else f"* {item}" for item in deliverables])
    return "\n".join(bullets) + "\n"


def generate_basic_public(project: str, summary: dict, info: dict) -> str:
    """Generate basic public section without AI."""
    commits = summary['top_commits']
    merged_prs = summary.get('merged_pr_list', [])
    intro = sentence_case(info['context'].rstrip('.'))
    deliverables = extract_public_pr_deliverables(merged_prs, 4)
    if len(deliverables) < 3:
        deliverables.extend(extract_public_commit_deliverables(commits, 4 - len(deliverables)))
    deliverables = dedupe_prefixes(deliverables)
    deliverables = deliverables[:3]
    bullets = [f"* {intro}."]
    if deliverables:
        cleaned = [ensure_public_verb(enrich_public_deliverable(item, project)) for item in deliverables]
        bullets.extend([f"* {item}." for item in cleaned])
    else:
        bullets.append("* Delivered steady progress on core initiatives.")

    return "\n".join(bullets) + "\n"


def generate_individual_section(member_label: str, summary: dict, report_type: str, use_ai: bool = True) -> str:
    info = SECTION_INFO_INDIVIDUAL_TECHNICAL if report_type == "technical" else SECTION_INFO_INDIVIDUAL_PUBLIC

    if use_ai and HAS_ANTHROPIC and os.environ.get('ANTHROPIC_API_KEY'):
        return generate_with_ai_individual(member_label, summary, info, report_type)

    return generate_basic_individual(member_label, summary, info, report_type)


def generate_with_ai_individual(member_label: str, summary: dict, info: dict, report_type: str) -> str:
    if not has_tokamak_client() and anthropic is None:
        return generate_basic_individual(member_label, summary, info, report_type)

    technical = report_type == "technical"
    commit_list = "\n".join([
        f"- [{c['repo']}] {sanitize_initial_commit(c['message'], c.get('repo'), technical)} (sha: {c['sha']})"
        for c in summary['top_commits'][:20]
    ])

    pr_list = "\n".join([
        f"- [{p['repo']}] PR#{p['pr_number']}: {sanitize_initial_commit(p['title'], p.get('repo'), technical)}"
        for p in summary['merged_pr_list'][:10]
    ])

    if report_type == "technical":
        prompt = f"""Write a monthly developer summary for {member_label}.

Context: {info['context']}
Total commits: {summary['total_commits']}
Merged PRs: {summary['merged_prs']}

Top commits:
{commit_list}

Merged PRs:
{pr_list}

Generate 6-8 bullet points summarizing key development activities. Rules:
1. Start each bullet with a past-tense verb.
2. Include technical details.
3. Add GitHub links: ([PR#XX](https://github.com/tokamak-network/REPO/pull/NUMBER)) or ([Commit](https://github.com/tokamak-network/REPO/commit/SHA)).

Output only the bullet points."""
    else:
        prompt = f"""Write a monthly activity summary for {member_label} targeting non-technical readers.

Context: {info['context']}
Total improvements: {summary['total_commits']}

Recent commits (for context only):
{commit_list}

Generate 4-6 bullet points:
1. No technical jargon.
2. Focus on value and outcomes.
3. No GitHub links.
4. Start with action verbs.

Output only the bullet points."""

    bullets = generate_with_llm(prompt, max_tokens=1200)
    if not bullets:
        return generate_basic_individual(member_label, summary, info, report_type)
    return f"{bullets}\n"


def generate_basic_individual(member_label: str, summary: dict, info: dict, report_type: str) -> str:
    def rewrite_initial_commit(text: str) -> str:
        lowered = text.strip().lower()
        if "initial commit" in lowered:
            return initial_commit_replacement(None, technical=report_type == "technical")
        return text

    if report_type == "public":
        deliverables = extract_public_pr_deliverables(summary.get('merged_pr_list', []), 3)
        if len(deliverables) < 2:
            deliverables.extend(extract_public_commit_deliverables(summary['top_commits'], 3 - len(deliverables)))
        deliverables = dedupe_prefixes(deliverables)
        deliverables = deliverables[:2]
    else:
        deliverables = extract_technical_deliverables(summary['top_commits'], 2)
    if deliverables:
        cleaned = [rewrite_initial_commit(item.replace(" ([Commit](", " ([Commit](")) for item in deliverables]
        return "; ".join(sentence_case(item) for item in cleaned)
    return "Delivered targeted progress across individual initiatives"


def generate_individuals_section(individual_summaries: Dict[str, Dict[str, Any]], report_type: str, use_ai: bool = True) -> str:
    if not individual_summaries:
        return ""

    entries = []
    for payload in individual_summaries.values():
        summary = payload["summary"]
        label = payload["label"]
        entries.append((summary["total_commits"], label, summary))

    entries.sort(key=lambda x: x[0], reverse=True)
    top_entries = entries[:8]
    remaining = max(len(entries) - len(top_entries), 0)

    lines = []
    for _, label, summary in top_entries:
        detail = generate_basic_individual(label, summary, SECTION_INFO_INDIVIDUAL_PUBLIC, report_type)
        if detail:
            lines.append(f"- {label}: {detail}.")

    if remaining:
        lines.append(f"- Others: {remaining} contributors with smaller updates.")

    return "\n".join(lines) + "\n"


def generate_highlight_with_ai(summaries: dict, report_type: str, total_commits: int, total_prs: int, total_repos: int, date_range: Optional[dict] = None) -> str:
    """Generate engaging highlight using AI for public reports."""
    if not has_tokamak_client() and (not HAS_ANTHROPIC or not os.environ.get('ANTHROPIC_API_KEY') or anthropic is None):
        if report_type == "technical":
            return generate_technical_highlight(summaries, total_commits, total_prs, total_repos)
        return generate_basic_highlight(total_commits, total_prs, total_repos, report_type)

    try:
        # Gather key achievements from each project
        achievements = []
        for project, summary in summaries.items():
            top_msgs = [c['message'][:100] for c in summary['top_commits'][:5]]
            achievements.append(f"{project}: {', '.join(top_msgs)}")

        if report_type == "public":
            date_label = "N/A"
            if date_range and date_range.get("start") and date_range.get("end"):
                date_label = f"{date_range['start']} to {date_range['end']}"
            prompt = f"""[Role]
You are a Visionary Tech Evangelist. Your task is to generate an engaging Public Development Report for Tokamak Network.

[Tone]
Inspiring, accessible, and benefit-oriented. Focus on "Why it matters" and "User Impact."

[Constraints]
1. Header: "Tokamak Network Ecosystem Update: [Date Range]"
2. Highlight Section:
   - Write a compelling 3-sentence intro about how Tokamak is making blockchain more accessible.
   - Use bold numbers for total development activity.
3. Content Grouping (Use User-Friendly Titles):
   - Group 2.2: "Advancing Privacy & Secure Transactions"
   - Group 2.3: "Empowering Community Staking & Rewards"
   - Group 2.4: "Scaling the Future: Rollup Infrastructure"
4. Formatting for Bullets:
   - Translate technical tasks into user benefits.
   - Use "Launched", "Secured", "Improved" to start sentences.
   - Example: Instead of "updated MPT key", use "Enhanced security for private wallet deposits."
5. Contributor Summary:
   - Focus on project-level achievements (e.g., "Thomas: Built a new on-chain documentation system for transparency").

[Data]
Date Range: {date_label}
Total commits: {total_commits}
Merged PRs: {total_prs}
Active repositories: {total_repos}
Key work areas:
{chr(10).join(achievements)}
"""

        else:  # technical
            date_label = "N/A"
            if date_range and date_range.get("start") and date_range.get("end"):
                date_label = f"{date_range['start']} to {date_range['end']}"
            prompt = f"""[Role]
You are a Senior Software Architect. Your task is to generate a highly detailed Technical Development Report for Tokamak Network.

[Tone]
Authoritative, dry, objective, and evidence-based. Focus on "What" and "How."

[Constraints]
1. Header: "Tokamak Network Technical Report: [Date Range]"
2. Highlight:
   - Write 2 concise sentences describing the most significant technical progress.
   - Use engineering language (e.g., refined ZK circuits, hardened bridge security, optimized backend concurrency).
   - After the 2 sentences, include a short numeric summary: "Total: X commits, Y merged PRs across Z repositories.".
   - Keep the tone dry, professional, and concise.
   - Output only the highlight text (no title, no bullets, no section headers).
3. Content Grouping:
   - Group 2.2: ZKP Private Channels (Ooo)
   - Group 2.3: Staking & Governance (Eco)
   - Group 2.4: Rollup Infrastructure (TRH)
4. Formatting for Bullets:
   - Every update must include the specific function name or module changed.
   - You MUST append the [Commit](URL) link at the end of each line if provided in data.
   - Format: "- [Feature/Fix]: [Detailed description mentioning code changes] ([Commit](Link))"
5. Contributor Summary:
   - Focus on the technical stack used (e.g., "Thomas: Configured Foundry and verified Solidity sources").

[Data]
Date Range: {date_label}
Total commits: {total_commits}
Merged PRs: {total_prs}
Active repositories: {total_repos}
Key development areas:
{chr(10).join(achievements)}
"""

        response = generate_with_llm(prompt, max_tokens=400)
        if response:
            return response
        if report_type == "technical":
            return generate_technical_highlight(summaries, total_commits, total_prs, total_repos)
        return generate_basic_highlight(total_commits, total_prs, total_repos, report_type)

    except Exception as e:
        if report_type == "technical":
            return generate_technical_highlight(summaries, total_commits, total_prs, total_repos)
        return generate_basic_highlight(total_commits, total_prs, total_repos, report_type)


def generate_basic_highlight(total_commits: int, total_prs: int, total_repos: int, report_type: str) -> str:
    """Generate basic highlight without AI."""
    if report_type == "public":
        return f"Tokamak Network continues to advance its mission of making blockchain technology more accessible and secure. This period saw meaningful progress across privacy technology, staking infrastructure, and Layer 2 deployment tools, bringing us closer to delivering real value for users and partners."
    else:
        return f"Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories."


@app.get("/")
async def root():
    return {"message": "Biweekly Report Generator API", "version": "1.0.0"}


@app.post("/api/analyze")
async def analyze_csv(
    file: UploadFile = File(...),
):
    try:
        content = await file.read()
        content_str = content.decode('utf-8')

        parsed = parse_csv_content(content_str)
        scope, start_date, end_date, days = detect_scope_from_timestamps(parsed["timestamps"])

        return JSONResponse({
            "success": True,
            "detected_scope": scope,
            "date_range": {
                "start": start_date,
                "end": end_date,
                "days": days,
            },
            "members": parsed["members"],
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate")
async def generate_report(
    file: UploadFile = File(...),
    report_type: str = Form("technical"),
    use_ai: bool = Form(True),
    report_scope: str = Form("auto"),
    project_filter: str = Form("all"),
    member_filter: str = Form("all"),
    include_individuals: bool = Form(True),
    report_grouping: str = Form("project"),
    repo_limit: int = Form(0),
):
    """Generate report from uploaded CSV file."""
    try:
        content = await file.read()
        content_str = content.decode('utf-8')

        parsed = parse_csv_content(content_str)
        project_data = parsed["projects"]
        repo_data = parsed["repos"]
        individual_data = parsed["individuals"]
        members = parsed["members"]

        if not project_data and not repo_data and not individual_data:
            raise HTTPException(status_code=400, detail="No valid GitHub data found in CSV")

        detected_scope, start_date, end_date, days = detect_scope_from_timestamps(parsed["timestamps"])
        scope = detected_scope if report_scope == "auto" else report_scope

        # Prepare summaries
        summaries: Dict[str, Dict[str, Any]] = {}
        project_keys = ["Ooo", "Eco", "TRH"]
        if project_filter != "all":
            project_keys = [project_filter]

        repo_count_total = 0
        repo_count_shown = 0
        repo_limit_applied = False

        if report_grouping == "repository":
            repo_entries = []
            for repo_name, repo_payload in repo_data.items():
                summary = prepare_summary(repo_name, repo_payload)
                summary["start_date"] = start_date
                summary["end_date"] = end_date
                repo_entries.append((repo_name, summary))

            repo_entries.sort(key=lambda item: repo_sort_key(item[1]), reverse=True)
            repo_count_total = len(repo_entries)

            if repo_limit and repo_limit > 0 and len(repo_entries) > repo_limit:
                selected = repo_entries[:repo_limit]
                remainder = repo_entries[repo_limit:]
                remainder_names = {name for name, _ in remainder}
                other_group: ActivityGroup = {"commits": [], "prs": [], "repos": set()}
                for repo_name in remainder_names:
                    payload = repo_data.get(repo_name)
                    if not payload:
                        continue
                    other_group["commits"].extend(payload.get("commits", []))
                    other_group["prs"].extend(payload.get("prs", []))
                    other_group["repos"].update(payload.get("repos", []))
                summaries = {name: summary for name, summary in selected}
                if other_group["commits"] or other_group["prs"]:
                    other_summary = prepare_summary("Other repos", dict(other_group))
                    other_summary["start_date"] = start_date
                    other_summary["end_date"] = end_date
                    summaries["Other repos"] = other_summary
                repo_count_shown = len(summaries)
                repo_limit_applied = True
            else:
                summaries = {name: summary for name, summary in repo_entries}
                repo_count_shown = len(summaries)
        else:
            for project in project_keys:
                if project in project_data:
                    summary = prepare_summary(project, project_data[project])
                    summary["start_date"] = start_date
                    summary["end_date"] = end_date
                    summaries[project] = summary

        individual_summaries = {}
        member_lookup = {m["id"]: m for m in members}
        if report_grouping != "repository" and include_individuals and scope in {"monthly", "biweekly"}:
            selected_members = list(individual_data.keys())
            if member_filter != "all":
                selected_members = [member_filter] if member_filter in individual_data else []

            for member_id in selected_members:
                data = individual_data.get(member_id)
                if not data:
                    continue
                label = member_lookup.get(member_id, {}).get("label", member_id)
                member_summary = prepare_summary(member_id, data)
                member_summary["start_date"] = start_date
                member_summary["end_date"] = end_date
                individual_summaries[member_id] = {
                    "label": label,
                    "summary": member_summary,
                }

        # Calculate totals
        total_commits = sum(s['total_commits'] for s in summaries.values())
        total_prs = sum(s['merged_prs'] for s in summaries.values())
        total_repos = sum(len(s['repos']) for s in summaries.values())

        date_range = {
            "start": start_date,
            "end": end_date,
        }

        full_report = None
        if use_ai:
            full_report = generate_full_report_with_ai(
                report_type,
                summaries,
                individual_summaries,
                date_range,
                total_commits,
                total_prs,
                total_repos,
                report_grouping,
            )

        # Generate sections
        sections = []
        section_info = SECTION_INFO_TECHNICAL if report_type == "technical" else SECTION_INFO_PUBLIC

        if report_grouping == "repository":
            entries = list(summaries.items())
            if "Other repos" in summaries:
                entries = [(name, summary) for name, summary in entries if name != "Other repos"]
                entries.append(("Other repos", summaries["Other repos"]))
            for repo_name, summary in entries:
                if report_type == "technical":
                    section = generate_repo_technical_section(repo_name, summary, use_ai)
                else:
                    section = generate_repo_public_section(repo_name, summary, use_ai)
                sections.append({
                    "project": repo_name,
                    "title": repo_name,
                    "content": section,
                })
        else:
            for project in project_keys:
                if project in summaries:
                    if report_type == "technical":
                        section = generate_technical_section(project, summaries[project], use_ai)
                    else:
                        section = generate_public_section(project, summaries[project], use_ai)
                    sections.append({
                        "project": project,
                        "title": f"{section_info[project]['number']}. {section_info[project]['title']}",
                        "content": section,
                    })

        if report_grouping != "repository" and include_individuals and scope in {"monthly", "biweekly"}:
            section = generate_individuals_section(individual_summaries, report_type, use_ai)
            if section:
                sections.append({
                    "project": "individuals",
                    "title": f"{SECTION_INFO_INDIVIDUAL_TECHNICAL['number']}. {SECTION_INFO_INDIVIDUAL_TECHNICAL['title']}",
                    "content": section,
                })

        # Generate highlight
        if use_ai and not full_report:
            highlight = generate_highlight_with_ai(
                summaries,
                report_type,
                total_commits,
                total_prs,
                total_repos,
                {"start": start_date, "end": end_date},
            )
        else:
            if report_type == "public":
                highlight = generate_public_highlight(summaries, total_commits, total_prs, scope)
            else:
                highlight = f"Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories."

        return JSONResponse({
            "success": True,
            "report_type": report_type,
            "report_scope": scope,
            "report_grouping": report_grouping,
            "date_range": {
                "start": start_date,
                "end": end_date,
                "days": days,
            },
            "stats": {
                "total_commits": total_commits,
                "total_prs": total_prs,
                "total_repos": total_repos,
            },
            "repo_limit_applied": repo_limit_applied,
            "repo_count_total": repo_count_total,
            "repo_count_shown": repo_count_shown,
            "highlight": highlight,
            "title": build_report_title(scope, start_date, end_date, days),
            "headline": build_report_headline(summaries, report_type),
            "full_report": full_report,
            "sections": sections,
            "summaries": summaries,
            "members": members,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "anthropic_available": HAS_ANTHROPIC,
        "tokamak_available": has_tokamak_client(),
        "api_key_set": bool(os.environ.get('ANTHROPIC_API_KEY')),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
