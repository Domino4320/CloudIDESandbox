import os
from pathlib import Path


def initialize_user_workspace(current_user_id: str = "mock_user_id"):
    directory = Path(__file__).parent.parent.parent.parent.parent
    path = directory / "workspaces" / current_user_id
    if os.path.exists(path):
        return
    os.mkdir(path)
