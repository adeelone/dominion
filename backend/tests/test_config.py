from __future__ import annotations

from backend.app.main import allowed_origins


def test_allowed_origins_default_to_local_frontend(monkeypatch) -> None:
    monkeypatch.delenv("BACKEND_CORS_ORIGINS", raising=False)

    assert allowed_origins() == ["http://localhost:5173"]


def test_allowed_origins_accept_comma_separated_values(monkeypatch) -> None:
    monkeypatch.setenv(
        "BACKEND_CORS_ORIGINS",
        "https://dominion.example.com, https://admin.dominion.example.com",
    )

    assert allowed_origins() == [
        "https://dominion.example.com",
        "https://admin.dominion.example.com",
    ]
