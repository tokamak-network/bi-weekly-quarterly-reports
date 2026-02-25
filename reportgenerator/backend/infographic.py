"""
Tokamak Network Ecosystem Infographic Generator.

Generates a self-contained HTML page with 2 tabbed views:
  A) Domain Landscape Map
  B) Blueprint (Activity + Synergy Analysis)
"""

import json
import os
import math
import base64
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tokamak-logos")
GITHUB_ORG_URL = "https://github.com/tokamak-network"

# ── Category definitions ──
# Max ~10 repos per category for visual balance.
CATEGORIES = {
    "Privacy & ZK": {"color": "#7C3AED", "bg": "#F5F3FF", "icon": "🔒"},
    "DeFi & Staking": {"color": "#2A72E5", "bg": "#EFF6FF", "icon": "💰"},
    "Core Infrastructure": {"color": "#475569", "bg": "#F8FAFC", "icon": "🏗️"},
    "Platform & Services": {"color": "#64748B", "bg": "#F1F5F9", "icon": "🖥️"},
    "Data & Analytics": {"color": "#0EA5E9", "bg": "#F0F9FF", "icon": "📊"},
    "AI & Machine Learning": {"color": "#EA580C", "bg": "#FFF7ED", "icon": "🧠"},
    "Automation & Tooling": {"color": "#D97706", "bg": "#FFFBEB", "icon": "⚙️"},
    "Gaming & Social": {"color": "#DC2626", "bg": "#FEF2F2", "icon": "🎮"},
    "Governance": {"color": "#0D9488", "bg": "#F0FDFA", "icon": "🏛️"},
    "Research & Education": {"color": "#CA8A04", "bg": "#FEFCE8", "icon": "📚"},
}

# Default classification — manually curated for known repos
DEFAULT_CLASSIFICATION = {
    "Privacy & ZK": [
        "Tokamak-zk-EVM", "Tokamak-zk-EVM-contracts", "private-app-channel-manager",
        "zk-dex-d1-private-voting", "dust-protocol", "zk-loot-box",
        "zk-mafia", "zk-dex", "zkdex-skills", "interactive-zkp-study",
    ],
    "DeFi & Staking": [
        "ton-staking-v2", "delegate-staking-mvp", "RAT-frontend",
        "staking-community-version", "Staking-v3-local-infra", "vton-airdrop-simulator",
        "TON-total-supply", "erc8004-test", "tokamak-landing-page",
    ],
    "Core Infrastructure": [
        "tokamak-thanos", "optimism", "DRB-node", "Commit-Reveal2",
        "Optimal-fraud-proof", "hybrid-dispute-emulator",
        "nexus-next-gen-smart-account-wallet-erc-4337",
    ],
    "Platform & Services": [
        "trh-platform-ui", "trh-sdk", "trh-backend", "trh-platform",
        "trh-platform-desktop", "tokamak-app-hub", "thanos-bridge",
        "nftgame-zk-dex",
    ],
    "Data & Analytics": [
        "tokamak-data-layer", "all-thing-eye", "bi-weekly-quarterly-reports",
        "Ooo-report-generator", "ECO-report-generator",
        "tokamak-thumbnail-generator",
    ],
    "AI & Machine Learning": [
        "SentinAI", "Tokamak-AI-Layer", "tokamak-ai-agent",
        "ai-kits", "ai-tokamak", "ai-playgrounds",
        "smart-contract-audit-tool",
    ],
    "Automation & Tooling": [
        "auto-research-press", "google-meet-analyze", "tokamak-architecht-bot",
        "crewcode", "ai-setup-guide", "agent-key-management",
        "24-7-playground", "eth-nanobot", "secure-vote",
    ],
    "Gaming & Social": [
        "tokamon", "syndi", "Zodiac",
    ],
    "Governance": [
        "tokamak-dao-v2", "tokamak-dao-agent", "dao-action-builder",
        "tokamak-agent-teams",
    ],
    "Research & Education": [
        "tokamak-learning", "tokamak-network-pilot", "tokamak-hr",
        "TokamakL2JS",
    ],
}

