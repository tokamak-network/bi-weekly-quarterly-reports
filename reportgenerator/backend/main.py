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
from pathlib import Path
import asyncio
from concurrent.futures import ThreadPoolExecutor

try:
    from dotenv import load_dotenv  # type: ignore
    ENV_PATH = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=ENV_PATH, override=True)
except Exception:
    ENV_PATH = None

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

REPO_DESCRIPTIONS = {
    # Ooo (Private App Channels)
    "Tokamak-zk-EVM": "Core ZK-EVM engine enabling private smart contract execution with zero-knowledge proofs on Ethereum",
    "Tokamak-zk-EVM-contracts": "On-chain smart contracts for ZK-EVM verification, deposit/withdrawal, and state management",
    "private-app-channel-manager": "SDK for creating and managing private application channels with encrypted state transitions",
    "tokamak-zkp-channel-manager-new": "Next-generation ZK proof channel manager with improved proof generation and verification",
    "TokamakL2JS": "JavaScript library for interacting with Tokamak Layer 2 from web applications",
    "Tokamak-zk-EVM-landing-page": "Public-facing website and documentation for the ZK-EVM project",
    # Eco (Staking & Governance)
    "ton-staking-v2": "TON token staking platform enabling holders to earn rewards while securing the network",
    "tokamak-economics-whitepaper-v2": "Tokenomics research and whitepaper defining the TON economic model and incentive structures",
    "RAT-frontend": "RAT (Reward-based Automated TON) verification interface for staking reward distribution",
    "staking-community-version": "Community-accessible staking dashboard for TON holders to manage their staking positions",
    "tokamak-dao-v2": "Decentralized governance platform where TON holders vote on protocol proposals and upgrades",
    "tokamak-landing-page": "Main Tokamak Network website serving as the public entry point to the ecosystem",
    # TRH (Rollup Hub)
    "trh-sdk": "Developer SDK for deploying custom Layer 2 rollups on Tokamak Rollup Hub with minimal configuration",
    "trh-backend": "Backend infrastructure powering the Tokamak Rollup Hub deployment and management services",
    "trh-platform-ui": "Web-based dashboard for managing and monitoring deployed L2 rollup instances",
    "DRB-node": "Distributed Random Beacon node providing verifiable randomness for rollup sequencing",
    "tokamak-thanos": "Tokamak Thanos rollup stack — optimistic rollup implementation for Ethereum scaling",
    "tokamak-rollup-hub-v2": "Next-generation Rollup Hub platform enabling one-click L2 chain deployment",
    "tokamak-thanos-stack": "Full-stack tooling and infrastructure for operating Thanos-based rollup chains",
    "tokamak-thanos-geth": "Modified Geth execution client optimized for the Tokamak Thanos rollup environment",
    # Other ecosystem repos
    "SentinAI": "AI-powered security sentinel for automated smart contract auditing, vulnerability detection, and verification reporting",
    "zk-dex-d1-private-voting": "Zero-knowledge proof based decentralized voting system enabling private, verifiable on-chain governance",
    "dust-protocol": "Privacy-focused protocol for confidential token transfers with fast withdrawal support and social login onboarding",
    "auto-research-press": "Automated research publication platform that aggregates and publishes blockchain ecosystem analysis reports",
}

SECTION_INFO_INDIVIDUAL_PUBLIC = {
    "number": "2.5",
    "title": "Individual Contributions",
    "context": "Individual project progress that complements the main initiatives.",
}


DEFAULT_TOKAMAK_BASE_URL = "https://api.ai.tokamak.network"
DEFAULT_TOKAMAK_MODEL = "gpt-5.2-pro"
DEFAULT_TOKAMAK_TIMEOUT = 30
MAX_AI_REPO_LIMIT = 20

REVIEWER_PERSONAS = [
    {
        "level": 1,
        "name": "General Reader",
        "name_ko": "일반 독자",
        "description": "Non-technical reader with no blockchain background",
        "prompt_prefix": (
            "You are a general reader with no technical or blockchain background. "
            "You are reading a company progress report for the first time.\n\n"
            "Review the report and provide honest feedback:\n"
            "1. Identify any sentences or terms you don't understand.\n"
            "2. Point out any jargon that needs simpler explanation.\n"
            "3. Assess whether the overall message and progress are clear.\n"
            "4. Note if the report feels too long, too short, or well-balanced."
        ),
        "prompt_prefix_technical": (
            "You are a junior developer who recently joined the team and is reading the technical report "
            "to understand what the team has been working on.\n\n"
            "Review the report and provide honest feedback:\n"
            "1. Identify any internal terms, acronyms, or references you don't understand.\n"
            "2. Assess whether the development progress is clearly communicated.\n"
            "3. Note if commit messages and PR descriptions are understandable.\n"
            "4. Check if the report helps a newcomer understand the project structure."
        ),
    },
    {
        "level": 2,
        "name": "Business Analyst",
        "name_ko": "비즈니스 분석가",
        "description": "Business professional evaluating investment potential",
        "prompt_prefix": (
            "You are a business analyst and potential investor evaluating a blockchain company's progress report.\n\n"
            "Review the report and provide feedback:\n"
            "1. Are the business implications and value propositions clear?\n"
            "2. Is the progress meaningful from an investment perspective?\n"
            "3. Are there missing market context or competitive insights?\n"
            "4. Does the report convey confidence and momentum?"
        ),
        "prompt_prefix_technical": (
            "You are a DevOps engineer evaluating the technical report for operational quality.\n\n"
            "Review the report and provide feedback:\n"
            "1. Are infrastructure changes, deployments, and CI/CD updates properly documented?\n"
            "2. Are there potential breaking changes or migration requirements mentioned?\n"
            "3. Is the scope of each change clear enough for release planning?\n"
            "4. Are there missing details about testing, environments, or dependencies?"
        ),
    },
    {
        "level": 3,
        "name": "Project Manager",
        "name_ko": "프로젝트 매니저",
        "description": "PM with moderate technical understanding",
        "prompt_prefix": (
            "You are a project manager with moderate technical understanding of blockchain development.\n\n"
            "Review the report and provide feedback:\n"
            "1. Are milestones and deliverables clearly communicated?\n"
            "2. Is there a clear narrative of progress and direction?\n"
            "3. Are there gaps in the project timeline or missing status updates?\n"
            "4. Is the scope of work appropriately represented?"
        ),
        "prompt_prefix_technical": (
            "You are a technical project manager overseeing blockchain development.\n\n"
            "Review the report and provide feedback:\n"
            "1. Are milestones, deliverables, and task completion clearly communicated?\n"
            "2. Is there a clear mapping between commits/PRs and project goals?\n"
            "3. Are there gaps in coverage — repositories or features not mentioned?\n"
            "4. Is the technical progress logically organized and easy to track?"
        ),
    },
    {
        "level": 4,
        "name": "Senior Developer",
        "name_ko": "시니어 개발자",
        "description": "Experienced developer familiar with blockchain systems",
        "prompt_prefix": (
            "You are a senior software developer with deep blockchain and distributed systems experience.\n\n"
            "Review the report and provide technical feedback:\n"
            "1. Is the technical content accurate and appropriately detailed?\n"
            "2. Are engineering achievements properly represented?\n"
            "3. Are there oversimplifications or missing technical context?\n"
            "4. Is the technical progression logical and well-articulated?"
        ),
        "prompt_prefix_technical": (
            "You are a senior software developer with deep blockchain and distributed systems experience.\n\n"
            "Review the technical report and provide detailed feedback:\n"
            "1. Is the technical content accurate and sufficiently detailed for a development audience?\n"
            "2. Are commit descriptions precise — do they explain what changed and why?\n"
            "3. Are there missing implementation details (e.g., algorithms, data structures, APIs)?\n"
            "4. Is the code quality narrative clear — refactoring, bug fixes, optimizations?"
        ),
    },
    {
        "level": 5,
        "name": "Blockchain Architect",
        "name_ko": "블록체인 아키텍트",
        "description": "Protocol researcher and systems architect",
        "prompt_prefix": (
            "You are a blockchain architect and protocol researcher with expertise in ZK proofs, "
            "rollup architectures, and DeFi systems.\n\n"
            "Review the report and provide expert-level feedback:\n"
            "1. Are architecture and protocol-level decisions well-justified?\n"
            "2. Is there sufficient depth on system design, security, and performance?\n"
            "3. Are there missing considerations for scalability or interoperability?\n"
            "4. Does the technical narrative align with industry best practices?"
        ),
        "prompt_prefix_technical": (
            "You are a blockchain architect and protocol researcher with expertise in ZK proofs, "
            "rollup architectures, and DeFi systems.\n\n"
            "Review the technical report and provide expert-level feedback:\n"
            "1. Are architecture decisions and protocol changes well-justified with sufficient context?\n"
            "2. Is there enough depth on system design, security implications, and performance impact?\n"
            "3. Are cross-repository dependencies and integration points clearly documented?\n"
            "4. Are there missing considerations for backward compatibility, migration, or breaking changes?"
        ),
    },
]


