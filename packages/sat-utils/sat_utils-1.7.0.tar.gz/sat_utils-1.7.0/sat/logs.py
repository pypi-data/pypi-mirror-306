import logging
import os
import time

from elasticsearch import BadRequestError, Elasticsearch
from elasticsearch.helpers import bulk

logger = logging.getLogger(__name__)


class SingletonLoggerMixin:
    _instance = None
    client_mock = None

    def __new__(cls, *args, **kwargs):
        # Only call this setup block the first time a SATLoggerSingleton is instantiated
        # Prevents multiple setup function calls
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            setup_sat_logging_with_defaults()

        return cls._instance


class SATLogger(SingletonLoggerMixin):
    """
    Logging wrapper for SAT applications.

    The purpose for the mixin is to enable a logging.basicConfig setup to be called a single time,
    but to allow all the application files to continue to use the same logging setup syntax.
    The singleton mixin will check to see if the setup function has already been called in the
    runtime, and if not it calls the setup
    (initializing the Elastic logging handler and formatters).
    """

    def __init__(self, name: str = __name__, level: int = logging.INFO) -> None:
        self.logger = logging.getLogger(name)

    def add_handlers(self, handlers: list[(logging.Handler, logging.Formatter)]) -> None:
        """
        Add additional handlers to the logger.
        Handlers should be a list of tuples with a logging.Handler and an
        optional logging.Formatter.
        """

        self.logger.warning(
            "Adding handlers to this instance of the logger only, "
            "will not persist throughout project. Update logging config to persist changes."
        )

        for tup in handlers:
            handler, formatter = tup
            if formatter:
                handler.setFormatter(formatter)
            else:
                handler.setFormatter(self.formatter)
            self.logger.addHandler(handler)

    def debug(self, msg: str, *args, **kwargs) -> None:
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        self.logger.critical(msg, *args, **kwargs)


class ElasticModuleFilter(logging.Filter):
    def filter(self, record):
        top_module_name = record.name.split(".")[0]
        return top_module_name not in ["elastic", "elastic_transport"]


def setup_sat_logging_with_defaults():
    """
    Sets up a basic logging config with an Elastic Client Handler using values
    from environment variables

    Depends on the following Environment Variables
    ELASTIC_ENABLE_LOGGING: string value for booleans,
        `'True'` or `'False'`: Decides whether Elastic log handler
        should be used, and also controls whether other needed configuration is checked for.
        Defaults to False

    ELASTIC_URL: str: url for the Elastic server including protocol and port,
        e.g. `'https://elk.example.com:9200`
    ELASTIC_USERNAME: str: elastic username
    ELASTIC_PASSWORD: str: elastic password
    ELASTIC_INDEX: str: Name of the index this app should log to
    APP_NAME: str: Name of the app label included in the logs
    """

    # Elastic loging feature flag defaults to false, don't want to blow up
    # local development or tests if no environment variables are set
    enable_elastic_string = os.getenv("ELASTIC_ENABLE_LOGGING", "")
    if enable_elastic_string.lower() == "true":
        enable_elastic_logging = True
    else:
        logger.warning("Elastic logging disabled, continuing without")
        enable_elastic_logging = False

    if enable_elastic_logging:
        elastic_url = os.environ["ELASTIC_URL"]
        elastic_username = os.environ["ELASTIC_USERNAME"]
        elastic_password = os.environ["ELASTIC_PASSWORD"]
        elastic_index = os.environ["ELASTIC_INDEX"]
        app_name = os.environ["APP_NAME"]
        elastic_client = get_elasticsearch_client(elastic_url, elastic_username, elastic_password)
    else:
        app_name = os.getenv("APP_NAME")  # If logging without elastic enabled, APP_NAME is optional
        elastic_client = None
        elastic_index = None

    log_level_string = os.getenv("LOGLEVEL", "INFO")
    log_level = getattr(logging, log_level_string.upper())

    setup_sat_logging(elastic_client, elastic_index, app_name, enable_elastic_logging, log_level)


def setup_sat_logging_bulk(
    client: Elasticsearch,
    index_name: str,
    app_name: str,
    enable_elastic_logging,
    loglevel: int = logging.INFO,
    batch_size: int = 100,
    batch_time: float = 2.0,
):
    log_handlers = [logging.StreamHandler()]

    if os.getenv("DEBUG"):
        loglevel = logging.DEBUG

    if enable_elastic_logging:
        elastic_handler = ElasticClientBulkHandler(
            client,
            index_name=index_name,
            document_labels={"app": app_name},
            level=loglevel,
            batch_size=batch_size,
            batch_time=batch_time,
        )
        elastic_handler.addFilter(ElasticModuleFilter())
        log_handlers.append(elastic_handler)

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=log_handlers,
    )


