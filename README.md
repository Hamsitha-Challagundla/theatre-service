# Blue Cloud Theatre Service

A microservice for managing theatres, screens, movies, and showtimes in the Blue Cloud Theatre Booking system.

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

## 🗄️ Database

Uses **Google Cloud SQL (MySQL)** with the following tables:

- **theatres** - Theatre locations and information
- **screens** - Individual screens within theatres
- **cinemas** - Cinema chains/organizations
- **showtimes** - Movie showtimes with pricing

## 🔄 ETag Support

All resources support ETags for optimistic concurrency control:

- **GET** requests return `ETag` header
- **PATCH/PUT/DELETE** require `If-Match` header with current ETag
- **GET** with `If-None-Match` returns 304 Not Modified if unchanged

Example:
```bash
# Get resource (returns ETag)
GET /theatres/1
ETag: "abc123"

# Update with ETag (prevents conflicts)
PATCH /theatres/1
If-Match: "abc123"
```

## ⚙️ Configuration

Environment variables:
```bash
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
DB_NAME=your_db_name
FASTAPIPORT=5002
```

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
   - Swagger UI: http://localhost:5002/docs
   - ReDoc: http://localhost:5002/redoc

## Configuration

- Default port: 5002 (configurable via FASTAPIPORT environment variable)
- Database: Google Cloud SQL (MySQL)
- ETag support for conditional requests (If-Match, If-None-Match headers)

## 📚 OpenAPI Documentation

The service automatically generates OpenAPI 3.0 documentation that can be accessed at `/docs` (Swagger UI) or `/redoc` (ReDoc). This provides interactive API documentation and testing capabilities.

## 🧪 Testing

### Using Swagger UI
1. Go to http://localhost:5002/docs
2. Click any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Using cURL

```bash
# Create cinema (201 Created)
curl -i -X POST http://localhost:5002/cinemas \
  -H "Content-Type: application/json" \
  -d '{"name": "AMC Theatres"}'

# Create theatre (201 Created)
curl -i -X POST http://localhost:5002/theatres \
  -H "Content-Type: application/json" \
  -d '{
    "cinema_id": 1,
    "name": "AMC Empire 25",
    "address": "234 W 42nd St, New York, NY"
  }'

# Create screen (201 Created)
curl -i -X POST http://localhost:5002/screens \
  -H "Content-Type: application/json" \
  -d '{
    "theatre_id": 1,
    "screen_number": 1,
    "num_rows": 10,
    "num_cols": 15
  }'
```

## 🚀 Deployment

### Local Development
```bash
python main.py
# or
uvicorn main:app --reload --port 5002
```


---

**Built with FastAPI** 🚀 | **Version 0.1.0** | **Python 3.11+**
