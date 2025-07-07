# GeoTrack Messenger

A comprehensive location tracking and messaging system with support for mobile apps, web panels, and Telegram bots.

## 🏗️ Architecture

GeoTrackMessenger consists of four main components:

- **Backend API**: FastAPI-based REST API with PostgreSQL/PostGIS
- **Mobile App**: Flutter application for iOS and Android
- **Telegram Bot**: Python bot for location sharing via Telegram
- **Web Panel**: Vue.js admin panel for monitoring and management

## 🛠️ Technology Stack

| Component | Technologies |
|-----------|-------------|
| Backend | FastAPI, PostgreSQL, PostGIS, Redis, SQLAlchemy |
| Mobile App | Flutter, Dart, Google Maps |
| Telegram Bot | Python, python-telegram-bot |
| Web Panel | Vue.js, Element Plus, Leaflet |
| Infrastructure | Docker, Docker Compose, Nginx |

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for web panel development)
- Flutter SDK (for mobile app development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd GeoTrackMessenger
   ```

2. **Configure environment variables:**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your settings
   ```

3. **Start the services:**
   ```bash
   # Development mode
   docker-compose -f docker-compose.dev.yml up -d

   # Production mode
   docker-compose up -d
   ```

4. **Access the services:**
   - Backend API: http://localhost:8000
   - Web Panel: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

## 📱 Features

### Core Features
- [x] User authentication and registration
- [x] Real-time location tracking
- [x] Location history storage
- [x] Geofencing capabilities
- [x] RESTful API endpoints
- [x] Docker containerization

### Mobile App Features
- [x] GPS location tracking
- [x] Map visualization
- [x] User authentication
- [x] Location sharing
- [ ] Push notifications
- [ ] Offline mode

### Telegram Bot Features
- [x] Location sharing via Telegram
- [x] Command-based interface
- [x] Custom keyboards
- [ ] Group messaging
- [ ] Alert notifications

### Web Panel Features
- [ ] Real-time map view
- [ ] User management
- [ ] Location analytics
- [ ] Geofence management
- [ ] Dashboard with statistics

## 🐳 Docker Deployment

### Development Environment

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Production Environment

```bash
docker-compose up -d
```

## 📊 API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flutter Documentation](https://flutter.dev/docs)
- [Vue.js Documentation](https://vuejs.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostGIS Documentation](https://postgis.net/docs/)