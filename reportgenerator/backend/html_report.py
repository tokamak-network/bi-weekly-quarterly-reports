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

from infographic import (
    classify_repos_from_csv,
    CATEGORIES,
    _activity_level,
    _escape_html,
    _build_landscape_html,
    _build_blueprint_html,
)


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
    markdown_report_kr: Optional[str] = None,
    language: str = "en",
    report_number: int = 2,
    report_title: str = "",
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

    # Cover title
    if report_title:
        cover_title_html = _escape(report_title).upper()
        # Split into two lines if possible (e.g., "BIWEEKLY REPORT #2" -> "BIWEEKLY<br>REPORT #2")
        words = cover_title_html.split()
        if len(words) >= 2:
            mid = len(words) // 2
            cover_title_html = ' '.join(words[:mid]) + '<br>' + ' '.join(words[mid:])
        page_title = _escape(report_title)
    else:
        cover_title_html = "BIWEEKLY<br>REPORT #{}".format(report_number)
        page_title = "Biweekly Report #{}".format(report_number)

    # Stats
    total_commits = stats.get("total_commits", 0)
    total_changes = stats.get("total_changes", stats.get("total_lines_added", 0) + stats.get("total_lines_deleted", 0))
    total_repos = stats.get("total_repos", len(summaries))
    total_contributors = stats.get("total_contributors", 0)
    net_change = stats.get("net_change", 0)

    # Build repo cards HTML
    repo_cards_html = ""
    sorted_repos = sorted(summaries.items(), key=lambda x: (x[0].lower() == "other repos", x[0].lower()))
    
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
    <div style="background:#fff;border:1px solid #e8e8e8;border-radius:12px;padding:32px;margin-bottom:24px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:16px;">
          <tr>
            <td style="vertical-align:middle;"><h3 style="margin:0;font-size:1.4rem;font-weight:700;color:#1a1a1a;">{_escape(repo_name)}</h3></td>
            <td style="vertical-align:middle;text-align:right;"><a href="{_escape(github_url)}" target="_blank" style="color:#2A72E5;text-decoration:none;font-size:0.85rem;font-weight:500;">GitHub &rarr;</a></td>
          </tr>
        </table>
        <p style="color:#555;font-size:0.9rem;line-height:1.6;margin-bottom:20px;">{_escape(overview)}</p>
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #f0f0f0;border-bottom:1px solid #f0f0f0;margin-bottom:16px;">
          <tr>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">+{_fmt(lines_added)}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Lines Added</div></td>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">-{_fmt(lines_deleted)}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Lines Deleted</div></td>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">{'+' if repo_net >= 0 else ''}{_fmt(repo_net)}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Net Change</div></td>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">{repo_contributors}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">Contributors</div></td>
          </tr>
        </table>
        <h4 style="font-size:0.9rem;font-weight:600;color:#1a1a1a;margin:16px 0 8px;">Key Accomplishments</h4>
        <ul style="padding-left:20px;color:#444;font-size:0.85rem;">{accomplishments_html}</ul>
        {extra_sections}
        <div style="margin-top:16px;padding-top:12px;border-top:1px solid #f0f0f0;font-size:0.85rem;">&#128100; <strong>Top Contributors:</strong> {contributors_html}</div>
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

    # ── Build infographic sections (Landscape + Blueprint) ──
    # Build repo_commits dict from summaries for classification
    infographic_repo_commits = {}  # type: Dict[str, int]
    infographic_repo_contributors = {}  # type: Dict[str, List[str]]
    infographic_repo_changes = {}  # type: Dict[str, int]
    for rname, rsum in summaries.items():
        if rname == "Other repos":
            continue
        infographic_repo_commits[rname] = rsum.get("total_commits", 0)
        infographic_repo_changes[rname] = rsum.get("total_changes", rsum.get("lines_added", 0) + rsum.get("lines_deleted", 0)) if isinstance(rsum, dict) else 0
        contribs = rsum.get("contributors", [])
        if contribs:
            infographic_repo_contributors[rname] = list(contribs)

    infographic_categorized = classify_repos_from_csv(infographic_repo_commits)

    inf_total_repos = sum(len(repos) for repos in infographic_categorized.values())
    inf_total_changes = sum(infographic_repo_changes.get(r["name"], 0) for repos in infographic_categorized.values() for r in repos)
    inf_active_cats = sum(1 for repos in infographic_categorized.values() if repos)

    # Inject lines_changed into each repo dict for landscape display
    for cat_repos in infographic_categorized.values():
        for repo in cat_repos:
            repo["lines_changed"] = infographic_repo_changes.get(repo["name"], 0)

    landscape_section_html = _build_landscape_html(
        infographic_categorized, inf_total_repos, inf_total_changes, inf_active_cats
    )
    blueprint_section_html = _build_blueprint_html(
        infographic_categorized, infographic_repo_contributors, None
    )

    # Build body content for English version
    body_en = f'''
  <!-- EXECUTIVE SUMMARY -->
  <div style="margin-bottom:48px;">
    <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">Executive Summary</h2>
    <h3 style="font-size:1.8rem;font-weight:800;color:#1a1a1a;line-height:1.3;margin-bottom:20px;">{_escape(headline_h3)}</h3>
    <p style="font-size:1rem;color:#444;line-height:1.8;max-width:900px;">{_escape(remaining_summary)}</p>
  </div>

  <div style="width:100%;height:1px;background:#e8e8e8;margin-bottom:48px;"></div>

  <!-- ECOSYSTEM LANDSCAPE -->
  <div style="margin-bottom:48px;">
    <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin-bottom:24px;">🗺️ Ecosystem Landscape</h2>
    {landscape_section_html}
  </div>

  <div style="width:100%;height:1px;background:#e8e8e8;margin-bottom:48px;"></div>

  <!-- CATEGORY FOCUS & SYNERGIES -->
  <div style="margin-bottom:48px;">
    {blueprint_section_html}
  </div>

  <div style="width:100%;height:1px;background:#e8e8e8;margin-bottom:48px;"></div>

  <!-- REPO CARDS -->
  <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin-bottom:24px;">Repository Breakdown</h2>

  {repo_cards_html}
'''

    # Build Korean body if available
    body_kr = ""
    if language == "both" and markdown_report_kr:
        parsed_kr = _parse_comprehensive_markdown(markdown_report_kr)
        exec_summary_kr = parsed_kr.get("executive_summary", "")
        headline_kr = parsed_kr.get("headline", "Tokamak Network 개발 보고서")

        exec_lines_kr = exec_summary_kr.split('\n') if exec_summary_kr else []
        headline_h3_kr = ""
        remaining_summary_kr = exec_summary_kr
        for line in exec_lines_kr:
            stripped = line.strip()
            if stripped and len(stripped) < 150 and not stripped.startswith('이 '):
                headline_h3_kr = stripped
                remaining_summary_kr = exec_summary_kr.replace(stripped, '', 1).strip()
                break
        if not headline_h3_kr:
            headline_h3_kr = "{} 커밋으로 {} 코드 변경 달성".format(_fmt(total_commits), _fmt_short(total_changes))

        # Build Korean repo cards from Korean parsed content
        repo_cards_html_kr = ""
        for pr_kr in parsed_kr.get("repos", []):
            kr_name = pr_kr.get("name", "")
            kr_overview = pr_kr.get("overview", "")
            kr_accomplishments = pr_kr.get("accomplishments", [])
            kr_accs_html = ""
            for acc in kr_accomplishments[:7]:
                if ": " in acc:
                    t, d = acc.split(": ", 1)
                    kr_accs_html += '<li style="margin-bottom:8px;line-height:1.5;"><strong>{}</strong></li>\n'.format(_escape(t))
                else:
                    kr_accs_html += '<li style="margin-bottom:8px;line-height:1.5;"><strong>{}</strong></li>\n'.format(_escape(acc))

            # Find matching English repo for stats
            matched_summary = None
            for rn, rs in summaries.items():
                if rn.lower() == kr_name.lower() or kr_name.lower() in rn.lower():
                    matched_summary = rs
                    break

            if matched_summary:
                kr_commits = matched_summary.get('total_commits', 0)
                kr_contributors = matched_summary.get('contributor_count', 0)
                kr_added = matched_summary.get('lines_added', 0)
                kr_deleted = matched_summary.get('lines_deleted', 0)
                kr_net = kr_added - kr_deleted
                kr_github = matched_summary.get('github_url', '')
            else:
                kr_commits = 0
                kr_contributors = 0
                kr_added = 0
                kr_deleted = 0
                kr_net = 0
                kr_github = pr_kr.get("github_url", "")

            repo_cards_html_kr += '''
    <div style="background:#fff;border:1px solid #e8e8e8;border-radius:12px;padding:32px;margin-bottom:24px;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:16px;">
          <tr>
            <td style="vertical-align:middle;"><h3 style="margin:0;font-size:1.4rem;font-weight:700;color:#1a1a1a;">{name}</h3></td>
            <td style="vertical-align:middle;text-align:right;"><a href="{github}" target="_blank" style="color:#2A72E5;text-decoration:none;font-size:0.85rem;font-weight:500;">GitHub &rarr;</a></td>
          </tr>
        </table>
        <p style="color:#555;font-size:0.9rem;line-height:1.6;margin-bottom:20px;">{overview}</p>
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid #f0f0f0;border-bottom:1px solid #f0f0f0;margin-bottom:16px;">
          <tr>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">+{added}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">추가 라인</div></td>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">-{deleted}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">삭제 라인</div></td>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">{net_sign}{net}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">순 변화</div></td>
            <td style="text-align:center;padding:16px 8px;"><div style="font-size:1.1rem;font-weight:700;color:#1a1a1a;">{contribs}</div><div style="font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:0.5px;">기여자</div></td>
          </tr>
        </table>
        <h4 style="font-size:0.9rem;font-weight:600;color:#1a1a1a;margin:16px 0 8px;">주요 성과</h4>
        <ul style="padding-left:20px;color:#444;font-size:0.85rem;">{accs}</ul>
    </div>'''.format(
                name=_escape(kr_name),
                github=_escape(kr_github),
                overview=_escape(kr_overview),
                commits=_fmt(kr_commits),
                contribs=kr_contributors,
                added=_fmt(kr_added),
                deleted=_fmt(kr_deleted),
                net_sign='+' if kr_net >= 0 else '',
                net=_fmt(kr_net),
                accs=kr_accs_html,
            )

        body_kr = '''
  <!-- EXECUTIVE SUMMARY (KR) -->
  <div style="margin-bottom:48px;">
    <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;">요약 보고</h2>
    <h3 style="font-size:1.8rem;font-weight:800;color:#1a1a1a;line-height:1.3;margin-bottom:20px;">{headline}</h3>
    <p style="font-size:1rem;color:#444;line-height:1.8;max-width:900px;">{summary}</p>
  </div>

  <div style="width:100%;height:1px;background:#e8e8e8;margin-bottom:48px;"></div>

  <!-- REPO CARDS (KR) -->
  <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin-bottom:24px;">저장소별 상세 보고</h2>

  {cards}
'''.format(
            headline=_escape(headline_h3_kr),
            summary=_escape(remaining_summary_kr),
            cards=repo_cards_html_kr,
        )

    # Language toggle elements
    toggle_html = ""
    toggle_style = ""
    toggle_script = ""
    if language == "both" and body_kr:
        toggle_style = """
  .lang-toggle { position:fixed; top:16px; right:16px; z-index:9999; display:flex; background:#fff; border:1px solid #e0e0e0; border-radius:20px; padding:4px; box-shadow:0 2px 8px rgba(0,0,0,0.1); font-size:0.8rem; }
  .lang-toggle button { border:none; background:transparent; padding:6px 14px; border-radius:16px; cursor:pointer; font-weight:500; color:#888; transition:all 0.2s; }
  .lang-toggle button.active { background:#2A72E5; color:#fff; }
  @media print { .lang-toggle { position:static; margin:8px auto; display:flex; justify-content:center; } .lang-kr { display:none !important; } .lang-en { display:block !important; } }
"""
        toggle_html = """
<div class="lang-toggle" id="langToggle">
  <button id="btnEn" class="active" onclick="switchLang('en')">🇺🇸 English</button>
  <button id="btnKr" onclick="switchLang('kr')">🇰🇷 한국어</button>
</div>
"""
        toggle_script = """
<script>
function switchLang(lang) {
  var en = document.getElementById('contentEn');
  var kr = document.getElementById('contentKr');
  var btnEn = document.getElementById('btnEn');
  var btnKr = document.getElementById('btnKr');
  if (lang === 'kr') {
    en.style.display = 'none';
    kr.style.display = 'block';
    btnEn.className = '';
    btnKr.className = 'active';
  } else {
    en.style.display = 'block';
    kr.style.display = 'none';
    btnEn.className = 'active';
    btnKr.className = '';
  }
}
</script>
"""

    # Wrap body content in language divs if bilingual
    if language == "both" and body_kr:
        body_section = '''
<div style="max-width:1100px;margin:0 auto;padding:48px 24px;">
  <div class="lang-en" id="contentEn" style="display:block;">
{en}
  </div>
  <div class="lang-kr" id="contentKr" style="display:none;">
{kr}
  </div>
</div>
'''.format(en=body_en, kr=body_kr)
    else:
        body_section = '''
<div style="max-width:1100px;margin:0 auto;padding:48px 24px;">
{en}
</div>
'''.format(en=body_en)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tokamak Network {page_title} — {_escape(date_short)}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; color:#1a1a1a; background:#f8f9fa; }}
  @page {{
    size: A4;
    margin: 0;
  }}
  @media print {{
    body {{ background:#fff; margin: 15mm; }}
  }}
  {toggle_style}
</style>
</head>
<body>

{toggle_html}

<!-- COVER PAGE -->
<div style="background-color:#111827;padding:80px 40px;text-align:center;">
    <img src="{stacked_logo}" alt="Tokamak Network" style="height:480px;margin-bottom:0;">
    <h1 style="font-size:3.5rem;font-weight:800;color:#fff;letter-spacing:-1px;line-height:1.1;margin-bottom:16px;">{cover_title_html}</h1>
    <div style="width:60px;height:3px;background:#2A72E5;margin:24px auto;"></div>
    <p style="font-size:1.2rem;color:#999999;font-weight:300;letter-spacing:4px;text-transform:uppercase;">Bi-Weekly Engineering Update</p>
    <p style="font-size:1.5rem;color:#d9d9d9;font-weight:500;margin-top:32px;">{_escape(date_display)}</p>
</div>

<!-- STATS BAR -->
<div style="background-color:#111827;padding:28px 40px;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:1100px;margin:0 auto;">
    <tr>
      <td style="text-align:center;padding:8px 16px;">
        <div style="font-size:2rem;font-weight:800;color:#fff;letter-spacing:-0.5px;">{_fmt_short(total_changes)}</div>
        <div style="font-size:0.7rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Lines Changed</div>
      </td>
      <td style="width:1px;background:#333333;" width="1"></td>
      <td style="text-align:center;padding:8px 16px;">
        <div style="font-size:2rem;font-weight:800;color:#fff;">{total_repos}</div>
        <div style="font-size:0.7rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Active Repos</div>
      </td>
      <td style="width:1px;background:#333333;" width="1"></td>
      <td style="text-align:center;padding:8px 16px;">
        <div style="font-size:2rem;font-weight:800;color:#fff;">{total_contributors}</div>
        <div style="font-size:0.7rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Contributors</div>
      </td>
      <td style="width:1px;background:#333333;" width="1"></td>
      <td style="text-align:center;padding:8px 16px;">
        <div style="font-size:2rem;font-weight:800;color:#2A72E5;">{_fmt_short(net_change)}</div>
        <div style="font-size:0.7rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Net Growth</div>
      </td>
    </tr>
  </table>
</div>

{body_section}

<!-- FOOTER -->
<div style="background-color:#111827;padding:60px 40px;text-align:center;">
  <div style="max-width:600px;margin:0 auto;">
    <img src="{stacked_logo}" alt="Tokamak Network" style="height:160px;margin-bottom:0;">
    <p style="color:#888;font-size:0.8rem;">Tokamak Network · {page_title} · {_escape(date_short)}</p>
    <p style="color:#aaa;font-size:0.7rem;margin-top:4px;">Generated automatically from GitHub activity data</p>
  </div>
</div>

{toggle_script}
</body>
</html>'''

    return html


def generate_email_summary_html(
    stats: dict,
    date_range: dict,
    report_url: str,
    report_title: str = "",
    report_number: int = 2,
    executive_summary: str = "",
    markdown_report: str = "",
) -> str:
    """Generate a lightweight Gmail-safe summary email (~20-30 KB).

    Includes: Cover page, KPI bar, Executive Summary, CTA button
    (linking to the full S3-hosted report), and Footer.

    Args:
        stats: Same dict as generate_html_report() receives.
        date_range: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}.
        report_url: Public URL of the full report on S3.
        report_title: e.g. "Biweekly Report #3".
        report_number: Fallback number if report_title is empty.
        executive_summary: Pre-built summary text. If empty, extracted
            from markdown_report or auto-generated from stats.
        markdown_report: Full markdown (used to extract exec summary
            if executive_summary is empty).

    Returns:
        Complete HTML string sized for Gmail (< 102 KB).
    """
    # ── Logos ──
    stacked_logo = _load_logo_base64("4_transparent.png")

    # ── Date formatting ──
    start = date_range.get("start", "N/A")
    end = date_range.get("end", "N/A")
    try:
        from datetime import datetime
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        date_display = f"{start_dt.strftime('%B %d')} — {end_dt.strftime('%d, %Y')}"
        date_short = f"{start_dt.strftime('%B %d')}-{end_dt.strftime('%d, %Y')}"
    except Exception:
        date_display = f"{start} — {end}"
        date_short = f"{start} to {end}"

    # ── Cover title ──
    if report_title:
        cover_title_html = _escape(report_title).upper()
        words = cover_title_html.split()
        if len(words) >= 2:
            mid = len(words) // 2
            cover_title_html = ' '.join(words[:mid]) + '<br>' + ' '.join(words[mid:])
        page_title = _escape(report_title)
    else:
        cover_title_html = "BIWEEKLY<br>REPORT #{}".format(report_number)
        page_title = "Biweekly Report #{}".format(report_number)

    # ── Stats ──
    total_commits = stats.get("total_commits", 0)
    total_changes = stats.get("total_changes", stats.get("total_lines_added", 0) + stats.get("total_lines_deleted", 0))
    total_repos = stats.get("total_repos", 0)
    total_contributors = stats.get("total_contributors", 0)
    net_change = stats.get("net_change", 0)

    # ── Executive summary ──
    exec_text = executive_summary
    if not exec_text and markdown_report:
        parsed = _parse_comprehensive_markdown(markdown_report)
        exec_text = parsed.get("executive_summary", "")
    if not exec_text:
        exec_text = (
            f"In this reporting period, Tokamak Network's engineering teams deployed "
            f"{_fmt(total_commits)} commits across {total_repos} active repositories, "
            f"processing {_fmt_short(total_changes)} total code changes with a net growth of "
            f"{_fmt_short(net_change)} lines. {total_contributors} contributors drove this development effort."
        )

    # ── Build the email HTML ──
    # NOTE: Gmail strips <style> blocks, so everything is inline.
    # No base64 logo images in email — Gmail blocks data: URIs in <img>.
    # Use the Tokamak blue color as a text stand-in for the logo.

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
</head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#1a1a1a;background:#f8f9fa;">

<!-- COVER -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#111827;">
  <tr><td style="padding:60px 40px 24px;text-align:center;">
    <div style="font-size:1rem;color:#2A72E5;letter-spacing:6px;text-transform:uppercase;font-weight:600;margin-bottom:24px;">TOKAMAK NETWORK</div>
    <h1 style="font-size:2.8rem;font-weight:800;color:#ffffff;letter-spacing:-1px;line-height:1.1;margin:0 0 16px;">{cover_title_html}</h1>
    <div style="width:60px;height:3px;background:#2A72E5;margin:24px auto;"></div>
    <p style="font-size:1.1rem;color:#999999;font-weight:300;letter-spacing:4px;text-transform:uppercase;margin:0;">Bi-Weekly Engineering Update</p>
    <p style="font-size:1.3rem;color:#d9d9d9;font-weight:500;margin:24px 0 0;">{_escape(date_display)}</p>
  </td></tr>
</table>

<!-- KPI BAR -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#111827;">
  <tr><td style="padding:0 40px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:700px;margin:0 auto;border-top:1px solid #333333;">
      <tr>
        <td style="text-align:center;padding:20px 8px;">
          <div style="font-size:1.8rem;font-weight:800;color:#ffffff;">{_fmt_short(total_changes)}</div>
          <div style="font-size:0.65rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Lines Changed</div>
        </td>
        <td style="width:1px;background:#333333;" width="1"></td>
        <td style="text-align:center;padding:20px 8px;">
          <div style="font-size:1.8rem;font-weight:800;color:#ffffff;">{total_repos}</div>
          <div style="font-size:0.65rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Active Repos</div>
        </td>
        <td style="width:1px;background:#333333;" width="1"></td>
        <td style="text-align:center;padding:20px 8px;">
          <div style="font-size:1.8rem;font-weight:800;color:#ffffff;">{total_contributors}</div>
          <div style="font-size:0.65rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Contributors</div>
        </td>
        <td style="width:1px;background:#333333;" width="1"></td>
        <td style="text-align:center;padding:20px 8px;">
          <div style="font-size:1.8rem;font-weight:800;color:#2A72E5;">{_fmt_short(net_change)}</div>
          <div style="font-size:0.65rem;color:#808080;text-transform:uppercase;letter-spacing:2px;margin-top:4px;">Net Growth</div>
        </td>
      </tr>
    </table>
  </td></tr>
</table>

<!-- EXECUTIVE SUMMARY -->
<table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr><td style="padding:48px 40px;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:700px;margin:0 auto;">
      <tr><td>
        <h2 style="font-size:0.7rem;font-weight:600;color:#2A72E5;text-transform:uppercase;letter-spacing:3px;margin:0 0 16px;">Executive Summary</h2>
        <p style="font-size:1rem;color:#444444;line-height:1.8;margin:0 0 40px;">{_escape(exec_text)}</p>

        <!-- CTA BUTTON -->
        <table cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;">
          <tr><td style="border-radius:8px;background:#2A72E5;text-align:center;">
            <a href="{_escape(report_url)}" target="_blank" style="display:inline-block;padding:16px 48px;color:#ffffff;font-size:1rem;font-weight:600;text-decoration:none;letter-spacing:0.5px;">View Full Report</a>
          </td></tr>
        </table>

        <p style="font-size:0.8rem;color:#999999;text-align:center;margin-top:16px;">
          Click the button above to read the complete report with all {total_repos} repository breakdowns, ecosystem landscape, and architecture blueprint.
        </p>
      </td></tr>
    </table>
  </td></tr>
</table>

<!-- FOOTER -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#111827;">
  <tr><td style="padding:40px;text-align:center;">
    <div style="font-size:1rem;color:#2A72E5;letter-spacing:4px;text-transform:uppercase;font-weight:600;margin-bottom:12px;">TOKAMAK NETWORK</div>
    <p style="color:#888888;font-size:0.8rem;margin:0;">{page_title} &middot; {_escape(date_short)}</p>
    <p style="color:#aaaaaa;font-size:0.7rem;margin:4px 0 0;">Generated automatically from GitHub activity data</p>
  </td></tr>
</table>

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