def refresh_env() -> None:
    if ENV_PATH is None:
        return
    try:
        load_dotenv(dotenv_path=ENV_PATH, override=True)  # type: ignore[name-defined]
    except Exception:
        return


def get_tokamak_base_url() -> str:
    return os.environ.get("TOKAMAK_BASE_URL", DEFAULT_TOKAMAK_BASE_URL)


def get_tokamak_api_key() -> str:
    return os.environ.get("TOKAMAK_API_KEY", "")


def get_tokamak_model() -> str:
    return os.environ.get("TOKAMAK_MODEL", DEFAULT_TOKAMAK_MODEL)


def get_tokamak_models() -> List[str]:
    raw = os.environ.get("TOKAMAK_MODELS", "")
    if not raw:
        raw = os.environ.get("TOKAMAK_AVAILABLE_MODELS", "")
    return [model.strip() for model in raw.split(",") if model.strip()]


def get_tokamak_timeout() -> int:
    raw = os.environ.get("TOKAMAK_REQUEST_TIMEOUT", "")
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_TOKAMAK_TIMEOUT
    return max(5, value)


def get_model_timeout(model: Optional[str]) -> int:
    base = get_tokamak_timeout()
    if not model:
        return base
    lowered = model.lower()
    if lowered.startswith("gemini"):
        return max(10, min(base, 20))
    if lowered.startswith("deepseek"):
        return max(10, min(base, 25))
    if lowered.startswith("gpt-5"):
        return 60
    return base


def get_model_temperature(model: Optional[str]) -> float:
    if not model:
        return 0.5
    lowered = model.lower()
    if lowered.startswith("gpt-5.2"):
        return 1.0
    if lowered.startswith("gemini"):
        return 0.7
    if lowered.startswith("deepseek"):
        return 0.6
    return 0.5


def model_style_hint(model: Optional[str], report_type: str) -> str:
    if not model:
        return ""
    lowered = model.lower()
    if report_type == "public":
        if lowered.startswith("gemini"):
            return "Use crisp, energetic phrasing with clear benefits."
        if lowered.startswith("deepseek"):
            return "Use analytical, concrete phrasing with practical outcomes."
        if lowered.startswith("gpt-5"):
            return "Use polished, executive-friendly phrasing with clear impact."
    else:
        if lowered.startswith("gemini"):
            return "Be concise and pragmatic; emphasize operational changes."
        if lowered.startswith("deepseek"):
            return "Be analytical and engineering-first; emphasize mechanisms."
        if lowered.startswith("gpt-5"):
            return "Be crisp and technical; emphasize architecture and verification."
    return ""


def sanitize_technical_highlight(text: str) -> str:
    if not text:
        return text
    normalized = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", normalized)
    filtered = []
    for sentence in sentences:
        lowered = sentence.lower()
        if "total:" in lowered:
            continue
        if re.search(r"\b\d+\s+(commits?|prs?|pull requests?|repositories?)\b", lowered):
            continue
        if re.search(r"\b(commits?|prs?|pull requests?|repositories?)\b", lowered):
            continue
        filtered.append(sentence)
    if not filtered:
        return normalized
    return " ".join(filtered[:2]).strip()


def sanitize_public_highlight(text: str) -> str:
    if not text:
        return text
    normalized = re.sub(r"\s+", " ", text).strip()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", normalized) if s.strip()]
    if not sentences:
        return normalized
    noise_patterns = [
        r"\buser wants\b",
        r"\bthey've provided\b",
        r"\bconstraints\b",
        r"\bi need to\b",
        r"\bmust avoid\b",
        r"\blooking at the data\b",
        r"\bbrainstorm\b",
        r"\bhmm\b",
        r"\bmust be\b",
        r"\bshould\b",
        r"\bprobably wants\b",
        r"\bfirst sentence\b",
        r"\bsecond sentence\b",
        r"\bthird sentence\b",
        r"\bchecking constraints\b",
        r"\bdouble-checking\b",
        r"\btime to output\b",
        r"\bexactly three sentences\b",
    ]
    filtered = []
    for sentence in sentences:
        lowered = sentence.lower()
        if any(re.search(pattern, lowered) for pattern in noise_patterns):
            continue
        if re.search(r"\b(i|i'm|i'll|i've|we|we're|we'll|we've)\b", lowered):
            continue
        if re.search(r"\bneed to|must|should|got it\b", lowered):
            continue
        filtered.append(sentence)
    if not filtered:
        return normalized
    return " ".join(filtered[:3]).strip()


def sanitize_repo_technical_section(section: str) -> str:
    if not section:
        return section
    lines = [line.rstrip() for line in section.splitlines()]
    bullets = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        # Skip meta-commentary lines
        if "tokamak network technical report" in lowered:
            continue
        if lowered.startswith("summary:") or lowered.startswith("total:"):
            continue
        if "development activities" in lowered and not stripped.startswith("*"):
            continue
        # Keep bullet points (with or without commit references)
        if stripped.startswith("*") or stripped.startswith("-"):
            bullets.append(stripped)
    return "\n".join(bullets).strip()


def trim_summary_for_ai(summary: dict, commit_limit: int, pr_limit: int) -> dict:
    trimmed = dict(summary)
    trimmed["top_commits"] = summary.get("top_commits", [])[:commit_limit]
    trimmed["merged_pr_list"] = summary.get("merged_pr_list", [])[:pr_limit]
    return trimmed