def setup_sat_logging(
    client: Elasticsearch,
    index_name: str,
    app_name: str,
    enable_elastic_logging,
    loglevel: int = logging.INFO,
):
    log_handlers = [logging.StreamHandler()]

    if os.getenv("DEBUG"):
        loglevel = logging.DEBUG

    if enable_elastic_logging:
        elastic_handler = ElasticClientHandler(
            client, index_name=index_name, document_labels={"app": app_name}, level=loglevel
        )
        elastic_handler.addFilter(ElasticModuleFilter())
        log_handlers.append(elastic_handler)

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=log_handlers,
    )


def get_elasticsearch_client(elastic_url: str, username: str, password: str) -> Elasticsearch:
    return Elasticsearch(elastic_url, basic_auth=(username, password), verify_certs=True)


class ElasticClientHandler(logging.Handler):
    """
    Log Handler that sends logs directly to an elastic index

    Does this by making an index call at the point of every logging call,
    if more throughput is needed use the Bulk Elastic handler
    """

    def __init__(
        self,
        client: Elasticsearch,
        index_name: str,
        document_labels: dict = None,
        level=logging.NOTSET,
    ):
        super().__init__(level)
        self.client = client
        self.index_name = index_name
        self.document_labels = document_labels
        self.addFilter(
            ElasticModuleFilter()
        )  # Need a filter here to prevent the elasticsearch module
        # from recursively sending logging calls

        # Create index if none exists
        try:
            self.client.indices.create(index=index_name)
        except BadRequestError:
            pass  # Index already exists so one doesn't have to be created

    def emit(self, record):
        formatted_data = self.format(record)
        logger.debug("Elastic handler emitting")

        # Explicitly handle messages where a CID field is not provided
        try:
            message_cid = record.cid
        except AttributeError:
            message_cid = None

        document = {"log_message": formatted_data, "cid": message_cid}

        if self.document_labels:
            document.update(self.document_labels)

        self.client.index(index=self.index_name, document=document)


class ElasticClientBulkHandler(ElasticClientHandler):
    """
    Log Handler that sends log messages to an elastic server.

    This handler uses batch methods to increase performance for applications with a lot of logs.
    Using this handler requires a call to `logging.shutdown`
    in your application entrypoint somewhere;
    the best way to implment that is using a `Try: Finally` block.
    If the logger isn't closed (either manually or via logging.shutdown),
    then the application might not be able to exit since the Elastic bulk
    client will continue to run a keep-alive thread until it is explicitly closed.
    """

    def __init__(
        self,
        client: Elasticsearch,
        index_name: str,
        document_labels: dict = None,
        level=logging.NOTSET,
        batch_size: int = 10,
        batch_time: float = 5.0,
    ):
        super().__init__(client, index_name, document_labels, level)
        self.batch_size = batch_size
        self.batch_time = batch_time
        self._queue = []
        self._batch_start_time = time.time()

        # Switching variable for using bulk, want to switch to single
        # requests during shutdown to avoid weird
        # hanging issues caused by leaving elastic messages on the bulk queue
        self._use_bulk = True

    def set_use_bulk(self, use_bulk):
        self._use_bulk = use_bulk

    def emit(self, record):
        formatted_data = self.format(record)
        logger.debug("Elastic handler emitting")

        # Explicitly handle messages where a CID field is not provided
        try:
            message_cid = record.cid
        except AttributeError:
            message_cid = None

        document = {"log_message": formatted_data, "cid": message_cid}

        if self.document_labels:
            document.update(self.document_labels)

        if self._use_bulk:
            document.update({"_index": self.index_name})
            self._queue.append(document)

            if len(self._queue) >= self.batch_size:
                self.flush()
            elif time.time() - self.batch_time >= self._batch_start_time:
                self.flush()
        else:
            self.client.index(index=self.index_name, document=document)

    def flush(self):
        logger.debug("Flushing")
        if self._queue and self._use_bulk:
            bulk(self.client, self._queue)
            logger.debug("Finished uploading to elastic")
        self._queue = []
        self._batch_start_time = time.time()
        super().flush()

    def close(self):
        logger.debug("Closing")
        self.flush()
        self.client.close()
        super().close()
