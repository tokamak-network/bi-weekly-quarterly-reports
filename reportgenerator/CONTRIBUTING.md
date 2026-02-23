# Contributing to Biweekly Report Generator

Thank you for your interest in contributing!

## Getting Started

1. Fork and clone the repository
2. Set up your environment (see [README.md](README.md))
3. Create a feature branch: `git checkout -b feat/your-feature`
4. Make your changes and test locally
5. Submit a Pull Request

## Development Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Code Style

- **Python**: PEP 8, Python 3.9 compatible
- **TypeScript/React**: Functional components, hooks-based
- **Commits**: Conventional commits (`feat:`, `fix:`, `docs:`)

## Areas for Contribution

- 📊 New report formats and templates
- 🤖 AI summary quality improvements
- 🎨 Frontend UI/UX enhancements
- 📈 Additional data sources beyond GitHub CSV
- 🧪 Testing coverage
- 📖 Documentation and i18n