def normalize_model_list(raw_value: Optional[str]) -> List[str]:
    if not raw_value:
        return []
    items = [item.strip() for item in raw_value.split(",") if item.strip()]
    seen: Set[str] = set()
    normalized: List[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(item)
    return normalized


def resolve_requested_models(model: Optional[str], models: Optional[str]) -> List[str]:
    requested = normalize_model_list(models or model)
    if requested:
        return requested
    defaults = get_tokamak_models()
    if defaults:
        return defaults
    return [get_tokamak_model()]


def has_tokamak_client(model: Optional[str] = None) -> bool:
    refresh_env()
    api_key = get_tokamak_api_key()
    if not api_key:
        return False
    if not HAS_OPENAI or OpenAI is None:
        return False
    selected = model or get_tokamak_model()
    return bool(selected)


def generate_with_tokamak(prompt: str, max_tokens: int, model: Optional[str] = None, timeout_override: Optional[int] = None, errors: Optional[List[str]] = None) -> Optional[str]:
    if not has_tokamak_client(model) or OpenAI is None:
        if errors is not None:
            errors.append("Tokamak client not available (missing API key or openai package)")
        return None
    selected_model = model or get_tokamak_model()
    timeout = timeout_override or get_model_timeout(selected_model)
    client = OpenAI(base_url=get_tokamak_base_url(), api_key=get_tokamak_api_key(), timeout=timeout)
    # Try responses API for gpt-5.2 first, fall back to chat completions
    if selected_model.startswith("gpt-5.2"):
        try:
            responses = getattr(client, "responses", None)
            if responses is not None:
                response = responses.create(
                    model=selected_model,
                    input=prompt,
                    max_output_tokens=max_tokens,
                    temperature=get_model_temperature(selected_model),
                    timeout=timeout,
                )
                text = getattr(response, "output_text", "")
                if text:
                    return text.strip()
        except Exception as exc:
            print(f"Tokamak responses API failed for {selected_model}, trying chat completions: {exc}")
            if errors is not None:
                errors.append(f"Tokamak responses API ({selected_model}): {exc}")

    try:
        temperature = get_model_temperature(selected_model)
        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
        )
        content = response.choices[0].message.content if response.choices else None
        return content.strip() if content else None
    except Exception as exc:
        print(f"Tokamak chat completions failed for model {selected_model}: {exc}")
        if errors is not None:
            errors.append(f"Tokamak chat completions ({selected_model}): {exc}")
        return None


def generate_with_anthropic(prompt: str, max_tokens: int, errors: Optional[List[str]] = None) -> Optional[str]:
    if not HAS_ANTHROPIC or not os.environ.get('ANTHROPIC_API_KEY') or anthropic is None:
        if errors is not None:
            errors.append("Anthropic client not available (missing API key or anthropic package)")
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
    except Exception as exc:
        if errors is not None:
            errors.append(f"Anthropic API: {exc}")
        return None


def generate_with_llm(prompt: str, max_tokens: int, model: Optional[str] = None, timeout_override: Optional[int] = None, errors: Optional[List[str]] = None) -> Optional[str]:
    tokamak_response = generate_with_tokamak(prompt, max_tokens, model, timeout_override, errors)
    if tokamak_response:
        return tokamak_response
    anthropic_response = generate_with_anthropic(prompt, max_tokens, errors)
    if anthropic_response:
        return anthropic_response
    return None


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
        cleaned = normalize_technical_highlight_phrase(sentence_case(cleaned))
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        items.append(cleaned)
        if len(items) >= limit:
            break
    if not items:
        for commit in commits:
            msg = commit.get("message", "")
            if not msg:
                continue
            msg = sanitize_initial_commit(msg, commit.get("repo"), True)
            cleaned = simplify_message(msg)
            if not cleaned:
                continue
            cleaned = normalize_technical_highlight_phrase(sentence_case(cleaned))
            items.append(cleaned)
            break
    return items


def generate_technical_highlight(
    summaries: Dict[str, Dict[str, Any]],
    total_commits: int,
    total_prs: int,
    total_repos: int,
) -> str:
    entries = sorted(summaries.items(), key=lambda item: repo_sort_key(item[1]), reverse=True)
    themes = derive_technical_themes(summaries)
    theme_sentence = ""
    if themes:
        theme_sentence = f"This sprint emphasized {themes[0]}" + (f" and {themes[1]}." if len(themes) > 1 else ".")
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
        return "Delivered focused engineering progress across core systems and tooling."

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

    sentences = " ".join(sentence for sentence in [theme_sentence, sentence_one, sentence_two] if sentence)
    return sentences.strip()


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
    total_repos: int,
    scope: str,
) -> str:
    theme = derive_public_theme(summaries)
    achievement = pick_public_achievement(summaries)
    return (
        f"Tokamak Network advanced {theme.lower()} with a focus on practical user impact. "
        f"{achievement}. "
        f"Total: **{total_commits}** commits, **{total_prs}** merged PRs across **{total_repos}** repositories."
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


def extract_repo_keywords(commits: List[Dict[str, Any]], prs: List[Dict[str, Any]], limit: int = 5) -> List[str]:
    keyword_map = {
        "k8s": "K8s",
        "grpc": "gRPC",
        "web3": "Web3",
        "postgres": "Postgres",
        "postgresql": "Postgres",
    }
    known_keywords = [
        "BLS",
        "UUPS",
        "MIPS",
        "EVM",
        "ZK",
        "ZKP",
        "L2",
        "RPC",
        "SDK",
        "API",
        "ABI",
        "DEX",
        "DAO",
        "RAT",
        "KZG",
        "EIP",
        "ERC",
        "RLP",
        "P2P",
        "JWT",
        "OAuth",
        "AMM",
        "MPC",
        "Redis",
        "Kafka",
        "Docker",
        "Kubernetes",
        "i18n",
        "l10n",
        "Railgun",
    ]
    results: List[str] = []
    seen: Set[str] = set()

    def add(token: str) -> None:
        if not token:
            return
        normalized = keyword_map.get(token.lower(), token)
        key = normalized.lower()
        if key in seen:
            return
        seen.add(key)
        results.append(normalized)

    entries = commits + prs
    for entry in entries:
        text = entry.get("message") or entry.get("title") or ""
        if not text:
            continue
        for token in re.findall(r"\b[A-Z]{2,10}\b", text):
            add(token)
        for token in re.findall(r"\b[A-Z][a-z]+[A-Z][A-Za-z0-9]+\b", text):
            add(token)
        for token in re.findall(r"\b[a-z]{1,4}\d{1,3}\b", text, flags=re.IGNORECASE):
            add(token)
        for token in known_keywords:
            if re.search(rf"\b{re.escape(token)}\b", text, flags=re.IGNORECASE):
                add(token)
        if len(results) >= limit:
            break

    return results[:limit]


def inject_keywords(sentence: str, keywords: List[str], used: Set[str], max_keywords: int) -> str:
    available = []
    lower_sentence = sentence.lower()
    for keyword in keywords:
        key = keyword.lower()
        if key in used or key in lower_sentence:
            continue
        available.append(keyword)
    if not available:
        return sentence
    selected = available[:max_keywords]
    for keyword in selected:
        used.add(keyword.lower())
    suffix = " and ".join(selected)
    if sentence.endswith("."):
        sentence = sentence[:-1]
    return f"{sentence}, including {suffix}"


def derive_technical_themes(summaries: Dict[str, Dict[str, Any]]) -> List[str]:
    theme_map = [
        ("staking and validator reliability", ["staking", "validator", "delegate", "reward", "slash", "seig"]),
        ("governance tooling", ["governance", "dao", "proposal", "vote"]),
        ("rollup infrastructure", ["rollup", "sequencer", "drb", "hub"]),
        ("zero-knowledge privacy", ["zk", "zero-knowledge", "proof", "privacy", "channel"]),
        ("wallet experience", ["wallet", "snap", "extension"]),
        ("developer tooling", ["sdk", "cli", "api", "rpc"]),
        ("infra performance", ["infra", "node", "database", "cache", "redis", "metrics", "monitor"]),
    ]
    entries = sorted(summaries.items(), key=lambda item: repo_sort_key(item[1]), reverse=True)
    text = " ".join(
        " ".join(c.get("message", "") for c in summary.get("top_commits", [])[:10])
        for _, summary in entries[:5]
    ).lower()
    themes = []
    for label, needles in theme_map:
        if any(needle in text for needle in needles):
            themes.append(label)
    return themes[:2]


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


def build_project_summary_paragraph(project: str, summary: dict, report_type: str) -> str:
    commits = summary.get("top_commits", [])
    merged_prs = summary.get("merged_pr_list", [])
    items = extract_public_pr_deliverables(merged_prs, 4)
    if len(items) < 3:
        items.extend(extract_public_commit_deliverables(commits, 4 - len(items)))
    items = dedupe_prefixes(items)[:3]
    if not items:
        return ""

    keywords = extract_repo_keywords(summary.get("top_commits", []), summary.get("merged_pr_list", []), 4)
    used_keywords: Set[str] = set()
    cleaned = []
    for item in items:
        text = ensure_public_verb(enrich_public_deliverable(item, project))
        text = rewrite_public_jargon(text)
        text = inject_keywords(text, keywords, used_keywords, 1)
        cleaned.append(strip_verb(text))

    clause = ", ".join(cleaned)
    if report_type == "technical":
        return f"Core development advanced through {clause}."
    return f"이번 회차에서 {clause}를 중심으로 진행 상황을 정리했습니다."


def build_repo_technical_overview(summary: dict) -> str:
    return ""


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
    model: Optional[str] = None,
) -> Optional[str]:
    if not has_tokamak_client(model):
        return None

    start = date_range.get("start") or "N/A"
    end = date_range.get("end") or "N/A"
    raw_data = build_raw_data_input(summaries, individual_summaries, report_type, report_grouping)

    if report_type == "technical":
        if report_grouping == "repository":
            prompt = f"""[Role]
You are a Senior Software Architect at Tokamak Network. Your task is to generate a highly detailed Technical Development Report based on the provided activity data.

[Output Rules]
1. Output only the final report. No analysis or meta commentary.
2. Start with a 2-sentence highlight, then a single stats line:
   Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories.
3. Then, for each repository in the input order, output:
   - A section header: ### <name>
   - One concise technical summary sentence.
   - 2-5 bullet points, each in the format:
     - [Action Verb] [Specific Function/Feature] in [Repository Path] ([Commit](URL))
4. If the repository name is "Other repos", provide a concise aggregate summary and 2-3 bullets about overall maintenance and supporting work.
5. Do not add extra headings, emojis, or additional sections.

[Data Input]
{raw_data}
"""
        else:
            prompt = f"""[Role]
You are a Senior Software Architect at Tokamak Network. Your task is to generate a highly detailed Technical Development Report based on the provided activity data.

[Output Rules]
1. Output only the final report. No analysis or meta commentary.
2. Start with a 2-sentence highlight, then a single stats line:
   Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories.
3. Then, for each project in the input order, output:
   - A section header: ### <name>
   - One concise technical summary sentence.
   - 2-5 bullet points, each in the format:
     - [Action Verb] [Specific Function/Feature] in [Repository Path] ([Commit](URL))
4. Do not add extra headings, emojis, or additional sections.

[Data Input]
{raw_data}
"""
    else:
        if report_grouping == "repository":
            prompt = f"""[Role]
You are a Visionary Tech Evangelist at Tokamak Network. Your task is to generate an engaging Public Ecosystem Update based on the provided activity data.

[Output Rules]
1. Output only the final report. No analysis or meta commentary.
2. Highlight must be exactly 3 sentences. No extra lines or stats here.
3. Then, for each repository in the input order, output:
   - A section header: ### <name>
   - One user-benefit summary sentence.
   - 2-5 bullet points starting with Launched/Secured/Improved, user-impact language only.
4. If the repository name is "Other repos", provide a concise aggregate summary and 2-3 bullets about overall maintenance and supporting work.
5. Do not add subheadings like "Launched"/"Secured" as standalone lines. Use bullets only.
6. Do not include commit links, file paths, emojis, or extra sections.

[Data Input]
{raw_data}
"""
        else:
            prompt = f"""[Role]
You are a Visionary Tech Evangelist at Tokamak Network. Your task is to generate an engaging Public Ecosystem Update based on the provided activity data.

[Output Rules]
1. Output only the final report. No analysis or meta commentary.
2. Highlight must be exactly 3 sentences. No extra lines or stats here.
3. Then, for each project in the input order, output:
   - A section header: ### <name>
   - One user-benefit summary sentence.
   - 2-5 bullet points starting with Launched/Secured/Improved, user-impact language only.
4. Do not add subheadings like "Launched"/"Secured" as standalone lines. Use bullets only.
5. Do not include commit links, file paths, emojis, or extra sections.

[Data Input]
{raw_data}
"""

    return generate_with_llm(prompt, max_tokens=2000, model=model)


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


def generate_technical_section(
    project: str,
    summary: dict,
    use_ai: bool = True,
    model: Optional[str] = None,
) -> str:
    """Generate technical report section."""
    info = SECTION_INFO_TECHNICAL[project]

    if use_ai and has_tokamak_client(model):
        section = generate_with_ai_technical(project, summary, info, model=model)
    else:
        section = generate_basic_technical(project, summary, info)

    overview = build_project_summary_paragraph(project, summary, "technical")
    if overview:
        return f"{overview}\n{section}"
    return section


def generate_public_section(
    project: str,
    summary: dict,
    use_ai: bool = True,
    model: Optional[str] = None,
    report_format: str = "concise",
) -> str:
    """Generate public report section."""
    info = SECTION_INFO_PUBLIC[project]

    if use_ai and has_tokamak_client(model):
        section = generate_with_ai_public(project, summary, info, model=model, report_format=report_format)
    else:
        section = generate_basic_public(project, summary, info)

    overview = build_project_summary_paragraph(project, summary, "public")
    if overview:
        return f"{overview}\n{section}"
    return section


def generate_repo_technical_section(
    repo_name: str,
    summary: dict,
    use_ai: bool = True,
    model: Optional[str] = None,
) -> str:
    info = {
        "number": "",
        "title": repo_name,
        "context": f"Repository activity summary for {repo_name}.",
        "overview_url": f"https://github.com/tokamak-network/{repo_name}",
    }
    if use_ai and has_tokamak_client(model):
        section = generate_with_ai_technical(repo_name, summary, info, model=model)
    else:
        section = generate_basic_technical(repo_name, summary, info)
    section = sanitize_repo_technical_section(section)
    if section:
        return section
    return generate_basic_technical(repo_name, summary, info)


def generate_repo_public_section(
    repo_name: str,
    summary: dict,
    use_ai: bool = True,
    model: Optional[str] = None,
    report_format: str = "concise",
) -> str:
    if repo_name == "Other repos":
        remaining = len(summary.get("repos", []))
        return (
            f"* Other Active Developments: Managed consistent updates across {remaining} other repositories, "
            "focusing on continuous maintenance, documentation, and automated testing to ensure a robust ecosystem.\n"
        )

    repo_desc = REPO_DESCRIPTIONS.get(repo_name, f"Development work on {repo_name}")
    info = {
        "number": "",
        "title": repo_name,
        "context": repo_desc,
        "overview_url": f"https://github.com/tokamak-network/{repo_name}",
        "business_focus": summary.get("business_focus", "Ecosystem development"),
    }
    print(f"[REPO PUBLIC] repo={repo_name}, use_ai={use_ai}, model={model}, format={report_format}, has_client={has_tokamak_client(model)}")
    if use_ai and has_tokamak_client(model):
        section = generate_with_ai_public(repo_name, summary, info, model=model, report_format=report_format)
    else:
        section = generate_basic_public(repo_name, summary, info)
    if section:
        return section
    return generate_basic_public(repo_name, summary, info)


