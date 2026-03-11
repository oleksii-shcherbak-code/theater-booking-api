# 🎭 Theater Booking API

Theater Booking API is a RESTful backend service built with **Django** and **Django REST Framework** for managing theatrical plays, performance schedules, and ticket bookings.

Authentication is implemented using **JWT**.  
The project follows **Clean Architecture principles** with a clear separation of concerns and production‑ready admin configuration.

---

## 🚀 Features

### 🔐 Authentication
- JWT authentication (access / refresh tokens)
- Custom user model (email as login)
- Endpoint for retrieving the current authenticated user

### 🎭 Plays
- CRUD operations for plays
- Relations with genres and actors
- Creation and modification restricted to administrators

### 📅 Schedule
- Theatre halls
- Performances
- Unique performance per hall and start time
- Management restricted to administrators

### 🎟 Booking
- Booking creation (cart‑like behavior)
- Ticket creation inside bookings
- Seat availability enforced at database level
- Booking confirmation
- Confirmed bookings become immutable

---

## 🧱 Architecture

Each domain application follows a consistent structure:

- `models.py` — data models
- `serializers.py` — validation and representation
- `views.py` — API endpoints
- `services.py` — business logic
- `selectors.py` — optimized read‑only queries
- `permissions.py` — access rules
- `urls.py` — routing

### Service Layer
All business logic is encapsulated in services:
- `create_booking`
- `add_ticket_to_booking`
- `confirm_booking`
- `create_play`
- `create_performance`

### Selectors
Selectors are used to:
- optimize database queries
- apply `select_related` / `prefetch_related`
- strictly separate read and write operations

---

## 🏁 Project Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---


### 🔐 JWT Authentication

### Demo User for API Testing

A demo user is already created for testing purposes:

```
Email: test@gmail.com
Password: test123
```

### Obtain JWT Tokens

```http
POST /api/auth/login/
Content-Type: application/json
```

```json
{
  "email": "test@gmail.com",
  "password": "test123"
}
```

### Use Access Token

```http
Authorization: Bearer <access_token>
```

### Refresh Access Token

```http
POST /api/auth/refresh/
Content-Type: application/json
```

```json
{
  "refresh": "<refresh_token>"
}
```

---

## 📚 API Endpoints

### 👤 Users

```http
GET /api/users/me/
```

### 🎭 Plays

```http
GET    /api/plays/
GET    /api/plays/{id}/
POST   /api/plays/            (admin only)
PATCH  /api/plays/{id}/       (admin only)
DELETE /api/plays/{id}/       (admin only)
```

### 📅 Performances

```http
GET    /api/performances/
GET    /api/performances/{id}/
POST   /api/performances/            (admin only)
PATCH  /api/performances/{id}/       (admin only)
DELETE /api/performances/{id}/       (admin only)
```

### 🎟 Bookings

```http
GET    /api/bookings/                 (current user only)
POST   /api/bookings/

POST   /api/bookings/{id}/add_ticket/
POST   /api/bookings/{id}/confirm/
```

---

## 🧑‍💼 Admin Panel

```http
/admin/
```

Admin interface includes:

- Inline ticket management inside bookings
- Autocomplete fields for related models
- Ticket count and total price calculation
- Admin action for booking confirmation
- Protection against modifying confirmed bookings

---

## 📖 API Documentation

### Swagger UI

```http
/api/docs/
```

---

## 🧪 Testing

```bash
pytest
```