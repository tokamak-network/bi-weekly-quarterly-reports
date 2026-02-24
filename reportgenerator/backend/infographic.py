"""
Tokamak Network Ecosystem Infographic Generator.

Generates a self-contained HTML page with 3 tabbed views:
  A) Domain Landscape Map
  B) Synergy Network Graph (SVG)
  C) Blueprint/Roadmap Timeline
"""

import json
import os
import math
import base64
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tokamak-logos")
GITHUB_ORG_URL = "https://github.com/tokamak-network"

# Category definitions with colors
CATEGORIES = {
    "Privacy & ZK": {"color": "#7C3AED", "bg": "#F5F3FF", "icon": "🔒"},
    "DeFi & Staking": {"color": "#2A72E5", "bg": "#EFF6FF", "icon": "💰"},
    "Infrastructure": {"color": "#64748B", "bg": "#F8FAFC", "icon": "🏗️"},
    "Developer Tools": {"color": "#16A34A", "bg": "#F0FDF4", "icon": "🛠️"},
    "AI & Automation": {"color": "#EA580C", "bg": "#FFF7ED", "icon": "🤖"},
    "Gaming & Social": {"color": "#DC2626", "bg": "#FEF2F2", "icon": "🎮"},
    "Governance": {"color": "#0D9488", "bg": "#F0FDFA", "icon": "🏛️"},
    "Research": {"color": "#CA8A04", "bg": "#FEFCE8", "icon": "📚"},
}

# Default classification based on PROJECT_REPOS and REPO_DESCRIPTIONS
DEFAULT_CLASSIFICATION = {
    "Privacy & ZK": [
        "Tokamak-zk-EVM", "Tokamak-zk-EVM-contracts", "private-app-channel-manager",
        "tokamak-zkp-channel-manager-new", "TokamakL2JS", "Tokamak-zk-EVM-landing-page",
        "zk-dex-d1-private-voting", "dust-protocol",
    ],
    "DeFi & Staking": [
        "ton-staking-v2", "staking-community-version", "RAT-frontend",
        "tokamak-landing-page",
    ],
    "Infrastructure": [
        "trh-sdk", "trh-backend", "trh-platform-ui", "DRB-node",
        "tokamak-thanos", "tokamak-rollup-hub-v2", "tokamak-thanos-stack",
        "tokamak-thanos-geth",
    ],
    "Developer Tools": [
        "TokamakL2JS",
    ],
    "AI & Automation": [
        "SentinAI", "auto-research-press",
    ],
    "Governance": [
        "tokamak-dao-v2", "tokamak-economics-whitepaper-v2",
    ],
    "Research": [
        "tokamak-economics-whitepaper-v2",
    ],
}

# Synergy connections (repo pairs that have cross-domain relationships)
SYNERGIES = [
    ("Tokamak-zk-EVM", "tokamak-thanos"),
    ("ton-staking-v2", "tokamak-dao-v2"),
    ("trh-sdk", "tokamak-thanos-stack"),
    ("SentinAI", "Tokamak-zk-EVM-contracts"),
    ("DRB-node", "zk-dex-d1-private-voting"),
    ("dust-protocol", "private-app-channel-manager"),
    ("tokamak-rollup-hub-v2", "trh-platform-ui"),
]

# Default descriptions for repos
DEFAULT_DESCRIPTIONS = {
    "Tokamak-zk-EVM": "Core ZK-EVM engine for private smart contract execution",
    "Tokamak-zk-EVM-contracts": "On-chain contracts for ZK-EVM verification",
    "private-app-channel-manager": "SDK for private application channels",
    "tokamak-zkp-channel-manager-new": "Next-gen ZK proof channel manager",
    "TokamakL2JS": "JavaScript library for Tokamak L2 interaction",
    "Tokamak-zk-EVM-landing-page": "ZK-EVM project documentation site",
    "ton-staking-v2": "TON token staking platform",
    "tokamak-economics-whitepaper-v2": "TON economic model & tokenomics research",
    "RAT-frontend": "Staking reward verification interface",
    "staking-community-version": "Community staking dashboard",
    "tokamak-dao-v2": "Decentralized governance platform",
    "tokamak-landing-page": "Main Tokamak Network website",
    "trh-sdk": "SDK for deploying custom L2 rollups",
    "trh-backend": "Rollup Hub backend infrastructure",
    "trh-platform-ui": "Rollup management dashboard",
    "DRB-node": "Distributed Random Beacon for rollup sequencing",
    "tokamak-thanos": "Optimistic rollup implementation for Ethereum",
    "tokamak-rollup-hub-v2": "One-click L2 chain deployment platform",
    "tokamak-thanos-stack": "Full-stack Thanos rollup tooling",
    "tokamak-thanos-geth": "Modified Geth for Thanos rollup",
    "SentinAI": "AI-powered smart contract security auditing",
    "zk-dex-d1-private-voting": "ZK-based private on-chain voting",
    "dust-protocol": "Privacy-focused confidential token transfers",
    "auto-research-press": "Automated blockchain research publisher",
}

