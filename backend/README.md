# Database

```python
alembic current # Print current state of the database

alembic upgrade head # Upgrade database to the latest migration
alembic upgrade <migration-id> # Upgrade database to specific migration

alembic stamp <migration-id> # Set database version without running migrations

alembic revision --autogenerate -m "revision message" # Generate new migration
```