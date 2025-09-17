def auth_header(client):
    client.post("/auth/register", json={"email": "u@x.com", "password": "pw123456"})
    r = client.post("/auth/login", json={"email": "u@x.com", "password": "pw123456"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}

def seed_parts(client, h):
    cpu = client.post("/parts/cpus", json={"name":"Ryzen 5","socket":"AM5","tdp_w":105}, headers=h).json()
    mb  = client.post("/parts/motherboards", json={"name":"B650","socket":"AM5","form_factor":"ATX","ram_type":"DDR5","ram_max_mts":6000}, headers=h).json()
    ram = client.post("/parts/ramkits", json={"name":"DDR5 5600","ram_type":"DDR5","speed_mts":5600,"size_gb":32,"sticks":2}, headers=h).json()
    gpu = client.post("/parts/gpus", json={"name":"RTX 4070","length_mm":300,"tdp_w":200}, headers=h).json()
    psu = client.post("/parts/psus", json={"name":"650W","wattage_w":650}, headers=h).json()
    case= client.post("/parts/cases", json={"name":"ATX Case","supported_form_factors":"ATX,mATX","gpu_max_length_mm":320}, headers=h).json()
    return cpu, mb, ram, gpu, psu, case

def test_build_validate_pass(client):
    h = auth_header(client)
    cpu, mb, ram, gpu, psu, case = seed_parts(client, h)
    b = client.post("/builds/", json={
        "cpu_id": cpu["id"], "motherboard_id": mb["id"], "ramkit_id": ram["id"],
        "gpu_id": gpu["id"], "psu_id": psu["id"], "case_id": case["id"]
    }, headers=h)
    assert b.status_code == 201
    v = client.get(f"/builds/{b.json()['id']}/validate", headers=h)
    assert v.status_code == 200 and v.json()["passed"] is True

def test_build_validate_fails_on_socket(client):
    h = auth_header(client)
    cpu = client.post("/parts/cpus", json={"name":"Ryzen","socket":"AM4","tdp_w":95}, headers=h).json()
    mb  = client.post("/parts/motherboards", json={"name":"B650","socket":"AM5","form_factor":"ATX","ram_type":"DDR5","ram_max_mts":6000}, headers=h).json()
    ram = client.post("/parts/ramkits", json={"name":"DDR5 5600","ram_type":"DDR5","speed_mts":5600,"size_gb":32,"sticks":2}, headers=h).json()
    gpu = client.post("/parts/gpus", json={"name":"RTX","length_mm":300,"tdp_w":200}, headers=h).json()
    psu = client.post("/parts/psus", json={"name":"650W","wattage_w":650}, headers=h).json()
    case= client.post("/parts/cases", json={"name":"ATX Case","supported_form_factors":"ATX,mATX","gpu_max_length_mm":320}, headers=h).json()
    b = client.post("/builds/", json={
        "cpu_id": cpu["id"], "motherboard_id": mb["id"], "ramkit_id": ram["id"],
        "gpu_id": gpu["id"], "psu_id": psu["id"], "case_id": case["id"]
    }, headers=h)
    v = client.get(f"/builds/{b.json()['id']}/validate", headers=h).json()
    assert v["passed"] is False
