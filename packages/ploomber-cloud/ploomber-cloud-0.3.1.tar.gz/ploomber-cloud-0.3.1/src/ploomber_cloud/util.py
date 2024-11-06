import re
import sys
import functools
from pathlib import Path
from click import exceptions as click_exceptions
from ploomber_cloud import exceptions
import click
import shutil
from enum import Enum
from typing import Type, Union
import os
from zipfile import ZipFile
from typing import Iterator
import itertools
import threading
import time
from contextlib import contextmanager

from ploomber_cloud.api import PloomberCloudClient
from ploomber_cloud.messages import FEATURE_PROMPT_MSG
from ploomber_cloud.models import UserTiers


def requires_init(func):
    """
    Wrapper around a function that checks and prompts if necessary
    for project initialization
    """
    from ploomber_cloud import init

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check for init, if not, prompt and run init flow
        if not Path("ploomber-cloud.json").exists():
            run_init = click.confirm(
                "Project must be initialized to continue. Would you like to initialize?"
            )

            if not run_init:
                raise exceptions.BasePloomberCloudException(
                    "This command requires a ploomber-cloud.json file.\n"
                    "Run 'ploomber-cloud init' to initialize your project."
                )

            init.init(from_existing=False, force=False, verbose=False)

        return func(*args, **kwargs)

    return wrapper


def _get_allowed_features_for_user_type(user_type: UserTiers):
    """
    This function returns the allowed features for the current user type.
    """
    from ploomber_cloud import resources

    return resources._get_resource_config_for_user_type(user_type)["allowedFeatures"]


def requires_permission(permissions: Union[list[str], str]):
    """
    Decorator that restricts function execution based on user permissions.

    This decorator checks if the user invoking the wrapped function has the required
    permissions. It can handle either a single permission string or a list of
    permission strings.

    Params:
        permissions (Union[list[str], str]): A single permission string or a list of
            permission strings that are required to execute the wrapped function.

    Returns:
        Callable: A decorator function.

    Raises:
        exceptions.UserTierForbiddenException: If the user doesn't have one or more
            of the required permissions.

    Usage:
        @requires_permission("read_data")
        def read_sensitive_data():
            ...

        @requires_permission(["write_data", "delete_data"])
        def modify_data():
            ...

    Note:
        If an empty list or None is passed as the permissions argument, the wrapped
        function will execute without any permission checks.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not permissions:
                return func(*args, **kwargs)

            allowed_features = _get_allowed_features_for_user_type(get_user_type())

            if isinstance(permissions, str):
                required_permissions = [permissions]
            else:
                required_permissions = permissions

            failed_permissions = []
            for permission in required_permissions:
                if permission not in allowed_features:
                    failed_permissions.append(permission)

            if failed_permissions:
                raise exceptions.UserTierForbiddenException(failed_permissions)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_user_type() -> UserTiers:
    client = PloomberCloudClient()
    user_info = client.me()["_model"]
    return UserTiers(user_info["type"])


def get_user_types_with_allowed_permission(permission: Union[str, list[str]]):
    """
    This function returns a list of user types that have the specified permission(s).

    Params
    """
    if isinstance(permission, str):
        permission = [permission]

    allowed_user_types: list[UserTiers] = []
    for user_type in UserTiers:
        allowed_features = _get_allowed_features_for_user_type(user_type)
        if all(perm in allowed_features for perm in permission):
            allowed_user_types.append(user_type)
    return allowed_user_types


def underscore(word: str) -> str:
    """
    Make an underscored, lowercase form from the expression in the string.
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", word)
    word = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", word)
    word = word.replace("-", "_")
    return word.lower()


def humanize(word: str) -> str:
    """
    Capitalize the first word and turn underscores into spaces and strip a
    trailing ``"_id"``, if any. Like :func:`titleize`, this is meant for
    creating pretty output.
    """
    word = re.sub(r"_id$", "", word)
    word = word.replace("_", " ")
    word = re.sub(r"(?i)([a-z\d]*)", lambda m: m.group(1).lower(), word)
    word = re.sub(r"^\w", lambda m: m.group(0).upper(), word)
    return word


def camel_case_to_human_readable(camel_case_text: str) -> str:
    return humanize(underscore(camel_case_text))


