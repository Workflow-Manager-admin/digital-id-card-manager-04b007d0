# Digital ID Card Manager – Backend API (Flask)

Flask-based REST API for managing users, authentication, and Digital ID card data.
Interfaces with a PostgreSQL database and is designed to be consumed by a React frontend.

---

**Note:** This backend supports plain user authentication only. There are **no roles, no RBAC (role-based access control), and no privilege/authorization levels** beyond simple login. All features of the backend are available to any authenticated user.

---

## 🛠 Environment Variables

Backend configuration is handled via a `.env` file in this (`id_backend_api/`) folder.

| Variable         | Purpose                                      | Example             |
|------------------|----------------------------------------------|---------------------|
| POSTGRES_URL     | Hostname/address of PostgreSQL DB            | localhost           |
| POSTGRES_USER    | DB username (see database setup)             | appuser             |
| POSTGRES_PASSWORD| DB user password (see database setup)        | dbuser123           |
| POSTGRES_DB      | Database name                                | myapp               |
| POSTGRES_PORT    | Port (default: 5000)                         | 5000                |
| SECRET_KEY       | Secret key for JWT token signing             | changeme            |

There are no environment variables for user roles or authorization—this backend uses generic, plain authentication only.

These are **required** for backend to start and connect securely to PostgreSQL!

---

## 🗄️ Database Integration

- The backend expects PostgreSQL env variables (see above).
- You must run database migrations (`schema.sql`) and create a user/DB as described in the database README.
- Environment configuration for the DB is also mirrored in `../digital-id-card-manager-e92f97cd/id_database/db_visualizer/postgres.env` (for Node.js DB tool).

---

## 🔗 Frontend Integration

- The React app calls this API at the base URL you specify (usually `http://localhost:5000`).
- CORS is enabled to allow connections from the frontend.
- JWT tokens are used for authentication – these are sent as `Authorization: Bearer ...` in request headers.

---

## 🚦 E2E Development/Deployment Steps

**1. Start the Database**
- Follow the DB container README and startup scripts.

**2. (Re)create migrations, then run the backend**
- Ensure `.env` is present and configured.
- Start the Flask backend (dev):
  ```
  export $(cat .env | xargs)
  python run.py
  ```
  Or use `flask run` with appropriate env vars.

**3. Set up and run the frontend**
- The React `.env` in the frontend must point to this backend:
  ```
  REACT_APP_API_URL=http://localhost:5000
  ```

**4. Integration Flow**
- Users sign up/login on the React app.
- React frontend calls `/auth`, `/idcards`, `/holders`, etc. here.
- Backend APIs handle business logic and DB access.

---

## 📝 API Documentation

- OpenAPI spec: `interfaces/openapi.json`
- Browse live Swagger UI at `/docs` when backend is running.

---

## 👩‍💻 Useful Scripts

- `generate_openapi.py` – Export updated OpenAPI JSON.
- Standard Python dependency management via `requirements.txt`.

---

## 👀 See Also

- Database README for schema, env vars
- Frontend README (`../id_card_frontend/`) for user/environment setup

---