def generate_with_ai_technical(project: str, summary: dict, info: dict, model: Optional[str] = None) -> str:
    """Generate technical section using Tokamak API."""
    if not has_tokamak_client(model):
        return generate_basic_technical(project, summary, info)

    commit_list = "\n".join([
        f"- [{c['repo']}] {sanitize_initial_commit(c['message'], c.get('repo'), True)} (sha: {c['sha']})"
        for c in summary['top_commits'][:12]
    ])

    pr_list = "\n".join([
        f"- [{p['repo']}] PR#{p['pr_number']}: {sanitize_initial_commit(p['title'], p.get('repo'), True)}"
        for p in summary['merged_pr_list'][:6]
    ])

    prompt = f"""[Role]
You are a Senior Software Architect at Tokamak Network. Your task is to generate a highly detailed Technical Development Report based on the provided activity data.

[Team & Project Context]
- Zero-Knowledge Proof-Based Private App Channels (Privacy technology).
- Decentralized Staking and Governance (Token economy).
- Tokamak Rollup Hub — One-Click Layer 2 Deployment (Infrastructure).

[Constraints]
0. Output only bullet points. Do not include analysis, reasoning, or meta commentary.
1. Header: "Tokamak Network Technical Report: [Date Range]"
2. Summary: Display "Total: X commits, Y merged PRs across Z repositories" only ONCE at the top.
3. Bullets: Every bullet point must follow this strict format:
   - "* [Action Verb] [Specific Function/Feature] in [Repository Directory Path] ([Commit](URL))"
   - Example: "* Implemented updateUserStorageSlot in Tokamak/zk/EVM/contracts ([Commit](https://...))"
4. Detail: Do not use vague words like "fixed" or "updated" alone. If the data is sparse, infer the technical context from the directory path or commit message to be as descriptive as possible.
5. Contributors: For each main contributor, summarize their primary technical achievement during this period.
6. {model_style_hint(model, "technical")}

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

    bullets = generate_with_llm(prompt, max_tokens=1500, model=model)
    if not bullets:
        return generate_basic_technical(project, summary, info)
    return f"{bullets}\n"


def _format_instructions_concise() -> str:
    """Format A (Concise): One-liner intro + bold-titled bullet points."""
    return """[Output Format: Concise (Format A)]
1. Start with exactly ONE sentence explaining what this project/repository does and why it matters to users.
2. Then list exactly 5 bullet points of key accomplishments from this period.
3. Each bullet MUST follow this pattern:
   * **Bold Action Phrase**: Followed by a plain-language explanation of the user-facing benefit.
   - Example: "* **Integrated Fast Withdrawal Capabilities**: Merged new withdrawal logic, significantly reducing the waiting time for users looking to unstake their assets."
4. Do NOT include any section headers like "Key Accomplishments" or project title headers.
5. Do NOT include a closing/summary paragraph."""


def _format_instructions_structured() -> str:
    """Format B (Structured): Title + intro paragraph + Key Accomplishments header + bullets."""
    return """[Output Format: Structured (Format B)]
1. Start with a title line: "[Project/Repository Name] Progress Update" or "[Project/Repository Name]: [Subtitle describing theme]"
2. Then write a 2-3 sentence overview paragraph explaining what this project does, why it matters, and what the focus of this period was.
3. Then add a "Key Accomplishments" or "Key Accomplishments:" header on its own line.
4. Then list exactly 5 bullet points of key accomplishments from this period.
5. Each bullet MUST follow this pattern:
   * **Bold Action Phrase**: Followed by a plain-language explanation of the user-facing benefit.
   - Example: "* **Integrated Fast Withdrawal Capabilities**: Merged new withdrawal logic, significantly reducing the waiting time for users looking to unstake their assets."
6. Do NOT include a closing/summary paragraph."""


def generate_with_ai_public(project: str, summary: dict, info: dict, model: Optional[str] = None, report_format: str = "concise") -> str:
    """Generate public section using Tokamak API."""
    if not has_tokamak_client(model):
        return generate_basic_public(project, summary, info)

    commit_list = "\n".join([
        f"- [{c['repo']}] {sanitize_initial_commit(c['message'], c.get('repo'), False)}"
        for c in summary['top_commits'][:12]
    ])

    pr_list = "\n".join([
        f"- [{p['repo']}] PR#{p['pr_number']}: {sanitize_initial_commit(p['title'], p.get('repo'), False)}"
        for p in summary.get('merged_pr_list', [])[:6]
    ])

    # Build repo descriptions for context
    repo_desc_lines = []
    seen_repos = set()
    for c in summary.get('top_commits', [])[:20]:
        repo = c.get('repo', '')
        if repo and repo not in seen_repos:
            seen_repos.add(repo)
            desc = REPO_DESCRIPTIONS.get(repo, '')
            if desc:
                repo_desc_lines.append(f"- {repo}: {desc}")
    repo_descriptions = "\n".join(repo_desc_lines) if repo_desc_lines else "N/A"

    format_instructions = _format_instructions_structured() if report_format == "structured" else _format_instructions_concise()

    prompt = f"""[Role]
You are writing a public progress update for Tokamak Network, targeting investors, community members, and general readers who want to understand what was accomplished and why it matters.

[About This Repository/Project]
{info['title']}: {info.get('context', '')}
Business Focus: {info.get('business_focus', 'Ecosystem development')}

[Repository Descriptions]
{repo_descriptions}

{format_instructions}

[Writing Rules]
1. Each bullet should:
   - Start with a strong action verb (Launched, Enhanced, Strengthened, Delivered, Integrated, Implemented, etc.)
   - Explain the user-facing benefit, not just the technical change
   - Translate technical jargon into plain language
   - Example: Instead of "refactored staking contract logic", write "Improved staking reliability so users experience fewer transaction failures"
2. Do NOT include: commit hashes, file paths, PR numbers, meta commentary, or internal project codenames (Ooo, Eco, TRH).
3. Output in English only.
4. {model_style_hint(model, "public")}

[Activity Data]
Date Range: {summary.get('start_date', 'N/A')} to {summary.get('end_date', 'N/A')}
Total commits: {summary['total_commits']}
Merged PRs: {summary.get('merged_prs', 0)}

Recent commits:
{commit_list}

Merged PRs:
{pr_list}
"""

    print(f"[AI PUBLIC] Calling model={model} for project={project} format={report_format}")
    bullets = generate_with_llm(prompt, max_tokens=1000, model=model)
    if not bullets:
        print(f"[AI PUBLIC] LLM returned None for project={project}, falling back to basic")
        return generate_basic_public(project, summary, info)
    print(f"[AI PUBLIC] Got AI response for project={project} ({len(bullets)} chars)")
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

    # Use repo description as intro if available
    repo_desc = REPO_DESCRIPTIONS.get(project, "")
    if repo_desc:
        intro = repo_desc
    else:
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


def generate_individual_section(
    member_label: str,
    summary: dict,
    report_type: str,
    use_ai: bool = True,
    model: Optional[str] = None,
) -> str:
    info = SECTION_INFO_INDIVIDUAL_TECHNICAL if report_type == "technical" else SECTION_INFO_INDIVIDUAL_PUBLIC

    if use_ai and has_tokamak_client(model):
        return generate_with_ai_individual(member_label, summary, info, report_type, model=model)

    return generate_basic_individual(member_label, summary, info, report_type)


def generate_with_ai_individual(
    member_label: str,
    summary: dict,
    info: dict,
    report_type: str,
    model: Optional[str] = None,
) -> str:
    if not has_tokamak_client(model):
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

Output only the bullet points. Do not include analysis, reasoning, or meta commentary."""
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

