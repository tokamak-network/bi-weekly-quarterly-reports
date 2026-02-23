# Ralph Loop Evaluation Log

## Iteration 0 (project grouping, no AI)
- **Sections:** 4 (only project groups, not individual repos)
- **Full report:** None
- **Verdict:** Wrong grouping mode. Need `report_grouping=repository` for comprehensive.

## Iteration 1 (repository grouping, no AI, comprehensive)
- **Sections:** 67 repos, full_report: 46K chars
- **Stats:** 2,161 commits, 12 PRs, 67 repos, 3.9M lines added, 16 contributors
- **Evaluation:**
  - ✅ 첫 페이지 임팩트: Executive Summary table with big numbers (4.9M total changes) — decent
  - ✅ 전체 레포 포함: All 67 repos included
  - ❌ 콘텐츠 깊이: Just commit message lists, no narrative, no context about WHY
  - ❌ 공격적 톤: Neutral/dry, no investor-facing language
  - ❌ ATI 대비: Numbers only, no narrative — literally what ATI does
  - ✅ Medium 마크다운: Clean markdown tables, proper headers
- **Score: 40/100** — Structure is there but no soul. Need AI.

## Iteration 2 (AI + deepseek-chat, repo_limit=5, comprehensive, repository grouping)
- **Sections:** 67 repos (limit only affects processing, all repos still included)
- **Full report:** 340K chars — massive improvement
- **Model:** deepseek-chat (gemini-3-flash was 503)
- **Evaluation:**
  - ✅ 첫 페이지 임팩트: Explosive headline, big numbers front and center (95/100)
  - ✅ 전체 레포 포함: All 67 repos (100/100)
  - ✅ 콘텐츠 깊이: Each repo has Overview, Goals, Accomplishments, Code Analysis, Next Steps (90/100)
  - ✅ 공격적 톤: "explodes", "monumental", "breakneck pace" (90/100)
  - ✅ ATI 대비: Numbers + rich narrative (85/100)
  - ⚠️ Medium 마크다운: Good but GitHub links show "[Will be added automatically]" (70/100)
  - ⚠️ Small repos (1 commit) get bloated 10-bullet sections (60/100)
- **Score: 75/100** — Major improvement, but link placeholders and proportionality issues
- **Fixes applied:** Removed GitHub placeholder from format instructions, added regex cleanup, scaled bullet count by repo size

## Iteration 3 (AI + deepseek-chat, fixes applied)
- **Sections:** 67 repos, full_report: 290K chars
- **Fixes verified:**
  - ✅ 0 placeholder links, 68 real GitHub URLs
  - ✅ Small repos (2 commits) get proportional 2-bullet sections (31 lines)
  - ✅ Large repos still get detailed 8-10 bullet sections
- **Evaluation:**
  - ✅ 첫 페이지 임팩트: 95/100
  - ✅ 전체 레포 포함: 100/100
  - ✅ 콘텐츠 깊이: 90/100
  - ✅ 공격적 톤: 90/100
  - ✅ ATI 대비: 90/100
  - ✅ Medium 마크다운: 95/100
- **Score: 93/100** — Exceeds 80% threshold. Ready for production.

## Code Changes Summary
1. CORS: Added localhost:3001 to allowed origins (was missing, caused "Failed to fetch")
2. python-dotenv: Installed in venv (was missing, API key never loaded)
3. Format instructions: Removed `**GitHub**: [Will be added automatically]` from template
4. AI post-processing: Added regex to strip any AI-generated GitHub placeholder lines, always insert real URL
5. Prompt: Added explicit instruction not to write placeholder text
6. Bullet scaling: Changed from "5-10 bullets always" to proportional based on commit count
