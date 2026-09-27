# Blog API — Django Version

The same Blog API as [blog-api (Node/Express)](https://github.com/Shaffizy/blog-api), rebuilt in **Django + Django REST Framework**, using the same MySQL schema and the same seed data — hosted on the same Aiven database — so both approaches can be compared directly on identical data.

## Tech Stack

- Python + Django
- Django REST Framework (DRF)
- MySQL (hosted on Aiven, shared with the Express version)

## Data Model

Both tables already exist in the shared Aiven database (created originally for the Express version). Django's models describe these existing tables using `managed = False` — Django reads/writes to them but never creates, alters, or drops them.

**users**
| Field | Type | Notes |
|------------|--------------|-------------------|
| id | INT | Primary key |
| username | VARCHAR(50) | Unique |
| email | VARCHAR(100) | Unique |
| password | VARCHAR(255) | Plain text for now — hashing planned |
| created_at | TIMESTAMP | Auto-set |

**posts**
| Field | Type | Notes |
|------------|-----------|----------------------------------|
| id | INT | Primary key |
| user_id | INT | Foreign key → users.id |
| title | VARCHAR(200) | |
| content | TEXT | |
| created_at | TIMESTAMP | Auto-set |

## Endpoints

### `POST /users/`

Register a new user.

**Body:**

```json
{ "username": "jane", "email": "jane@test.com", "password": "1234" }
```

**Response — 201:**

```json
{ "id": 16, "username": "jane", "email": "jane@test.com" }
```

**Response — 400:** validation errors (missing fields, duplicate username/email), handled automatically by DRF's serializer.

---

### `GET /posts/`

List posts, newest first, with the author's username joined in. Paginated automatically by DRF.

**Query params:**
| Param | Type | Default | Description |
|-------|------|---------|-----------------|
| page | int | 1 | Page number |

**Example:** `GET /posts/?page=2`

**Response — 200:**

```json
{
  "count": 53,
  "next": "http://127.0.0.1:8000/posts/?page=3",
  "previous": "http://127.0.0.1:8000/posts/?page=1",
  "results": [
    {
      "id": 44,
      "user": 8,
      "username": "noahtaylor8",
      "title": "...",
      "content": "...",
      "created_at": "..."
    }
  ]
}
```

---

### `POST /posts/`

Create a post for an existing user.

**Body:**

```json
{ "user": 1, "title": "My Post", "content": "Hello world" }
```

**Response — 201:**

```json
{
  "id": 54,
  "user": 1,
  "username": "noahokafor1",
  "title": "My Post",
  "content": "Hello world",
  "created_at": "..."
}
```

**Response — 400:** missing fields, handled automatically by DRF's serializer.

---

### `GET /posts/<id>/`

Get a single post by ID, with author's username.

**Response — 200:** same shape as one item in `/posts/` results.
**Response — 404:** `{ "detail": "Not found." }`

---

### `PATCH /posts/<id>/`

Update a post's title and/or content.

**Body (either or both fields):**

```json
{ "title": "Updated title" }
```

**Response — 200:** the full updated post object.

---

### `DELETE /posts/<id>/`

Delete a post.

**Response — 204:** No content (Django convention — success with an empty body).

## Comparison Notes: Express vs Django

| Concept               | Express (blog-api)                    | Django (this repo)                             |
| --------------------- | ------------------------------------- | ---------------------------------------------- |
| Table definitions     | Raw SQL in `schema.sql`               | Python classes in `models.py`                  |
| Response shaping      | Manual, inline per route (`res.json`) | Reusable `serializers.py`, defined once        |
| Request handling      | Function per route in `index.js`      | Class-based views in `views.py`                |
| URL routing           | Inline with route definitions         | Separate `urls.py` mapping file                |
| JOIN (author on post) | Manual SQL `JOIN`                     | `select_related('user')` — ORM writes the JOIN |
| Pagination            | Manual `LIMIT`/`OFFSET` math          | Automatic via `PageNumberPagination`           |
| Input validation      | Manual `if` checks per field          | Automatic via serializer field rules           |

## Running Locally

1. Clone the repo
2. Create and activate a virtual environment:
