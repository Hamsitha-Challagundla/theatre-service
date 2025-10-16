# Nebula Booking Theatre Service

A microservice for managing theatres, screens, movies, and showtimes in the Nebula Booking system.

## Overview

This service provides CRUD operations for:
- **Theatres**: Physical locations where movies are shown
- **Screens**: Individual screens within theatres
- **Movies**: Film information and metadata
- **Showtimes**: Specific movie showings with dates, times, and pricing

## API Endpoints

### Health Check
- `GET /health` - Basic health check
- `GET /health/{path_echo}` - Health check with path parameter

### Theatres
- `POST /theatres` - Create a new theatre
- `GET /theatres` - List all theatres (with filtering)
- `GET /theatres/{theatre_id}` - Get specific theatre
- `PATCH /theatres/{theatre_id}` - Update theatre (partial)
- `PUT /theatres/{theatre_id}` - Replace theatre (complete)
- `DELETE /theatres/{theatre_id}` - Delete theatre

### Screens
- `POST /screens` - Create a new screen
- `GET /screens` - List all screens (with filtering)
- `GET /screens/{screen_id}` - Get specific screen
- `PATCH /screens/{screen_id}` - Update screen (partial)
- `PUT /screens/{screen_id}` - Replace screen (complete)
- `DELETE /screens/{screen_id}` - Delete screen

### Movies
- `POST /movies` - Create a new movie
- `GET /movies` - List all movies (with filtering)
- `GET /movies/{movie_id}` - Get specific movie
- `PATCH /movies/{movie_id}` - Update movie (partial)
- `PUT /movies/{movie_id}` - Replace movie (complete)
- `DELETE /movies/{movie_id}` - Delete movie

### Showtimes
- `POST /showtimes` - Create a new showtime
- `GET /showtimes` - List all showtimes (with filtering)
- `GET /showtimes/{showtime_id}` - Get specific showtime
- `PATCH /showtimes/{showtime_id}` - Update showtime (partial)
- `PUT /showtimes/{showtime_id}` - Replace showtime (complete)
- `DELETE /showtimes/{showtime_id}` - Delete showtime

## Data Models

### Theatre
- Basic information: name, address, contact details
- Location: city, state, postal code, country
- Capacity and operational status

### Screen
- Associated with a theatre
- Screen number, name, capacity
- Screen type (IMAX, 3D, Standard, etc.)
- Active status

### Movie
- Title, description, genre
- Duration, release date, rating
- Director and cast information
- Active status

### Showtime
- Links theatre, screen, and movie
- Show date and time
- Pricing and seat availability
- Active status

## Running the Service

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the service:
   ```bash
   python main.py
   ```

3. Access the API documentation:
   - Swagger UI: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

## Configuration

- Default port: 8001 (configurable via FASTAPIPORT environment variable)
- All endpoints currently return "NOT IMPLEMENTED" (501 status code)
- Ready for implementation of actual business logic

## OpenAPI Documentation

The service automatically generates OpenAPI 3.0 documentation that can be accessed at `/docs` (Swagger UI) or `/redoc` (ReDoc). This provides interactive API documentation and testing capabilities.