# Default descriptions for repos
DEFAULT_DESCRIPTIONS = {
    "Tokamak-zk-EVM": "Core ZK-EVM engine for private smart contract execution",
    "Tokamak-zk-EVM-contracts": "On-chain contracts for ZK-EVM verification",
    "private-app-channel-manager": "SDK for private application channels",
    "zk-dex-d1-private-voting": "ZK-based private on-chain voting & DEX",
    "dust-protocol": "Privacy-focused confidential token transfers",
    "zk-loot-box": "ZK-powered randomized loot box mechanics",
    "zk-mafia": "ZK proof-based social deduction game",
    "zk-dex": "Zero-knowledge decentralized exchange",
    "zkdex-skills": "Skill system for ZK DEX platform",
    "interactive-zkp-study": "Interactive zero-knowledge proof tutorials",
    "ton-staking-v2": "TON token staking platform v2",
    "delegate-staking-mvp": "Delegated staking minimum viable product",
    "RAT-frontend": "Staking reward verification interface",
    "staking-community-version": "Community staking dashboard",
    "Staking-v3-local-infra": "Local infrastructure for staking v3 testing",
    "vton-airdrop-simulator": "vTON airdrop simulation tool",
    "TON-total-supply": "TON token total supply tracker",
    "erc8004-test": "ERC-8004 standard testing implementation",
    "tokamak-landing-page": "Main Tokamak Network website",
    "tokamak-thanos": "Optimistic rollup implementation for Ethereum",
    "optimism": "Optimism rollup fork & customizations",
    "DRB-node": "Distributed Random Beacon node",
    "Commit-Reveal2": "Commit-reveal scheme implementation v2",
    "Optimal-fraud-proof": "Optimized fraud proof research",
    "hybrid-dispute-emulator": "Hybrid dispute resolution emulator",
    "nexus-next-gen-smart-account-wallet-erc-4337": "ERC-4337 smart account wallet",
    "trh-platform-ui": "Tokamak Rollup Hub dashboard UI",
    "trh-sdk": "SDK for deploying custom L2 rollups",
    "trh-backend": "Rollup Hub backend infrastructure",
    "trh-platform": "Rollup Hub platform core",
    "trh-platform-desktop": "Rollup Hub desktop application",
    "tokamak-app-hub": "Tokamak application hub portal",
    "thanos-bridge": "Thanos L2 bridge implementation",
    "nftgame-zk-dex": "NFT gaming with ZK DEX integration",
    "tokamak-data-layer": "Tokamak data layer infrastructure",
    "all-thing-eye": "Comprehensive monitoring & observation tool",
    "bi-weekly-quarterly-reports": "Automated bi-weekly & quarterly report generator",
    "Ooo-report-generator": "Out-of-office report generation tool",
    "ECO-report-generator": "Ecosystem report generator",
    "tokamak-thumbnail-generator": "Automated thumbnail generation tool",
    "SentinAI": "AI-powered smart contract security analysis",
    "Tokamak-AI-Layer": "AI integration layer for Tokamak ecosystem",
    "tokamak-ai-agent": "AI agent for Tokamak operations",
    "ai-kits": "AI development toolkit & utilities",
    "ai-tokamak": "AI applications for Tokamak network",
    "ai-playgrounds": "AI experimentation playground",
    "smart-contract-audit-tool": "Automated smart contract auditing tool",
    "auto-research-press": "Automated blockchain research publisher",
    "google-meet-analyze": "Google Meet transcript analysis tool",
    "tokamak-architecht-bot": "Architecture planning automation bot",
    "crewcode": "Collaborative coding automation framework",
    "ai-setup-guide": "AI environment setup guide & scripts",
    "agent-key-management": "Agent key & credential management",
    "24-7-playground": "Always-on development sandbox",
    "eth-nanobot": "Ethereum micro-transaction automation",
    "secure-vote": "Secure voting system implementation",
    "tokamon": "Tokamak-themed collectible game",
    "syndi": "Social syndication & engagement platform",
    "Zodiac": "Zodiac-themed game mechanics & contracts",
    "tokamak-dao-v2": "Decentralized governance platform v2",
    "tokamak-dao-agent": "AI-powered DAO governance agent",
    "dao-action-builder": "DAO proposal & action builder interface",
    "tokamak-agent-teams": "Multi-agent team coordination for DAO",
    "tokamak-learning": "Educational platform for Tokamak ecosystem",
    "tokamak-network-pilot": "Tokamak network pilot program resources",
    "tokamak-hr": "Human resources management system",
    "TokamakL2JS": "JavaScript library for Tokamak L2 interaction",
}


def _load_logo_base64():
    # type: () -> str
    path = os.path.join(LOGO_DIR, "5_symbol_clrd_cropped.png")
    if not os.path.exists(path):
        path = os.path.join(LOGO_DIR, "5_symbol_clrd_transparent.png")
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return "data:image/png;base64," + data


