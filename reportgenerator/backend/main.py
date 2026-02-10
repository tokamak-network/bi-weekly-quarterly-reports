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
from typing import Optional

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

app = FastAPI(title="Biweekly Report Generator API")

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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


def get_project_for_repo(repo_name: str) -> Optional[str]:
    for project, repos in PROJECT_REPOS.items():
        if repo_name in repos:
            return project
    return None


def parse_csv_content(content: str) -> dict:
    """Parse CSV content and return GitHub activities grouped by project."""
    project_data = defaultdict(lambda: {"commits": [], "prs": [], "repos": set()})

    reader = csv.DictReader(io.StringIO(content))
    for row in reader:
        if row.get('source') != 'github':
            continue

        repo = row.get('repository', '').strip('"')
        if not repo:
            continue

        project = get_project_for_repo(repo)
        if not project:
            continue

        entry_type = row.get('type', '')
        message = row.get('message', '').strip('"')
        title = row.get('title', '').strip('"')
        sha = row.get('sha', '').strip('"')
        pr_number = row.get('pr_number', '').strip('"')
        timestamp = row.get('timestamp', '')
        additions = row.get('additions', '0') or '0'
        deletions = row.get('deletions', '0') or '0'
        state = row.get('state', '').strip('"')

        project_data[project]["repos"].add(repo)

        if entry_type == 'commit' and message:
            if message.lower().startswith('merge '):
                continue
            project_data[project]["commits"].append({
                "repo": repo,
                "message": message.split('\n')[0][:200],
                "sha": sha[:8] if sha else "",
                "timestamp": timestamp,
                "additions": int(additions),
                "deletions": int(deletions),
            })
        elif entry_type == 'pull_request' and title:
            project_data[project]["prs"].append({
                "repo": repo,
                "title": title,
                "pr_number": pr_number,
                "state": state,
                "timestamp": timestamp,
            })

    # Convert sets to lists for JSON serialization
    result = {}
    for project, data in project_data.items():
        result[project] = {
            "commits": data["commits"],
            "prs": data["prs"],
            "repos": list(data["repos"]),
        }

    return result


def prepare_summary(project: str, data: dict) -> dict:
    """Prepare summary for a project."""
    commits = data['commits']
    prs = data['prs']
    repos = data['repos']

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


def generate_with_ai_technical(project: str, summary: dict, info: dict) -> str:
    """Generate technical section using Claude API."""
    client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

    commit_list = "\n".join([
        f"- [{c['repo']}] {c['message']} (sha: {c['sha']})"
        for c in summary['top_commits'][:20]
    ])

    pr_list = "\n".join([
        f"- [{p['repo']}] PR#{p['pr_number']}: {p['title']}"
        for p in summary['merged_pr_list'][:10]
    ])

    prompt = f"""You are writing a biweekly development report for Tokamak Network's {info['title']} team.

Project Context: {info['context']}
Total commits: {summary['total_commits']}
Merged PRs: {summary['merged_prs']}

Top commits:
{commit_list}

Merged PRs:
{pr_list}

Generate 8-10 bullet points summarizing key development activities. Follow these rules:
1. Each bullet should start with a past-tense verb (Implemented, Fixed, Added, Refactored)
2. Include technical details
3. Add GitHub links: ([PR#XX](https://github.com/tokamak-network/REPO/pull/NUMBER)) or ([Commit](https://github.com/tokamak-network/REPO/commit/SHA))

Output only the bullet points."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4.5",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        bullets = response.content[0].text.strip()
        return f"#### {info['number']}. {info['title']} ([Overview]({info['overview_url']})).\n\n{bullets}\n"
    except Exception as e:
        return generate_basic_technical(project, summary, info)


def generate_with_ai_public(project: str, summary: dict, info: dict) -> str:
    """Generate public section using Claude API."""
    client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

    commit_list = "\n".join([
        f"- [{c['repo']}] {c['message']}"
        for c in summary['top_commits'][:20]
    ])

    prompt = f"""Write a biweekly report for Tokamak Network targeting INVESTORS, PARTNERS, and COMMUNITY.

Project: {info['title']}
Context: {info['context']}
Business Focus: {info['business_focus']}
Total improvements: {summary['total_commits']}

Recent commits (for context only):
{commit_list}

Generate 5-7 bullet points for NON-TECHNICAL audience:
1. NO technical jargon (no "commit", "PR", "API", "SDK", "contract")
2. Focus on VALUE and user benefits
3. Use business language: "improved", "enhanced", "launched"
4. NO GitHub links
5. Start with action verbs: "Enhanced", "Launched", "Improved"

Output only the bullet points."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4.5",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        bullets = response.content[0].text.strip()
        return f"#### {info['number']}. {info['title']}\n\n{bullets}\n"
    except Exception as e:
        return generate_basic_public(project, summary, info)


def generate_basic_technical(project: str, summary: dict, info: dict) -> str:
    """Generate basic technical section without AI."""
    bullets = []
    for commit in summary['top_commits'][:10]:
        msg = commit['message']
        msg = re.sub(r'^(feat|fix|refactor|test|docs|chore)(\([^)]+\))?:\s*', '', msg, flags=re.IGNORECASE)
        if msg:
            link = f"https://github.com/tokamak-network/{commit['repo']}/commit/{commit['sha']}"
            bullets.append(f"* {msg[0].upper()}{msg[1:]} ([Commit]({link})).")

    return f"#### {info['number']}. {info['title']} ([Overview]({info['overview_url']})).\n\n" + "\n".join(bullets) + "\n"


def generate_basic_public(project: str, summary: dict, info: dict) -> str:
    """Generate basic public section without AI."""
    bullets = [
        f"* Made significant progress with {summary['total_commits']} improvements.",
        f"* Enhanced system reliability across {len(summary['repos'])} components.",
        "* Continued work toward upcoming milestones.",
    ]
    return f"#### {info['number']}. {info['title']}\n\n" + "\n".join(bullets) + "\n"


def generate_highlight_with_ai(summaries: dict, report_type: str, total_commits: int, total_prs: int, total_repos: int) -> str:
    """Generate engaging highlight using AI for public reports."""
    if not HAS_ANTHROPIC or not os.environ.get('ANTHROPIC_API_KEY'):
        return generate_basic_highlight(total_commits, total_prs, total_repos, report_type)

    try:
        client = anthropic.Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

        # Gather key achievements from each project
        achievements = []
        for project, summary in summaries.items():
            top_msgs = [c['message'][:100] for c in summary['top_commits'][:5]]
            achievements.append(f"{project}: {', '.join(top_msgs)}")

        if report_type == "public":
            prompt = f"""You are writing an executive highlight for Tokamak Network's biweekly report.
Target audience: INVESTORS, PARTNERS, and COMMUNITY members who may not read the full report.

This period's activity:
- Total improvements: {total_commits}
- Major features completed: {total_prs}
- Active project areas: {total_repos}

Key work areas (for context, do NOT use technical terms):
{chr(10).join(achievements)}

Write a compelling 3-4 sentence highlight that:
1. HOOKS the reader immediately - make them want to read more
2. Emphasizes STRATEGIC VALUE and BUSINESS IMPACT
3. Mentions specific achievements in accessible language (e.g., "privacy technology", "staking infrastructure", "deployment platform")
4. Creates EXCITEMENT about Tokamak Network's progress
5. Sounds confident and forward-looking

DO NOT:
- Use numbers like "314 commits" or "6 PRs" as the main message
- Use technical jargon (no "commits", "PRs", "repositories", "contracts", "nodes")
- Be generic or boring

Examples of GOOD hooks:
- "Tokamak Network is redefining blockchain privacy..."
- "This period marked a pivotal step toward..."
- "Major breakthroughs in privacy technology..."

Write ONLY the highlight paragraph, no labels or headers."""

        else:  # technical
            prompt = f"""You are writing a technical highlight for Tokamak Network's biweekly development report.
Target audience: DEVELOPERS, TECHNICAL PARTNERS, and ENGINEERING teams.

This period's metrics:
- Total commits: {total_commits}
- Merged PRs: {total_prs}
- Active repositories: {total_repos}

Key development areas:
{chr(10).join(achievements)}

Write a concise 3-4 sentence technical highlight that:
1. Summarizes the most SIGNIFICANT technical achievements
2. Mentions specific systems/components improved (e.g., "zk-SNARK circuits", "staking contracts", "DRB nodes")
3. Highlights architectural improvements or major refactors
4. Notes any critical bug fixes or security enhancements
5. Sounds professional and technically precise

Include relevant metrics (commits, PRs) but focus on WHAT was achieved, not just numbers.

Examples:
- "This period focused on strengthening the ZK proof system with optimized Groth16 verification..."
- "Major infrastructure improvements landed across the staking and rollup deployment stack..."

Write ONLY the highlight paragraph, no labels or headers."""

        response = client.messages.create(
            model="claude-sonnet-4.5",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()

    except Exception as e:
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


@app.post("/api/generate")
async def generate_report(
    file: UploadFile = File(...),
    report_type: str = Form("technical"),
    use_ai: bool = Form(True)
):
    """Generate report from uploaded CSV file."""
    try:
        content = await file.read()
        content_str = content.decode('utf-8')

        project_data = parse_csv_content(content_str)

        if not project_data:
            raise HTTPException(status_code=400, detail="No valid GitHub data found in CSV")

        # Prepare summaries
        summaries = {}
        for project in ["Ooo", "Eco", "TRH"]:
            if project in project_data:
                summaries[project] = prepare_summary(project, project_data[project])

        # Calculate totals
        total_commits = sum(s['total_commits'] for s in summaries.values())
        total_prs = sum(s['merged_prs'] for s in summaries.values())
        total_repos = sum(len(s['repos']) for s in summaries.values())

        # Generate sections
        sections = []
        section_info = SECTION_INFO_TECHNICAL if report_type == "technical" else SECTION_INFO_PUBLIC

        for project in ["Ooo", "Eco", "TRH"]:
            if project in summaries:
                if report_type == "technical":
                    section = generate_technical_section(project, summaries[project], use_ai)
                else:
                    section = generate_public_section(project, summaries[project], use_ai)
                sections.append({
                    "project": project,
                    "title": section_info[project]["title"],
                    "content": section,
                })

        # Generate highlight
        if use_ai:
            highlight = generate_highlight_with_ai(summaries, report_type, total_commits, total_prs, total_repos)
        else:
            highlight = f"Total: {total_commits} commits, {total_prs} merged PRs across {total_repos} repositories."

        return JSONResponse({
            "success": True,
            "report_type": report_type,
            "stats": {
                "total_commits": total_commits,
                "total_prs": total_prs,
                "total_repos": total_repos,
            },
            "highlight": highlight,
            "sections": sections,
            "summaries": summaries,
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "anthropic_available": HAS_ANTHROPIC,
        "api_key_set": bool(os.environ.get('ANTHROPIC_API_KEY')),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
