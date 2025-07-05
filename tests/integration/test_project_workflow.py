"""
Integration tests for the VibeFactory project workflow.
"""
import time
from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient


def test_complete_project_workflow(
    test_client: TestClient, sample_project_data: Dict[str, Any]
) -> None:
    """
    Test the complete workflow of creating a project and generating code for its tasks.
    """
    # Step 1: Create a new project
    create_response = test_client.post("/projects/", json=sample_project_data)
    assert create_response.status_code == 201
    project = create_response.json()
    project_id = project["id"]
    
    # Verify the project was created with tasks
    assert "tasks" in project
    assert len(project["tasks"]) > 0
    
    # Step 2: Get the project to verify its state
    get_response = test_client.get(f"/projects/{project_id}")
    assert get_response.status_code == 200
    project = get_response.json()
    
    # Step 3: Generate code for each task
    for task in project["tasks"]:
        task_id = task["id"]
        
        # Generate code for the task
        generate_response = test_client.post(
            f"/projects/{project_id}/tasks/{task_id}/generate"
        )
        assert generate_response.status_code == 200
        
        # Get the updated task to verify code was generated
        get_task_response = test_client.get(f"/projects/{project_id}")
        assert get_task_response.status_code == 200
        
        # Find the task in the project
        updated_project = get_task_response.json()
        updated_task = next(
            (t for t in updated_project["tasks"] if t["id"] == task_id),
            None
        )
        assert updated_task is not None
        
        # Verify the task has code or an error message
        assert "code" in updated_task or "error" in updated_task
        
        # Small delay to avoid rate limiting (if applicable)
        time.sleep(0.5)
