"""
Nebula Booking Theatre Service API

FastAPI application for managing theatres, screens, cinemas, and showtimes.
"""

import os

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

from routers import theatre_routes, screen_routes, cinema_routes, showtime_routes, health_routes


# Configuration
port = int(os.environ.get("FASTAPIPORT", 5002))

# FastAPI application
app = FastAPI(
    title="Nebula Booking Theatre Service API",
    description="FastAPI app using Pydantic v2 models for Theatre, Screen, and Cinema management",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_routes.router)
app.include_router(theatre_routes.router)
app.include_router(screen_routes.router)
app.include_router(cinema_routes.router)
app.include_router(showtime_routes.router)


@app.get("/")
def root():
    """Root endpoint with welcome message."""
    return {"message": "Welcome to the Nebula Booking Theatre Service API. See /docs for OpenAPI UI."}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Favicon endpoint to avoid noisy 404s from browsers."""
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
 
 