-- Initialize PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create test database
CREATE DATABASE geotrackmessenger_test_db WITH OWNER = geotrack_user;

-- Connect to test database and enable PostGIS
\c geotrackmessenger_test_db
CREATE EXTENSION IF NOT EXISTS postgis;
