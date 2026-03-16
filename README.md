# 📚 Library Management System — IUH

Hệ thống quản lý thư viện xây dựng với **FastAPI + PostgreSQL + Docker + Static Frontend**.

> **Môn học:** Phát triển ứng dụng — HK2 2025–2026  
> **Trường:** Đại học Công nghiệp TP.HCM (IUH)

---

## 🏗️ Kiến trúc dự án

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/                 # Route handlers
│   │   ├── services/            # Business logic layer
│   │   ├── models/              # SQLAlchemy ORM models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── core/                # Config, JWT, dependencies
│   │   └── database/            # DB session & Base
│   ├── tests/                   # Pytest test suite
│   ├── alembic/                 # Database migrations
│   ├── seed.py                  # Demo data seeder
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── login.html
│   ├── dashboard.html
│   ├── readers.html
│   ├── books.html
│   ├── book-copies.html
│   ├── borrows.html
│   ├── reports.html
│   ├── users.html
│   ├── css/style.css
│   ├── js/api.js
│   └── nginx.conf
└── docker-compose.yml
```

---

## ⚡ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, SQLAlchemy |
| Database | PostgreSQL 15 |
| Auth | JWT (python-jose), Passlib bcrypt |
| Migrations | Alembic |
| Frontend | Static HTML, Vanilla JS, Fetch API |
| Container | Docker, Docker Compose |
| Web Server | Nginx (frontend), Uvicorn (backend) |
| Testing | Pytest, HTTPX |

---

## 🚀 Chạy dự án

### Khởi động bằng Docker (Khuyến nghị)

```bash
# Copy env file
cp .env.example .env

# Khởi động toàn bộ hệ thống
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

### Tài khoản mặc định (sau khi seed)

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Thủ thư | `librarian1` | `lib123` |
| Thủ thư | `librarian2` | `lib123` |

---

## 📡 API Endpoints

### Auth
```
POST /api/auth/login      # Đăng nhập → JWT token
POST /api/auth/register   # Đăng ký tài khoản
```

### Readers (Độc giả)
```
GET    /api/readers
POST   /api/readers
GET    /api/readers/{id}
PUT    /api/readers/{id}
DELETE /api/readers/{id}
```

### Book Titles (Đầu sách)
```
GET    /api/book-titles
POST   /api/book-titles
GET    /api/book-titles/{id}
PUT    /api/book-titles/{id}
DELETE /api/book-titles/{id}
GET    /api/book-titles/{id}/copies
```

### Book Copies (Bản sao)
```
CRUD   /api/book-copies
```

### Categories (Chuyên ngành)
```
CRUD   /api/categories
```

### Borrows (Mượn/Trả)
```
POST   /api/borrows               # Mượn sách
POST   /api/borrows/{id}/return   # Trả sách
GET    /api/borrows
```

### Reports (Báo cáo)
```
GET /api/reports/top-borrowed         # Top sách mượn nhiều
GET /api/reports/unreturned-readers   # Độc giả chưa trả
```

---

## 📋 Business Rules

1. Mỗi độc giả chỉ được **mượn 1 cuốn sách tại một thời điểm**
2. Thời hạn mượn mặc định: **14 ngày**
3. Trạng thái bản sao: `available` → `borrowed` → `available` (khi trả)
4. Quá hạn → trạng thái `overdue`

---

## 🗄️ Database Schema

```
users          → Admin & Librarian accounts (JWT auth)
readers        → Library members (no login)
categories     → Book specializations
book_titles    → Book catalog entries
book_copies    → Physical book instances (1 title → N copies)
borrows        → Borrow/return records
```

---

## 🧪 Chạy Tests

```bash
cd backend
pip install -r requirements.txt
pytest
```

**Test coverage:**
- ✅ Auth (login, register, duplicate check)
- ✅ Reader CRUD
- ✅ Book title & copy creation
- ✅ Borrow flow (prevent double borrow)
- ✅ Return flow
- ✅ Reports API

---

## 🌱 Seed Data

```bash
cd backend
python seed.py
```

Tạo dữ liệu mẫu:
- 5 chuyên ngành
- 10 đầu sách
- 30 bản sao sách
- 20 độc giả
- 1 admin + 3 thủ thư
- 15 phiếu mượn

---

## 🔄 Git Commit Phases

| Phase | Commit |
|---|---|
| Phase 1 | `chore(project): initialize project structure` |
| Phase 2 | `chore(docker): add docker-compose configuration` |
| Phase 3 | `feat(db): create sqlalchemy models` |
| Phase 4 | `feat(auth): implement JWT authentication` |
| Phase 5 | `feat(api): implement full CRUD endpoints` |
| Phase 6 | `feat(seed): add demo data` |
| Phase 7 | `feat(frontend): implement static HTML UI` |
| Phase 8 | `test(api): add pytest test suite` |

---

## 📄 License

MIT — IUH 2026
