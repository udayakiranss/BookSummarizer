# Book-Insight

A FastAPI-based application for AI-powered book analysis and insights. Built with modern Python tooling including UV for fast dependency management.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- ⚡ **UV** - Ultra-fast Python package manager
- 🐳 **Docker** - Containerized deployment ready
- 🔧 **Environment Configuration** - Secure environment variable management
- 📚 **AI Integration** - OpenAI API integration ready
- 🗄️ **Database Support** - SQLAlchemy ORM with SQLite/PostgreSQL support

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- OpenAI API key (optional for basic endpoints)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Book-Insight
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Run the application**
   ```bash
   uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### API Endpoints

- **Health Check**: `GET /health`
- **Ping**: `GET /api/ping`
- **API Documentation**: `GET /docs` (Interactive Swagger UI)

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Project Structure

```
Book-Insight/
├── api/                    # API routes
│   └── routes.py
├── config/                 # Configuration
│   └── config.py
├── data/                   # Database files (ignored by git)
├── main.py                 # FastAPI application entry point
├── pyproject.toml          # UV project configuration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Development

### Adding New Features

1. Create new API routes in `api/routes.py`
2. Add database models in `config/config.py`
3. Update environment variables in `.env.example`
4. Test endpoints using the interactive docs at `/docs`

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for AI features | Required |
| `DB_URL` | Database connection string | `sqlite:///./data/app.db` |
| `HOST` | Server host | `127.0.0.1` |
| `PORT` | Server port | `8000` |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.