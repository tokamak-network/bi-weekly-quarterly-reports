"""
Tokamak Network Ecosystem Infographic Generator.

Generates a self-contained HTML page with an interactive ecosystem map
showing repositories organized by domain/category.
"""

import json
import os
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


def _load_logo_base64() -> str:
    path = os.path.join(LOGO_DIR, "4_transparent.png")
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
    repo_to_cat: Dict[str, str] = {}
    for cat, repos in cat_map.items():
        for r in repos:
            if r not in repo_to_cat:  # first category wins
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

    # Build result
    result: Dict[str, List[Dict[str, Any]]] = {cat: [] for cat in CATEGORIES}
    seen = set()
    for repo, commits in sorted(repo_commits.items(), key=lambda x: -x[1]):
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

    # Also add repos from default classification that aren't in CSV
    for cat, repos in cat_map.items():
        if cat not in CATEGORIES:
            continue
        for repo in repos:
            if repo not in seen:
                seen.add(repo)
                result[cat].append({
                    "name": repo,
                    "description": desc.get(repo, _infer_description(repo)),
                    "commits": 0,
                })

    return result


def _infer_description(repo_name: str) -> str:
    """Infer a description from repo name."""
    name = repo_name.replace("-", " ").replace("_", " ")
    return f"{name} component"


def _activity_level(commits: int) -> Tuple[str, str]:
    """Return (color, label) for activity level."""
    if commits >= 20:
        return "#22C55E", "high"
    elif commits >= 5:
        return "#EAB308", "medium"
    else:
        return "#9CA3AF", "low"


