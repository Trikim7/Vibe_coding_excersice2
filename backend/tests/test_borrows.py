def test_create_category(client, auth_headers):
    cat = {"ma_chuyen_nganh": "TEST01", "ten": "Test Category", "mo_ta": "Test desc"}
    resp = client.post("/api/categories", json=cat, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["ten"] == "Test Category"


def _create_category(client, auth_headers, ma="CAT01"):
    resp = client.post("/api/categories", json={"ma_chuyen_nganh": ma, "ten": "Cat"}, headers=auth_headers)
    return resp.json()


def test_create_book_title(client, auth_headers):
    cat = _create_category(client, auth_headers, "BCAT01")
    book = {
        "ma_dau_sach": "BT001", "ten": "Python Book", "tac_gia": "Author A",
        "nha_xuat_ban": "NXB Test", "so_trang": 300, "so_luong": 3,
        "category_id": cat["id"]
    }
    resp = client.post("/api/book-titles", json=book, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["ma_dau_sach"] == "BT001"


def _create_book_and_copy(client, auth_headers, ma_dau="BT_T1", ma_copy="CP_T1"):
    cat = _create_category(client, auth_headers, f"C_{ma_dau}")
    book = client.post("/api/book-titles", json={
        "ma_dau_sach": ma_dau, "ten": "Book", "so_luong": 1, "category_id": cat["id"]
    }, headers=auth_headers).json()
    copy = client.post("/api/book-copies", json={
        "ma_ban_sao": ma_copy, "dau_sach_id": book["id"], "tinh_trang": "available"
    }, headers=auth_headers).json()
    return book, copy


def test_create_book_copy(client, auth_headers):
    _, copy = _create_book_and_copy(client, auth_headers, "BT002", "CP002")
    assert copy["tinh_trang"] == "available"


def test_borrow_flow(client, auth_headers):
    _, copy = _create_book_and_copy(client, auth_headers, "BT003", "CP003")
    reader = client.post("/api/readers", json={"ma_doc_gia": "DG_B01", "ho_ten": "Borrow Test", "gioi_tinh": "Nam"}, headers=auth_headers).json()

    borrow_resp = client.post("/api/borrows", json={
        "ma_sach": copy["id"], "ma_doc_gia": reader["id"]
    }, headers=auth_headers)
    assert borrow_resp.status_code == 201
    borrow = borrow_resp.json()
    assert borrow["tinh_trang"] == "active"


def test_prevent_double_borrow(client, auth_headers):
    _, copy1 = _create_book_and_copy(client, auth_headers, "BT004", "CP004")
    _, copy2 = _create_book_and_copy(client, auth_headers, "BT005", "CP005")
    reader = client.post("/api/readers", json={"ma_doc_gia": "DG_B02", "ho_ten": "Double Test", "gioi_tinh": "Nu"}, headers=auth_headers).json()

    client.post("/api/borrows", json={"ma_sach": copy1["id"], "ma_doc_gia": reader["id"]}, headers=auth_headers)
    resp2 = client.post("/api/borrows", json={"ma_sach": copy2["id"], "ma_doc_gia": reader["id"]}, headers=auth_headers)
    assert resp2.status_code == 400  # Should prevent double borrow


def test_return_flow(client, auth_headers):
    _, copy = _create_book_and_copy(client, auth_headers, "BT006", "CP006")
    reader = client.post("/api/readers", json={"ma_doc_gia": "DG_B03", "ho_ten": "Return Test", "gioi_tinh": "Nam"}, headers=auth_headers).json()

    borrow = client.post("/api/borrows", json={"ma_sach": copy["id"], "ma_doc_gia": reader["id"]}, headers=auth_headers).json()
    return_resp = client.post(f"/api/borrows/{borrow['id']}/return", headers=auth_headers)
    assert return_resp.status_code == 200
    assert return_resp.json()["tinh_trang"] == "returned"


def test_reports(client, auth_headers):
    resp_top = client.get("/api/reports/top-borrowed", headers=auth_headers)
    assert resp_top.status_code == 200
    resp_unret = client.get("/api/reports/unreturned-readers", headers=auth_headers)
    assert resp_unret.status_code == 200
