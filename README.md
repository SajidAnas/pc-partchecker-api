# PC Part Checker API

PC Part Checker API is a microservice built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Docker Compose**.  
It allows users to register/login, add PC parts, create PC builds, and validate hardware compatibility.

---

## Features

- **Authentication**
  - Register and login using email + password
  - JWT-based token authentication

- **PC Parts Management**
  - Add and list CPUs, Motherboards, RAM Kits, GPUs, PSUs, and Cases
  - Paginated listing for large inventories

- **Build Validation**
  - Create builds by combining parts
  - Validate compatibility (CPU ↔ Motherboard socket, RAM type, PSU wattage, GPU size vs. case, etc.)

- **API Documentation**
  - Interactive Swagger UI at `/docs`
  - ReDoc at `/redoc`

- **Testing**
  - Unit tests with **PyTest**
  - Load testing with **Locust**

- **CI/CD Ready**
  - GitHub Actions for linting and testing

---

## Tech Stack

- **FastAPI** – Web framework for APIs
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM for database models
- **Docker Compose** – Container orchestration
- **PyTest** – Unit testing
- **Locust** – Load testing

---

## Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop) with WSL2 enabled (Windows)
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/pc-partchecker-api.git
   cd pc-partchecker-api
   ```

2. Copy environment file and start containers:
   ```bash
   cp .env.example .env # Make necessary edits
   docker compose up --build
   ```

3. Access services:
   - API: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Locust UI: [http://localhost:8089](http://localhost:8089)

---

## Usage

### Register a User
```bash
POST /auth/register
{
  "email": "user@example.com",
  "password": "securepass"
}
```

### Login to Get Token
```bash
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepass"
}
```
Response includes a JWT token for authentication.

### Add a Part
```bash
POST /parts/cpus
Authorization: Bearer <token>
{
  "name": "Ryzen 5 5600X",
  "socket": "AM4",
  "tdp_w": 65
}
```

### Create a Build
```bash
POST /builds/
Authorization: Bearer <token>
{
  "cpu_id": 1,
  "motherboard_id": 2,
  "ramkit_id": 3,
  "gpu_id": 4,
  "psu_id": 5,
  "case_id": 6
}
```

### Validate a Build
```bash
GET /builds/{id}/validate
Authorization: Bearer <token>
```

---

## Running Tests

### Unit Tests
```bash
docker compose exec app pytest -q
```

### Load Tests
1. Open [http://localhost:8089](http://localhost:8089)
2. Configure number of users and spawn rate
3. Start the test to simulate concurrent load

---

## Project Structure

```
pc-partchecker-api/
│── app/
│   ├── api/        # Routes
│   ├── core/       # Config & security
│   ├── db/         # Database models & session
│   ├── schemas/    # Pydantic schemas
│   ├── tests/      # PyTest tests
│   └── main.py     # FastAPI entrypoint
│── scripts/
│   ├── loadtest/        # Locust load tests
│── docker-compose.yml
│── Dockerfile
│── requirements.txt
│── locustfile.py
│── README.md
```

---

## Future Improvements

- Add storage and cooling compatibility checks
- Implement user-owned saved builds with sharing
- Make a simple front end for non-technical users
- Deploy to cloud with CI/CD pipeline

---
