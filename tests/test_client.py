import pytest
from flowforge.client import FlowForgeClient
from flowforge.models import Workflow

def test_client_init():
    client = FlowForgeClient(base_url="http://localhost:8080", api_key="test")
    assert client.base_url == "http://localhost:8080"
    client.close()

def test_workflow_model():
    w = Workflow(name="test", description="desc")
    assert w.name == "test"
    assert w.status == "DRAFT"
