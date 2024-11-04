import os
import enum
from urllib.parse import urljoin


class MLOpsAPIEntity(enum.Enum):
    Workspace = "workspace"
    Experiment = "mlflow_experiment"


class MLOpsAPI:

    @staticmethod
    def get_tracking_url(api_host: str, workspace_id: str) -> str:
        return f"{api_host}/mlflow/workspaces/{workspace_id}"

    @staticmethod
    def get_update_artifact_endpoint() -> str:
        return f"{os.environ['OIP_API_HOST']}/mlflow/mlflow_artifacts"

    @staticmethod
    def get_update_run_endpoint() -> str:
        return f"{os.environ['OIP_API_HOST']}/mlflow/mlflow_runs"

    @staticmethod
    def get_create_entity_endpoint(workspace_id: str, entity: str) -> str:
        api_host = os.environ["OIP_API_HOST"]
        tracking_host = MLOpsAPI.get_tracking_url(api_host, workspace_id)
        return urljoin(tracking_host + "/", f"api/2.0/mlflow/{entity}/create")

    @staticmethod
    def get_retrieve_entity_endpoint(entity: MLOpsAPIEntity) -> str:
        api_host = os.environ["OIP_API_HOST"]
        return urljoin(api_host + "/", f"entities/{entity.value}")
