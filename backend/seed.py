"""
Seed script to populate the database with demo data.
Run with: python seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, timedelta
import uuid
from app.database.base import SessionLocal, engine, Base
import app.models  # noqa
from app.models.user import User
from app.models.reader import Reader
from app.models.category import Category
from app.models.book_title import BookTitle
from app.models.book_copy import BookCopy
from app.models.borrow import Borrow
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed():
    print("Seeding database...")

    # --- Categories (5) ---
    categories = [
        Category(ma_chuyen_nganh="CNTT", ten="Công nghệ thông tin", mo_ta="Sách về lập trình, CNTT"),
        Category(ma_chuyen_nganh="KT", ten="Kinh tế", mo_ta="Sách kinh tế, quản trị"),
        Category(ma_chuyen_nganh="VH", ten="Văn học", mo_ta="Sách văn học Việt Nam và thế giới"),
        Category(ma_chuyen_nganh="KH", ten="Khoa học tự nhiên", mo_ta="Toán, lý, hóa, sinh"),
        Category(ma_chuyen_nganh="NN", ten="Ngoại ngữ", mo_ta="Tiếng Anh, Nhật, Trung"),
    ]
    db.add_all(categories)
    db.flush()
    print(f"  Added {len(categories)} categories")

    # --- Book Titles (10) ---
    book_titles = [
        BookTitle(ma_dau_sach="DS001", ten="Lập trình Python cơ bản", nha_xuat_ban="NXB Giáo dục", so_trang=350, tac_gia="Nguyễn Văn A", so_luong=5, category_id=categories[0].id),
        BookTitle(ma_dau_sach="DS002", ten="Cơ sở dữ liệu", nha_xuat_ban="NXB ĐH QG", so_trang=400, tac_gia="Trần Thị B", so_luong=4, category_id=categories[0].id),
        BookTitle(ma_dau_sach="DS003", ten="Kinh tế vi mô", nha_xuat_ban="NXB Tài chính", so_trang=280, tac_gia="Lê Văn C", so_luong=3, category_id=categories[1].id),
        BookTitle(ma_dau_sach="DS004", ten="Quản trị doanh nghiệp", nha_xuat_ban="NXB Thống kê", so_trang=320, tac_gia="Phạm Thị D", so_luong=4, category_id=categories[1].id),
        BookTitle(ma_dau_sach="DS005", ten="Truyện Kiều", nha_xuat_ban="NXB Văn học", so_trang=200, tac_gia="Nguyễn Du", so_luong=6, category_id=categories[2].id),
        BookTitle(ma_dau_sach="DS006", ten="Đắc Nhân Tâm", nha_xuat_ban="NXB Tổng hợp", so_trang=320, tac_gia="Dale Carnegie", so_luong=5, category_id=categories[2].id),
        BookTitle(ma_dau_sach="DS007", ten="Giải tích toán học", nha_xuat_ban="NXB Giáo dục", so_trang=450, tac_gia="Nguyễn Đình Trí", so_luong=3, category_id=categories[3].id),
        BookTitle(ma_dau_sach="DS008", ten="Vật lý đại cương", nha_xuat_ban="NXB ĐH QG", so_trang=500, tac_gia="Lương Duyên Bình", so_luong=4, category_id=categories[3].id),
        BookTitle(ma_dau_sach="DS009", ten="English Grammar in Use", nha_xuat_ban="Cambridge", so_trang=380, tac_gia="Raymond Murphy", so_luong=5, category_id=categories[4].id),
        BookTitle(ma_dau_sach="DS010", ten="Tiếng Nhật Bước đầu", nha_xuat_ban="NXB Lao động", so_trang=280, tac_gia="Nhóm tác giả", so_luong=3, category_id=categories[4].id),
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
        ("DG001", "Nguyễn Minh Tuấn", "DHCNTT17A", date(2000, 3, 15), "Nam"),
        ("DG002", "Trần Thị Hoa", "DHKT18B", date(2001, 5, 20), "Nu"),
        ("DG003", "Lê Quốc Hùng", "DHCNTT17B", date(2000, 7, 11), "Nam"),
        ("DG004", "Phạm Thị Lan", "DHKT19A", date(2002, 1, 25), "Nu"),
        ("DG005", "Hoàng Văn Đức", "DHCNTT18A", date(2001, 9, 5), "Nam"),
        ("DG006", "Ngô Thị Mai", "DHVH17A", date(2000, 12, 10), "Nu"),
        ("DG007", "Vũ Minh Khoa", "DHCNTT19A", date(2002, 4, 18), "Nam"),
        ("DG008", "Đặng Thị Ngọc", "DHKT17A", date(1999, 8, 22), "Nu"),
        ("DG009", "Trịnh Văn Long", "DHKH18A", date(2001, 6, 30), "Nam"),
        ("DG010", "Bùi Thị Hương", "DHNN19B", date(2002, 2, 14), "Nu"),
        ("DG011", "Lý Minh Nhật", "DHCNTT20A", date(2003, 3, 7), "Nam"),
        ("DG012", "Dương Thị Thảo", "DHKT20B", date(2003, 11, 19), "Nu"),
        ("DG013", "Phan Văn Thắng", "DHCNTT18B", date(2001, 10, 28), "Nam"),
        ("DG014", "Cao Thị Bích", "DHVH19A", date(2002, 7, 3), "Nu"),
        ("DG015", "Hồ Quang Vinh", "DHKH17B", date(2000, 5, 16), "Nam"),
        ("DG016", "Võ Thị Trang", "DHNN18A", date(2001, 8, 9), "Nu"),
        ("DG017", "Đinh Văn Hải", "DHCNTT19B", date(2002, 1, 21), "Nam"),
        ("DG018", "Lưu Thị Kim", "DHKT19B", date(2002, 4, 4), "Nu"),
        ("DG019", "Mạc Văn Phú", "DHVH20A", date(2003, 6, 13), "Nam"),
        ("DG020", "Nông Thị Yến", "DHNN17A", date(1999, 12, 27), "Nu"),
    ]
    readers = []
    for ma, ten, lop, ns, gt in readers_data:
        readers.append(Reader(ma_doc_gia=ma, ho_ten=ten, lop=lop, ngay_sinh=ns, gioi_tinh=gt))
    db.add_all(readers)
    db.flush()
    print(f"  Added {len(readers)} readers")

    # --- Users (1 admin + 3 librarians) ---
    admin = User(username="admin", password_hash=get_password_hash("admin123"), role="admin", full_name="Quản trị viên", email="admin@library.iuh.edu.vn")
    lib1 = User(username="librarian1", password_hash=get_password_hash("lib123"), role="librarian", full_name="Nguyễn Thị Thu Thư", email="thuthu1@library.iuh.edu.vn")
    lib2 = User(username="librarian2", password_hash=get_password_hash("lib123"), role="librarian", full_name="Trần Văn Thủ", email="thuthu2@library.iuh.edu.vn")
    lib3 = User(username="librarian3", password_hash=get_password_hash("lib123"), role="librarian", full_name="Lê Thị Thư Viện", email="thuthu3@library.iuh.edu.vn")
    db.add_all([admin, lib1, lib2, lib3])
    db.flush()
    print("  Added 1 admin + 3 librarians")

    # --- Borrow Records (15) ---
    borrow_records = []
    available_copies = [c for c in copies if c.tinh_trang == "available"]

    for i in range(15):
        reader = readers[i]
        copy = available_copies[i]
        borrow_date = date(2025, 1, 10) + timedelta(days=i * 5)
        is_returned = i < 10  # first 10 are returned

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
        print(f"Error: {e}")
        raise
    finally:
        db.close()
