"""This module create and send request to MLManagement server."""
import atexit
import inspect
from contextlib import _GeneratorContextManager
from typing import Any, Dict, Optional

import cloudpickle

from ML_management.mlmanagement import variables
from ML_management.mlmanagement.base_exceptions import MLMServerError
from ML_management.mlmanagement.session import AuthSession
from ML_management.mlmanagement.variables import (
    active_run_stack,
    get_server_ml_api,
)
from ML_management.mlmanagement.visibility_options import VisibilityOptions
from mlflow import ActiveRun
from mlflow.entities import RunStatus
from mlflow.exceptions import MlflowException, RestException
from mlflow.models import Model
from mlflow.tracking import _RUN_ID_ENV_VAR
from mlflow.utils import env


def create_kwargs(frame):
    """Get name and kwargs of function by its frame."""
    function_name = inspect.getframeinfo(frame)[2]  # get name of function
    _, _, _, kwargs = inspect.getargvalues(frame)  # get kwargs of function
    kwargs.pop("self", None)
    kwargs.pop("parts", None)
    kwargs.pop("python_path", None)

    return (
        function_name,
        kwargs,
    )  # return name of mlflow function and kwargs for that function


def request(
    function_name,
    kwargs,
    url=None,
    stream=False,
) -> _GeneratorContextManager:
    """Create mlflow_request and send it to server."""
    mlflow_request = {
        "function_name": function_name,
        "kwargs": kwargs,
        "active_experiment": variables.active_experiment,
        "active_run_ids": [run.info.run_id for run in active_run_stack],
    }

    url = url if url is not None else get_server_ml_api()

    return AuthSession().post(url=url, stream=stream, json=mlflow_request)


def send_request_to_server(function_name, kwargs):
    """
    Send request to server.

    Takes frame of mlflow func and extra_attr
    extra_attr is needed if original mlflow function is in the mlflow.<extra_attr> package
    for example function log_model is in mlflow.pyfunc module (mlflow.pyfunc.log_model())
    """
    with request(function_name, kwargs) as response:
        response_content = response.content

        try:
            decoded_result = cloudpickle.loads(response_content)
        except Exception:
            raise MLMServerError(f"Server error: {response_content.decode()}, status: {response.status_code}") from None

        # raise error if mlflow is supposed to raise error
        if isinstance(decoded_result, MlflowException):
            is_rest = decoded_result.json_kwargs.pop("isRest", False)
            if is_rest:
                created_json = {
                    "error_code": decoded_result.error_code,
                    "message": decoded_result.message,
                }
                decoded_result = RestException(created_json)
            raise decoded_result
        elif isinstance(decoded_result, Exception):
            raise decoded_result
        return decoded_result


def _check_if_call_from_predict_function():
    """
    Check if call to server was from predict function of model.

    Calls from predict function are prohibited and will do and return nothing.
    """
    from ML_management.model.model_type_to_methods_map import ModelMethodName
    from ML_management.model.patterns.model_pattern import Model

    predict_func_name = ModelMethodName.predict_function.name

    for frame in inspect.stack():
        if frame.function == predict_func_name and Model in frame[0].f_locals.get("self").__class__.__mro__:
            return True
    return False


def request_for_function(frame):
    """
    Send request to server or call mlflow function straightforward.

    Input parameters:
    :param frame: frame of equivalent mlflow function
    :param extra_attrs: list of extra modules for mlflow library, for example "tracking" (mlflow.tracking)
    :param class_name: the name of the class whose function is being called
    """
    if _check_if_call_from_predict_function():
        return None

    function_name, kwargs = create_kwargs(frame)

    return send_request_to_server(function_name, kwargs)


def set_experiment(
    experiment_name: str,
    visibility: VisibilityOptions = VisibilityOptions.PRIVATE,
) -> dict:
    """
    Set the given experiment as the active experiment.

    The experiment must either be specified by name via
    experiment_name.
    Set global variable active_experiment_name to that experiment_name.
    """
    variables.active_experiment = request_for_function(inspect.currentframe())
    return variables.active_experiment


def start_run(
    experiment_id: Optional[str] = None,
    run_name: Optional[str] = None,
    nested: bool = False,
    tags: Optional[Dict[str, Any]] = None,
) -> ActiveRun:
    """
    Start a new MLflow run, setting it as the active run under which metrics and parameters will be logged.

    The return value can be used as a context manager within a with block; otherwise, you must call end_run() to
    terminate the current run.
    If you pass a run_id or the MLFLOW_RUN_ID environment variable is set, start_run attempts to resume a run with
    the specified run ID and other parameters are ignored. run_id takes precedence over MLFLOW_RUN_ID.
    If resuming an existing run, the run status is set to RunStatus.RUNNING.
    Add that created run to active_run_stack.
    """
    if len(active_run_stack) > 0 and not nested:
        raise Exception(
            (
                "Run with UUID {} is already active. To start a new run, first end the "
                "current run with mlmanagement.end_run(). To start a nested "
                "run, call start_run with nested=True"
            ).format(active_run_stack[0].info.run_id)
        )
    _active_run = request_for_function(inspect.currentframe())
    active_run_stack.append(_active_run)
    return _active_run


def active_run() -> Optional[ActiveRun]:
    """Get the currently active Run, or None if no such run exists."""
    return active_run_stack[-1] if len(active_run_stack) > 0 else None


finished_run_status = RunStatus.to_string(RunStatus.FINISHED)


def end_run(status: str = finished_run_status) -> None:
    """End an active MLflow run (if there is one)."""
    if len(active_run_stack) > 0:
        # Clear out the global existing run environment variable as well.
        env.unset_variable(_RUN_ID_ENV_VAR)
        run = active_run_stack[-1]
        set_terminated(run.info.run_id, status)
        active_run_stack.pop()


atexit.register(end_run)


def set_terminated(run_id: str, status: Optional[str] = None, end_time: Optional[int] = None) -> None:
    """Set a run’s status to terminated."""
    return request_for_function(
        inspect.currentframe(),
    )


default_model = Model()


def _exit(self, exc_type, exc_val, exc_tb):
    """Redefine __exit__ function of class ActiveRun."""
    status = RunStatus.FINISHED if exc_type is None else RunStatus.FAILED
    end_run(RunStatus.to_string(status))
    return exc_type is None


# Rewrite __exit__ method to enable using Python ``with`` syntax of ActiveRun class.
ActiveRun.__exit__ = _exit


def start_run_if_not_exist():
    """If run doesn't exist call start_run() function."""
    if len(active_run_stack) == 0:
        start_run()
