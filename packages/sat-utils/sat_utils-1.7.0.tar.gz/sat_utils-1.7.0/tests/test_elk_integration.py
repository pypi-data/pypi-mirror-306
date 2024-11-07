import logging
import os
from unittest.mock import MagicMock, patch

import pytest
from sat.logs import ElasticClientHandler, setup_sat_logging_with_defaults


@pytest.fixture
def log_stuff(request):
    mock_client = MagicMock()
    elastic_handler = ElasticClientHandler(
        client=mock_client, index_name="test", document_labels={"app": "test"}, level=logging.INFO
    )
    elastic_handler.setLevel(logging.INFO)
    test_formatter = logging.Formatter("%(message)s")
    elastic_handler.setFormatter(test_formatter)
    logger = logging.getLogger(request.node.name)
    logger.setLevel(logging.INFO)
    logger.addHandler(elastic_handler)

    return logger, mock_client


@patch.dict(os.environ, {"ELASTIC_ENABLE_LOGGING": "False"}, clear=True)
def test_default_setup_no_elastic():
    setup_sat_logging_with_defaults()


@patch.dict(
    os.environ,
    {
        "ELASTIC_ENABLE_LOGGING": "True",
        "ELASTIC_URL": "test-url",
        "ELASTIC_USERNAME": "test-user",
        "ELASTIC_INDEX": "test-index",
        "APP_NAME": "test-app-name",
    },
    clear=True,
)
def test_fails_when_missing_required_env():
    """When Elastic is enabled but username isn't defined, setup should raise a key error"""
    with pytest.raises(KeyError):
        setup_sat_logging_with_defaults()


@patch.dict(
    os.environ,
    {
        "ELASTIC_ENABLE_LOGGING": "True",
        "ELASTIC_URL": "test-url",
        "ELASTIC_USERNAME": "test-user",
        "ELASTIC_PASSWORD": "test-pass",
        "ELASTIC_INDEX": "test-index",
        "APP_NAME": "test-app-name",
    },
    clear=True,
)
def test_default_setup_with_elastic():
    with patch("sat.logs.Elasticsearch") as elastic_mock:
        setup_sat_logging_with_defaults()
        elastic_mock.assert_called_with(
            "test-url", basic_auth=("test-user", "test-pass"), verify_certs=True
        )


def test_without_fixture():
    mock_client = MagicMock()
    elastic_handler = ElasticClientHandler(
        client=mock_client, index_name="test", document_labels={"app": "test"}, level=logging.INFO
    )
    elastic_handler.setLevel(logging.INFO)
    test_formatter = logging.Formatter("%(message)s")
    elastic_handler.setFormatter(test_formatter)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(elastic_handler)
    logger.info("test 1 message 1")
    logger.info("test 1 message 2")


def test_log_sent(log_stuff):
    """Just assert that the bulk upload method is called if a single message is sent"""
    test_logger, mock_elastic_client = log_stuff
    test_logger.info("test 2 message 1", extra={"cid": "test-cid"})
    mock_elastic_client.index.assert_called()


def test_extra_handling(log_stuff):
    logger, mock_elastic_client = log_stuff

    logger.info("test 3 message 1", extra={"cid": "test 3 cid 1"})

    expected_log_document = {
        "app": "test",
        "log_message": "test 3 message 1",
        "cid": "test 3 cid 1",
    }
    mock_elastic_client.index.assert_called_with(index="test", document=expected_log_document)
