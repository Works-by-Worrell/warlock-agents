import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_firestore_client(mocker):
    """
    Mock fixture to isolate firestore operations from network dependencies.
    """
    mock_db = MagicMock()
    # Stub: mocker.patch will patch the client when implementation is added.
    return mock_db
