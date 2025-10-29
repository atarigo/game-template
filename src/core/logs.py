import logging

import structlog


def format_callsite(logger, method_name, event_dict: dict) -> dict:
    """
    1. remove module, func_name, lineno from event_dict
    2. add callsite if not present
    """

    module = event_dict.pop("module", "")
    func_name = event_dict.pop("func_name", "")
    lineno = event_dict.pop("lineno", "")

    if "callsite" not in event_dict:
        event_dict["callsite"] = f"{module}.{func_name}:{lineno}"

    return event_dict


def configure(level: int = logging.DEBUG) -> None:
    logging.getLogger().handlers.clear()

    # todo: update settings for production
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    structlog.processors.CallsiteParameter.MODULE,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ],
            ),
            format_callsite,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
