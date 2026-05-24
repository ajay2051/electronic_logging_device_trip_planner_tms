# FleetPulse TMS — Backend

An FMCSA-compliant ELD trip planning and trucking management API built with **Django + Django REST Framework**.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | Django + Django REST Framework |
| Database | PostgreSQL (default) + PostGIS (GIS/spatial) |
| Auth | JWT (Simple JWT) |
| Task Queue | Celery + Redis |
| Task Monitor | Flower |
| Email | Django Email (password reset, verification) |

---

## Environment Setup

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/fleetpulse
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.your-provider.com
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=your-email-password
```

---

## Installation & Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --database=default
python manage.py migrate --database=gis

# Start dev server
python manage.py runserver

# Start Celery worker
celery -A project worker --loglevel=INFO

# Start Flower (task monitor)
celery -A project worker flower
```

---

## API Endpoints

| Method | URL | Description | Auth |
|---|---|---|---|
| `POST` | `/api/v1/auth/login/` | Login, returns JWT | ✗ |
| `POST` | `/api/v1/auth/create_users/` | Register new user | ✗ |
| `GET` | `/api/v1/auth/verify_users/:id/:token/` | Email verification | ✗ |
| `POST` | `/api/v1/auth/forgot-password/` | Request password reset | ✗ |
| `PUT` | `/api/v1/auth/forgot-password-confirm/:user_id/:token/` | Confirm new password | ✗ |
| `GET` | `/api/v1/auth/list_users/` | List all users | ✓ Admin |
| `POST` | `/api/v1/route/create/` | Save a planned route | ✓ Driver |
| `GET` | `/api/v1/route/list/` | List all routes | ✓ Admin |
| `POST` | `/api/v1/log/create/` | Submit driver log(s) | ✓ Driver |
| `GET` | `/api/v1/log/list/` | List all driver logs | ✓ Admin |

---

## Authentication Flow

1. Register → verification email sent automatically
2. User clicks the link in the email → account activated
3. Login returns `access_token` + user info
4. All protected routes require `Authorization: Bearer <token>`
5. Expired tokens return `401 token_not_valid`

### Roles

| Role | Access |
|---|---|
| `driver` | Create routes, submit logs |
| `admin` | Full read access to all routes, logs, users |

---

## Key Models

- **User** — role-based (`driver` / `admin`), email-verified
- **Route** — GeoJSON pickup/dropoff locations with distance + ETA
- **Driverlog** — FMCSA daily log fields, FK to Route, supports bulk create (`many=True`)

---

## Notes

- `/log/create/` accepts an **array** of log objects — always send as a list even for a single entry
- Routes store coordinates in GeoJSON `[lng, lat]` order (PostGIS standard)
- Password reset tokens are single-use and delivered via email link with `?user_id=&token=` params