"""
HTML Report Generator for Tokamak Network Comprehensive Reports.

Converts the comprehensive markdown report + raw summary data into a
self-contained HTML file styled after reference-report-v2.html.
"""

import base64
import json
import os
import re
from typing import Any, Dict, List, Optional
from collections import Counter


LOGO_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "tokamak-logos")

# Load GitHub username mapping (member_id -> github_username)
_GITHUB_MEMBERS_PATH = os.path.join(os.path.dirname(__file__), "github_members.json")
try:
    with open(_GITHUB_MEMBERS_PATH) as _f:
        GITHUB_MEMBERS: Dict[str, str] = json.load(_f)
except (FileNotFoundError, json.JSONDecodeError):
    GITHUB_MEMBERS = {}
GITHUB_ORG_URL = "https://github.com/tokamak-network"


def _load_logo_base64(filename: str) -> str:
    """Load a logo file and return its base64 data URI."""
    path = os.path.join(LOGO_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{data}"


def _fmt(n: int) -> str:
    """Format number with commas."""
    return f"{n:,}"


def _fmt_short(n: int) -> str:
    """Format large numbers like 4.9M."""
    abs_n = abs(n)
    sign = "+" if n > 0 else ("-" if n < 0 else "")
    if abs_n >= 1_000_000:
        val = abs_n / 1_000_000
        if val == int(val):
            return f"{sign}{int(val)}M"
        return f"{sign}{val:.1f}M"
    if abs_n >= 1_000:
        val = abs_n / 1_000
        if val == int(val):
            return f"{sign}{int(val)}K"
        return f"{sign}{val:.1f}K"
    return f"{sign}{_fmt(abs_n)}"


def _parse_comprehensive_markdown(markdown: str) -> dict:
    """Parse comprehensive markdown report into structured data.
    
    Returns:
        {
            "headline": str,
            "executive_summary": str,
            "repos": [
                {
                    "name": str,
                    "github_url": str,
                    "overview": str,
                    "accomplishments": [str],
                    "code_analysis": str,
                    "next_steps": str,
                    "period_goals": str,
                }
            ]
        }
    """
    result = {
        "headline": "",
        "executive_summary": "",
        "repos": [],
    }

    # Split into headline section and repo sections
    # AI outputs use either `# Repo` + `## Sub` OR `## Repo` + `### Sub`
    # Detect which pattern is used by checking for `# RepoName` (h1) repo headers
    h1_repo_pattern = re.compile(r'^# ([^#\n].+)$', re.MULTILINE)
    h2_repo_pattern = re.compile(r'^## ([^#\n].+)$', re.MULTILINE)

    h1_matches = list(h1_repo_pattern.finditer(markdown))
    h2_matches = list(h2_repo_pattern.finditer(markdown))

    # If we have h1 repo sections with h2 subsections, use h1 as repo level
    # Filter out headline-like h1s (e.g. "Tokamak Network..." at the very top)
    real_h1_repos = []
    for m in h1_matches:
        name = m.group(1).strip()
        # Skip if it looks like a report title rather than a repo name
        if any(kw in name.lower() for kw in ['tokamak network', 'development report', 'biweekly', 'update', 'ecosystem']):
            continue
        real_h1_repos.append(m)

    h3_repo_pattern = re.compile(r'^### ([^#\n].+)$', re.MULTILINE)
    h3_matches = list(h3_repo_pattern.finditer(markdown))

    if len(real_h1_repos) >= 2:
        # Pattern: # RepoName → ## Subsection
        repo_matches = real_h1_repos
        sub_pattern = r'^## (.+)$'
    elif len(h2_matches) >= 2:
        # Pattern: ## RepoName → ### Subsection
        repo_matches = h2_matches
        sub_pattern = r'^### (.+)$'
    elif len(h3_matches) >= 2:
        # Pattern: ### RepoName (no subsection headers, just bullets)
        repo_matches = h3_matches
        sub_pattern = r'^#### (.+)$'
    else:
        repo_matches = []
        sub_pattern = r'^### (.+)$'

    if repo_matches:
        header_text = markdown[:repo_matches[0].start()].strip()
        # Extract headline (first # line or bold line)
        lines = header_text.split('\n')
        headline_parts = []
        summary_parts = []
        in_summary = False
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('---') or stripped.startswith('| '):
                if in_summary:
                    continue
                continue
            # Skip GitHub link lines (e.g. **GitHub**: [Link](url))
            if '**GitHub**' in stripped or 'GitHub]: ' in stripped or '[Link](' in stripped:
                continue
            if stripped.startswith('# ') and not stripped.startswith('## '):
                headline_parts.append(stripped.lstrip('# ').strip())
            elif stripped.startswith('**') and stripped.endswith('**'):
                # Date range line
                continue
            else:
                # Could be exec summary paragraph or subheadline
                in_summary = True
                summary_parts.append(stripped)

        result["headline"] = ' '.join(headline_parts) if headline_parts else "Tokamak Network Development Report"
        result["executive_summary"] = '\n'.join(summary_parts).strip()

    # Parse each repo section
    for i, match in enumerate(repo_matches):
        repo_name = match.group(1).strip()
        start = match.end()
        end = repo_matches[i + 1].start() if i + 1 < len(repo_matches) else len(markdown)
        section_text = markdown[start:end].strip()

        repo = {
            "name": repo_name,
            "github_url": "",
            "overview": "",
            "accomplishments": [],
            "code_analysis": "",
            "next_steps": "",
            "period_goals": "",
        }

        # Extract GitHub URL from [Link](url) or raw URL
        gh_match = re.search(r'\[Link\]\((https?://\S+?)\)', section_text)
        if not gh_match:
            gh_match = re.search(r'\*\*GitHub\*\*:\s*(https?://\S+)', section_text)
        if gh_match:
            repo["github_url"] = gh_match.group(1).strip()
        else:
            repo["github_url"] = "{}/{}".format(GITHUB_ORG_URL, repo_name)

        # Parse subsections using detected pattern (## or ###)
        subsections = re.split(sub_pattern, section_text, flags=re.MULTILINE)
        # subsections[0] is content before first subsection header
        # Then alternating: subsection_name, subsection_content, ...

        # If no subsections found, the overview might be in subsections[0]
        pre_content = subsections[0].strip() if subsections else ""
        if pre_content:
            # Clean out GitHub link lines and stats tables
            clean_lines = []
            for line in pre_content.split('\n'):
                stripped = line.strip()
                if '**GitHub**' in stripped or '[Link](' in stripped:
                    continue
                if stripped.startswith('|') or stripped.startswith('---'):
                    continue
                if stripped:
                    clean_lines.append(stripped)
            overview_text = ' '.join(clean_lines)
            if overview_text and len(overview_text) > 30:
                repo["overview"] = _clean_markdown(overview_text)

        for j in range(1, len(subsections), 2):
            sub_name = subsections[j].strip().lower()
            sub_content = subsections[j + 1].strip() if j + 1 < len(subsections) else ""

            if 'overview' in sub_name or 'summary' in sub_name:
                repo["overview"] = _clean_markdown(sub_content)
            elif 'accomplishment' in sub_name or 'key work' in sub_name or 'highlight' in sub_name:
                # Parse bullet points
                bullets = re.findall(r'[*\-]\s+\*?\*?(.+?)(?:\n|$)', sub_content)
                repo["accomplishments"] = [_clean_markdown(b.strip().rstrip('*')) for b in bullets if b.strip()]
            elif 'code analysis' in sub_name or 'code change' in sub_name:
                repo["code_analysis"] = _clean_markdown(sub_content)
            elif 'next step' in sub_name or 'looking ahead' in sub_name:
                repo["next_steps"] = _clean_markdown(sub_content)
            elif 'period goal' in sub_name or 'objective' in sub_name:
                repo["period_goals"] = _clean_markdown(sub_content)
            elif 'statistic' in sub_name:
                continue  # Skip stats table subsection

        result["repos"].append(repo)

    # Sort repos alphabetically, keep "Other repos" at end
    result["repos"].sort(key=lambda r: (r["name"].lower() == "other repos", r["name"].lower()))

    return result


def _clean_markdown(text: str) -> str:
    """Remove markdown formatting, keep plain text."""
    # Remove **bold**
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Remove *italic*
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    # Remove [link](url) -> link
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    # Remove markdown tables
    text = re.sub(r'\|.*\|', '', text)
    text = re.sub(r'---+', '', text)
    return text.strip()


def _get_contributor_counts(summary: dict) -> List[dict]:
    """Get contributors with their commit counts from raw commit data."""
    commits = summary.get("top_commits", [])
    # Also check raw commits if available
    all_commits = summary.get("_all_commits", commits)
    
    counter = Counter()
    for c in all_commits:
        author = c.get("member_id") or c.get("author") or c.get("member_name", "Unknown")
        if author:
            counter[author] += 1
    
    # If we don't have detailed commit data, use the contributors list
    if not counter and summary.get("contributors"):
        total = summary.get("total_commits", 0)
        contributors = summary["contributors"]
        if len(contributors) == 1:
            counter[contributors[0]] = total
        else:
            # Distribute evenly as fallback
            per = total // len(contributors) if contributors else 0
            for c in contributors:
                counter[c] = per
    
    return [{"name": name, "commits": count} for name, count in counter.most_common()]


def generate_html_report(
    summaries: Dict[str, Dict[str, Any]],
    markdown_report: str,
    date_range: dict,
    stats: dict,
) -> str:
    """Generate a self-contained HTML report.
    
    Args:
        summaries: Per-repo summary dicts from prepare_summary()
        markdown_report: The full comprehensive markdown report text
        date_range: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
        stats: {"total_commits", "total_lines_added", "total_lines_deleted", 
                "total_repos", "total_contributors", "net_change", "total_changes"}
    
    Returns:
        Complete self-contained HTML string.
    """
    # Load logos
    stacked_logo = _load_logo_base64("4_transparent.png")
    horizontal_logo = _load_logo_base64("1_transparent.png")

    # Parse markdown for content
    parsed = _parse_comprehensive_markdown(markdown_report)

    # Format date range
    start = date_range.get("start", "N/A")
    end = date_range.get("end", "N/A")
    
    # Parse dates for display
    try:
        from datetime import datetime
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        date_display = f"{start_dt.strftime('%B %d')} — {end_dt.strftime('%d, %Y')}"
        date_short = f"{start_dt.strftime('%B %d')}-{end_dt.strftime('%d, %Y')}"
    except Exception:
        date_display = f"{start} — {end}"
        date_short = f"{start} to {end}"

    # Stats
    total_commits = stats.get("total_commits", 0)
    total_changes = stats.get("total_changes", stats.get("total_lines_added", 0) + stats.get("total_lines_deleted", 0))
    total_repos = stats.get("total_repos", len(summaries))
    total_contributors = stats.get("total_contributors", 0)
    net_change = stats.get("net_change", 0)

    # Build repo cards HTML
    repo_cards_html = ""
    sorted_repos = sorted(summaries.items(), key=lambda x: x[1].get("total_commits", 0), reverse=True)
    
    for repo_name, summary in sorted_repos:
        if repo_name == "Other repos":
            continue
        
        # Find parsed markdown data for this repo
        parsed_repo = None
        for pr in parsed["repos"]:
            if pr["name"].lower() == repo_name.lower() or repo_name.lower() in pr["name"].lower():
                parsed_repo = pr
                break

        github_url = summary.get("github_url") or f"{GITHUB_ORG_URL}/{repo_name}"
        lines_added = summary.get("lines_added", 0)
        lines_deleted = summary.get("lines_deleted", 0)
        repo_net = lines_added - lines_deleted
        repo_commits = summary.get("total_commits", 0)
        repo_contributors = summary.get("contributor_count", 0)

        overview = parsed_repo["overview"] if parsed_repo and parsed_repo["overview"] else ""
        # Ensure overview ends at a complete sentence if it needs trimming
        if len(overview) > 600:
            # Cut at last sentence boundary within limit
            cut = overview[:600]
            last_period = max(cut.rfind('. '), cut.rfind('.\n'), cut.rfind('.'))
            if last_period > 200:
                overview = cut[:last_period + 1]
            else:
                overview = cut

        # Accomplishments
        accomplishments = parsed_repo["accomplishments"] if parsed_repo else []
        accomplishments_html = ""
        for acc in accomplishments[:7]:
            # Split on ": " to get title and description
            if ": " in acc:
                title, desc = acc.split(": ", 1)
                accomplishments_html += f'<li style="margin-bottom:8px;line-height:1.5;"><strong>{_escape(title)}</strong></li>\n'
            else:
                accomplishments_html += f'<li style="margin-bottom:8px;line-height:1.5;"><strong>{_escape(acc)}</strong></li>\n'

        # Contributors with GitHub profile links (via github_members.json mapping)
        contributor_counts = _get_contributor_counts(summary)
        contributors_html = ""
        for i, c in enumerate(contributor_counts[:3]):
            if i > 0:
                contributors_html += " · "
            name = c["name"]
            github_user = GITHUB_MEMBERS.get(name.lower())
            if github_user:
                contributors_html += (
                    f'<a href="https://github.com/{_escape(github_user)}" target="_blank" '
                    f'style="color:#2A72E5;text-decoration:none;font-weight:500;">{_escape(name)}</a> '
                    f'<span style="color:#888;">({c["commits"]} commits)</span>'
                )
            else:
                contributors_html += (
                    f'<span style="color:#1a1a1a;font-weight:500;">{_escape(name)}</span> '
                    f'<span style="color:#888;">({c["commits"]} commits)</span>'
                )

        # Code analysis & next steps
        code_analysis = parsed_repo.get("code_analysis", "") if parsed_repo else ""
        next_steps = parsed_repo.get("next_steps", "") if parsed_repo else ""

        extra_sections = ""
        if code_analysis:
            extra_sections += f'''
        <h4 style="font-size:0.9rem;font-weight:600;color:#1a1a1a;margin:16px 0 8px;">Code Analysis</h4>
        <p style="color:#444;font-size:0.85rem;line-height:1.6;">{_escape(code_analysis)}</p>'''
        if next_steps:
            extra_sections += f'''
        <h4 style="font-size:0.9rem;font-weight:600;color:#1a1a1a;margin:16px 0 8px;">Next Steps</h4>
        <p style="color:#444;font-size:0.85rem;line-height:1.6;">{_escape(next_steps)}</p>'''

        repo_cards_html += f'''
    <div style="background:#fff;border:1px solid #e8e8e8;border-radius:12px;padding:32px;margin-bottom:24px;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
            <h3 style="margin:0;font-size:1.4rem;font-weight:700;color:#1a1a1a;">{_escape(repo_name)}</h3>
            <a href="{_escape(github_url)}" target="_blank" style="color:#2A72E5;text-decoration:none;font-size:0.85rem;font-weight:500;">GitHub →</a>
        </div>
        <p style="color:#555;font-size:0.9rem;line-height:1.6;margin-bottom:20px;">{_escape(overview)}</p>
        <div style="display:flex;gap:24px;justify-content:space-around;padding:16px 0;border-top:1px solid #f0f0f0;border-bottom:1px solid #f0f0f0;margin-bottom:16px;">
            <div style="text-align:center;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">{_fmt(repo_commits)}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Commits</div></div>
            <div style="text-align:center;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">{repo_contributors}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Contributors</div></div>
            <div style="text-align:center;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">+{_fmt(lines_added)}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Lines Added</div></div>
            <div style="text-align:center;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">-{_fmt(lines_deleted)}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Lines Deleted</div></div>
            <div style="text-align:center;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">{'+' if repo_net >= 0 else ''}{_fmt(repo_net)}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Net Change</div></div>
        </div>
        <h4 style="font-size:0.9rem;font-weight:600;color:#1a1a1a;margin:16px 0 8px;">Key Accomplishments</h4>
        <ul style="padding-left:20px;color:#444;font-size:0.85rem;">{accomplishments_html}</ul>
        {extra_sections}
        <div style="margin-top:16px;padding-top:12px;border-top:1px solid #f0f0f0;font-size:0.85rem;">👤 <strong>Top Contributors:</strong> {contributors_html}</div>
    </div>'''

    # Executive summary - use parsed or fallback
    exec_summary = parsed["executive_summary"] or (
        f"In this reporting period, Tokamak Network's engineering teams deployed "
        f"{_fmt(total_commits)} commits across {total_repos} active repositories, "
        f"processing {_fmt_short(total_changes)} total code changes with a net growth of "
        f"{_fmt_short(net_change)} lines. {total_contributors} contributors drove this development effort."
    )

    # Extract headline from parsed
    headline_text = parsed.get("headline", "Tokamak Network Development Report")
    # Try to extract a punchy subheadline from exec summary first line
    exec_lines = exec_summary.split('\n')
    # Find a short punchy line for headline h3
    headline_h3 = ""
    remaining_summary = exec_summary
    for line in exec_lines:
        stripped = line.strip()
        if stripped and len(stripped) < 120 and not stripped.startswith('In '):
            headline_h3 = stripped
            remaining_summary = exec_summary.replace(stripped, '', 1).strip()
            break
    if not headline_h3:
        headline_h3 = f"{_fmt(total_commits)} Commits Drive {_fmt_short(total_changes)} Code Changes"

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tokamak Network Development Report — {_escape(date_short)}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; color:#1a1a1a; background:#f8f9fa; }}
  @media print {{ body {{ background:#fff; }} }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div style="min-height:100vh;background:linear-gradient(160deg,#0d0d0d 0%,#1a1a2e 50%,#0d0d0d 100%);display:flex;flex-direction:column;justify-content:center;align-items:center;padding:60px 40px;position:relative;overflow:hidden;">
  <div style="position:absolute;inset:0;background-image:repeating-linear-gradient(45deg,transparent,transparent 35px,rgba(255,255,255,0.015) 35px,rgba(255,255,255,0.015) 36px),repeating-linear-gradient(-45deg,transparent,transparent 35px,rgba(255,255,255,0.015) 35px,rgba(255,255,255,0.015) 36px);"></div>
  <div style="position:relative;z-index:1;text-align:center;">
    <img src="{stacked_logo}" alt="Tokamak Network" style="height:480px;margin-bottom:0;">
    <h1 style="font-size:3.5rem;font-weight:800;color:#fff;letter-spacing:-1px;line-height:1.1;margin-bottom:16px;">DEVELOPMENT<br>REPORT</h1>
    <div style="width:60px;height:3px;background:#2A72E5;margin:24px auto;"></div>
    <p style="font-size:1.2rem;color:rgba(255,255,255,0.6);font-weight:300;letter-spacing:4px;text-transform:uppercase;">Bi-Weekly Engineering Update</p>
    <p style="font-size:1.5rem;color:rgba(255,255,255,0.85);font-weight:500;margin-top:32px;">{_escape(date_display)}</p>
  </div>
</div>

<!-- STATS BAR -->
<div style="background:#111827;padding:28px 40px;">
  <div style="max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <div style="text-align:center;flex:1;min-width:140px;">
      <div style="font-size:2rem;font-weight:800;color:#fff;letter-spacing:-0.5px;">{_fmt(total_commits)}</div>
      <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Commits</div>
    </div>
    <div style="width:1px;height:40px;background:rgba(255,255,255,0.1);"></div>
    <div style="text-align:center;flex:1;min-width:140px;">
      <div style="font-size:2rem;font-weight:800;color:#fff;">{_fmt_short(total_changes)}</div>
      <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Lines Changed</div>
    </div>
    <div style="width:1px;height:40px;background:rgba(255,255,255,0.1);"></div>
    <div style="text-align:center;flex:1;min-width:140px;">
      <div style="font-size:2rem;font-weight:800;color:#fff;">{total_repos}</div>
      <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Active Repos</div>
    </div>
    <div style="width:1px;height:40px;background:rgba(255,255,255,0.1);"></div>
    <div style="text-align:center;flex:1;min-width:140px;">
      <div style="font-size:2rem;font-weight:800;color:#fff;">{total_contributors}</div>
      <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Contributors</div>
    </div>
    <div style="width:1px;height:40px;background:rgba(255,255,255,0.1);"></div>
    <div style="text-align:center;flex:1;min-width:140px;">
      <div style="font-size:2rem;font-weight:800;color:#2A72E5;">{_fmt_short(net_change)}</div>
      <div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Net Growth</div>
    </div>
  </div>
</div>

<!-- BODY -->
<div style="max-width:1100px;margin:0 auto;padding:48px 24px;">

  <!-- EXECUTIVE SUMMARY -->
  <div style="margin-bottom:48px;">
    <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">Executive Summary</h2>
    <h3 style="font-size:1.8rem;font-weight:800;color:#1a1a1a;line-height:1.3;margin-bottom:20px;">{_escape(headline_h3)}</h3>
    <p style="font-size:1rem;color:#444;line-height:1.8;max-width:900px;">{_escape(remaining_summary)}</p>
  </div>

  <div style="width:100%;height:1px;background:#e8e8e8;margin-bottom:48px;"></div>

  <!-- REPO CARDS -->
  <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin-bottom:24px;">Repository Breakdown</h2>

  {repo_cards_html}

</div>

<!-- FOOTER -->
<div style="background:linear-gradient(160deg,#0d0d0d 0%,#1a1a2e 50%,#0d0d0d 100%);padding:60px 40px;text-align:center;">
  <div style="max-width:600px;margin:0 auto;">
    <img src="{stacked_logo}" alt="Tokamak Network" style="height:160px;margin-bottom:0;">
    <p style="color:#888;font-size:0.8rem;">Tokamak Network · Bi-Weekly Development Report · {_escape(date_short)}</p>
    <p style="color:#aaa;font-size:0.7rem;margin-top:4px;">Generated automatically from GitHub activity data</p>
  </div>
</div>
</body>
</html>'''

    return html


def _strip_markdown(text: str) -> str:
    """Remove markdown syntax artifacts from AI-generated text."""
    import re
    # Remove heading markers (### ## #)
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers (**text** -> text, *text* -> text)
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove inline code backticks
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text.strip()


def _escape(text: str) -> str:
    """HTML-escape text (also strips markdown artifacts)."""
    text = _strip_markdown(text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
