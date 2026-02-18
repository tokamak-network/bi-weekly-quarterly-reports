# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tokamak Network의 GitHub CSV 데이터를 기반으로 격주/분기 보고서를 자동 생성하는 웹 애플리케이션.
AI 기반 요약, 다중 리뷰어 피드백 시스템, Medium 퍼블리싱 기능 제공.

## How to Run

### Backend
```bash
cd reportgenerator/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
- Runs on `http://localhost:8000`
- Alternative: `uvicorn main:app --reload --port 8000`

### Frontend
```bash
cd reportgenerator/frontend
npm install
npm run dev
```
- Runs on `http://localhost:3000`
- Build: `npm run build`
- Lint: `npm run lint`

### Environment Variables (`.env` auto-loaded)
- `TOKAMAK_API_KEY` - AI API 키 (필수)
- `TOKAMAK_BASE_URL` - API base URL (기본: https://api.ai.tokamak.network)
- `TOKAMAK_MODEL` - 기본 모델명
- `TOKAMAK_MODELS` / `TOKAMAK_AVAILABLE_MODELS` - 모델 목록 (쉼표 구분)
- `TOKAMAK_REQUEST_TIMEOUT` - 요청 타임아웃 초 (기본: 30)
- `ANTHROPIC_API_KEY` - Anthropic fallback용

## Tech Stack

- **Backend**: FastAPI 0.109.0, Uvicorn, Python 3.11
- **Frontend**: Next.js 14.1.0, React 18, TypeScript 5, Tailwind CSS 3
- **AI**: OpenAI-compatible API (`openai`), Anthropic Claude API (`anthropic`)
- **UI**: react-dropzone, lucide-react

## Architecture

### Single-File Structure
- **Backend**: `reportgenerator/backend/main.py` (~3100줄) — 모든 API 로직
- **Frontend**: `reportgenerator/frontend/src/app/page.tsx` (~2000줄) — 모든 UI 로직

### LLM Provider Fallback Chain (`main.py:560`)
`generate_with_llm()` → `generate_with_tokamak()` (line 494) → `generate_with_anthropic()` (line 540)
- Tokamak: OpenAI client with custom base_url. GPT-5.2 모델은 `responses.create()` 먼저 시도 후 `chat.completions.create()` fallback
- Anthropic: `claude-sonnet-4.5` 하드코딩
- `refresh_env()` (line 281): 각 엔드포인트 시작 시 `.env` 재로드 (런타임 변경 반영)

### Report Generation Pipeline (`main.py:2432`)
CSV 업로드 → `parse_csv_content()` (line 603) → 프로젝트/레포별 그룹화 → AI 요약 → 보고서 조립
- Public (투자자용) / Technical (개발자용) 두 가지 모드
- Format A (Concise) / Format B (Structured) 형식 선택
- `ThreadPoolExecutor(max_workers=min(5, len(entries)))` 로 레포별 AI 요청 병렬화 (repository 그룹핑만)

### Review System (`main.py:2796`)
5단계 리뷰어: 일반 독자(Lv.1) → 비즈니스 분석가(Lv.2) → 프로젝트 매니저(Lv.3) → 시니어 개발자(Lv.4) → 블록체인 아키텍트(Lv.5)

각 리뷰어는 `{issues, strengths, overall_score, summary}` JSON 반환.

**Review JSON 파싱 파이프라인** (`_do_review` line 2832):
1. 마크다운 코드펜스 제거, 첫 `{` 앞 텍스트 제거
2. `json.loads()` 직접 파싱
3. `_try_repair_json()` — 잘린 JSON 복구 (미닫힌 브래킷 추가)
4. balanced bracket 추출 (depth 추적)
5. regex fallback
6. 실패 시 빈 fallback 데이터 + 파싱 실패 시 lightweight 프롬프트로 자동 1회 재시도

**리포트 truncation**: 리뷰 시 `MAX_REVIEW_CHARS = 15000` 으로 잘라서 전송 (LLM 타임아웃 방지)

### Timeout 설정
| 구간 | 백엔드 | 프론트엔드 |
|------|--------|-----------|
| 기본 LLM 호출 | `get_model_timeout()` (GPT-5: 60s, Gemini: 20s, DeepSeek: 25s, 기본: 30s) | — |
| Review | `max(model_timeout × 3, 180s)` | 360s (6분) |
| Review 재시도 | `min(60s, review_timeout / 2)` | — |
| Improve | `max(model_timeout × 3, 180s)` | 240s (4분) |

### Frontend 3-Step Workflow (`page.tsx`)
1. **Generate** — CSV 업로드, 옵션 선택, 보고서 생성
2. **Review & Improve** — 리뷰어별 피드백, "Apply this change" 수동 적용, AI Improvement 일괄 반영
3. **Publish** — Medium 형식 변환, 다운로드

**"Apply this change" 매칭** (`handleApplyIssue` line 560): exact match → whitespace-flexible regex → case-insensitive regex 순서

**상태 추적**: `appliedIssues` (Set) + `appliedChanges` (Array) 로 변경 이력 관리. AI Improvement 시 이미 수동 적용된 이슈 자동 제외.

**ViewMode**: original / improved / diff (line-by-line diff via `computeDiff`)

## Key API Endpoints

- `POST /api/generate` — CSV → 보고서 생성 (FormData: file, report_type, use_ai, model, report_grouping, report_format, repo_limit)
- `POST /api/review` — AI 리뷰어 피드백 생성 (FormData: report_text, report_type, report_format, reviewer_level, model)
- `POST /api/improve` — 리뷰 피드백 기반 보고서 개선 (FormData: report_text, report_type, reviews_json, model, report_format)
- `GET /api/reviewers` — 리뷰어 목록 조회
- `GET /api/health` — 서버 상태 확인

## Development Notes

- CORS: localhost:3000, localhost:3002 허용
- AI 응답의 JSON 파싱 실패 시 fallback 로직: 빈 issues/strengths, score=5, 파싱 실패 raw 텍스트를 summary에 포함
- issue 객체 검증: description 필수, severity는 low/medium/high만 허용, 유효하지 않은 항목은 drop
- overall_score 파싱: int, float, "5/10", "5 out of 10" 등 다양한 형식 지원
