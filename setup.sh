#!/bin/bash

# GeoTrack Messenger Setup Script

set -e

echo "🚀 Setting up GeoTrack Messenger..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating environment file..."
    cp backend/.env.example backend/.env
    echo "✅ Environment file created. Please edit backend/.env with your settings."
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if backend is healthy
echo "🔍 Checking backend health..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy!"
        break
    fi
    echo "⏳ Waiting for backend... (attempt $i/30)"
    sleep 2
done

# Show status
echo "📊 Service Status:"
docker-compose -f docker-compose.dev.yml ps

echo ""
echo "🎉 GeoTrack Messenger is now running!"
echo ""
echo "📍 Access points:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo "   - Database: localhost:5432"
echo "   - Redis: localhost:6379"
echo ""
echo "📱 Next steps:"
echo "   1. Set up your Telegram bot token in backend/.env"
echo "   2. Configure the mobile app to point to your backend"
echo "   3. Install and run the web panel: cd web_panel && npm install && npm run dev"
echo ""
echo "🛑 To stop all services: docker-compose -f docker-compose.dev.yml down"
