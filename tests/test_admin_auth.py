
import pytest

import app as app_module


@pytest.fixture
def admin_client(monkeypatch):
    app_module.app.config.update(
        TESTING=True,
        SECRET_KEY="test-only-secret-key"
    )

    monkeypatch.setattr(
        app_module, "ADMIN_USERNAME", "testadmin"
    )
    monkeypatch.setattr(
        app_module, "ADMIN_PASSWORD", "testpassword123"
    )

    with app_module.app.test_client() as client:
        yield client


def test_admin_login_with_valid_credentials(admin_client):
    response = admin_client.post(
        "/admin/login",
        data={
            "username": "testadmin",
            "password": "testpassword123"
        },
        follow_redirects=False
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin")

    with admin_client.session_transaction() as session:
        assert session.get("admin_logged_in") is True
