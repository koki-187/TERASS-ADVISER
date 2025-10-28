"""Integration tests for the TERASS Adviser API using Flask's test client."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict

import pytest

import api_server
from src.engine.reward_calculator import (
    BONUS_STAGE_THRESHOLD,
    RATE_SELF_BONUS,
    RATE_SELF_NORMAL,
)


@pytest.fixture
def feedback_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect feedback storage to a temporary location for tests."""

    path = tmp_path / "feedback_data.json"
    monkeypatch.setattr(api_server, "FEEDBACK_FILE", str(path))
    return path


@pytest.fixture
def client(feedback_path: Path):
    """Provide a Flask test client with isolated feedback storage."""

    api_server.app.config["TESTING"] = True
    feedback_path.write_text("[]", encoding="utf-8")
    with api_server.app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers() -> Dict[str, str]:
    """Headers containing the valid API token for authenticated requests."""

    return {
        "X-API-Token": api_server.API_TOKEN,
        "Content-Type": "application/json",
    }


def test_health_check(client) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_api_info(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "TERASS Adviser API"


def test_reward_calculation(client, auth_headers) -> None:
    payload = {
        "deals": [
            {
                "tax_excluded_fee": 5_000_000,
                "source": "self",
                "date": "2025-04-01",
            }
        ]
    }
    response = client.post(
        "/api/v1/reward/calculate",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    expected_reward = 5_000_000 * RATE_SELF_NORMAL
    assert data["total_reward"] == expected_reward

    multi_payload = {
        "deals": [
            {
                "tax_excluded_fee": 15_000_000,
                "source": "self",
                "date": "2025-04-01",
            },
            {
                "tax_excluded_fee": 10_000_000,
                "source": "self",
                "date": "2025-05-01",
            },
        ]
    }
    response = client.post(
        "/api/v1/reward/calculate",
        json=multi_payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    expected_total = 15_000_000 * RATE_SELF_NORMAL + 10_000_000 * RATE_SELF_NORMAL
    assert data["total_reward"] == expected_total


def test_reward_bonus_activation(client, auth_headers) -> None:
    """Verify that rewards after the bonus threshold use the bonus rate."""

    deals = []
    running_total = 0
    month = 1
    while running_total < BONUS_STAGE_THRESHOLD:
        deals.append(
            {
                "tax_excluded_fee": 5_000_000,
                "source": "self",
                "date": f"2025-{month:02d}-01",
            }
        )
        running_total += 5_000_000
        month += 1

    deals.append(
        {
            "tax_excluded_fee": 5_000_000,
            "source": "self",
            "date": f"2025-{month:02d}-01",
        }
    )

    response = client.post(
        "/api/v1/reward/calculate",
        json={"deals": deals},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    bonus_detail = data["details"][-1]
    assert bonus_detail["bonus_activated"] is True
    assert bonus_detail["rate_applied"] == RATE_SELF_BONUS


def test_agent_class(client, auth_headers) -> None:
    payload = {
        "region": "capital",
        "period_sales": 12_000_000,
        "cumulative_cases": 5,
    }
    response = client.post(
        "/api/v1/agent/class",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["class"] == "Senior"


def test_feedback_submission(client, auth_headers, feedback_path) -> None:
    payload = {
        "user_id": "test_agent_001",
        "category": "feature_request",
        "message": "モバイルアプリがあると便利です",
        "context": {
            "platform": "test",
            "timestamp": datetime.now().isoformat(),
        },
    }
    response = client.post(
        "/api/v1/feedback",
        json=payload,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "feedback_id" in data

    stored = json.loads(feedback_path.read_text(encoding="utf-8"))
    assert len(stored) == 1
    assert stored[0]["message"] == payload["message"]


def test_feedback_listing(client, auth_headers, feedback_path) -> None:
    entries = [
        {
            "id": "fb_20240101000000",
            "timestamp": "2024-01-01T00:00:00",
            "user_id": "agent123",
            "category": "general",
            "message": "テスト",
            "context": {},
            "status": "pending",
        }
    ]
    feedback_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    response = client.get("/api/v1/feedback", headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == len(entries)
    assert data["feedback"] == entries


def test_authentication_required(client) -> None:
    payload = {"deals": [{"tax_excluded_fee": 1_000_000, "source": "self"}]}
    response = client.post(
        "/api/v1/reward/calculate",
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 401

    response = client.post(
        "/api/v1/reward/calculate",
        json=payload,
        headers={
            "X-API-Token": "wrong-token",
            "Content-Type": "application/json",
        },
    )
    assert response.status_code == 401


@pytest.fixture(autouse=True)
def cleanup_feedback_file(feedback_path: Path):
    """Ensure the feedback file is removed after each test."""

    yield
    if feedback_path.exists():
        feedback_path.unlink()

