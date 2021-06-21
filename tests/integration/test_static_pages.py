import pytest


@pytest.mark.django_db
def test_research_materials(client):
    resp = client.get("/research-materials/")

    assert resp.status_code == 200