Output only the bullet points. Do not include analysis, reasoning, or meta commentary."""

    bullets = generate_with_llm(prompt, max_tokens=1200, model=model)
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


def generate_individuals_section(
    individual_summaries: Dict[str, Dict[str, Any]],
    report_type: str,
    use_ai: bool = True,
    model: Optional[str] = None,
) -> str:
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
        detail = generate_individual_section(label, summary, report_type, use_ai, model=model)
        if detail:
            lines.append(f"- {label}: {detail}.")

    if remaining:
        lines.append(f"- Others: {remaining} contributors with smaller updates.")

    return "\n".join(lines) + "\n"


def generate_highlight_with_ai(
    summaries: dict,
    report_type: str,
    total_commits: int,
    total_prs: int,
    total_repos: int,
    date_range: Optional[dict] = None,
    model: Optional[str] = None,
) -> str:
    """Generate engaging highlight using AI for public reports."""
    if not has_tokamak_client(model):
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
You are writing the opening highlight paragraph for Tokamak Network's bi-weekly progress report. Your audience includes investors, TON token holders, community members, and general readers.

[About Tokamak Network]
Tokamak Network is building Ethereum Layer 2 infrastructure with three core initiatives:
- Privacy: Zero-knowledge proof technology for private transactions
- Staking & Governance: TON token staking rewards and decentralized governance
- Rollup Hub: One-click Layer 2 deployment platform for developers
IMPORTANT: Do NOT use internal project codenames like "Ooo", "Eco", or "TRH" in the output.

[Instructions]
1. Write exactly 3 sentences that serve as an executive summary.
2. Sentence 1: State what Tokamak Network accomplished this period in a way that excites investors and community.
3. Sentence 2: Connect the technical work to real user/business benefits (e.g., "users can now...", "this means faster...", "developers will be able to...").
4. Sentence 3: Include bold activity numbers — **{total_commits}** commits, **{total_prs}** merged PRs across **{total_repos}** repositories.
5. Do NOT use bullet points, headers, or meta commentary. Output only the 3 sentences.
6. Output in English only.

[Activity Data]
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
You are a Senior Software Architect. Your task is to generate a concise technical highlight for Tokamak Network.

[Tone]
Authoritative, dry, objective, and evidence-based. Focus on "What" and "How."

[Constraints]
0. Output only the highlight text. Do not include analysis, reasoning, or meta commentary.
1. Highlight must be exactly 2 sentences.
2. Do not include section headers, bullet points, or grouping labels.
3. Output in English only.
4. Avoid listing repository names; keep it outcome-focused.
5. Do not mention commit, PR, or repository counts.

[Data]
Date Range: {date_label}
Total commits: {total_commits}
Merged PRs: {total_prs}
Active repositories: {total_repos}
Key development areas:
{chr(10).join(achievements)}
"""

        response = generate_with_llm(prompt, max_tokens=400, model=model)
        if response:
            cleaned = response.strip()
            if report_type == "technical" and re.match(r"^Total:\s*\d+", cleaned, flags=re.IGNORECASE):
                return generate_technical_highlight(summaries, total_commits, total_prs, total_repos)
            if report_type == "technical":
                return sanitize_technical_highlight(cleaned)
            cleaned_public = sanitize_public_highlight(cleaned)
            if cleaned_public:
                return cleaned_public
            return generate_basic_highlight(total_commits, total_prs, total_repos, report_type)
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
        return (
            f"Tokamak Network advanced user-facing delivery across privacy, staking, and rollup tooling. "
            f"Key work tightened reliability and reduced friction for builders and users. "
            f"Total: **{total_commits}** commits, **{total_prs}** merged PRs across **{total_repos}** repositories."
        )
    else:
        return "Delivered focused engineering progress across core systems and tooling."


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
    model: Optional[str] = Form(None),
    models: Optional[str] = Form(None),
    report_scope: str = Form("auto"),
    project_filter: str = Form("all"),
    member_filter: str = Form("all"),
    include_individuals: bool = Form(True),
    report_grouping: str = Form("project"),
    repo_limit: int = Form(0),
    report_format: str = Form("concise"),
):
    """Generate report from uploaded CSV file."""
    try:
        refresh_env()
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
            effective_repo_limit = repo_limit
            forced_limit_applied = False
            if use_ai:
                if effective_repo_limit <= 0 or effective_repo_limit > MAX_AI_REPO_LIMIT:
                    effective_repo_limit = MAX_AI_REPO_LIMIT
                    forced_limit_applied = True

            repo_entries = []
            for repo_name, repo_payload in repo_data.items():
                summary = prepare_summary(repo_name, repo_payload)
                summary["start_date"] = start_date
                summary["end_date"] = end_date
                repo_entries.append((repo_name, summary))

            repo_entries.sort(key=lambda item: repo_sort_key(item[1]), reverse=True)
            repo_count_total = len(repo_entries)

            if effective_repo_limit and effective_repo_limit > 0 and len(repo_entries) > effective_repo_limit:
                selected = repo_entries[:effective_repo_limit]
                remainder = repo_entries[effective_repo_limit:]
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
                if forced_limit_applied:
                    repo_limit_applied = True
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

        requested_models = resolve_requested_models(model, models) if use_ai else []
        multi_model = len(requested_models) > 1
        selected_model = requested_models[0] if requested_models else None

        full_report = None
        allow_full_report = use_ai and report_grouping != "repository"
        if allow_full_report and not multi_model:
            full_report = generate_full_report_with_ai(
                report_type,
                summaries,
                individual_summaries,
                date_range,
                total_commits,
                total_prs,
                total_repos,
                report_grouping,
                model=selected_model,
            )

        # Generate sections
        sections = []
        section_info = SECTION_INFO_TECHNICAL if report_type == "technical" else SECTION_INFO_PUBLIC
        section_use_ai = use_ai
        # Note: Gemini Flash model restriction for technical reports removed
        # to ensure consistent AI generation across all report types
        highlight_use_ai = use_ai

        if report_grouping == "repository":
            entries = list(summaries.items())
            if "Other repos" in summaries:
                entries = [(name, summary) for name, summary in entries if name != "Other repos"]
                entries.append(("Other repos", summaries["Other repos"]))

            # Parallel generation for repository sections
            def _gen_repo_section(repo_name_and_summary):
                rn, sm = repo_name_and_summary
                sm = trim_summary_for_ai(sm, 12, 6) if use_ai else sm
                if report_type == "technical":
                    content = generate_repo_technical_section(rn, sm, section_use_ai, model=selected_model)
                else:
                    content = generate_repo_public_section(rn, sm, section_use_ai, model=selected_model, report_format=report_format)
                return {"project": rn, "title": rn, "content": content}

            with ThreadPoolExecutor(max_workers=min(5, len(entries))) as executor:
                sections = list(executor.map(_gen_repo_section, entries))
        else:
            for project in project_keys:
                if project in summaries:
                    if report_type == "technical":
                        section = generate_technical_section(project, summaries[project], section_use_ai, model=selected_model)
                    else:
                        section = generate_public_section(project, summaries[project], section_use_ai, model=selected_model, report_format=report_format)
                    sections.append({
                        "project": project,
                        "title": f"{section_info[project]['number']}. {section_info[project]['title']}",
                        "content": section,
                    })

        if report_grouping != "repository" and include_individuals and scope in {"monthly", "biweekly"}:
            section = generate_individuals_section(individual_summaries, report_type, use_ai, model=selected_model)
            if section:
                sections.append({
                    "project": "individuals",
                    "title": f"{SECTION_INFO_INDIVIDUAL_TECHNICAL['number']}. {SECTION_INFO_INDIVIDUAL_TECHNICAL['title']}",
                    "content": section,
                })

        # Generate highlight
        if highlight_use_ai and not full_report:
            highlight = generate_highlight_with_ai(
                summaries,
                report_type,
                total_commits,
                total_prs,
                total_repos,
                {"start": start_date, "end": end_date},
                model=selected_model,
            )
        else:
            if report_type == "public":
                highlight = generate_public_highlight(summaries, total_commits, total_prs, total_repos, scope)
            else:
                highlight = generate_technical_highlight(summaries, total_commits, total_prs, total_repos)

        model_reports: Dict[str, Dict[str, Any]] = {}
        if use_ai and multi_model:
            for candidate in requested_models:
                report_payload: Dict[str, Any] = {}
                candidate_full_report = generate_full_report_with_ai(
                    report_type,
                    summaries,
                    individual_summaries,
                    date_range,
                    total_commits,
                    total_prs,
                    total_repos,
                    report_grouping,
                    model=candidate,
                )
                if candidate_full_report:
                    report_payload["full_report"] = candidate_full_report

                candidate_sections = []
                if report_grouping == "repository":
                    entries = list(summaries.items())
                    if "Other repos" in summaries:
                        entries = [(name, summary) for name, summary in entries if name != "Other repos"]
                        entries.append(("Other repos", summaries["Other repos"]))
                    for repo_name, summary in entries:
                        summary = trim_summary_for_ai(summary, 12, 6)
                        if report_type == "technical":
                            section = generate_repo_technical_section(repo_name, summary, True, model=candidate)
                        else:
                            section = generate_repo_public_section(repo_name, summary, True, model=candidate, report_format=report_format)
                        candidate_sections.append({
                            "project": repo_name,
                            "title": repo_name,
                            "content": section,
                        })
                else:
                    for project in project_keys:
                        if project in summaries:
                            if report_type == "technical":
                                section = generate_technical_section(project, summaries[project], use_ai, model=candidate)
                            else:
                                section = generate_public_section(project, summaries[project], use_ai, model=candidate, report_format=report_format)
                            candidate_sections.append({
                                "project": project,
                                "title": f"{section_info[project]['number']}. {section_info[project]['title']}",
                                "content": section,
                            })

                if report_grouping != "repository" and include_individuals and scope in {"monthly", "biweekly"}:
                    section = generate_individuals_section(individual_summaries, report_type, use_ai, model=candidate)
                    if section:
                        candidate_sections.append({
                            "project": "individuals",
                            "title": f"{SECTION_INFO_INDIVIDUAL_TECHNICAL['number']}. {SECTION_INFO_INDIVIDUAL_TECHNICAL['title']}",
                            "content": section,
                        })

                if highlight_use_ai:
                    candidate_highlight = generate_highlight_with_ai(
                        summaries,
                        report_type,
                        total_commits,
                        total_prs,
                        total_repos,
                        {"start": start_date, "end": end_date},
                        model=candidate,
                    )
                else:
                    if report_type == "public":
                        candidate_highlight = generate_public_highlight(
                            summaries,
                            total_commits,
                            total_prs,
                            total_repos,
                            scope,
                        )
                    else:
                        candidate_highlight = generate_technical_highlight(
                            summaries,
                            total_commits,
                            total_prs,
                            total_repos,
                        )
                report_payload.update({
                    "highlight": candidate_highlight,
                    "sections": candidate_sections,
                })
                model_reports[candidate] = report_payload

        title = ""
        headline = ""
        if report_type != "public":
            title = build_report_title(scope, start_date, end_date, days)
            headline = build_report_headline(summaries, report_type)

        return JSONResponse({
            "success": True,
            "report_type": report_type,
            "report_format": report_format,
            "report_scope": scope,
            "report_grouping": report_grouping,
            "model": selected_model,
            "models": requested_models,
            "model_reports": model_reports,
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
            "title": title,
            "headline": headline,
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
        "tokamak_models": get_tokamak_models() or [get_tokamak_model()],
        "api_key_set": bool(get_tokamak_api_key()),
    }


@app.get("/api/reviewers")
async def list_reviewers():
    return JSONResponse({
        "reviewers": [
            {
                "level": p["level"],
                "name": p["name"],
                "name_ko": p["name_ko"],
                "description": p["description"],
            }
            for p in REVIEWER_PERSONAS
        ],
    })


@app.post("/api/review")
async def review_report(
    report_text: str = Form(...),
    report_type: str = Form("public"),
    reviewer_level: int = Form(3),
    model: Optional[str] = Form(None),
    report_format: str = Form("concise"),
):
    """Review a generated report using a virtual reviewer persona."""
    refresh_env()

    persona = None
    for p in REVIEWER_PERSONAS:
        if p["level"] == reviewer_level:
            persona = p
            break

    if not persona:
        raise HTTPException(status_code=400, detail=f"Invalid reviewer level: {reviewer_level}")

    selected_model = model or get_tokamak_model()

    try:
        return await _do_review(report_text, report_type, reviewer_level, selected_model, persona, report_format)
    except HTTPException:
        raise
    except Exception as exc:
        print(f"Review endpoint error: {exc}")
        return JSONResponse({
            "success": False,
            "error": f"Review error: {str(exc)[:500]}",
            "reviewer": persona["name"],
            "reviewer_ko": persona["name_ko"],
            "reviewer_level": reviewer_level,
        })


async def _do_review(report_text: str, report_type: str, reviewer_level: int, selected_model: str, persona: dict, report_format: str):
    import json as _json

    report_type_label = (
        "Public/Investor-facing report" if report_type == "public"
        else "Technical development report"
    )

    # Select appropriate prompt prefix based on report type
    if report_type == "technical" and "prompt_prefix_technical" in persona:
        active_prompt_prefix = persona["prompt_prefix_technical"]
    else:
        active_prompt_prefix = persona["prompt_prefix"]

    format_context = ""
    if report_type == "public":
        if report_format == "structured":
            format_context = (
                "\n[Report Format]\n"
                "This report uses Format B (Structured): Each section should have a title, "
                "an introductory paragraph explaining the project, a 'Key Accomplishments' header, "
                "and 5 bullet points with **bold action phrases** followed by explanations.\n"
                "When reviewing, also evaluate whether the structure is consistent across sections "
                "(e.g., all sections have titles, intro paragraphs, and the Key Accomplishments header).\n"
            )
        else:
            format_context = (
                "\n[Report Format]\n"
                "This report uses Format A (Concise): Each section should have a one-sentence project overview "
                "followed by 5 bullet points with **bold action phrases** followed by explanations. "
                "No section headers like 'Key Accomplishments' or project title headers.\n"
                "When reviewing, also evaluate whether the format is compact and scannable, "
                "and whether the one-liner intros are informative enough without being too verbose.\n"
            )
    else:
        format_context = (
            "\n[Report Format]\n"
            "This is a Technical Development Report. Each section has a ### header, "
            "a one-sentence technical summary, and 2-5 bullet points in the format: "
            "[Action Verb] [Specific Function/Feature] in [Repository Path] ([Commit](URL)).\n"
            "When reviewing, evaluate whether technical details are accurate, commit references are meaningful, "
            "and the engineering narrative is clear and comprehensive.\n"
        )

    prompt = f"""{active_prompt_prefix}

[Report Type]
{report_type_label}
{format_context}
[Report to Review]
{report_text}

[Output Format]
Provide your review as JSON. For each issue, include the EXACT original text and your proposed revision so the author can see specific suggested changes (like Google Docs "Suggest edits" mode):
{{
  "issues": [
    {{
      "category": "clarity|accuracy|depth|structure|tone",
      "description": "What the issue is and why it matters",
      "suggestion": "How to fix it",
      "severity": "low|medium|high",
      "original_text": "The exact sentence or phrase from the report that should be changed",
      "revised_text": "Your improved version of that sentence or phrase"
    }}
  ],
  "strengths": ["What the report does well"],
  "overall_score": <1-10>,
  "summary": "2-3 sentence overall assessment with actionable next steps"
}}

IMPORTANT:
- For each issue, you MUST include original_text (copied from the report) and revised_text (your improved version).
- Be specific and constructive. Show exactly what to change, not just what's wrong.
- Output ONLY the JSON. No additional text or markdown fences."""

    review_timeout = max(get_model_timeout(selected_model) * 2, 120)
    llm_errors: List[str] = []
    response = generate_with_llm(prompt, max_tokens=3000, model=selected_model, timeout_override=review_timeout, errors=llm_errors)

    if not response:
        error_detail = "; ".join(llm_errors) if llm_errors else "All AI providers failed"
        return JSONResponse({
            "success": False,
            "error": f"Failed to generate review: {error_detail}",
            "reviewer": persona["name"],
            "reviewer_ko": persona["name_ko"],
            "reviewer_level": reviewer_level,
        })

    cleaned = response.strip()
    # Remove markdown code fences (```json ... ``` or ``` ... ```)
    if "```" in cleaned:
        cleaned = re.sub(r"```(?:json)?\s*\n?", "", cleaned)
        cleaned = cleaned.strip()

    # Try to extract JSON from mixed content (e.g., LLM adds text before/after JSON)
    review_data = None
    try:
        review_data = _json.loads(cleaned)
    except (_json.JSONDecodeError, ValueError):
        pass

    if review_data is None:
        # Try to find a balanced JSON object containing "issues"
        brace_start = cleaned.find("{")
        if brace_start != -1:
            depth = 0
            end_idx = -1
            for i in range(brace_start, len(cleaned)):
                if cleaned[i] == "{":
                    depth += 1
                elif cleaned[i] == "}":
                    depth -= 1
                    if depth == 0:
                        end_idx = i
                        break
            if end_idx != -1:
                candidate = cleaned[brace_start : end_idx + 1]
                try:
                    review_data = _json.loads(candidate)
                except (_json.JSONDecodeError, ValueError):
                    pass

    if review_data is None:
        # Last resort: try regex for any JSON-like block
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned)
        if json_match:
            try:
                review_data = _json.loads(json_match.group())
            except (_json.JSONDecodeError, ValueError):
                pass

    if review_data is None:
        review_data = {
            "issues": [],
            "strengths": [],
            "overall_score": 5,
            "summary": cleaned[:2000] if len(cleaned) > 2000 else cleaned,
        }

    # Ensure required fields exist with correct types
    if not isinstance(review_data.get("issues"), list):
        review_data["issues"] = []
    if not isinstance(review_data.get("strengths"), list):
        review_data["strengths"] = []
    if not isinstance(review_data.get("overall_score"), (int, float)):
        review_data["overall_score"] = 5
    if not isinstance(review_data.get("summary"), str):
        review_data["summary"] = "Review completed."

    return JSONResponse({
        "success": True,
        "reviewer": persona["name"],
        "reviewer_ko": persona["name_ko"],
        "reviewer_level": reviewer_level,
        "reviewer_description": persona["description"],
        "review": review_data,
    })


