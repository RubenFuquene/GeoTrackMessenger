# Development Configuration for GeoTrack Messenger

## Environment Setup

### Backend Configuration
- Copy `backend/.env.example` to `backend/.env`
- Update the following variables:
  - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
  - `SECRET_KEY`: A strong secret key for JWT
  - `DATABASE_URL`: PostgreSQL connection string
  - `REDIS_URL`: Redis connection string

### Database Setup
The project uses PostgreSQL with PostGIS extension:
- Database: `geotrackmessenger_db`
- User: `geotrack_user`
- Password: `geotrack_password`
- Port: `5432`

### Redis Configuration
- Port: `6379`
- Used for caching and background tasks

## Development Workflow

### 1. Start Development Services
```bash
# Using Docker Compose (recommended)
docker-compose -f docker-compose.dev.yml up -d

# Or using setup scripts
./setup.sh      # Linux/Mac
setup.bat       # Windows
```

### 2. Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Mobile App Development
```bash
cd mobile_app
flutter pub get
flutter run
```

### 4. Telegram Bot Development
```bash
cd telegram_bot
pip install -r requirements.txt
python bot.py
```

### 5. Web Panel Development
```bash
cd web_panel
npm install
npm run dev
```

## Service URLs

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Web Panel**: http://localhost:3000
- **Database**: localhost:5432
- **Redis**: localhost:6379

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Mobile App Tests
```bash
cd mobile_app
flutter test
```

## Useful Commands

### Docker Commands
```bash
# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop all services
docker-compose -f docker-compose.dev.yml down

# Rebuild services
docker-compose -f docker-compose.dev.yml up --build

# Clean up
docker-compose -f docker-compose.dev.yml down -v
docker system prune -f
```

### Database Commands
```bash
# Connect to database
docker exec -it geotrackmessenger_db_1 psql -U geotrack_user -d geotrackmessenger_db

# Run migrations
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Backend Commands
```bash
# Run with hot reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy .
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 8000, 5432, 6379, 3000 are available
2. **Docker not starting**: Check Docker Desktop is running
3. **Database connection**: Ensure PostgreSQL service is healthy
4. **Bot not responding**: Check Telegram bot token in .env file

### Reset Development Environment
```bash
# Stop all services
docker-compose -f docker-compose.dev.yml down -v

# Remove all containers and volumes
docker system prune -a -f

# Start fresh
docker-compose -f docker-compose.dev.yml up -d
```

## Production Deployment

For production deployment, use:
```bash
docker-compose up -d
```

This includes:
- Nginx reverse proxy
- SSL termination
- Production optimizations
- Health checks
- Monitoring