# Default synergy data (used when no AI classification is provided)
DEFAULT_SYNERGIES = [
    {
        "domains": ["Privacy & ZK", "Infrastructure"],
        "title": "Private Rollup Execution",
        "description": "ZK-EVM proof generation runs on top of the Thanos rollup stack, enabling private L2 transaction execution by combining zero-knowledge circuits with optimistic rollup settlement.",
        "involved_repos": ["Tokamak-zk-EVM", "tokamak-thanos"],
        "potential": "high",
    },
    {
        "domains": ["DeFi & Staking", "Governance"],
        "title": "Staking-Powered Governance",
        "description": "TON stakers gain voting power in the DAO proportional to their stake, linking economic commitment to governance influence and aligning incentives across the network.",
        "involved_repos": ["ton-staking-v2", "tokamak-dao-v2"],
        "potential": "high",
    },
    {
        "domains": ["Infrastructure", "Developer Tools"],
        "title": "Rollup Developer SDK",
        "description": "The TRH SDK wraps the Thanos rollup stack into a developer-friendly interface, enabling one-click L2 chain deployment without managing low-level infrastructure.",
        "involved_repos": ["trh-sdk", "tokamak-thanos-stack"],
        "potential": "high",
    },
    {
        "domains": ["AI & Automation", "Privacy & ZK"],
        "title": "AI-Powered Security Auditing",
        "description": "SentinAI uses automated analysis to audit ZK-EVM smart contracts, detecting potential vulnerabilities in zero-knowledge circuit implementations.",
        "involved_repos": ["SentinAI", "Tokamak-zk-EVM-contracts"],
        "potential": "medium",
    },
    {
        "domains": ["Privacy & ZK", "Governance"],
        "title": "Private Voting",
        "description": "Zero-knowledge proofs allow governance votes to be verified without revealing individual choices, enabling confidential on-chain voting in the DAO.",
        "involved_repos": ["zk-dex-d1-private-voting", "tokamak-dao-v2"],
        "potential": "medium",
    },
    {
        "domains": ["DeFi & Staking", "Infrastructure"],
        "title": "L2 Staking Infrastructure",
        "description": "Staking contracts are deployed on the Thanos L2 rollup, reducing gas costs for stakers while inheriting Ethereum L1 security guarantees.",
        "involved_repos": ["ton-staking-v2", "tokamak-thanos"],
        "potential": "medium",
    },
    {
        "domains": ["Infrastructure", "AI & Automation"],
        "title": "Automated Infrastructure Monitoring",
        "description": "AI agents analyze DRB node metrics and logs to detect anomalies in rollup sequencing and random beacon generation.",
        "involved_repos": ["DRB-node", "SentinAI"],
        "potential": "low",
    },
    {
        "domains": ["Research", "DeFi & Staking"],
        "title": "Tokenomics Research",
        "description": "Economic modeling research directly informs staking reward curves and token distribution parameters in the staking contracts.",
        "involved_repos": ["tokamak-economics-whitepaper-v2", "ton-staking-v2"],
        "potential": "high",
    },
]

# Default blueprint is no longer used — blueprint is generated dynamically
# from actual repo activity data in _build_blueprint_from_activity().
DEFAULT_BLUEPRINT = None


def _load_logo_base64() -> str:
    path = os.path.join(LOGO_DIR, "3_transparent.png")
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{data}"


