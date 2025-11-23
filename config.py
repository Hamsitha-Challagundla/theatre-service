"""
Configuration for Theatre Service with Google Cloud SQL
"""

import os


class Config:
    # Google Cloud SQL Database configuration (MySQL)
    # For Cloud SQL connection via Unix socket (when running on GCP):
    # mysql+pymysql://USER:PASSWORD@/DATABASE?unix_socket=/cloudsql/PROJECT:REGION:INSTANCE
    # For external/public IP connection (local development):
    # mysql+pymysql://USER:PASSWORD@PUBLIC_IP:3306/DATABASE

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://user:password@localhost:3306/theatre_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'

    # Cloud SQL connection pooling settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', '5')),
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', '1800')),
        'pool_pre_ping': True,
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', '2'))
    }

    # Application configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # External services
    MOVIE_SERVICE_URL = os.getenv('MOVIE_SERVICE_URL', 'http://localhost:8050')
    BOOKING_SERVICE_URL = os.getenv('BOOKING_SERVICE_URL', 'http://localhost:5002')
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5004')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
