
# LianSkinCare - Architecture

## Architectural Style

Modular Monolith.

## Backend Architecture

- API Layer: FastAPI endpoints
- Core Layer: Configuration and shared infrastructure
- Database Layer: SQLAlchemy and database configuration
- Modules Layer: Business domains

## Initial Backend Modules

- Authentication
- Users
- Products
- Categories
- Brands
- Cart
- Inventory
- Orders
- Reviews

## Database

PostgreSQL with SQLAlchemy 2 and Alembic.

## Architectural Principles

- Separation of Concerns
- SOLID Principles
- Domain-Driven Design where appropriate
- Database Normalization
- Dependency Injection
- Transaction Management

## Important Decisions

- One centralized warehouse
- Products can have multiple variants
- Each variant has independent SKU, price and stock
- Only registered users can place orders
- Inventory reservation is required during checkout
