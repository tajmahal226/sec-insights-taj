# GitHub Copilot Instructions for SEC Insights

## Project Overview

SEC Insights is a full-stack Retrieval Augmented Generation (RAG) application that uses LlamaIndex to answer questions about SEC 10-K & 10-Q documents. The application features:

- Chat-based Document Q&A against a pool of documents
- Citation of source data with PDF viewer and highlighting
- API-based tools integration (polygon.io) for quantitative questions
- Token-level streaming of LLM responses via Server-Sent Events
- Production-ready infrastructure with Vercel and Render.com deployments

## Architecture

**Frontend:**
- Next.js 13+ with TypeScript and React
- Tailwind CSS for styling
- Located in `frontend/` directory
- Hosted on Vercel

**Backend:**
- FastAPI (Python 3.11+)
- LlamaIndex for RAG capabilities
- PostgreSQL 15 with PGVector for vector storage
- SQLAlchemy for ORM
- OpenAI (gpt-3.5-turbo + text-embedding-ada-002)
- Located in `backend/` directory
- Hosted on Render.com

**Infrastructure:**
- AWS S3 + CloudFront for document storage
- LocalStack for local S3 emulation
- Docker Compose for local development
- Arize Phoenix for LLM observability
- Sentry for monitoring and profiling

## Development Setup

### Backend Setup

**Prerequisites:**
- Python 3.11+ (managed via pyenv)
- Poetry for dependency management
- Docker and Docker Compose
- PostgreSQL 15

**Quick Start:**
```bash
cd backend
poetry shell
poetry install
cp .env.development .env
# Edit .env to add your OPENAI_API_KEY
set -a && source .env
make migrate
make run
make seed_db_local  # Optional: populate with sample data
```

**Key Backend Commands:**
- `make run` - Start backend server with Docker services (DB, LocalStack, Phoenix)
- `make run_docker` - Run everything in Docker containers
- `make migrate` - Run database migrations
- `make refresh_db` - Wipe and recreate local database
- `make seed_db_local` - Seed local DB with sample SEC filings
- `make chat` - Start REPL chat interface for testing
- `poetry run pytest` - Run backend tests
- `poetry run pylint app` - Lint backend code

**Backend File Structure:**
- `backend/app/` - Main application code
  - `app/api/` - API routes and endpoints
  - `app/models/` - Database models
  - `app/chat/` - RAG and chat logic
- `backend/tests/` - Test files
- `backend/scripts/` - Utility scripts for seeding, chat, etc.
- `backend/alembic/` - Database migrations

### Frontend Setup

**Prerequisites:**
- Node.js 18+
- npm

**Quick Start:**
```bash
cd frontend
npm install
npm run dev
```

**Key Frontend Commands:**
- `npm run dev` - Start development server (localhost:3000)
- `npm run build` - Production build
- `npm run lint` - Lint frontend code
- `npm run type-check` - TypeScript type checking

**Frontend File Structure:**
- `frontend/src/pages/` - Next.js pages
  - `index.tsx` - Landing page with document selector
  - `conversation/[id].tsx` - Chat interface with PDF viewer
- `frontend/src/components/` - React components
- `frontend/libs/` - Shared libraries and utilities

## Code Quality & Testing

### Backend
- Use `pylint` for Python linting (configuration in `pyproject.toml`)
- Use `pytest` for testing
- Follow FastAPI best practices
- Type hints are required for all functions

### Frontend
- Use ESLint for linting
- TypeScript strict mode is enabled
- Follow Next.js and React best practices
- Run `npm run build` before committing to catch TypeScript errors

## Common Development Tasks

### Adding a New API Endpoint
1. Create route handler in `backend/app/api/routers/`
2. Add route to router in appropriate file
3. Update API models in `backend/app/models/`
4. Add corresponding frontend API call in `frontend/src/` utilities
5. Run tests and update as needed

### Modifying RAG Logic
1. RAG logic is in `backend/app/chat/`
2. Query engines and tools are configured there
3. Test changes using `make chat` REPL interface
4. Monitor with Arize Phoenix at http://localhost:6006/

### Database Changes
1. Modify models in `backend/app/models/`
2. Create migration: `poetry run alembic revision --autogenerate -m "description"`
3. Review generated migration in `backend/alembic/versions/`
4. Apply migration: `make migrate`
5. Test with `make refresh_db` for clean slate

### Adding Dependencies

**Backend:**
```bash
cd backend
poetry add <package-name>
poetry lock
```

**Frontend:**
```bash
cd frontend
npm install <package-name>
```

## Environment Variables

### Backend (.env)
Required variables (see `.env.development` for template):
- `OPENAI_API_KEY` - OpenAI API key
- `DATABASE_URL` - PostgreSQL connection string
- `S3_ASSET_BUCKET_NAME` - S3 bucket for documents
- `AWS_KEY` / `AWS_SECRET` - AWS credentials
- `POLYGON_IO_API_KEY` - Polygon.io API key (optional)
- `SEC_EDGAR_COMPANY_NAME` / `SEC_EDGAR_EMAIL` - SEC compliance info

### Frontend
- `NEXT_PUBLIC_BACKEND_URL` - Backend API URL

## Deployment

### Frontend (Vercel)
- Automatic deployments on push to `main`
- Preview deployments for PRs
- Set `NEXT_PUBLIC_BACKEND_URL` in Vercel settings

### Backend (Render.com)
- Automatic deployments on push to `main`
- Configuration in `render.yaml`
- Set environment variables in Render dashboard

## Troubleshooting

- Check `backend/troubleshooting.md` for backend issues
- Review FAQ.md for common questions
- Check open/closed GitHub issues
- Join #sec-insights Discord channel

## Important Notes

- **Do not commit secrets** - Use environment variables
- **Test locally before pushing** - Run both backend and frontend tests
- **Follow the existing code patterns** - Consistency is important
- **Update documentation** - Keep README files and this file up to date
- **SEC Compliance** - When downloading SEC filings, always set proper `SEC_EDGAR_COMPANY_NAME` and `SEC_EDGAR_EMAIL` in `.env` per [SEC's Internet Security Policy](https://www.sec.gov/os/webmaster-faq#code-support)

## Best Practices for Issues

When creating issues for Copilot coding agent:
- Be specific about the problem and expected behavior
- Include file paths that need to be changed
- Specify acceptance criteria (e.g., "should include unit tests")
- For bugs, include steps to reproduce
- Label appropriately (bug, enhancement, documentation, etc.)

## Suitable Tasks for Copilot

**Good tasks:**
- Bug fixes with clear reproduction steps
- Adding test coverage for existing functionality
- Documentation updates
- Code cleanup and technical debt
- Adding new API endpoints with clear specifications
- UI component updates with specific requirements

**Tasks requiring human review:**
- Complex RAG logic changes
- Security-sensitive modifications
- Database schema migrations
- Deployment configuration changes
- Third-party API integrations
