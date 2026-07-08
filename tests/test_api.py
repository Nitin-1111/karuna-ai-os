"""Integration tests for FastAPI REST endpoints."""

from typing import Any

from fastapi.testclient import TestClient


def test_health_docs_and_openapi(api_client: TestClient) -> None:
    """Health, docs, ReDoc, and OpenAPI should be available."""

    assert api_client.get("/").status_code == 200
    assert api_client.get("/health").json()["status"] == "ok"
    assert api_client.get("/health/live").json()["status"] == "alive"
    assert api_client.get("/health/ready").json()["status"] == "ready"
    assert api_client.get("/version").status_code == 200
    assert api_client.get("/docs").status_code == 200
    assert api_client.get("/redoc").status_code == 200

    openapi = api_client.get("/openapi.json").json()
    assert "/api/v1/agents" in openapi["paths"]
    assert "/api/v1/workflows/run" in openapi["paths"]
    assert "/api/v1/documents" in openapi["paths"]


def test_agent_endpoints(api_client: TestClient) -> None:
    """Agent endpoints should list, read, execute, and validate agents."""

    list_response = api_client.get("/api/v1/agents")
    assert list_response.status_code == 200
    assert {agent["agent_type"] for agent in list_response.json()["agents"]} == {
        "content",
        "nutrition",
        "research",
        "review",
    }

    get_response = api_client.get("/api/v1/agents/research")
    assert get_response.status_code == 200
    assert get_response.json()["display_name"] == "Research Agent"

    run_response = api_client.post(
        "/api/v1/agents/research/run",
        json={"input": "phase nine agent request"},
    )
    assert run_response.status_code == 200
    assert run_response.json()["agent_type"] == "research"

    assert api_client.get("/api/v1/agents/unsupported").status_code == 400
    assert api_client.post(
        "/api/v1/agents/research/run",
        json={"input": ""},
    ).status_code == 422


def test_workflow_endpoint(api_client: TestClient) -> None:
    """Workflow endpoint should execute the existing sequential workflow."""

    response = api_client.post(
        "/api/v1/workflows/run",
        json={
            "request": "phase nine workflow request",
            "metadata": {"source": "pytest"},
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["execution_status"] == "completed"
    assert payload["workflow_metadata"]["source"] == "pytest"
    assert payload["final_output"] is not None

    error_response = api_client.post(
        "/api/v1/workflows/run",
        json={"request": "valid", "metadata": {"source": ""}},
    )
    assert error_response.status_code == 400


def test_document_endpoints(
    api_client: TestClient,
    document_payload: dict[str, Any],
) -> None:
    """Document endpoints should create, list, read, delete, and validate."""

    invalid_response = api_client.post(
        "/api/v1/documents",
        json={"filename": "bad.txt", "content_base64": "not-base64"},
    )
    assert invalid_response.status_code == 400

    create_response = api_client.post("/api/v1/documents", json=document_payload)
    assert create_response.status_code == 201
    document = create_response.json()["document"]
    document_id = document["document_id"]
    assert document["original_filename"] == "phase9.txt"

    list_response = api_client.get("/api/v1/documents")
    assert list_response.status_code == 200
    assert [item["document_id"] for item in list_response.json()["documents"]] == [
        document_id
    ]

    read_response = api_client.get(f"/api/v1/documents/{document_id}")
    assert read_response.status_code == 200
    assert read_response.json()["content_base64"] == document_payload["content_base64"]

    delete_response = api_client.delete(f"/api/v1/documents/{document_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "document_id": document_id,
        "status": "deleted",
    }

    assert api_client.get(f"/api/v1/documents/{document_id}").status_code == 404
