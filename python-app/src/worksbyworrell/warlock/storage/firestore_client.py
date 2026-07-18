import json
import os

# Placeholder for firestore SDK. Implementation to resolve Firestore client setup.
# from google.cloud import firestore


def _load_from_firestore(agent_id: str, client=None) -> dict:
    """
    Load public config configurations and private overlays from Firestore.
    To be fully implemented in Phase 4.
    """
    if client is not None:
        doc = client.collection("agent_configurations").document(agent_id).get()
        if doc.exists:
            return doc.to_dict()

    return {}


def _load_from_local_fs(agent_id: str) -> dict:
    """
    Fallback loader reading configuration from local JSON files.
    """
    mock_path = os.path.join("tests", "mock_data", f"{agent_id}.json")
    if not os.path.exists(mock_path):
        return {"name": agent_id, "public_scope": "Fallback Demo Mode Enabled"}

    with open(mock_path, "r") as f:
        return json.load(f)


STORAGE_STRATEGIES = {"prod": _load_from_firestore, "local": _load_from_local_fs}


def get_agent_config(agent_id: str) -> dict:
    """
    Resolves storage strategy based on environmental markers.
    """
    env = "prod" if os.environ.get("GCP_PROJECT_ID") else "local"
    strategy = STORAGE_STRATEGIES.get(env, _load_from_local_fs)
    return strategy(agent_id)
