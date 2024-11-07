import logging
from unittest.mock import MagicMock

import pytest
from sat.logs import ElasticClientHandler


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


def test_similarly_named_module_log_sent(log_stuff):
    """
    Ensure that elastic module filtering only targets the elastic library, not similarly named files

    The ElasticClientHandler has a filter on it that ignores anything in the elastic module.
    This is done to prevent an infinite recursion that would arise by the elastic library itself
    making logging calls while processing a log message, infinitely recursing with more log calls.
    This test file is named similarly to the elastic library,
    to ensure that the filter is only targeting what we want it to target and not
    client code/other modules that have names like `elastic`
    """
    test_logger, mock_elastic_client = log_stuff
    test_logger.info("test 2 message 1", extra={"cid": "test-cid"})
    mock_elastic_client.index.assert_called()
