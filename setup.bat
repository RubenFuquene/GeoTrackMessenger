@echo off
REM GeoTrack Messenger Setup Script for Windows

echo 🚀 Setting up GeoTrack Messenger...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist "backend\.env" (
    echo 📝 Creating environment file...
    copy "backend\.env.example" "backend\.env"
    echo ✅ Environment file created. Please edit backend\.env with your settings.
)

REM Start services
echo 🐳 Starting Docker services...
docker-compose -f docker-compose.dev.yml up -d

REM Wait for services to start
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak > nul

REM Show status
echo 📊 Service Status:
docker-compose -f docker-compose.dev.yml ps

echo.
echo 🎉 GeoTrack Messenger is now running!
echo.
echo 📍 Access points:
echo    - Backend API: http://localhost:8000
echo    - API Documentation: http://localhost:8000/docs
echo    - Database: localhost:5432
echo    - Redis: localhost:6379
echo.
echo 📱 Next steps:
echo    1. Set up your Telegram bot token in backend\.env
echo    2. Configure the mobile app to point to your backend
echo    3. Install and run the web panel: cd web_panel ^&^& npm install ^&^& npm run dev
echo.
echo 🛑 To stop all services: docker-compose -f docker-compose.dev.yml down

pause
