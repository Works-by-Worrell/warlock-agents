import pytest
from unittest.mock import MagicMock
from worksbyworrell.warlock.storage.firestore_client import _load_from_firestore


def test_load_from_firestore_success(mock_firestore_client):
    """
    Verify Firestore integration fetches config fields correctly when mocked.
    """
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {"overlay_id": "recruiters_pass", "restricted_mode": False}
    mock_firestore_client.collection.return_value.document.return_value.get.return_value = mock_doc

    result = _load_from_firestore(agent_id="warlock-prime", client=mock_firestore_client)

    assert result["restricted_mode"] is False