def classify_repos_from_csv(
    repo_commits,          # type: Dict[str, int]
    descriptions=None,     # type: Optional[Dict[str, str]]
    classification=None,   # type: Optional[Dict[str, List[str]]]
):
    # type: (...) -> Dict[str, List[Dict[str, Any]]]
    """Classify repos into categories. Returns {category: [{name, description, commits}]}."""

    desc = dict(DEFAULT_DESCRIPTIONS)
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
        elif any(k in name_lower for k in ("stak", "ton-", "swap", "defi", "bridge", "airdrop")):
            repo_to_cat[repo] = "DeFi & Staking"
        elif any(k in name_lower for k in ("thanos", "rollup", "node", "geth", "l1", "fraud", "dispute")):
            repo_to_cat[repo] = "Core Infrastructure"
        elif any(k in name_lower for k in ("trh", "platform", "hub", "desktop")):
            repo_to_cat[repo] = "Platform & Services"
        elif any(k in name_lower for k in ("data", "report", "analyt", "monitor", "explorer")):
            repo_to_cat[repo] = "Data & Analytics"
        elif any(k in name_lower for k in ("sentinai", "ai-layer", "ai-agent", "ml", "ai-kit")):
            repo_to_cat[repo] = "AI & Machine Learning"
        elif any(k in name_lower for k in ("auto", "bot", "agent", "script", "tool", "cli", "setup")):
            repo_to_cat[repo] = "Automation & Tooling"
        elif any(k in name_lower for k in ("game", "social", "nft", "market", "tokamon", "zodiac")):
            repo_to_cat[repo] = "Gaming & Social"
        elif any(k in name_lower for k in ("dao", "gov", "vote", "proposal")):
            repo_to_cat[repo] = "Governance"
        elif any(k in name_lower for k in ("research", "paper", "doc", "learn", "study", "whitepaper")):
            repo_to_cat[repo] = "Research & Education"
        else:
            repo_to_cat[repo] = "Platform & Services"

    # Build result — only include repos with actual commits (> 0)
    result = {cat: [] for cat in CATEGORIES}  # type: Dict[str, List[Dict[str, Any]]]
    seen = set()  # type: set
    for repo, commits in sorted(repo_commits.items(), key=lambda x: -x[1]):
        if commits <= 0:
            continue
        cat = repo_to_cat.get(repo, "Platform & Services")
        if cat not in CATEGORIES:
            cat = "Platform & Services"
        if repo in seen:
            continue
        seen.add(repo)
        result[cat].append({
            "name": repo,
            "description": desc.get(repo, _infer_description(repo)),
            "commits": commits,
        })

    return result


def _infer_description(repo_name):
    # type: (str) -> str
    name = repo_name.replace("-", " ").replace("_", " ")
    return name + " component"


def _activity_level(commits):
    # type: (int) -> Tuple[str, str]
    if commits >= 20:
        return "#22C55E", "high"
    elif commits >= 5:
        return "#EAB308", "medium"
    else:
        return "#9CA3AF", "low"


def _escape_html(s):
    # type: (str) -> str
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")


def generate_infographic_html(
    categorized_repos,  # type: Dict[str, List[Dict[str, Any]]]
    title="Tokamak Network Ecosystem",  # type: str
    date_range=None,    # type: Optional[Dict[str, str]]
    synergies=None,     # type: Optional[List[Dict[str, Any]]]
    blueprint=None,     # type: Optional[Dict[str, Any]]
    repo_contributors=None,  # type: Optional[Dict[str, List[str]]]
):
    # type: (...) -> str
    """Generate a self-contained HTML infographic page with 2 tabbed views."""

    logo_data = _load_logo_base64()

    total_repos = sum(len(repos) for repos in categorized_repos.values())
    total_commits = sum(r["commits"] for repos in categorized_repos.values() for r in repos)
    active_categories = sum(1 for repos in categorized_repos.values() if repos)

    date_label = ""
    if date_range:
        date_label = "{0} — {1}".format(date_range.get("start", ""), date_range.get("end", ""))

    # Build contributor map if not provided
    if repo_contributors is None:
        repo_contributors = {}

    # ── View A: Domain Landscape ──
    landscape_html = _build_landscape_html(categorized_repos, total_repos, total_commits, active_categories)

    # ── View B: Blueprint (Activity + Synergy) ──
    blueprint_html = _build_blueprint_html(categorized_repos, repo_contributors, synergies)

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
body{{
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    background:#f8f9fa;
    color:#1a1a1a;
    line-height:1.5;
    min-height:100vh;
}}

