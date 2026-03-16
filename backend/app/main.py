from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, readers, categories, book_titles, book_copies, borrows, reports
from app.database.base import Base, engine
import app.models  # noqa: F401 - ensure all models are imported

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    description="Hệ thống quản lý thư viện - IUH",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(readers.router)
app.include_router(categories.router)
app.include_router(book_titles.router)
app.include_router(book_copies.router)
app.include_router(borrows.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"message": "Library Management System API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
