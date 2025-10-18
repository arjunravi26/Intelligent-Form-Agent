import pytest
from unittest.mock import patch, MagicMock
from src.abstractive_qa import AbstractiveQA


@pytest.fixture
def mock_read_config():
    with patch("src.abstractive_qa.read_config") as mock:
        # Mock read_config() to return fake values depending on key
        def side_effect(key):
            if key == "SYSTEM_PROMPT_ABSTRACIVE_QA":
                return "You are a helpful medical assistant."
            elif key == "LLM_MODEL":
                return "mistralai/Mixtral-8x7B-Instruct-v0.1"
            return None
        mock.side_effect = side_effect
        yield mock


@pytest.fixture
def mock_inference_client():
    with patch("src.abstractive_qa.InferenceClient") as mock_client:
        yield mock_client


def test_init_reads_config_success(mock_read_config):
    """Ensure AbstractiveQA initializes properly with valid config."""
    qa = AbstractiveQA(claim_data="Patient has fever.")
    assert qa.system_prompt == "You are a helpful medical assistant."
    assert qa.model == "mistralai/Mixtral-8x7B-Instruct-v0.1"
    assert qa.claim_data == "Patient has fever."


def test_init_raises_error_if_no_system_prompt():
    """Ensure ValueError is raised when system prompt missing."""
    with patch("src.abstractive_qa.read_config", return_value=None):
        with pytest.raises(ValueError):
            AbstractiveQA(claim_data="Test claim data")


@patch("os.getenv", return_value="fake_token")
def test_qa_returns_answer_and_reasoning(mock_env, mock_read_config, mock_inference_client):
    """Test qa() returns tuple (answer, reasoning) when client works."""
    # Mock client.chat_completion response
    mock_instance = MagicMock()
    mock_instance.chat_completion.return_value.choices = [
        MagicMock(message=MagicMock(content='{"answer": "Dr. Smith", "reasoning": "Found in text"}'))
    ]
    mock_inference_client.return_value = mock_instance

    qa = AbstractiveQA(claim_data="Claim: treated by Dr. Smith.")
    result = qa.qa("Who treated the patient?")
    assert result == ("Dr. Smith", "Found in text")


@patch("os.getenv", return_value="fake_token")
def test_qa_returns_none_on_exception(mock_env, mock_read_config):
    """Ensure qa() gracefully returns None when an exception occurs."""
    with patch("src.abstractive_qa.InferenceClient", side_effect=Exception("Connection failed")):
        qa = AbstractiveQA(claim_data="Sample claim")
        result = qa.qa("What happened?")
        assert result is None
