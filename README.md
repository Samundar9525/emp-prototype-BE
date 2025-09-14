# Docker Setup

This backend is containerized using Docker and can be run as part of the full-stack application using Docker Compose.

## Prerequisites
- Docker installed on your system
- Docker Compose installed

## Running with Docker Compose

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd django-postgres
   ```

2. **Build and start the services**:
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL database (port 5432)
   - Django backend (port 8000)
   - Angular frontend (port 4200)
   - Nginx proxy (port 80)

3. **Access the application**:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:4200 or http://localhost (via Nginx)
   - Admin panel: http://localhost:8000/admin

4. **Database initialization**:
   The database will be automatically created and migrated when the containers start. Sample data can be loaded using the management commands inside the backend container.

## Backend Docker Details

The backend uses a multi-stage Dockerfile that:
- Uses Python 3.12 slim image
- Installs system dependencies (gcc)
- Installs Python dependencies from `requirements.txt`
- Creates a non-root user for security
- Collects static files
- Runs with Gunicorn for production

### Environment Variables
The backend uses environment variables defined in `.env`:
- Database connection settings
- Django settings (DEBUG, SECRET_KEY, etc.)
- JWT token lifetimes
- CORS settings

### Management Commands
To run Django management commands in the backend container:
```bash
docker-compose exec backend python manage.py <command>
```

For example, to load sample data:
```bash
docker-compose exec backend python manage.py loaddata <fixture>
```

## Stopping the Services
```bash
docker-compose down
```

To also remove volumes (including database data):
```bash
docker-compose down -v
```

# Loading sample database in postgres
To initialize the database in postgres run the following command
- point to the database directory
- psql -U username -c "CREATE DATABASE employee"
- psql -U username employee < employee.sql

Provide the password of your postgres the ERD diagram is shown below with (including django migrated tables)
# Schema 
<img width="1829" height="966" alt="image" src="https://github.com/user-attachments/assets/5fb08cb0-f298-430c-a76c-76c61bd93949" />


# Admin Panel :
- Adding employee
<img width="1605" height="811" alt="image" src="https://github.com/user-attachments/assets/b922066e-1446-4f1c-adce-8fed19aa65ca" />
- View Employee 
<img width="1920" height="848" alt="image" src="https://github.com/user-attachments/assets/07571d5e-c0f7-4db2-8205-da1c9159d8f9" />
- Addding View 
<img width="1906" height="873" alt="{CB7EF089-EC8E-492A-A938-46687EF70AE1}" src="https://github.com/user-attachments/assets/dcd124b3-be30-4ffb-8e58-64e070ce94b5" />

and so on ...



