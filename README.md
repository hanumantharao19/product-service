# product-service
# test
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
