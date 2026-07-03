"""FlowForge API Client."""
import httpx
from typing import Optional

from .models import Workflow, Task, WorkflowInstance
from .auth import AuthProvider


class FlowForgeClient:
    def __init__(
        self,
        base_url: str = "https://api.flowforge.io",
        api_key: Optional[str] = None,
        auth: Optional[AuthProvider] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self._auth = auth
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
        )

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        try:
            response = self._client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError:
            # HTTP-Fehler (4xx/5xx) unverändert weitergeben
            raise
        except httpx.HTTPError as e:
            raise RuntimeError(f"Request to FlowForge failed: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error while communicating with FlowForge: {e}") from e

    def list_workflows(
        self,
        tenant_id: str,
        page: int = 0,
        size: int = 20,
    ) -> list[Workflow]:
        r = self._request(
            "GET",
            "/api/v1/workflows",
            params={"tenantId": tenant_id, "page": page, "size": size},
        )
        return [Workflow(**w) for w in r.json().get("content", [])]

    def get_workflow(self, workflow_id: str) -> Workflow:
        r = self._request("GET", f"/api/v1/workflows/{workflow_id}")
        return Workflow(**r.json())

    def create_workflow(
        self,
        name: str,
        definition: dict,
        tenant_id: str,
        description: str = "",
    ) -> Workflow:
        r = self._request(
            "POST",
            "/api/v1/workflows",
            json={
                "name": name,
                "definition": definition,
                "tenantId": tenant_id,
                "description": description,
            },
        )
        return Workflow(**r.json())

    def start_workflow(
        self,
        workflow_id: str,
        variables: Optional[dict] = None,
    ) -> WorkflowInstance:
        r = self._request(
            "POST",
            f"/api/v1/workflows/{workflow_id}/start",
            json={"variables": variables or {}},
        )
        return WorkflowInstance(**r.json())

    def get_task(self, task_id: str) -> Task:
        r = self._request("GET", f"/api/v1/tasks/{task_id}")
        return Task(**r.json())

    def complete_task(self, task_id: str, output: dict) -> Task:
        r = self._request(
            "POST",
            f"/api/v1/tasks/{task_id}/complete",
            json=output,
        )
        return Task(**r.json())

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()