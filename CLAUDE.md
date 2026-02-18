# CLAUDE.md - Project Context

## Project Overview

Tokamak Network의 GitHub CSV 데이터를 기반으로 격주/분기 보고서를 자동 생성하는 웹 애플리케이션.
AI 기반 요약, 다중 리뷰어 피드백 시스템, Medium 퍼블리싱 기능 제공.

## Project Structure

```
bi-weekly-quarterly-reports/
├── biweekly/                    # 격주 보고서 아카이브 (2023-2026)
├── quarterly/                   # 분기 보고서 아카이브 (2024-2025)
└── reportgenerator/             # 메인 애플리케이션
    ├── backend/                 # FastAPI 백엔드
    │   ├── main.py              # 핵심 서버 코드 (~3100줄)
    │   └── requirements.txt     # Python 의존성
    └── frontend/                # Next.js 프론트엔드
        ├── src/app/page.tsx     # 메인 UI 컴포넌트 (~2000줄)
        ├── src/app/layout.tsx
        └── package.json
```

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

### Frontend
```bash
cd reportgenerator/frontend
npm install
npm run dev
```
- Runs on `http://localhost:3000`

## Tech Stack

- **Backend**: FastAPI 0.109.0, Uvicorn, Python 3.11
- **Frontend**: Next.js 14.1.0, React 18, TypeScript 5, Tailwind CSS 3
- **AI**: Anthropic Claude API (`anthropic`), OpenAI-compatible API (`openai`)
- **UI Libraries**: react-dropzone (파일 업로드), lucide-react (아이콘)

## Key Environment Variables

- `TOKAMAK_API_KEY` - AI API 키 (필수)
- `TOKAMAK_BASE_URL` - API base URL (기본: https://api.ai.tokamak.network)
- `TOKAMAK_MODEL` - 기본 모델명
- `.env` 파일로 자동 로드됨

## Key API Endpoints

- `POST /api/generate` - CSV → 보고서 생성
- `POST /api/review` - AI 리뷰어 피드백 생성
- `POST /api/improve` - 리뷰 피드백 기반 보고서 개선
- `GET /api/reviewers` - 리뷰어 목록 조회
- `GET /api/health` - 서버 상태 확인

## Architecture & Features

### Report Generation
- CSV 업로드 → 파싱 → 프로젝트/레포별 그룹화 → AI 요약 → 보고서 조립
- Public (투자자용) / Technical (개발자용) 두 가지 모드
- Format A (Concise) / Format B (Structured) 형식 선택
- ThreadPoolExecutor로 병렬 AI 요청

### Review System (5단계 리뷰어)
1. 일반 독자 (General Reader) - Lv.1
2. 비즈니스 분석가 (Business Analyst) - Lv.2
3. 프로젝트 매니저 (Project Manager) - Lv.3
4. 시니어 개발자 (Senior Developer) - Lv.4
5. 블록체인 아키텍트 (Blockchain Architect) - Lv.5

각 리뷰어는 issues, strengths, overall_score, summary를 JSON으로 반환.
"Apply this change" 버튼으로 개별 피드백 수동 적용 가능.
AI Improvement로 선택된 리뷰어 피드백 일괄 반영 가능 (이미 수동 적용된 이슈는 자동 제외).

### Frontend State (page.tsx)
- 3-step 워크플로우: Generate → Review & Improve → Publish
- ViewMode: original / improved / diff
- appliedIssues (Set) + appliedChanges (Array) 로 변경 이력 추적
- renderMarkdownWithHighlight로 리포트 렌더링 + 하이라이트

## Development Notes

- 프론트엔드 메인 코드는 `page.tsx` 단일 파일에 집중됨
- 백엔드 메인 코드는 `main.py` 단일 파일에 집중됨
- AI 응답의 JSON 파싱 실패 시 fallback 로직 있음 (빈 issues/strengths, score=5)
- "Apply this change"는 exact match → whitespace-flexible match → case-insensitive match 순서로 시도
- CORS: localhost:3000, localhost:3002 허용

## Git Branch

- `main` - 기본 브랜치
- `claude/review-report-summary-auPfX` - 현재 개발 브랜치 (리뷰 시스템 개선)