.header{{
    background:#fff;
    color:#1a1a1a;
    text-align:center;
    padding:24px 24px 16px;
    border-bottom:1px solid #e8e8e8;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}}
.header-logo{{height:120px;margin-bottom:4px;object-fit:contain;}}
.header h1{{font-size:28px;font-weight:700;letter-spacing:-0.5px;color:#1a1a1a;margin-bottom:4px;}}
.header .subtitle{{font-size:14px;color:#555;font-weight:400;}}
.header .date-label{{font-size:12px;color:#888;margin-top:6px;}}

.tab-bar{{
    display:flex;justify-content:center;gap:0;background:#fff;
    border-bottom:1px solid #e8e8e8;position:sticky;top:0;z-index:100;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);
}}
.tab-btn{{
    background:none;border:none;color:#888;font-size:15px;font-weight:500;
    padding:14px 28px;cursor:pointer;border-bottom:3px solid transparent;
    transition:all 0.2s;font-family:inherit;
}}
.tab-btn:hover{{color:#1a1a1a;background:rgba(42,114,229,0.04);}}
.tab-btn.active{{color:#2A72E5;font-weight:700;border-bottom-color:#2A72E5;}}

.tab-panel{{display:none;animation:fadeIn 0.3s ease;}}
.tab-panel.active{{display:block;}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(8px);}}to{{opacity:1;transform:translateY(0);}}}}

/* Stats */
.stats-bar{{display:flex;justify-content:center;gap:48px;padding:20px 24px;background:#fff;border-bottom:1px solid #e8e8e8;}}
.stat{{display:flex;flex-direction:column;align-items:center;}}
.stat-num{{font-size:26px;font-weight:700;color:#2A72E5;}}
.stat-label{{font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;margin-top:2px;}}

.legend,.activity-legend{{display:flex;justify-content:center;flex-wrap:wrap;gap:14px;padding:12px 24px;background:#fff;border-bottom:1px solid #f0f0f0;}}
.legend-item{{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#555;}}
.legend-dot{{width:9px;height:9px;border-radius:50%;display:inline-block;flex-shrink:0;}}
.legend-label{{font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;font-weight:600;}}

.landscape-grid{{
    max-width:1400px;margin:0 auto;padding:28px 24px;
    display:grid;grid-template-columns:repeat(2,1fr);gap:20px;
}}

.category-section{{
    background:#fff;border-radius:12px;overflow:hidden;
    border:1px solid #e8e8e8;box-shadow:0 1px 3px rgba(0,0,0,0.04);
    transition:border-color 0.2s;
}}
.category-section:hover{{border-color:#d0d0d0;}}
.category-header{{
    display:flex;align-items:center;gap:10px;padding:14px 16px;
    font-weight:600;font-size:14px;color:#1a1a1a;background:#fff;
    border-left:4px solid #888;
}}
.category-icon{{font-size:16px;}}
.category-title{{flex:1;}}
.category-count{{background:#f0f0f0;color:#555;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;}}
.category-repos{{padding:10px;display:flex;flex-direction:column;gap:6px;}}

.repo-card{{
    display:block;padding:12px 14px;border-radius:6px;background:#f8f9fa;
    text-decoration:none;color:inherit;transition:all 0.15s;cursor:pointer;border:1px solid transparent;
}}
.repo-card:hover{{background:#f0f0f0;border-color:#e8e8e8;transform:translateX(2px);}}
.repo-top{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;}}
.repo-name{{font-weight:600;font-size:12px;color:#1a1a1a;word-break:break-all;}}
.repo-lines-total{{font-weight:700;font-size:13px;color:#1a1a1a;white-space:nowrap;margin-left:8px;}}
.repo-desc{{font-size:11px;color:#666;margin-bottom:6px;line-height:1.3;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden;}}
.repo-bottom{{display:flex;justify-content:space-between;align-items:baseline;}}
.repo-contributors{{font-size:10px;color:#888;}}
.repo-lines-detail{{font-size:10px;white-space:nowrap;}}
.repo-lines-added{{color:#22c55e;font-weight:600;}}
.repo-lines-deleted{{color:#ef4444;font-weight:600;}}
.repo-card:hover .repo-desc{{-webkit-line-clamp:unset;overflow:visible;}}

/* Blueprint */
.blueprint-container{{max-width:1200px;margin:0 auto;padding:32px 24px;}}
.section-heading{{
    font-size:20px;font-weight:700;color:#1a1a1a;margin-bottom:4px;
    display:flex;align-items:center;gap:10px;
}}
.section-subtitle{{font-size:13px;color:#888;margin-bottom:20px;}}
.section-badge{{
    display:inline-block;font-size:10px;font-weight:700;text-transform:uppercase;
    letter-spacing:0.5px;padding:3px 10px;border-radius:4px;
}}
.badge-factual{{background:#EFF6FF;color:#2A72E5;}}
.badge-ai{{background:#FFF7ED;color:#EA580C;}}

.activity-domain-group{{margin-bottom:28px;}}
.activity-domain-title{{
    font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:12px;
    padding-bottom:6px;border-bottom:2px solid #e8e8e8;
    display:flex;align-items:center;gap:8px;
}}
.activity-domain-commits{{font-size:12px;font-weight:400;color:#888;}}

.activity-cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;}}
.activity-card{{
    background:#fff;border:1px solid #e8e8e8;border-radius:10px;padding:14px 16px;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);transition:border-color 0.2s;
}}
.activity-card:hover{{border-color:#d0d0d0;}}
.activity-card-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;}}
.activity-card-name{{font-weight:700;font-size:14px;color:#1a1a1a;}}
.activity-card-commits{{
    background:#EFF6FF;color:#2A72E5;padding:2px 10px;border-radius:8px;
    font-size:12px;font-weight:700;
}}
.activity-card-contributors{{font-size:12px;color:#555;margin-bottom:4px;}}
.activity-card-desc{{font-size:12px;color:#888;line-height:1.4;}}

.synergy-section{{margin-top:40px;padding-top:32px;border-top:2px solid #e8e8e8;}}
.synergy-cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px;margin-top:16px;}}
.synergy-card{{
    background:#fff;border:1px solid #e8e8e8;border-radius:10px;padding:18px 20px;
    box-shadow:0 1px 3px rgba(0,0,0,0.04);border-left:4px solid #EA580C;
}}
.synergy-card-title{{font-size:15px;font-weight:700;color:#1a1a1a;margin-bottom:8px;}}
.synergy-card-repos{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;}}
.synergy-repo-chip{{
    background:#f0f0f0;padding:3px 10px;border-radius:6px;font-size:11px;
    color:#555;font-weight:600;
}}
.synergy-repo-chip .commit-count{{color:#2A72E5;font-weight:700;margin-left:4px;}}
.synergy-card-reason{{font-size:13px;color:#555;line-height:1.5;}}
.synergy-card-label{{
    display:inline-block;font-size:10px;font-weight:700;color:#EA580C;
    background:#FFF7ED;padding:2px 8px;border-radius:4px;margin-bottom:8px;
}}
.synergy-card-basis{{font-size:11px;color:#888;margin-top:8px;font-style:italic;}}

.footer{{text-align:center;padding:24px;color:#888;font-size:11px;border-top:1px solid #e8e8e8;margin-top:32px;}}
.footer a{{color:#2A72E5;text-decoration:none;}}

@media print{{
    body{{background:white;}}
    .tab-bar{{position:static;}}
    .tab-panel{{display:block !important;page-break-before:always;}}
    .tab-panel:first-of-type{{page-break-before:auto;}}
}}
@media(max-width:768px){{
    .header h1{{font-size:22px;}}
    .header-logo{{height:200px;}}
    .stats-bar{{gap:20px;}}
    .stat-num{{font-size:20px;}}
    .landscape-grid{{grid-template-columns:1fr;padding:16px;}}
    .activity-cards{{grid-template-columns:1fr;}}
    .synergy-cards{{grid-template-columns:1fr;}}
    .tab-btn{{padding:10px 16px;font-size:13px;}}
}}
</style>
</head>
<body>

<div class="header">
    {logo_img}
    <h1>{title}</h1>
    <div class="subtitle">Interactive Ecosystem Infographic</div>
    {date_html}
</div>

<div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('landscape',this)">🗺️ Landscape</button>
    <button class="tab-btn" onclick="switchTab('blueprint',this)">📍 Blueprint</button>
</div>

<div id="panel-landscape" class="tab-panel active">
{landscape_html}
</div>

<div id="panel-blueprint" class="tab-panel">
{blueprint_html}
</div>

<div class="footer">
    <p>Generated by <a href="{github_url}">Tokamak Network</a> Report Generator</p>
    <p style="margin-top:4px;">Click any repository card to view on GitHub</p>
</div>

<script>
function switchTab(id, btn) {{
    document.querySelectorAll('.tab-panel').forEach(function(p){{ p.classList.remove('active'); }});
    document.querySelectorAll('.tab-btn').forEach(function(b){{ b.classList.remove('active'); }});
    document.getElementById('panel-' + id).classList.add('active');
    btn.classList.add('active');
}}
</script>

</body>
</html>'''.format(
        title=_escape_html(title),
        logo_img=("<img src='" + logo_data + "' alt='Tokamak Network' class='header-logo'>" if logo_data else ""),
        date_html=("<div class='date-label'>" + _escape_html(date_label) + "</div>" if date_label else ""),
        landscape_html=landscape_html,
        blueprint_html=blueprint_html,
        github_url=GITHUB_ORG_URL,
    )

    return html


def _build_landscape_html(categorized_repos, total_repos, total_commits, active_categories):
    # type: (Dict[str, List[Dict[str, Any]]], int, int, int) -> str

    stats_html = '''
    <div class="stats-bar">
        <div class="stat"><span class="stat-num">{changes}</span><span class="stat-label">Code Changes</span></div>
        <div class="stat"><span class="stat-num">{repos}</span><span class="stat-label">Active Projects</span></div>
        <div class="stat"><span class="stat-num">{cats}</span><span class="stat-label">Categories</span></div>
    </div>
    '''.format(repos=total_repos, changes="{:,}".format(total_commits), cats=active_categories)

    legend_items = []
    for cat_name, cat_info in CATEGORIES.items():
        if categorized_repos.get(cat_name):
            legend_items.append(
                '<span class="legend-item"><span class="legend-dot" style="background:{color};"></span>{name}</span>'.format(
                    color=cat_info["color"], name=cat_name
                )
            )
    legend_html = '<div class="legend">{items}</div>'.format(items="".join(legend_items))

    activity_legend = '''
    <div class="activity-legend">
        <span class="legend-label">Activity:</span>
        <span class="legend-item"><span class="legend-dot" style="background:#22C55E;"></span>High (20+)</span>
        <span class="legend-item"><span class="legend-dot" style="background:#EAB308;"></span>Medium (5-19)</span>
        <span class="legend-item"><span class="legend-dot" style="background:#9CA3AF;"></span>Low (&lt;5)</span>
    </div>
    '''

    categories_html = []
    # Sort categories by total code changes descending
    sorted_cats = []
    for cat_name, cat_info in CATEGORIES.items():
        repos = categorized_repos.get(cat_name, [])
        if not repos:
            continue
        cat_total = sum(r.get("lines_changed", 0) for r in repos)
        sorted_cats.append((cat_name, cat_info, repos, cat_total))
    sorted_cats.sort(key=lambda x: -x[3])

    for cat_name, cat_info, repos, _cat_total in sorted_cats:
        # Sort repos within category by code changes descending
        repos = sorted(repos, key=lambda r: -(r.get("lines_changed", 0)))

        repo_cards = []
        for repo in repos:
            lines_changed = repo.get("lines_changed", 0)
            lines_added = repo.get("lines_added", 0)
            lines_deleted = repo.get("lines_deleted", 0)
            repo_cards.append('''
                <a href="{url}/{name}" target="_blank" rel="noopener"
                   class="repo-card" style="border-left:3px solid {cat_color};">
                    <div class="repo-top">
                        <span class="repo-name">{name_esc}</span>
                        <span class="repo-lines-total" style="font-size:16px;font-weight:800;color:{cat_color};text-align:right;"><span style="display:block;font-size:9px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Code Changes</span>{lines_total}</span>
                    </div>
                    <div class="repo-desc">{desc}</div>
                    <div class="repo-bottom">
                        <span class="repo-lines-detail" style="font-size:11px;font-weight:600;"><span class="repo-lines-added">+{added}</span> / <span class="repo-lines-deleted">-{deleted}</span></span>
                    </div>
                </a>
            '''.format(
                url=GITHUB_ORG_URL,
                name=repo["name"],
                cat_color=cat_info["color"],
                name_esc=_escape_html(repo["name"]),
                desc=_escape_html(repo.get("description", "")),
                lines_total="{:,}".format(lines_changed),
                added="{:,}".format(lines_added),
                deleted="{:,}".format(lines_deleted),
            ))

        repo_count = len(repos)
        cat_lines = sum(r.get("lines_changed", 0) for r in repos)
        cat_lines_str = "{:,}".format(cat_lines) if cat_lines > 0 else "0"
        categories_html.append('''
            <div class="category-section" data-category="{cat_name}">
                <div class="category-header" style="border-left-color:{color};">
                    <span class="category-icon">{icon}</span>
                    <span class="category-title">{cat_name}</span>
                    <span class="category-count">{count} projects · {lines} code changes</span>
                </div>
                <div class="category-repos">
                    {cards}
                </div>
            </div>
        '''.format(
            cat_name=cat_name,
            color=cat_info["color"],
            icon=cat_info["icon"],
            count=repo_count,
            lines=cat_lines_str,
            cards="".join(repo_cards),
        ))

    return '''
    {stats}
    {legend}
    {activity_legend}
    <div class="landscape-grid">
        {categories}
    </div>
    '''.format(stats=stats_html, legend=legend_html, activity_legend=activity_legend, categories="".join(categories_html))


def _build_blueprint_html(categorized_repos, repo_contributors, synergies_data):
    # type: (Dict[str, List[Dict[str, Any]]], Dict[str, List[str]], Optional[List[Dict[str, Any]]]) -> str
    """Build Blueprint section with Category Focus & Potential Synergies."""

    total_repos = sum(len(repos) for repos in categorized_repos.values())
    total_commits = sum(r["commits"] for repos in categorized_repos.values() for r in repos)

    # Build category focus cards
    focus_cards = _build_category_focus_cards(categorized_repos)

    return '''
    <div class="blueprint-container">
        <div class="section-heading">
            📊 Category Focus &amp; Potential Synergies
            <span class="section-badge badge-factual">Heuristic Analysis</span>
        </div>
        <div class="section-subtitle">{total_repos} active projects · {total_changes} code changes — Current focus and cross-category synergy opportunities</div>
        <div style="margin-top:20px;">
            {focus_cards}
        </div>
    </div>
    '''.format(
        total_repos=total_repos,
        total_changes="{:,}".format(total_commits),
        focus_cards=focus_cards,
    )


# Synergy pair descriptions for heuristic generation
SYNERGY_PAIR_DESCRIPTIONS = {
    ("Privacy & ZK", "DeFi & Staking"): "ZK proof technology combined with staking protocols could enable privacy-preserving staking services where users earn rewards without exposing their positions.",
    ("Privacy & ZK", "Core Infrastructure"): "Integrating ZK proofs into the rollup infrastructure could provide private transaction processing at the L2 level, improving both privacy and scalability.",
    ("Privacy & ZK", "Governance"): "ZK-based governance would allow token holders to vote on proposals without revealing their voting power or identity, strengthening democratic participation.",
    ("Privacy & ZK", "Gaming & Social"): "ZK proofs can enable verifiably fair game mechanics and private social interactions, creating trustless gaming experiences.",
    ("DeFi & Staking", "Core Infrastructure"): "Tighter integration between staking contracts and rollup infrastructure could reduce gas costs for staking operations and enable cross-L2 staking.",
    ("DeFi & Staking", "Governance"): "Combining staking with governance enables stake-weighted voting and delegation mechanisms, aligning economic incentives with protocol decision-making.",
    ("DeFi & Staking", "Platform & Services"): "Embedding staking functionality into the Rollup Hub platform would let L2 operators offer native staking to their users out of the box.",
    ("Core Infrastructure", "Platform & Services"): "Deeper integration between Thanos rollup stack and the Rollup Hub platform could streamline L2 deployment pipelines and operational tooling.",
    ("Core Infrastructure", "AI & Machine Learning"): "AI-driven monitoring and anomaly detection for rollup nodes could improve infrastructure reliability and automate incident response.",
    ("AI & Machine Learning", "Data & Analytics"): "Combining AI capabilities with analytics infrastructure could enable predictive insights on ecosystem health and development velocity.",
    ("AI & Machine Learning", "Automation & Tooling"): "AI-powered automation tools could assist with code review, smart contract auditing, and developer onboarding workflows.",
    ("Data & Analytics", "Governance"): "Data-driven governance dashboards could surface key metrics to inform proposal discussions and track the impact of governance decisions.",
    ("Platform & Services", "Automation & Tooling"): "Automating platform deployment and monitoring workflows would reduce operational overhead for Rollup Hub users.",
    ("Gaming & Social", "DeFi & Staking"): "Gaming platforms with integrated token staking could create play-to-earn mechanics backed by real DeFi yield.",
    ("Research & Education", "Privacy & ZK"): "Educational content on ZK proofs and interactive tutorials could accelerate developer onboarding into the privacy stack.",
}


def _build_category_focus_cards(categorized_repos):
    # type: (Dict[str, List[Dict[str, Any]]]) -> str
    """Build category focus + synergy cards for active categories."""

    active_cats = []  # type: List[tuple]
    for cat_name, cat_info in CATEGORIES.items():
        repos = categorized_repos.get(cat_name, [])
        if not repos:
            continue
        cat_lines = sum(r.get("lines_changed", 0) for r in repos)
        active_cats.append((cat_name, cat_info, repos, cat_lines))

    active_cats.sort(key=lambda x: -x[3])
    active_cat_names = [c[0] for c in active_cats]

    cards_html = []
    for cat_name, cat_info, repos, cat_commits in active_cats:
        # Current Focus: auto-generate from data
        repo_count = len(repos)
        top_repos = sorted(repos, key=lambda r: -r.get("lines_changed", 0))[:3]
        top_repo_strs = []
        for r in top_repos:
            r_lines = r.get("lines_changed", 0)
            top_repo_strs.append("{name} ({lines} code changes)".format(
                name=r["name"], lines="{:,}".format(r_lines)
            ))
        top_list = ", ".join(top_repo_strs)
        cat_lines = sum(r.get("lines_changed", 0) for r in repos)

        if repo_count == 1:
            focus_text = "{cat} has 1 active project: {top}. Development is focused and concentrated.".format(
                cat=cat_name, top=top_list
            )
        else:
            focus_text = "{cat} has {count} active projects with {lines} code changes. Key activity includes {top}.".format(
                cat=cat_name, count=repo_count, lines="{:,}".format(cat_lines), top=top_list
            )

        # Potential Synergies: find matching pairs
        synergy_texts = []
        for other_cat in active_cat_names:
            if other_cat == cat_name:
                continue
            pair = tuple(sorted([cat_name, other_cat]))
            desc = SYNERGY_PAIR_DESCRIPTIONS.get(pair)
            if desc:
                synergy_texts.append(desc)
            if len(synergy_texts) >= 2:
                break

        synergy_html = ""
        if synergy_texts:
            synergy_items = "".join(
                '<li style="margin-bottom:6px;">{text}</li>'.format(text=_escape_html(t))
                for t in synergy_texts
            )
            synergy_html = '''
                <div style="margin-top:12px;">
                    <div style="font-size:0.8rem;font-weight:600;color:#EA580C;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">Potential Synergies</div>
                    <ul style="padding-left:18px;font-size:12px;color:#555;line-height:1.5;">{items}</ul>
                </div>
            '''.format(items=synergy_items)

        # Repo chips
        repo_chips = "".join(
            '<span class="synergy-repo-chip">{name}<span class="commit-count">({lines} code lines)</span></span>'.format(
                name=_escape_html(r["name"]), lines="{:,}".format(r.get("lines_changed", 0))
            )
            for r in top_repos
        )

        cards_html.append('''
            <div style="background:#fff;border:1px solid #e8e8e8;border-radius:10px;padding:20px 24px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,0.04);border-left:4px solid {color};">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                    <span style="font-size:18px;">{icon}</span>
                    <span style="font-size:16px;font-weight:700;color:#1a1a1a;">{cat_name}</span>
                    <span style="background:#f0f0f0;color:#555;padding:2px 10px;border-radius:10px;font-size:11px;font-weight:700;margin-left:auto;">{count} projects · {lines} code changes</span>
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;">{chips}</div>
                <div style="margin-bottom:8px;">
                    <div style="font-size:0.8rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Current Focus</div>
                    <div style="font-size:13px;color:#444;line-height:1.5;">{focus}</div>
                </div>
                {synergy}
            </div>
        '''.format(
            color=cat_info["color"],
            icon=cat_info["icon"],
            cat_name=_escape_html(cat_name),
            count=repo_count,
            lines="{:,}".format(sum(r.get("lines_changed", 0) for r in repos)),
            chips=repo_chips,
            focus=_escape_html(focus_text),
            synergy=synergy_html,
        ))

    return "".join(cards_html)


def _generate_heuristic_synergies(categorized_repos, repo_contributors):
    # type: (Dict[str, List[Dict[str, Any]]], Dict[str, List[str]]) -> List[Dict[str, Any]]
    """Legacy heuristic synergy generator. Kept for standalone infographic compatibility."""
    return []
