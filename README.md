# E-Commerce Product Service

A Python FastAPI microservice that manages product information using PostgreSQL and SQLAlchemy.

## 1. Technology Stack

- Python
- FastAPI
- Uvicorn
- PostgreSQL 18
- SQLAlchemy
- Pydantic
- Docker
- Kubernetes

## 2. Project Structure

```text
product-service/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       └── products.py
├── .env
├── .gitignore
├── .dockerignore
├── Dockerfile
├── requirements.txt
├── deployment.yaml
├── service.yaml
└── README.md
```

## 3. Prerequisites

Install the following software:

- Python 3.10 or later, compatible with the project dependencies
- PostgreSQL
- Git
- Visual Studio Code (optional)

Verify the installations:

```bash
python --version
git --version
```

On Windows PowerShell, check the PostgreSQL service:

```powershell
Get-Service *postgres*
```

Check whether PostgreSQL is accepting connections:

```powershell
Test-NetConnection localhost -Port 5432
```

If PostgreSQL is running on port `5432`, `TcpTestSucceeded` should be `True`.

## 4. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd product-service
```

Replace `<YOUR_REPOSITORY_URL>` with your actual Git repository URL.

## 5. Verify PostgreSQL and the Database

The application uses the `product_db` database.

Open PowerShell and connect using the PostgreSQL command-line client:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5432 -U postgres -d product_db
```

Enter your PostgreSQL password when prompted.

Check the current database and tables:

```sql
SELECT current_database();
\dt
SELECT * FROM products LIMIT 10;
```

Exit PostgreSQL:

```sql
\q
```

If the database or table does not exist on a new machine, create and configure it according to your application's database setup before starting the service. Do not recreate an existing database unnecessarily.

## 6. Create a Python Virtual Environment

From the project root, run:

```bash
python -m venv venv
```

Activate the virtual environment in Git Bash on Windows:

```bash
source venv/Scripts/activate
```

Verify Python:

```bash
python --version
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install python-dotenv
```

The `python-dotenv` package is required because `app/database.py` uses `load_dotenv()`.

## 7. Configure Environment Variables

Create a `.env` file in the project root:

```bash
touch .env
```

Open it in Notepad:

```bash
notepad .env
```

Add your database connection string:

```dotenv
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_ENCODED_PASSWORD@localhost:5432/product_db
```

Replace `YOUR_ENCODED_PASSWORD` with your actual PostgreSQL password, URL-encoding special characters as required.

For example, `@` inside the password must be encoded as `%40`.

**Security guidelines:**

- Never commit `.env` to Git.
- Never hardcode database passwords in Python files.
- Use environment variables or a secret manager for production deployments.
- Keep `.env` excluded in `.gitignore`.

Example `.gitignore` entries:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

## 8. Start the FastAPI Application

Ensure you are in the project root and the virtual environment is activated.

Run:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Explanation:

- `app.main` refers to `app/main.py`.
- `app` is the FastAPI application instance.
- `--reload` automatically restarts the server during local development.
- `--port 8001` starts the API on port 8001.

Keep the terminal open while the service is running.

## 9. Verify the Application

Open these URLs in your browser.

| Endpoint | Purpose |
|---|---|
| http://127.0.0.1:8001/health | Checks application health |
| http://127.0.0.1:8001/ready | Checks database connectivity |
| http://127.0.0.1:8001/docs | Opens interactive Swagger API documentation |

Expected health response:

```json
{
  "status": "healthy",
  "service": "product-service"
}
```

Expected readiness response:

```json
{
  "status": "ready",
  "database": "connected"
}
```

## 10. Test Product APIs

Open Swagger:

http://127.0.0.1:8001/docs

Use the available product endpoints to test operations such as:

- Create a product
- Retrieve products
- Retrieve a product by ID
- Update a product, if implemented
- Delete a product, if implemented

Use the actual routes defined in `app/routes/products.py`.

After creating a product, verify that it is saved in PostgreSQL:

```sql
SELECT * FROM products;
```

## 11. Stop the Application

Press:

```text
CTRL + C
```

Deactivate the Python virtual environment:

```bash
deactivate
```

## 12. Troubleshooting

### Error: `psql: command not found`

On Windows, use the full path to the PostgreSQL client:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" --version
```

### Error: `DATABASE_URL is not set`

Verify that `.env` exists in the project root and contains the `DATABASE_URL` variable.

### Error: `ModuleNotFoundError`

Activate the virtual environment and install dependencies:

```bash
source venv/Scripts/activate
python -m pip install -r requirements.txt
python -m pip install python-dotenv
```

### Error: Database connection refused

Check the PostgreSQL Windows service and port:

```powershell
Get-Service *postgres*
Test-NetConnection localhost -Port 5432
```

### Error: Password authentication failed

Verify the database username, password, hostname, port, and URL encoding of special characters. Do not reset the password unless necessary.

### Error: Port 8001 is already in use

Run the service on another port temporarily:

```bash
python -m uvicorn app.main:app --reload --port 8002
```

Use the new port when testing the endpoints.

## 13. Run with Docker

Build the image:

```bash
docker build -t product-service:1.0 .
```

When running in Docker, `localhost` inside the container refers to the container itself, not your Windows host. Configure the database hostname appropriately for your Docker networking setup and provide `DATABASE_URL` through an environment variable or secret.

Example for a database host reachable as `host.docker.internal`:

```bash
docker run --rm -p 8001:8001 --env-file .env product-service:1.0
```

This example assumes PostgreSQL is reachable from the container using the hostname configured in `.env`.

## 14. Application Architecture

```text
Client / Frontend
       |
       v
FastAPI Product Service
       |
       v
SQLAlchemy ORM
       |
       v
PostgreSQL Database
       |
       v
product_db.products
```

The FastAPI service exposes HTTP endpoints, validates request data with Pydantic, uses SQLAlchemy to interact with PostgreSQL, and returns product information to clients.

## 15. Important Notes

- Keep the existing database and its data when restarting the service.
- Do not commit passwords or other secrets.
- Use `--reload` only for local development.
- Use appropriate secret management and production server settings when deploying.
- Database schema creation in application startup is suitable for simple development projects; use database migrations such as Alembic as the project grows.





# product-service
## Database Configuration

The `product-service` uses the `DATABASE_URL` environment variable.

### 1. Local PostgreSQL

When PostgreSQL is running on the local laptop and the application is running in Kind/Docker:

```yaml
env:
  - name: DATABASE_URL
    value: "postgresql://postgres:<PASSWORD>@host.docker.internal:5432/product_db"
```

Example:

```text
host.docker.internal:5432
```

`host.docker.internal` allows the container/Kind environment to connect to PostgreSQL running on the local laptop.

---

### 2. AWS RDS PostgreSQL

When using PostgreSQL in AWS RDS:

```yaml
env:
  - name: DATABASE_URL
    value: "postgresql://postgres:<PASSWORD>@<RDS_ENDPOINT>:5432/product_db"
```

Example:

```text
postgresql://postgres:<PASSWORD>@product-product-dev-rds.xxxxxxxxx.us-east-1.rds.amazonaws.com:5432/product_db
```

Get the RDS endpoint using:

```bash
terraform output db_endpoint
```

### Difference

```text
Local PostgreSQL:
host.docker.internal:5432

AWS RDS:
<RDS_ENDPOINT>:5432
```

The application code does not change. Only the `DATABASE_URL` changes.

> **Security:** Do not commit the real database password in `deployment.yaml` or Git. Use Kubernetes Secrets or AWS Secrets Manager for credentials.
