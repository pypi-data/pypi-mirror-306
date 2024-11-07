import logging
from unittest.mock import MagicMock, patch

import pytest
from sat.logs import ElasticClientBulkHandler


@pytest.fixture
def log_stuff(request):
    with patch("sat.logs.bulk") as bulk_patch:
        mock_client = MagicMock()
        elastic_handler = ElasticClientBulkHandler(
            client=mock_client,
            index_name="test",
            document_labels={"app": "test"},
            level=logging.INFO,
            batch_size=1,
            batch_time=10.0,
        )
        elastic_handler.setLevel(logging.INFO)
        test_formatter = logging.Formatter("%(message)s")
        elastic_handler.setFormatter(test_formatter)
        logger = logging.getLogger(request.node.name)
        logger.setLevel(logging.INFO)
        logger.addHandler(elastic_handler)

        yield logger, mock_client, bulk_patch
    logging.shutdown()


def test_without_fixture():
    mock_client = MagicMock()
    elastic_handler = ElasticClientBulkHandler(
        client=mock_client,
        index_name="test",
        document_labels={"app": "test"},
        level=logging.INFO,
        batch_size=10,
        batch_time=10.0,
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
    test_logger, mock_elastic_client, bulk_patch = log_stuff
    test_logger.info("test 2 message 1", extra={"cid": "test-cid"})
    bulk_patch.assert_called()


def test_extra_handling(log_stuff):
    logger, mock_elastic_client, bulk_patch = log_stuff

    logger.info("test 3 message 1", extra={"cid": "test 3 cid 1"})

    expected_log_document = {
        "_index": "test",
        "app": "test",
        "log_message": "test 3 message 1",
        "cid": "test 3 cid 1",
    }

    bulk_patch.assert_called_with(mock_elastic_client, [expected_log_document])


def test_bulk_handler():
    with patch("sat.logs.bulk") as bulk_patch:
        mock_client = MagicMock()
        elastic_handler = ElasticClientBulkHandler(
            client=mock_client,
            index_name="test",
            document_labels={"app": "test"},
            level=logging.INFO,
            batch_size=3,
            batch_time=1000.0,
        )
        elastic_handler.setLevel(logging.INFO)
        test_formatter = logging.Formatter("%(message)s")
        elastic_handler.setFormatter(test_formatter)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(elastic_handler)

        logger.info("test_1")
        logger.info("test_2")
        bulk_patch.assert_not_called()

        logger.info("test_3")
        bulk_patch.assert_called()


def test_bulk_not_called():
    with patch("sat.logs.bulk") as bulk_patch:
        mock_client = MagicMock()
        elastic_handler = ElasticClientBulkHandler(
            client=mock_client,
            index_name="test",
            document_labels={"app": "test"},
            level=logging.INFO,
            batch_size=10,
            batch_time=1000.0,
        )
        elastic_handler.setLevel(logging.INFO)
        test_formatter = logging.Formatter("%(message)s")
        elastic_handler.setFormatter(test_formatter)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(elastic_handler)

        logger.info("test_1")
        logger.info("test_2")
        logger.info("test_3")
        bulk_patch.assert_called()
