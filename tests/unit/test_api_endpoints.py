"""
Unit tests for the VibeFactory API endpoints.
"""
import uuid
from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(test_client: TestClient) -> None:
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "description" in data


def test_health_check(test_client: TestClient) -> None:
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


class TestProjectEndpoints:
    """Test suite for project-related endpoints."""
    
    def test_create_project(
        self, test_client: TestClient, sample_project_data: Dict[str, Any]
    ) -> None:
        """Test creating a new project."""
        response = test_client.post("/projects/", json=sample_project_data)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["description"] == sample_project_data["description"]
        assert "tasks" in data
        assert isinstance(data["tasks"], list)
    
    def test_get_project(
        self, test_client: TestClient, sample_project_data: Dict[str, Any]
    ) -> None:
        """Test retrieving a project by ID."""
        # First, create a project
        create_response = test_client.post("/projects/", json=sample_project_data)
        assert create_response.status_code == 201
        project_id = create_response.json()["id"]
        
        # Then, retrieve it
        response = test_client.get(f"/projects/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert data["description"] == sample_project_data["description"]
    
    def test_get_nonexistent_project(self, test_client: TestClient) -> None:
        """Test retrieving a project that doesn't exist."""
        non_existent_id = str(uuid.uuid4())
        response = test_client.get(f"/projects/{non_existent_id}")
        assert response.status_code == 404
        assert "Project not found" in response.json()["detail"]


class TestTaskEndpoints:
    """Test suite for task-related endpoints."""
    
    def test_generate_task_code(
        self, test_client: TestClient, sample_project_data: Dict[str, Any]
    ) -> None:
        """Test generating code for a task."""
        # First, create a project
        create_response = test_client.post("/projects/", json=sample_project_data)
        assert create_response.status_code == 201
        project_id = create_response.json()["id"]
        task_id = 1  # Assuming the first task has ID 1
        
        # Then, generate code for a task
        response = test_client.post(f"/projects/{project_id}/tasks/{task_id}/generate")
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        assert "status" in data
        assert "code" in data or "error" in data
    
    def test_generate_code_for_nonexistent_task(
        self, test_client: TestClient, sample_project_data: Dict[str, Any]
    ) -> None:
        """Test generating code for a task that doesn't exist."""
        # First, create a project
        create_response = test_client.post("/projects/", json=sample_project_data)
        assert create_response.status_code == 201
        project_id = create_response.json()["id"]
        
        # Try to generate code for a non-existent task
        non_existent_task_id = 999
        response = test_client.post(
            f"/projects/{project_id}/tasks/{non_existent_task_id}/generate"
        )
        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
