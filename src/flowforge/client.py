"""FlowForge API Client."""
import httpx
from typing import Optional
from .models import Workflow, Task, WorkflowInstance
from .auth import AuthProvider

class FlowForgeClient:
    def __init__(self, base_url: str = "https://api.flowforge.io", api_key: Optional[str] = None, auth: Optional[AuthProvider] = None):
        self.base_url = base_url.rstrip("/")
        self._auth = auth
        self._client = httpx.Client(base_url=self.base_url, headers={"Authorization": f"Bearer {api_key}"} if api_key else {})

    def list_workflows(self, tenant_id: str, page: int = 0, size: int = 20) -> list[Workflow]:
        r = self._client.get("/api/v1/workflows", params={"tenantId": tenant_id, "page": page, "size": size})
        r.raise_for_status()
        return [Workflow(**w) for w in r.json().get("content", [])]

    def get_workflow(self, workflow_id: str) -> Workflow:
        r = self._client.get(f"/api/v1/workflows/{workflow_id}")
        r.raise_for_status()
        return Workflow(**r.json())

    def create_workflow(self, name: str, definition: dict, tenant_id: str, description: str = "") -> Workflow:
        r = self._client.post("/api/v1/workflows", json={"name": name, "definition": definition, "tenantId": tenant_id, "description": description})
        r.raise_for_status()
        return Workflow(**r.json())

    def start_workflow(self, workflow_id: str, variables: Optional[dict] = None) -> WorkflowInstance:
        r = self._client.post(f"/api/v1/workflows/{workflow_id}/start", json={"variables": variables or {}})
        r.raise_for_status()
        return WorkflowInstance(**r.json())

    def get_task(self, task_id: str) -> Task:
        r = self._client.get(f"/api/v1/tasks/{task_id}")
        r.raise_for_status()
        return Task(**r.json())

    def complete_task(self, task_id: str, output: dict) -> Task:
        r = self._client.post(f"/api/v1/tasks/{task_id}/complete", json=output)
        r.raise_for_status()
        return Task(**r.json())

    def close(self):
        self._client.close()

    def __enter__(self): return self
    def __exit__(self, *args): self.close()