def generate_infographic_html(
    categorized_repos: Dict[str, List[Dict[str, Any]]],
    title: str = "Tokamak Network Ecosystem",
    date_range: Optional[Dict[str, str]] = None,
) -> str:
    """Generate a self-contained HTML infographic page."""
    
    logo_data = _load_logo_base64()
    
    # Count totals
    total_repos = sum(len(repos) for repos in categorized_repos.values())
    total_commits = sum(r["commits"] for repos in categorized_repos.values() for r in repos)
    active_categories = sum(1 for repos in categorized_repos.values() if repos)
    
    date_label = ""
    if date_range:
        date_label = f'{date_range.get("start", "")} — {date_range.get("end", "")}'

    # Build category cards HTML
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
                   class="repo-card" style="border-left: 3px solid {cat_info["color"]};"
                   title="{repo["description"]}&#10;&#10;{commit_text}">
                    <div class="repo-header">
                        <span class="activity-dot" style="background:{act_color};" title="{act_label} activity"></span>
                        <span class="repo-name">{repo["name"]}</span>
                    </div>
                    <div class="repo-desc">{repo["description"]}</div>
                </a>
            ''')
        
        repo_count = len(repos)
        categories_html.append(f'''
            <div class="category-section" data-category="{cat_name}">
                <div class="category-header" style="background:{cat_info["color"]};">
                    <span class="category-icon">{cat_info["icon"]}</span>
                    <span class="category-title">{cat_name}</span>
                    <span class="category-count">{repo_count}</span>
                </div>
                <div class="category-repos">
                    {"".join(repo_cards)}
                </div>
            </div>
        ''')

    categories_joined = "\n".join(categories_html)
    
    # Stats bar
    stats_html = f'''
        <div class="stats-bar">
            <div class="stat"><span class="stat-num">{total_repos}</span><span class="stat-label">Repositories</span></div>
            <div class="stat"><span class="stat-num">{total_commits:,}</span><span class="stat-label">Commits</span></div>
            <div class="stat"><span class="stat-num">{active_categories}</span><span class="stat-label">Categories</span></div>
        </div>
    '''

    # Legend
    legend_items = []
    for cat_name, cat_info in CATEGORIES.items():
        if categorized_repos.get(cat_name):
            legend_items.append(
                f'<span class="legend-item"><span class="legend-dot" style="background:{cat_info["color"]};"></span>{cat_name}</span>'
            )
    legend_html = f'<div class="legend">{"".join(legend_items)}</div>'

    # Activity legend
    activity_legend = '''
        <div class="activity-legend">
            <span class="legend-label">Activity:</span>
            <span class="legend-item"><span class="legend-dot" style="background:#22C55E;"></span>High (20+)</span>
            <span class="legend-item"><span class="legend-dot" style="background:#EAB308;"></span>Medium (5-19)</span>
            <span class="legend-item"><span class="legend-dot" style="background:#9CA3AF;"></span>Low (&lt;5)</span>
        </div>
    '''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
body{{
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    background:#F8FAFC;
    color:#1E293B;
    line-height:1.5;
    min-height:100vh;
}}

/* Header */
.header{{
    background:linear-gradient(135deg,#1E293B 0%,#0F172A 100%);
    color:white;
    text-align:center;
    padding:48px 24px 40px;
    position:relative;
    overflow:hidden;
}}
.header::before{{
    content:'';
    position:absolute;
    top:0;left:0;right:0;bottom:0;
    background:radial-gradient(ellipse at 50% 0%,rgba(42,114,229,0.15) 0%,transparent 70%);
    pointer-events:none;
}}
.header-logo{{
    height:80px;
    margin-bottom:16px;
    filter:drop-shadow(0 2px 8px rgba(0,0,0,0.3));
}}
.header h1{{
    font-size:32px;
    font-weight:700;
    letter-spacing:-0.5px;
    margin-bottom:8px;
}}
.header .subtitle{{
    font-size:15px;
    color:#94A3B8;
    font-weight:400;
}}
.header .date-label{{
    font-size:13px;
    color:#64748B;
    margin-top:8px;
}}

/* Stats */
.stats-bar{{
    display:flex;
    justify-content:center;
    gap:48px;
    padding:24px;
    background:white;
    border-bottom:1px solid #E2E8F0;
}}
.stat{{display:flex;flex-direction:column;align-items:center;}}
.stat-num{{font-size:28px;font-weight:700;color:#2A72E5;}}
.stat-label{{font-size:12px;color:#64748B;text-transform:uppercase;letter-spacing:0.5px;margin-top:2px;}}

/* Legend */
.legend,.activity-legend{{
    display:flex;
    justify-content:center;
    flex-wrap:wrap;
    gap:16px;
    padding:16px 24px;
    background:white;
    border-bottom:1px solid #E2E8F0;
}}
.legend-item{{
    display:inline-flex;
    align-items:center;
    gap:6px;
    font-size:13px;
    color:#475569;
}}
.legend-dot{{
    width:10px;height:10px;border-radius:50%;
    display:inline-block;flex-shrink:0;
}}
.legend-label{{
    font-size:12px;color:#94A3B8;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;
}}

/* Main grid */
.main{{
    max-width:1400px;
    margin:0 auto;
    padding:32px 24px;
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(340px,1fr));
    gap:24px;
}}

/* Category sections */
.category-section{{
    background:white;
    border-radius:12px;
    overflow:hidden;
    box-shadow:0 1px 3px rgba(0,0,0,0.08),0 1px 2px rgba(0,0,0,0.06);
    transition:box-shadow 0.2s;
}}
.category-section:hover{{
    box-shadow:0 4px 12px rgba(0,0,0,0.1),0 2px 4px rgba(0,0,0,0.06);
}}
.category-header{{
    display:flex;
    align-items:center;
    gap:10px;
    padding:14px 18px;
    color:white;
    font-weight:600;
    font-size:15px;
}}
.category-icon{{font-size:18px;}}
.category-title{{flex:1;}}
.category-count{{
    background:rgba(255,255,255,0.2);
    padding:2px 10px;
    border-radius:12px;
    font-size:12px;
    font-weight:700;
}}
.category-repos{{
    padding:12px;
    display:flex;
    flex-direction:column;
    gap:8px;
}}

/* Repo cards */
.repo-card{{
    display:block;
    padding:10px 12px;
    border-radius:8px;
    background:#F8FAFC;
    text-decoration:none;
    color:inherit;
    transition:all 0.15s;
    cursor:pointer;
}}
.repo-card:hover{{
    background:#EFF6FF;
    transform:translateX(2px);
}}
.repo-header{{
    display:flex;
    align-items:center;
    gap:8px;
    margin-bottom:4px;
}}
.activity-dot{{
    width:8px;height:8px;border-radius:50%;
    flex-shrink:0;
}}
.repo-name{{
    font-weight:600;
    font-size:13px;
    color:#1E293B;
    word-break:break-all;
}}
.repo-desc{{
    font-size:12px;
    color:#64748B;
    line-height:1.4;
    display:-webkit-box;
    -webkit-line-clamp:2;
    -webkit-box-orient:vertical;
    overflow:hidden;
}}
.repo-card:hover .repo-desc{{
    -webkit-line-clamp:unset;
    overflow:visible;
}}

/* Footer */
.footer{{
    text-align:center;
    padding:32px 24px;
    color:#94A3B8;
    font-size:12px;
    border-top:1px solid #E2E8F0;
    background:white;
    margin-top:32px;
}}
.footer a{{color:#2A72E5;text-decoration:none;}}

/* SVG overlay for synergy lines */
.synergy-svg{{
    position:fixed;
    top:0;left:0;
    width:100%;height:100%;
    pointer-events:none;
    z-index:0;
    display:none; /* hidden by default, enable via JS toggle */
}}

/* Print */
@media print{{
    body{{background:white;}}
    .header{{padding:24px;}}
    .main{{padding:16px;gap:16px;}}
    .category-section{{break-inside:avoid;box-shadow:0 0 0 1px #E2E8F0;}}
    .repo-card:hover{{transform:none;}}
}}

/* Responsive */
@media(max-width:768px){{
    .header h1{{font-size:24px;}}
    .stats-bar{{gap:24px;}}
    .stat-num{{font-size:22px;}}
    .main{{grid-template-columns:1fr;padding:16px;}}
}}
</style>
</head>
<body>

<div class="header">
    {"<img src='" + logo_data + "' alt='Tokamak Network' class='header-logo'>" if logo_data else ""}
    <h1>{title}</h1>
    <div class="subtitle">Repository Ecosystem Map — Organized by Domain</div>
    {"<div class='date-label'>" + date_label + "</div>" if date_label else ""}
</div>

{stats_html}
{legend_html}
{activity_legend}

<div class="main">
{categories_joined}
</div>

<div class="footer">
    <p>Generated by <a href="{GITHUB_ORG_URL}">Tokamak Network</a> Report Generator</p>
    <p style="margin-top:4px;">Click any repository card to view on GitHub</p>
</div>

<script>
// Hover tooltip enhancement
document.querySelectorAll('.repo-card').forEach(card => {{
    card.addEventListener('mouseenter', function() {{
        this.style.zIndex = '10';
    }});
    card.addEventListener('mouseleave', function() {{
        this.style.zIndex = '';
    }});
}});
</script>

</body>
</html>'''
    
    return html
