# Coworking booking api example
Training project, aimed at practicing development methodologies and architectural patterns.
## How to start ?
1. Set all environment variables in .env
2. Use docker compose: `docker compose up`
3. Open `http://localhost:<your_port>/docs` to view api documentation
## Tech Stack
- FastAPI - web framework.
- PostgreSQL - relational database.
- Redis - cache and message broker.
- Alembic - for database migrations.
- Punq - DI container.
- SqlAlchemy - ORM.
- Taskiq - for async background tasks.
- Pydantic - data validation.
- Pydantic settings - for loading settings from .env file.
## Project structure
```
CoworkingBookApi
├── api # FastAPI routes, DI container, entrypoint
├── domain # Entities and value objects
├── infra # Repositories, cache, background tasks with broker, settings
├── logic # CQRS-style commands, queries, handlers, mediator
```
The project follows a layered architecture with CQRS-like command/query
separation and a mediator pattern for dispatching handlers. Repositories
use the Unit of Work pattern for transaction management.