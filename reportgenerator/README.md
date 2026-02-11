# Biweekly Report Generator

GitHub CSV 데이터를 기반으로 Biweekly 레포트를 생성하는 웹 애플리케이션입니다.

## 기능

- **CSV 드래그 앤 드롭 업로드**: GitHub export CSV 파일을 쉽게 업로드
- **레포트 타입 선택**:
  - **Public/Investor**: 투자자, 파트너, 커뮤니티 대상 비기술적 레포트
  - **Technical**: 개발자 대상 기술 레포트 (GitHub 링크 포함)
- **AI 요약**: Tokamak AI (OpenAI-compatible) 또는 Claude API로 요약 생성
- **레포트 분류**: Repository 기반(기본) 또는 Project 기반 선택
- **레포 제한**: 상위 N개 레포 + Other repos 묶기 지원
- **다양한 형식으로 다운로드**: MD, CSV, TSV

## 프로젝트 구조

```
ReportGenerator/
├── frontend/          # Next.js 프론트엔드
│   ├── src/app/
│   │   ├── page.tsx   # 메인 페이지
│   │   ├── layout.tsx
│   │   └── globals.css
│   └── package.json
├── backend/           # FastAPI 백엔드
│   ├── main.py
│   └── requirements.txt
└── README.md
```

## 설치 및 실행

### 1. 백엔드 설정

```bash
cd backend

# 가상환경 생성 (선택사항)
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정 (AI 기능 사용 시)
export TOKAMAK_API_KEY="your-api-key"
export TOKAMAK_BASE_URL="https://api.ai.tokamak.network"
export TOKAMAK_MODEL="gpt-5.2-pro"

# (선택) Anthropic fallback
export ANTHROPIC_API_KEY="your-claude-key"

# 서버 실행
python main.py
# 또는
uvicorn main:app --reload --port 8000
```

백엔드는 http://localhost:8000 에서 실행됩니다.

### 2. 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드는 http://localhost:3000 또는 3002 에서 실행됩니다.

## 사용법

1. http://localhost:3000 접속
2. GitHub CSV 파일을 드래그 앤 드롭으로 업로드
3. 레포트 타입 선택 (Public 또는 Technical)
4. AI 요약 옵션 설정
5. "Generate Report" 클릭
6. 결과 확인 후 원하는 형식으로 다운로드

## API 엔드포인트

### POST /api/generate

레포트 생성

**Parameters:**
- `file`: CSV 파일 (multipart/form-data)
- `report_type`: "technical" 또는 "public"
- `use_ai`: true/false
- `report_grouping`: "repository" 또는 "project"
- `repo_limit`: 0 (전체) 또는 상위 N개

**Response:**
```json
{
  "success": true,
  "report_type": "public",
  "stats": {
    "total_commits": 314,
    "total_prs": 6,
    "total_repos": 12
  },
  "highlight": "...",
  "sections": [...]
}
```

### GET /api/health

서버 상태 확인

## 환경변수

| 변수명 | 설명 | 필수 |
|--------|------|------|
| TOKAMAK_API_KEY | Tokamak AI API 키 | AI 기능 사용 시 필수 |
| TOKAMAK_BASE_URL | Tokamak API base URL | 선택 |
| TOKAMAK_MODEL | Tokamak 모델명 | 선택 |
| ANTHROPIC_API_KEY | Claude API 키 (fallback) | 선택 |