def classify_repos_from_csv(
    repo_commits: Dict[str, int],
    descriptions: Optional[Dict[str, str]] = None,
    classification: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """Classify repos into categories. Returns {category: [{name, description, commits}]}."""

    desc = {**DEFAULT_DESCRIPTIONS}
    if descriptions:
        desc.update(descriptions)

    if classification:
        cat_map = classification
    else:
        cat_map = DEFAULT_CLASSIFICATION

    # Build reverse map: repo -> category
    repo_to_cat = {}  # type: Dict[str, str]
    for cat, repos in cat_map.items():
        for r in repos:
            if r not in repo_to_cat:
                repo_to_cat[r] = cat

    # Classify remaining repos by name heuristics
    for repo in repo_commits:
        if repo in repo_to_cat:
            continue
        name_lower = repo.lower()
        if any(k in name_lower for k in ("zk", "priv", "proof", "snark")):
            repo_to_cat[repo] = "Privacy & ZK"
        elif any(k in name_lower for k in ("stak", "ton-", "swap", "defi", "bridge")):
            repo_to_cat[repo] = "DeFi & Staking"
        elif any(k in name_lower for k in ("thanos", "rollup", "trh", "node", "geth", "l2", "chain")):
            repo_to_cat[repo] = "Infrastructure"
        elif any(k in name_lower for k in ("sdk", "lib", "tool", "cli", "js", "api")):
            repo_to_cat[repo] = "Developer Tools"
        elif any(k in name_lower for k in ("ai", "auto", "bot", "agent", "sentinel")):
            repo_to_cat[repo] = "AI & Automation"
        elif any(k in name_lower for k in ("game", "social", "nft", "market")):
            repo_to_cat[repo] = "Gaming & Social"
        elif any(k in name_lower for k in ("dao", "gov", "vote", "proposal")):
            repo_to_cat[repo] = "Governance"
        elif any(k in name_lower for k in ("research", "paper", "doc", "spec", "whitepaper")):
            repo_to_cat[repo] = "Research"
        else:
            repo_to_cat[repo] = "Infrastructure"

    # Build result — only include repos with actual commits (> 0)
    result = {cat: [] for cat in CATEGORIES}  # type: Dict[str, List[Dict[str, Any]]]
    seen = set()  # type: set
    for repo, commits in sorted(repo_commits.items(), key=lambda x: -x[1]):
        if commits <= 0:
            continue
        cat = repo_to_cat.get(repo, "Infrastructure")
        if cat not in CATEGORIES:
            cat = "Infrastructure"
        if repo in seen:
            continue
        seen.add(repo)
        result[cat].append({
            "name": repo,
            "description": desc.get(repo, _infer_description(repo)),
            "commits": commits,
        })

    # Only show repos that have actual commits in the CSV data.
    # Do NOT add repos from default classification that have 0 commits.

    return result


def _infer_description(repo_name: str) -> str:
    name = repo_name.replace("-", " ").replace("_", " ")
    return f"{name} component"


def _activity_level(commits: int) -> Tuple[str, str]:
    if commits >= 20:
        return "#22C55E", "high"
    elif commits >= 5:
        return "#EAB308", "medium"
    else:
        return "#9CA3AF", "low"


def _escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")


def generate_infographic_html(
    categorized_repos: Dict[str, List[Dict[str, Any]]],
    title: str = "Tokamak Network Ecosystem",
    date_range: Optional[Dict[str, str]] = None,
    synergies: Optional[List[Dict[str, Any]]] = None,
    blueprint: Optional[Dict[str, Any]] = None,
) -> str:
    """Generate a self-contained HTML infographic page with 3 tabbed views."""

    logo_data = _load_logo_base64()

    # Count totals
    total_repos = sum(len(repos) for repos in categorized_repos.values())
    total_commits = sum(r["commits"] for repos in categorized_repos.values() for r in repos)
    active_categories = sum(1 for repos in categorized_repos.values() if repos)

    date_label = ""
    if date_range:
        date_label = f'{date_range.get("start", "")} — {date_range.get("end", "")}'

    # Use defaults if not provided
    syn_data = synergies if synergies else DEFAULT_SYNERGIES

    # Filter synergies: only keep those whose involved repos have actual commits
    active_repo_names = set()
    for repos in categorized_repos.values():
        for r in repos:
            if r["commits"] > 0:
                active_repo_names.add(r["name"])

    # Also filter: only keep synergies where both domains have active repos
    active_domains = {cat for cat, repos in categorized_repos.items() if repos}
    filtered_synergies = []
    for s in syn_data:
        domains = s.get("domains", [])
        involved = s.get("involved_repos", [])
        # Both domains must have repos and at least one involved repo must be active
        if (len(domains) >= 2
                and domains[0] in active_domains
                and domains[1] in active_domains
                and any(r in active_repo_names for r in involved)):
            filtered_synergies.append(s)
    syn_data = filtered_synergies

    # ── View A: Domain Landscape ──
    landscape_html = _build_landscape_html(categorized_repos, total_repos, total_commits, active_categories)

    # ── View B: Synergy Network Graph ──
    synergy_html = _build_synergy_html(categorized_repos, syn_data)

    # ── View C: Blueprint Timeline (always derived from activity data) ──
    blueprint_html = _build_blueprint_html(blueprint, categorized_repos)

    # ── Synergy data as JSON for tooltips ──
    syn_json = json.dumps(syn_data)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_escape_html(title)}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
body{{
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    background:#f8f9fa;
    color:#1a1a1a;
    line-height:1.5;
    min-height:100vh;
}}