@app.post("/api/improve")
async def improve_report(
    report_text: str = Form(...),
    report_type: str = Form("public"),
    reviews_json: str = Form("[]"),
    model: Optional[str] = Form(None),
    report_format: str = Form("concise"),
):
    """Improve a report based on reviewer feedback."""
    import json as _json

    refresh_env()

    try:
        reviews = _json.loads(reviews_json)
    except (_json.JSONDecodeError, ValueError):
        reviews = []

    if not reviews:
        raise HTTPException(status_code=400, detail="No review feedback provided")

    selected_model = model or get_tokamak_model()

    feedback_text = ""
    for review in reviews:
        reviewer_name = review.get("reviewer", "Reviewer")
        review_data = review.get("review", {})
        issues = review_data.get("issues", [])
        strengths = review_data.get("strengths", [])
        summary = review_data.get("summary", "")

        feedback_text += f"\n--- {reviewer_name} (Score: {review_data.get('overall_score', 'N/A')}/10) ---\n"
        feedback_text += f"Summary: {summary}\n"
        if strengths:
            feedback_text += "Strengths: " + "; ".join(strengths) + "\n"
        for issue in issues:
            severity = issue.get("severity", "medium")
            category = issue.get("category", "")
            desc = issue.get("description", "")
            suggestion = issue.get("suggestion", "")
            feedback_text += f"- [{severity}] {category}: {desc} -> {suggestion}\n"

    if report_type == "public":
        tone_instruction = (
            "Maintain an accessible, benefit-oriented tone. "
            "Avoid technical jargon. Focus on user impact and business value."
        )
    else:
        tone_instruction = (
            "Maintain a professional, technically precise tone. "
            "Include specific technical details, architecture decisions, and implementation specifics."
        )

    format_instruction = ""
    if report_type == "public":
        if report_format == "structured":
            format_instruction = (
                "8. Preserve Format B (Structured) across all sections: each section must have "
                "a title, introductory paragraph, 'Key Accomplishments' header, and 5 bullet points "
                "with **bold action phrases**. Ensure all sections follow this structure consistently."
            )
        else:
            format_instruction = (
                "8. Preserve Format A (Concise) across all sections: each section must have "
                "a one-sentence project overview followed by 5 bullet points with **bold action phrases**. "
                "No extra headers or title lines. Keep it compact and scannable."
            )
    else:
        format_instruction = (
            "8. Preserve the technical report format: each section must have a ### header, "
            "a one-sentence technical summary, and 2-5 bullet points in the format: "
            "[Action Verb] [Specific Function/Feature] in [Repository Path] ([Commit](URL)). "
            "Preserve all commit links, SHA references, and PR numbers. "
            "Do NOT remove technical details, function names, or repository paths."
        )

    prompt = f"""[Role]
You are a senior technical writer at a blockchain company. Your task is to improve a report based on reviewer feedback.

[Instructions]
1. Read the original report and the reviewer feedback carefully.
2. Address each reviewer's concerns where valid.
3. {tone_instruction}
4. Preserve all factual content — do not invent or fabricate information.
5. Keep the same overall structure (headers, sections).
6. Improve clarity, flow, and readability.
7. Output ONLY the improved report in markdown. No meta-commentary.
{format_instruction}

[Original Report]
{report_text}

[Reviewer Feedback]
{feedback_text}

[Improved Report]"""

    improved = generate_with_llm(prompt, max_tokens=3000, model=selected_model)

    if not improved:
        return JSONResponse({
            "success": False,
            "error": "Failed to improve report. Check AI model availability.",
        })

    return JSONResponse({
        "success": True,
        "improved_report": improved.strip(),
        "model": selected_model,
        "reviews_applied": len(reviews),
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
