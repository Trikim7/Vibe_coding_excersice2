"""
Seed script to populate the database with demo data.
Run with: python seed.py
Idempotent: safe to run multiple times.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
from app.database.base import SessionLocal, engine, Base
import app.models  # noqa
from app.models.user import User
from app.models.reader import Reader
from app.models.category import Category
from app.models.book_title import BookTitle
from app.models.book_copy import BookCopy
from app.models.borrow import Borrow
from app.core.security import get_password_hash

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed():
    # --- Guard: skip if already seeded ---
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Database already seeded. Skipping.")
        return

    print("Seeding database...")

    # --- Categories (5) ---
    categories = [
        Category(ma_chuyen_nganh="CNTT", ten="Cong nghe thong tin", mo_ta="Sach ve lap trinh, CNTT"),
        Category(ma_chuyen_nganh="KT",   ten="Kinh te",             mo_ta="Sach kinh te, quan tri"),
        Category(ma_chuyen_nganh="VH",   ten="Van hoc",             mo_ta="Sach van hoc Viet Nam va the gioi"),
        Category(ma_chuyen_nganh="KH",   ten="Khoa hoc tu nhien",   mo_ta="Toan, ly, hoa, sinh"),
        Category(ma_chuyen_nganh="NN",   ten="Ngoai ngu",           mo_ta="Tieng Anh, Nhat, Trung"),
    ]
    db.add_all(categories)
    db.flush()
    print(f"  Added {len(categories)} categories")

    # --- Book Titles (10) ---
    book_titles = [
        BookTitle(ma_dau_sach="DS001", ten="Lap trinh Python co ban",     nha_xuat_ban="NXB Giao duc",  so_trang=350, tac_gia="Nguyen Van A",      so_luong=5, category_id=categories[0].id),
        BookTitle(ma_dau_sach="DS002", ten="Co so du lieu",               nha_xuat_ban="NXB DH QG",     so_trang=400, tac_gia="Tran Thi B",         so_luong=4, category_id=categories[0].id),
        BookTitle(ma_dau_sach="DS003", ten="Kinh te vi mo",               nha_xuat_ban="NXB Tai chinh", so_trang=280, tac_gia="Le Van C",           so_luong=3, category_id=categories[1].id),
        BookTitle(ma_dau_sach="DS004", ten="Quan tri doanh nghiep",       nha_xuat_ban="NXB Thong ke",  so_trang=320, tac_gia="Pham Thi D",         so_luong=4, category_id=categories[1].id),
        BookTitle(ma_dau_sach="DS005", ten="Truyen Kieu",                 nha_xuat_ban="NXB Van hoc",   so_trang=200, tac_gia="Nguyen Du",          so_luong=6, category_id=categories[2].id),
        BookTitle(ma_dau_sach="DS006", ten="Dac Nhan Tam",               nha_xuat_ban="NXB Tong hop",  so_trang=320, tac_gia="Dale Carnegie",      so_luong=5, category_id=categories[2].id),
        BookTitle(ma_dau_sach="DS007", ten="Giai tich toan hoc",         nha_xuat_ban="NXB Giao duc",  so_trang=450, tac_gia="Nguyen Dinh Tri",    so_luong=3, category_id=categories[3].id),
        BookTitle(ma_dau_sach="DS008", ten="Vat ly dai cuong",           nha_xuat_ban="NXB DH QG",     so_trang=500, tac_gia="Luong Duyen Binh",   so_luong=4, category_id=categories[3].id),
        BookTitle(ma_dau_sach="DS009", ten="English Grammar in Use",      nha_xuat_ban="Cambridge",     so_trang=380, tac_gia="Raymond Murphy",     so_luong=5, category_id=categories[4].id),
        BookTitle(ma_dau_sach="DS010", ten="Tieng Nhat Buoc dau",        nha_xuat_ban="NXB Lao dong",  so_trang=280, tac_gia="Nhom tac gia",       so_luong=3, category_id=categories[4].id),
    ]
    db.add_all(book_titles)
    db.flush()
    print(f"  Added {len(book_titles)} book titles")

    # --- Book Copies (30) ---
    copies = []
    copy_counter = 1
    for bt in book_titles:
        for i in range(bt.so_luong):
            copies.append(BookCopy(
                ma_ban_sao=f"BC{copy_counter:03d}",
                dau_sach_id=bt.id,
                tinh_trang="available",
                ngay_nhap=date(2023, 1, 1) + timedelta(days=copy_counter * 3)
            ))
            copy_counter += 1
            if copy_counter > 31:
                break
        if copy_counter > 31:
            break
    db.add_all(copies)
    db.flush()
    print(f"  Added {len(copies)} book copies")

    # --- Readers (20) ---
    readers_data = [
        ("DG001", "Nguyen Minh Tuan",  "DHCNTT17A", date(2000, 3, 15),  "Nam"),
        ("DG002", "Tran Thi Hoa",      "DHKT18B",   date(2001, 5, 20),  "Nu"),
        ("DG003", "Le Quoc Hung",      "DHCNTT17B", date(2000, 7, 11),  "Nam"),
        ("DG004", "Pham Thi Lan",      "DHKT19A",   date(2002, 1, 25),  "Nu"),
        ("DG005", "Hoang Van Duc",     "DHCNTT18A", date(2001, 9, 5),   "Nam"),
        ("DG006", "Ngo Thi Mai",       "DHVH17A",   date(2000, 12, 10), "Nu"),
        ("DG007", "Vu Minh Khoa",      "DHCNTT19A", date(2002, 4, 18),  "Nam"),
        ("DG008", "Dang Thi Ngoc",     "DHKT17A",   date(1999, 8, 22),  "Nu"),
        ("DG009", "Trinh Van Long",    "DHKH18A",   date(2001, 6, 30),  "Nam"),
        ("DG010", "Bui Thi Huong",     "DHNN19B",   date(2002, 2, 14),  "Nu"),
        ("DG011", "Ly Minh Nhat",      "DHCNTT20A", date(2003, 3, 7),   "Nam"),
        ("DG012", "Duong Thi Thao",    "DHKT20B",   date(2003, 11, 19), "Nu"),
        ("DG013", "Phan Van Thang",    "DHCNTT18B", date(2001, 10, 28), "Nam"),
        ("DG014", "Cao Thi Bich",      "DHVH19A",   date(2002, 7, 3),   "Nu"),
        ("DG015", "Ho Quang Vinh",     "DHKH17B",   date(2000, 5, 16),  "Nam"),
        ("DG016", "Vo Thi Trang",      "DHNN18A",   date(2001, 8, 9),   "Nu"),
        ("DG017", "Dinh Van Hai",      "DHCNTT19B", date(2002, 1, 21),  "Nam"),
        ("DG018", "Luu Thi Kim",       "DHKT19B",   date(2002, 4, 4),   "Nu"),
        ("DG019", "Mac Van Phu",       "DHVH20A",   date(2003, 6, 13),  "Nam"),
        ("DG020", "Nong Thi Yen",      "DHNN17A",   date(1999, 12, 27), "Nu"),
    ]
    readers = []
    for ma, ten, lop, ns, gt in readers_data:
        readers.append(Reader(ma_doc_gia=ma, ho_ten=ten, lop=lop, ngay_sinh=ns, gioi_tinh=gt))
    db.add_all(readers)
    db.flush()
    print(f"  Added {len(readers)} readers")

    # --- Users (1 admin + 3 librarians) ---
    # Use short passwords to avoid any bcrypt issues
    admin = User(username="admin",      password_hash=get_password_hash("admin123"), role="admin",     full_name="Quan tri vien",        email="admin@library.iuh.edu.vn")
    lib1  = User(username="librarian1", password_hash=get_password_hash("lib123"),   role="librarian", full_name="Nguyen Thi Thu Thu",    email="thuthu1@library.iuh.edu.vn")
    lib2  = User(username="librarian2", password_hash=get_password_hash("lib123"),   role="librarian", full_name="Tran Van Thu",          email="thuthu2@library.iuh.edu.vn")
    lib3  = User(username="librarian3", password_hash=get_password_hash("lib123"),   role="librarian", full_name="Le Thi Thu Vien",       email="thuthu3@library.iuh.edu.vn")
    db.add_all([admin, lib1, lib2, lib3])
    db.flush()
    print("  Added 1 admin + 3 librarians")

    # --- Borrow Records (15) ---
    borrow_records = []
    available_copies = [c for c in copies if c.tinh_trang == "available"]

    for i in range(min(15, len(available_copies), len(readers))):
        reader = readers[i]
        copy = available_copies[i]
        borrow_date = date(2025, 1, 10) + timedelta(days=i * 5)
        is_returned = i < 10  # first 10 returned

        borrow = Borrow(
            ma_sach=copy.id,
            ma_doc_gia=reader.id,
            ma_thu_thu=lib1.id,
            ngay_muon=borrow_date,
            ngay_tra=borrow_date + timedelta(days=14) if is_returned else None,
            tinh_trang="returned" if is_returned else "active",
        )
        borrow_records.append(borrow)

        if not is_returned:
            copy.tinh_trang = "borrowed"

    db.add_all(borrow_records)
    db.commit()
    print(f"  Added {len(borrow_records)} borrow records")
    print("\nSeed completed successfully!")
    print("\nLogin credentials:")
    print("  Admin:     admin / admin123")
    print("  Librarian: librarian1 / lib123")


if __name__ == "__main__":
    try:
        seed()
    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(0)  # Exit 0 so uvicorn still starts
    finally:
        db.close()
