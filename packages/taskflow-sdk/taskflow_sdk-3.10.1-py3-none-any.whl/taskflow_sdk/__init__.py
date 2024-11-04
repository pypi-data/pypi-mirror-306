import logging

import taskflow_sdk.cli
import taskflow_sdk.version
import taskflow_sdk.plugin
from taskflow_sdk.interfaces import Tracker, Action, ActionExecutionRejection  # noqa: F401
from taskflow_sdk.forms import ValidationAction, FormValidationAction  # noqa: F401

logger = logging.getLogger(__name__)

__version__ = taskflow_sdk.version.__version__

if __name__ == "__main__":
    import taskflow_sdk.__main__

    taskflow_sdk.__main__.main()
