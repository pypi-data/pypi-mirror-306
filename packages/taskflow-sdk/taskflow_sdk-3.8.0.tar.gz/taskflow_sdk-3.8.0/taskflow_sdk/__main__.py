import logging

from taskflow_sdk import utils
from taskflow_sdk.endpoint import create_argument_parser, run
from taskflow_sdk.constants import APPLICATION_ROOT_LOGGER_NAME
from taskflow_sdk.tracing.utils import get_tracer_provider


def main_from_args(args):
    """Run with arguments."""
    logging.getLogger("matplotlib").setLevel(logging.WARN)

    utils.configure_colored_logging(args.loglevel)
    utils.configure_file_logging(
        logging.getLogger(APPLICATION_ROOT_LOGGER_NAME),
        args.log_file,
        args.loglevel,
        args.logging_config_file,
    )
    utils.update_sanic_log_level()
    tracer_provider = get_tracer_provider(args)

    run(
        args.actions,
        args.port,
        args.cors,
        args.ssl_certificate,
        args.ssl_keyfile,
        args.ssl_password,
        args.auto_reload,
        tracer_provider,
    )


def main():
    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    main_from_args(cmdline_args)


if __name__ == "__main__":
    main()
