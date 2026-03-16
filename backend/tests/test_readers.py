def test_create_reader(client, auth_headers):
    reader = {"ma_doc_gia": "DG999", "ho_ten": "Nguyen Test", "lop": "DHCNTT21A", "gioi_tinh": "Nam"}
    resp = client.post("/api/readers", json=reader, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["ma_doc_gia"] == "DG999"
    assert data["ho_ten"] == "Nguyen Test"


def test_list_readers(client, auth_headers):
    resp = client.get("/api/readers", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_reader(client, auth_headers):
    r = client.post("/api/readers", json={"ma_doc_gia": "DG998", "ho_ten": "Get Test", "gioi_tinh": "Nu"}, headers=auth_headers).json()
    resp = client.get(f"/api/readers/{r['id']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["ma_doc_gia"] == "DG998"


def test_update_reader(client, auth_headers):
    r = client.post("/api/readers", json={"ma_doc_gia": "DG997", "ho_ten": "Old Name", "gioi_tinh": "Nam"}, headers=auth_headers).json()
    resp = client.put(f"/api/readers/{r['id']}", json={"ho_ten": "New Name"}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["ho_ten"] == "New Name"


def test_delete_reader(client, auth_headers):
    r = client.post("/api/readers", json={"ma_doc_gia": "DG996", "ho_ten": "Delete Me", "gioi_tinh": "Nam"}, headers=auth_headers).json()
    resp = client.delete(f"/api/readers/{r['id']}", headers=auth_headers)
    assert resp.status_code == 200


def test_duplicate_ma_doc_gia(client, auth_headers):
    client.post("/api/readers", json={"ma_doc_gia": "DG995", "ho_ten": "First", "gioi_tinh": "Nam"}, headers=auth_headers)
    resp = client.post("/api/readers", json={"ma_doc_gia": "DG995", "ho_ten": "Second", "gioi_tinh": "Nu"}, headers=auth_headers)
    assert resp.status_code == 400