/* Header */
.header{{
    background:#fff;
    color:#1a1a1a;
    text-align:center;
    padding:24px 24px 16px;
    position:relative;
    border-bottom:1px solid #e8e8e8;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}}
.header-logo{{
    height:200px;
    margin-bottom:8px;
    object-fit:contain;
}}
.header h1{{
    font-size:28px;
    font-weight:700;
    letter-spacing:-0.5px;
    color:#1a1a1a;
    margin-bottom:4px;
}}
.header .subtitle{{
    font-size:14px;
    color:#555;
    font-weight:400;
}}
.header .date-label{{
    font-size:12px;
    color:#888;
    margin-top:6px;
}}

/* Tabs */
.tab-bar{{
    display:flex;
    justify-content:center;
    gap:0;
    background:#fff;
    border-bottom:1px solid #e8e8e8;
    position:sticky;
    top:0;
    z-index:100;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}}
.tab-btn{{
    background:none;
    border:none;
    color:#888;
    font-size:15px;
    font-weight:500;
    padding:14px 28px;
    cursor:pointer;
    border-bottom:3px solid transparent;
    transition:all 0.2s;
    font-family:inherit;
    position:relative;
}}
.tab-btn:hover{{
    color:#1a1a1a;
    background:rgba(42,114,229,0.04);
}}
.tab-btn.active{{
    color:#2A72E5;
    font-weight:700;
    border-bottom-color:#2A72E5;
}}

/* Tab panels */
.tab-panel{{
    display:none;
    animation:fadeIn 0.3s ease;
}}
.tab-panel.active{{
    display:block;
}}
@keyframes fadeIn{{
    from{{opacity:0;transform:translateY(8px);}}
    to{{opacity:1;transform:translateY(0);}}
}}

/* ── View A: Landscape ── */
.stats-bar{{
    display:flex;
    justify-content:center;
    gap:48px;
    padding:20px 24px;
    background:#fff;
    border-bottom:1px solid #e8e8e8;
}}
.stat{{display:flex;flex-direction:column;align-items:center;}}
.stat-num{{font-size:26px;font-weight:700;color:#2A72E5;}}
.stat-label{{font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;margin-top:2px;}}

.legend,.activity-legend{{
    display:flex;
    justify-content:center;
    flex-wrap:wrap;
    gap:14px;
    padding:12px 24px;
    background:#fff;
    border-bottom:1px solid #f0f0f0;
}}
.legend-item{{
    display:inline-flex;
    align-items:center;
    gap:6px;
    font-size:12px;
    color:#555;
}}
.legend-dot{{
    width:9px;height:9px;border-radius:50%;
    display:inline-block;flex-shrink:0;
}}
.legend-label{{
    font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;
}}

.landscape-grid{{
    max-width:1400px;
    margin:0 auto;
    padding:28px 24px;
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
    gap:20px;
}}

.category-section{{
    background:#fff;
    border-radius:12px;
    overflow:hidden;
    border:1px solid #e8e8e8;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
    transition:border-color 0.2s;
}}
.category-section:hover{{
    border-color:#d0d0d0;
}}
.category-header{{
    display:flex;
    align-items:center;
    gap:10px;
    padding:14px 16px;
    font-weight:600;
    font-size:14px;
    color:#1a1a1a;
    background:#fff;
    border-left:4px solid #888;
}}
.category-icon{{font-size:16px;}}
.category-title{{flex:1;}}
.category-count{{
    background:#f0f0f0;
    color:#555;
    padding:2px 10px;
    border-radius:10px;
    font-size:11px;
    font-weight:700;
}}
.category-repos{{
    padding:10px;
    display:flex;
    flex-direction:column;
    gap:6px;
}}

.repo-card{{
    display:block;
    padding:8px 10px;
    border-radius:6px;
    background:#f8f9fa;
    text-decoration:none;
    color:inherit;
    transition:all 0.15s;
    cursor:pointer;
    border:1px solid transparent;
}}
.repo-card:hover{{
    background:#f0f0f0;
    border-color:#e8e8e8;
    transform:translateX(2px);
}}
.repo-header{{
    display:flex;
    align-items:center;
    gap:7px;
    margin-bottom:3px;
}}
.activity-dot{{
    width:7px;height:7px;border-radius:50%;
    flex-shrink:0;
}}
.repo-name{{
    font-weight:600;
    font-size:12px;
    color:#1a1a1a;
    word-break:break-all;
}}
.repo-desc{{
    font-size:11px;
    color:#555;
    line-height:1.3;
    display:-webkit-box;
    -webkit-line-clamp:2;
    -webkit-box-orient:vertical;
    overflow:hidden;
}}
.repo-card:hover .repo-desc{{
    -webkit-line-clamp:unset;
    overflow:visible;
}}

/* ── View B: Synergy Network ── */
.synergy-container{{
    display:flex;
    flex-direction:column;
    align-items:center;
    padding:32px 16px;
    min-height:700px;
}}
.synergy-svg-wrap{{
    position:relative;
    width:100%;
    max-width:800px;
}}
.synergy-svg{{
    width:100%;
    height:auto;
}}
.synergy-legend{{
    display:flex;
    gap:24px;
    margin-top:20px;
    flex-wrap:wrap;
    justify-content:center;
}}
.synergy-legend-item{{
    display:flex;
    align-items:center;
    gap:8px;
    font-size:12px;
    color:#555;
}}
.synergy-legend-line{{
    width:32px;
    height:0;
    border-top:3px solid #888;
}}
.synergy-legend-line.dashed{{
    border-top-style:dashed;
}}
.synergy-legend-line.thick{{
    border-top-width:4px;
    border-top-color:#2A72E5;
}}
.synergy-legend-line.thin{{
    border-top-width:2px;
    border-top-color:#888;
}}

/* Tooltip */
.tooltip{{
    position:fixed;
    background:#fff;
    border:1px solid #e8e8e8;
    border-radius:12px;
    padding:14px 18px;
    max-width:360px;
    font-size:12px;
    color:#1a1a1a;
    pointer-events:none;
    z-index:1000;
    display:none;
    box-shadow:0 4px 16px rgba(0,0,0,0.10);
}}
.tooltip-title{{
    font-weight:700;
    font-size:14px;
    color:#1a1a1a;
    margin-bottom:6px;
}}
.tooltip-level{{
    display:inline-block;
    font-size:10px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.5px;
    padding:2px 8px;
    border-radius:4px;
    margin-bottom:6px;
}}
.tooltip-level.high{{background:#EFF6FF;color:#2A72E5;}}
.tooltip-level.medium{{background:#FFF7ED;color:#EA580C;}}
.tooltip-level.low{{background:#F8FAFC;color:#64748B;}}
.tooltip-desc{{
    color:#555;
    line-height:1.5;
    margin-bottom:8px;
}}
.tooltip-repos{{
    display:flex;
    flex-wrap:wrap;
    gap:4px;
}}
.tooltip-chip{{
    background:#f0f0f0;
    padding:2px 8px;
    border-radius:4px;
    font-size:10px;
    color:#555;
}}

/* ── View C: Blueprint ── */
.blueprint-container{{
    max-width:1100px;
    margin:0 auto;
    padding:32px 24px;
}}
.blueprint-vision{{
    text-align:center;
    padding:24px 32px;
    background:#fff;
    border:1px solid #e8e8e8;
    border-radius:12px;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
    margin-bottom:32px;
    font-size:15px;
    color:#444;
    line-height:1.6;
}}
.blueprint-vision .vision-label{{
    font-size:0.75rem;
    text-transform:uppercase;
    letter-spacing:1px;
    color:#2A72E5;
    font-weight:700;
    margin-bottom:8px;
}}

.timeline{{
    display:flex;
    gap:0;
    position:relative;
}}
.timeline::before{{
    content:'';
    position:absolute;
    top:28px;
    left:0;
    right:0;
    height:3px;
    background:linear-gradient(90deg,#2A72E5,#7C3AED,#16A34A);
    border-radius:2px;
    z-index:0;
}}

.phase{{
    flex:1;
    position:relative;
    padding:0 12px;
}}
.phase-dot{{
    width:16px;
    height:16px;
    border-radius:50%;
    background:#2A72E5;
    border:3px solid #f8f9fa;
    position:relative;
    z-index:1;
    margin:20px auto 16px;
}}
.phase:nth-child(2) .phase-dot{{background:#7C3AED;}}
.phase:nth-child(3) .phase-dot{{background:#16A34A;}}

.phase-card{{
    background:#fff;
    border:1px solid #e8e8e8;
    border-radius:12px;
    padding:24px;
    margin-top:8px;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}}
.phase-timeframe{{
    font-size:0.75rem;
    text-transform:uppercase;
    letter-spacing:0.8px;
    color:#2A72E5;
    font-weight:700;
    margin-bottom:4px;
}}
.phase:nth-child(2) .phase-timeframe{{color:#7C3AED;}}
.phase:nth-child(3) .phase-timeframe{{color:#16A34A;}}

.phase-title{{
    font-size:16px;
    font-weight:700;
    color:#1a1a1a;
    margin-bottom:12px;
}}
.phase-goals{{
    list-style:none;
    padding:0;
}}
.phase-goals li{{
    font-size:13px;
    color:#444;
    padding:6px 0;
    border-bottom:1px solid #f0f0f0;
    display:flex;
    align-items:flex-start;
    gap:8px;
}}
.phase-goals li:last-child{{border-bottom:none;}}
.phase-goals li::before{{
    content:'→';
    color:#888;
    flex-shrink:0;
    font-weight:700;
}}
.phase-chips{{
    display:flex;
    flex-wrap:wrap;
    gap:4px;
    margin-top:12px;
}}
.phase-chip{{
    padding:2px 8px;
    border-radius:4px;
    font-size:10px;
    font-weight:600;
    background:#f0f0f0;
    color:#555;
}}

.you-are-here{{
    text-align:center;
    margin-top:16px;
    margin-bottom:4px;
}}
.you-are-here span{{
    display:inline-block;
    background:#2A72E5;
    color:white;
    padding:4px 14px;
    border-radius:12px;
    font-size:11px;
    font-weight:700;
    letter-spacing:0.5px;
}}

/* Footer */
.footer{{
    text-align:center;
    padding:24px;
    color:#888;
    font-size:11px;
    border-top:1px solid #e8e8e8;
    margin-top:32px;
}}
.footer a{{color:#2A72E5;text-decoration:none;}}

/* Print */
@media print{{
    body{{background:white;color:#1a1a1a;}}
    .tab-bar{{position:static;}}
    .tab-panel{{display:block !important;page-break-before:always;}}
    .tab-panel:first-of-type{{page-break-before:auto;}}
    .tooltip{{display:none !important;}}
}}

/* Responsive */
@media(max-width:768px){{
    .header h1{{font-size:22px;}}
    .header-logo{{height:200px;}}
    .stats-bar{{gap:20px;}}
    .stat-num{{font-size:20px;}}
    .landscape-grid{{grid-template-columns:1fr;padding:16px;}}
    .timeline{{flex-direction:column;gap:16px;}}
    .timeline::before{{display:none;}}
    .tab-btn{{padding:10px 16px;font-size:13px;}}
}}
</style>
</head>
<body>

<div class="header">
    {"<img src='" + logo_data + "' alt='Tokamak Network' class='header-logo'>" if logo_data else ""}
    <h1>{_escape_html(title)}</h1>
    <div class="subtitle">Interactive Ecosystem Infographic</div>
    {"<div class='date-label'>" + _escape_html(date_label) + "</div>" if date_label else ""}
</div>

<div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('landscape',this)">🗺️ Landscape</button>
    <button class="tab-btn" onclick="switchTab('synergy',this)">🔗 Synergies</button>
    <button class="tab-btn" onclick="switchTab('blueprint',this)">📍 Blueprint</button>
</div>

<div id="panel-landscape" class="tab-panel active">
{landscape_html}
</div>

<div id="panel-synergy" class="tab-panel">
{synergy_html}
</div>

<div id="panel-blueprint" class="tab-panel">
{blueprint_html}
</div>

<div class="tooltip" id="tooltip"></div>

<div class="footer">
    <p>Generated by <a href="{GITHUB_ORG_URL}">Tokamak Network</a> Report Generator</p>
    <p style="margin-top:4px;">Click any repository card to view on GitHub</p>
</div>

<script>
var synergyData = {syn_json};

function switchTab(id, btn) {{
    document.querySelectorAll('.tab-panel').forEach(function(p){{ p.classList.remove('active'); }});
    document.querySelectorAll('.tab-btn').forEach(function(b){{ b.classList.remove('active'); }});
    document.getElementById('panel-' + id).classList.add('active');
    btn.classList.add('active');
}}

// Tooltip handling
var tip = document.getElementById('tooltip');
function showTip(e, html) {{
    tip.innerHTML = html;
    tip.style.display = 'block';
    var x = e.clientX + 16;
    var y = e.clientY + 16;
    if (x + 320 > window.innerWidth) x = e.clientX - 336;
    if (y + 200 > window.innerHeight) y = e.clientY - 200;
    tip.style.left = x + 'px';
    tip.style.top = y + 'px';
}}
function hideTip() {{
    tip.style.display = 'none';
}}

// Domain node hover
document.querySelectorAll('.domain-node').forEach(function(node) {{
    node.addEventListener('mouseenter', function(e) {{
        var domain = this.getAttribute('data-domain');
        var repos = JSON.parse(this.getAttribute('data-repos') || '[]');
        var h = '<div class="tooltip-title">' + domain + '</div>';
        // find synergies involving this domain
        var related = synergyData.filter(function(s){{ return s.domains.indexOf(domain) !== -1; }});
        if (related.length > 0) {{
            h += '<div class="tooltip-desc">' + related.map(function(s){{return s.title;}}).join(', ') + '</div>';
        }}
        if (repos.length > 0) {{
            h += '<div class="tooltip-repos">' + repos.map(function(r){{return '<span class="tooltip-chip">'+r+'</span>';}}).join('') + '</div>';
        }}
        showTip(e, h);
    }});
    node.addEventListener('mousemove', function(e) {{
        var x = e.clientX + 16;
        var y = e.clientY + 16;
        if (x + 320 > window.innerWidth) x = e.clientX - 336;
        if (y + 200 > window.innerHeight) y = e.clientY - 200;
        tip.style.left = x + 'px';
        tip.style.top = y + 'px';
    }});
    node.addEventListener('mouseleave', hideTip);
}});

// Synergy line hover — shows reasoning, repos, and level
document.querySelectorAll('.synergy-line').forEach(function(line) {{
    line.addEventListener('mouseenter', function(e) {{
        var idx = parseInt(this.getAttribute('data-idx'));
        var s = synergyData[idx];
        if (!s) return;
        var lvl = (s.potential || 'medium').toLowerCase();
        var lvlLabel = lvl.charAt(0).toUpperCase() + lvl.slice(1) + ' Synergy';
        var h = '<div class="tooltip-title">' + s.title + '</div>';
        h += '<span class="tooltip-level ' + lvl + '">' + lvlLabel + '</span>';
        h += '<div class="tooltip-desc">' + s.description + '</div>';
        h += '<div class="tooltip-repos">' + (s.involved_repos||[]).map(function(r){{return '<span class="tooltip-chip">'+r+'</span>';}}).join('') + '</div>';
        showTip(e, h);
    }});
    line.addEventListener('mousemove', function(e) {{
        var x = e.clientX + 16;
        var y = e.clientY + 16;
        if (x + 360 > window.innerWidth) x = e.clientX - 376;
        if (y + 200 > window.innerHeight) y = e.clientY - 200;
        tip.style.left = x + 'px';
        tip.style.top = y + 'px';
    }});
    line.addEventListener('mouseleave', hideTip);
}});
</script>

</body>
</html>'''

    return html


def _build_landscape_html(
    categorized_repos: Dict[str, List[Dict[str, Any]]],
    total_repos: int,
    total_commits: int,
    active_categories: int,
) -> str:
    """Build the Domain Landscape Map tab content."""

    stats_html = f'''
    <div class="stats-bar">
        <div class="stat"><span class="stat-num">{total_repos}</span><span class="stat-label">Repositories</span></div>
        <div class="stat"><span class="stat-num">{total_commits:,}</span><span class="stat-label">Commits</span></div>
        <div class="stat"><span class="stat-num">{active_categories}</span><span class="stat-label">Categories</span></div>
    </div>
    '''

    legend_items = []
    for cat_name, cat_info in CATEGORIES.items():
        if categorized_repos.get(cat_name):
            legend_items.append(
                f'<span class="legend-item"><span class="legend-dot" style="background:{cat_info["color"]};"></span>{cat_name}</span>'
            )
    legend_html = f'<div class="legend">{"".join(legend_items)}</div>'

    activity_legend = '''
    <div class="activity-legend">
        <span class="legend-label">Activity:</span>
        <span class="legend-item"><span class="legend-dot" style="background:#22C55E;"></span>High (20+)</span>
        <span class="legend-item"><span class="legend-dot" style="background:#EAB308;"></span>Medium (5-19)</span>
        <span class="legend-item"><span class="legend-dot" style="background:#9CA3AF;"></span>Low (&lt;5)</span>
    </div>
    '''

    categories_html = []
    for cat_name, cat_info in CATEGORIES.items():
        repos = categorized_repos.get(cat_name, [])
        if not repos:
            continue

        repo_cards = []
        for repo in repos:
            act_color, act_label = _activity_level(repo["commits"])
            commit_text = f'{repo["commits"]} commits' if repo["commits"] > 0 else "no recent activity"
            repo_cards.append(f'''
                <a href="{GITHUB_ORG_URL}/{repo["name"]}" target="_blank" rel="noopener"
                   class="repo-card" style="border-left:3px solid {cat_info["color"]};"
                   title="{_escape_html(repo["description"])}&#10;&#10;{commit_text}">
                    <div class="repo-header">
                        <span class="activity-dot" style="background:{act_color};" title="{act_label} activity"></span>
                        <span class="repo-name">{_escape_html(repo["name"])}</span>
                    </div>
                    <div class="repo-desc">{_escape_html(repo["description"])}</div>
                </a>
            ''')

        repo_count = len(repos)
        cat_commits = sum(r["commits"] for r in repos)
        categories_html.append(f'''
            <div class="category-section" data-category="{cat_name}">
                <div class="category-header" style="border-left-color:{cat_info["color"]};">
                    <span class="category-icon">{cat_info["icon"]}</span>
                    <span class="category-title">{cat_name}</span>
                    <span class="category-count">{repo_count} repos · {cat_commits} commits</span>
                </div>
                <div class="category-repos">
                    {"".join(repo_cards)}
                </div>
            </div>
        ''')

    return f'''
    {stats_html}
    {legend_html}
    {activity_legend}
    <div class="landscape-grid">
        {"".join(categories_html)}
    </div>
    '''


def _build_synergy_html(
    categorized_repos: Dict[str, List[Dict[str, Any]]],
    synergies: List[Dict[str, Any]],
) -> str:
    """Build the Synergy Network Graph SVG tab content."""

    # Determine active domains (ones with repos)
    active_domains = [cat for cat, repos in categorized_repos.items() if repos]

    if not active_domains:
        return '<div class="synergy-container"><p>No domain data available.</p></div>'

    # SVG dimensions
    W = 700
    H = 700
    CX = W / 2
    CY = H / 2
    R = 240  # radius for domain nodes

    # Position domain nodes radially
    domain_positions = {}  # type: Dict[str, Tuple[float, float]]
    n = len(active_domains)
    for i, domain in enumerate(active_domains):
        angle = (2 * math.pi * i / n) - math.pi / 2  # start from top
        x = CX + R * math.cos(angle)
        y = CY + R * math.sin(angle)
        domain_positions[domain] = (x, y)

    # Build SVG lines for synergies
    lines_svg = []
    for idx, syn in enumerate(synergies):
        d1 = syn.get("domains", [None, None])[0]
        d2 = syn.get("domains", [None, None])[1] if len(syn.get("domains", [])) > 1 else None
        if not d1 or not d2:
            continue
        if d1 not in domain_positions or d2 not in domain_positions:
            continue
        x1, y1 = domain_positions[d1]
        x2, y2 = domain_positions[d2]
        potential = syn.get("potential", "medium")
        stroke_width = 3 if potential == "high" else 2
        dash = "" if potential in ("high", "medium") else 'stroke-dasharray="8,4"'
        opacity = 0.7 if potential == "high" else 0.4 if potential == "medium" else 0.25
        color = "#2A72E5" if potential == "high" else "#8B949E"
        # Visible line
        lines_svg.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{stroke_width}" {dash} '
            f'opacity="{opacity}" style="pointer-events:none;" />'
        )
        # Invisible wider overlay for easier hover targeting
        lines_svg.append(
            f'<line class="synergy-line" data-idx="{idx}" '
            f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="transparent" stroke-width="18" '
            f'style="cursor:pointer;pointer-events:stroke;" />'
        )

    # Build SVG nodes for domains
    nodes_svg = []
    for domain in active_domains:
        x, y = domain_positions[domain]
        cat_info = CATEGORIES.get(domain, {"color": "#8B949E", "icon": "?"})
        color = cat_info["color"]
        repos = categorized_repos.get(domain, [])
        repo_names = [r["name"] for r in repos]
        repo_json = json.dumps(repo_names)
        repo_count = len(repos)
        node_r = 32 + min(repo_count, 10) * 2  # scale node size

        # Glow filter
        nodes_svg.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r + 8}" '
            f'fill="{color}" opacity="0.08" />'
        )
        nodes_svg.append(
            f'<circle class="domain-node" data-domain="{_escape_html(domain)}" '
            f'data-repos=\'{_escape_html(repo_json)}\' '
            f'cx="{x:.1f}" cy="{y:.1f}" r="{node_r}" '
            f'fill="{color}" opacity="0.85" style="cursor:pointer;" />'
        )
        # Label
        label_parts = domain.split(" & ")
        if len(label_parts) == 1:
            nodes_svg.append(
                f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" '
                f'fill="white" font-size="11" font-weight="700" style="pointer-events:none;">{_escape_html(domain)}</text>'
            )
        else:
            nodes_svg.append(
                f'<text x="{x:.1f}" y="{y - 2:.1f}" text-anchor="middle" '
                f'fill="white" font-size="11" font-weight="700" style="pointer-events:none;">{_escape_html(label_parts[0])} &amp;</text>'
            )
            nodes_svg.append(
                f'<text x="{x:.1f}" y="{y + 12:.1f}" text-anchor="middle" '
                f'fill="white" font-size="11" font-weight="700" style="pointer-events:none;">{_escape_html(label_parts[1])}</text>'
            )
        # Repo count badge
        nodes_svg.append(
            f'<text x="{x:.1f}" y="{y + node_r + 16:.1f}" text-anchor="middle" '
            f'fill="#888" font-size="10">{repo_count} repos</text>'
        )

    # Center hub node
    center_hub = f'''
        <circle cx="{CX}" cy="{CY}" r="52" fill="#2A72E5" opacity="0.12" />
        <circle cx="{CX}" cy="{CY}" r="42" fill="#2A72E5" opacity="0.9" />
        <text x="{CX}" y="{CY - 6}" text-anchor="middle" fill="white" font-size="11" font-weight="800">Tokamak</text>
        <text x="{CX}" y="{CY + 8}" text-anchor="middle" fill="white" font-size="10" font-weight="600">Network</text>
    '''

    # Lines from center to each domain (subtle)
    center_lines = []
    for domain in active_domains:
        x, y = domain_positions[domain]
        center_lines.append(
            f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" '
            f'stroke="#e8e8e8" stroke-width="1" opacity="0.5" />'
        )

    svg = f'''
    <svg class="synergy-svg" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
        {"".join(center_lines)}
        {"".join(lines_svg)}
        {center_hub}
        {"".join(nodes_svg)}
    </svg>
    '''

    legend = '''
    <div class="synergy-legend">
        <div class="synergy-legend-item">
            <span class="synergy-legend-line thick"></span>
            <span>High synergy</span>
        </div>
        <div class="synergy-legend-item">
            <span class="synergy-legend-line thin"></span>
            <span>Medium synergy</span>
        </div>
        <div class="synergy-legend-item">
            <span class="synergy-legend-line thin dashed"></span>
            <span>Potential synergy</span>
        </div>
    </div>
    '''

    return f'''
    <div class="synergy-container">
        <div class="synergy-svg-wrap">
            {svg}
        </div>
        {legend}
    </div>
    '''


def _build_blueprint_from_activity(
    categorized_repos: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Any]:
    """Generate blueprint data purely from actual repo activity levels.

    Repos are sorted by commit count and grouped into three tiers:
      - Active Development: repos with ≥20 commits
      - Emerging: repos with 5–19 commits
      - Exploratory: repos with 1–4 commits

    No speculative language — only factual descriptions of current work.
    """
    all_repos = []
    for cat_name, repos in categorized_repos.items():
        for r in repos:
            if r["commits"] > 0:
                all_repos.append({**r, "category": cat_name})

    all_repos.sort(key=lambda x: -x["commits"])

    active = [r for r in all_repos if r["commits"] >= 20]
    emerging = [r for r in all_repos if 5 <= r["commits"] < 20]
    exploratory = [r for r in all_repos if 1 <= r["commits"] < 5]

    def _make_goals(repos: list) -> list:
        goals = []
        for r in repos[:6]:  # cap at 6 per phase
            goals.append(f'Active work in {r["name"]} ({r["commits"]} commits) — {r["description"]}')
        return goals

    # Derive vision from what's actually being built
    domain_commits = defaultdict(int)
    for r in all_repos:
        domain_commits[r["category"]] += r["commits"]
    top_domains = sorted(domain_commits.items(), key=lambda x: -x[1])[:3]
    domain_names = [d[0] for d in top_domains]
    vision = (
        f"Current development is concentrated across {', '.join(domain_names)}. "
        f"The ecosystem shows {len(all_repos)} repositories with recent commit activity, "
        f"with the highest concentration in {domain_names[0] if domain_names else 'infrastructure'}."
    )

    phases = []
    if active:
        phases.append({
            "timeframe": "Active Development",
            "goals": _make_goals(active),
            "key_repos": [r["name"] for r in active[:6]],
        })
    if emerging:
        phases.append({
            "timeframe": "Emerging",
            "goals": _make_goals(emerging),
            "key_repos": [r["name"] for r in emerging[:6]],
        })
    if exploratory:
        phases.append({
            "timeframe": "Exploratory",
            "goals": _make_goals(exploratory),
            "key_repos": [r["name"] for r in exploratory[:6]],
        })

    return {"vision": vision, "phases": phases}


def _build_blueprint_html(
    blueprint: Optional[Dict[str, Any]],
    categorized_repos: Dict[str, List[Dict[str, Any]]],
) -> str:
    """Build the Blueprint/Roadmap Timeline tab content.

    Blueprint is always generated from actual repo activity data.
    The `blueprint` parameter from AI is ignored to avoid fabrication.
    """

    # Always derive from real data
    bp = _build_blueprint_from_activity(categorized_repos)
    vision = bp.get("vision", "")
    phases = bp.get("phases", [])

    # Build repo -> domain color map
    repo_colors = {}  # type: Dict[str, str]
    for cat_name, cat_info in CATEGORIES.items():
        for repo in categorized_repos.get(cat_name, []):
            repo_colors[repo["name"]] = cat_info["color"]

    vision_html = ""
    if vision:
        vision_html = f'''
        <div class="blueprint-vision">
            <div class="vision-label">📊 Ecosystem Activity Summary</div>
            {_escape_html(vision)}
        </div>
        '''

    phase_meta = [
        {"label": "Active Development", "desc": "High commit activity (20+ commits)", "color": "#2A72E5"},
        {"label": "Emerging", "desc": "Moderate activity (5–19 commits)", "color": "#7C3AED"},
        {"label": "Exploratory", "desc": "Early-stage activity (1–4 commits)", "color": "#16A34A"},
    ]

    phases_html = []
    for i, phase in enumerate(phases[:3]):
        timeframe = phase.get("timeframe", f"Phase {i+1}")
        goals = phase.get("goals", [])
        key_repos = phase.get("key_repos", [])

        goals_li = "".join(f"<li>{_escape_html(g)}</li>" for g in goals)
        chips = ""
        if key_repos:
            chip_items = []
            for rname in key_repos:
                color = repo_colors.get(rname, "#888")
                chip_items.append(
                    f'<span class="phase-chip" style="border-left:3px solid {color};">{_escape_html(rname)}</span>'
                )
            chips = f'<div class="phase-chips">{"".join(chip_items)}</div>'

        meta = phase_meta[i] if i < len(phase_meta) else {"label": timeframe, "desc": "", "color": "#888"}
        phases_html.append(f'''
            <div class="phase">
                <div class="phase-dot"></div>
                {"<div class='you-are-here'><span>▼ Current Focus</span></div>" if i == 0 else ""}
                <div class="phase-card">
                    <div class="phase-timeframe">{_escape_html(timeframe)}</div>
                    <div class="phase-title">{_escape_html(meta["desc"])}</div>
                    <ul class="phase-goals">
                        {goals_li}
                    </ul>
                    {chips}
                </div>
            </div>
        ''')

    return f'''
    <div class="blueprint-container">
        {vision_html}
        <div class="timeline">
            {"".join(phases_html)}
        </div>
    </div>
    '''