def pretty_print(
    obj: list, delimiter: str = ",", last_delimiter: str = "and", repr_: bool = False
) -> str:
    """
    Returns a formatted string representation of an array
    """
    if repr_:
        sorted_ = sorted(repr(element) for element in obj)
    else:
        sorted_ = sorted(f"'{element}'" for element in obj)

    if len(sorted_) > 1:
        sorted_[-1] = f"{last_delimiter} {sorted_[-1]}"

    return f"{delimiter} ".join(sorted_)


def raise_error_on_duplicate_keys(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    duplicate_keys = []
    for k, v in ordered_pairs:
        if k in d:
            duplicate_keys.append(k)
        else:
            d[k] = v
    if duplicate_keys:
        raise ValueError(f"Duplicate keys: {pretty_print(duplicate_keys)}")
    return d


def prompt_for_choice_from_list(
    choices, initial_prompt, index=False, ignore_case=False
):
    """Prompt a user to choose from options in a list format"""
    choices.append("exit")
    if ignore_case:
        choices = [c.lower() for c in choices]
    prompt = []
    for i, item in enumerate(choices):
        prompt.append(f"  {i + 1}. {item}\n")

    prompt.append(initial_prompt)

    prompt_str = "".join(prompt)
    choice = None

    # Prompt user for choice
    while True:
        choice = click.prompt(prompt_str, type=str)
        if ignore_case:
            choice = choice.lower()
        # Case: user enters number
        if choice.isnumeric() and 0 < int(choice) <= len(choices):
            choice = choices[int(choice) - 1]
            break
        elif choice in choices:  # Case: user enters id
            break
        else:  # Case: user enters invalid
            click.echo("Please enter a valid choice.")

    if choice == "exit":
        click.echo("Exited.")
        raise click_exceptions.Exit()

    if index:
        return choices.index(choice)

    return choice


def print_divider():
    """Print a horizontal line the width of the terminal"""
    w, _ = shutil.get_terminal_size()
    click.echo("—" * w)


def get_project_details_mappings(projects):
    """Function for returning lookup of:
    1. Project ID that is displayed to the user and its original ID.
       Projects with custom name are displayed as project id (custom name).
    2. Project custom names and the corresponding ID.
    """

    display_id_mapping = {}
    project_name_mapping = {}

    for project in projects:
        pid = display_id = project["id"]
        name = project["name"]
        if name and pid != name:
            display_id = f"{pid} ({name})"
        display_id_mapping[display_id], project_name_mapping[name] = pid, pid

    return display_id_mapping, project_name_mapping


def prompt_for_feature(feature_enum: Type[Enum]):
    """
    Helper function to help prompt for a feature

    Params:
    _______
    - feature_enum: Type[Enum]
        Enum class with the features to choose from
    """

    click.echo(
        FEATURE_PROMPT_MSG
    )  # use echo since capsys doesn't capture the prompt output
    feature = prompt_for_choice_from_list(
        [feature.value for feature in feature_enum], ""
    )
    return feature


class Spinner:
    def __init__(self, message=""):
        self.message = message
        self.stop_event = threading.Event()

    def spin(self):
        spinner = itertools.cycle(["-", "/", "|", "\\"])
        while not self.stop_event.is_set():
            sys.stdout.write(f"\r{next(spinner)} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)

    def start(self):
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()


@contextmanager
def spinner(message=""):
    s = Spinner(message)
    s.start()
    try:
        yield
    finally:
        s.stop()


def write_project_to_disk(stream: Iterator[bytes], download_path: Path) -> str:
    """
    Process and write the response stream of an HTTP request to disk,
    then extract the contents.

    Params:
    _______
    - stream: Iterator[bytes]
        An iterator yielding bytes of the zip file content.
    - download_path: Path
        The path where the project will be downloaded and extracted.

    Returns:
    ________
    str
        The path to the extracted project directory.

    Raises:
    _______
    OSError:
        If there's an error creating directories, writing files, or extracting the zip.
    """
    target_dir = os.path.abspath(os.path.join(os.getcwd(), download_path))
    zip_path = os.path.join(target_dir, "project.zip")

    try:
        os.makedirs(target_dir, exist_ok=True)

        with open(zip_path, "wb") as f:
            for chunk in stream:
                f.write(chunk)

        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(target_dir)

        os.remove(zip_path)

        return target_dir

    except OSError as e:
        # Clean up if an error occurs
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        raise OSError(f"Error processing project files: {str(e)}")
