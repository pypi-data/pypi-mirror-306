from typing import List, Tuple, Dict, Any
import ast
import os
import shutil
import re
import traceback
import inspect

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

from owlsight.utils.logger_manager import LoggerManager

logger = LoggerManager.get_logger(__name__)


def extract_markdown(md_string: str) -> List[Tuple[str, str]]:
    """
    Extract language and code blocks from a markdown string.
    """
    pattern = r"```(\w+)([\s\S]*?)```"
    return [(match[0].strip(), match[1].strip()) for match in re.findall(pattern, md_string)]


def replace_bracket_placeholders(text: str, var_dict: Dict[str, Any]) -> str:
    """
    Evaluates python expressions in the form of `{{}}` in the given text and replaces them with the result.
    Supports method calls and simple expressions.

    Parameters
    ----------
    text : str
        The input string that contains placeholders in the form of `{{}}`.
    var_dict : dict
        A dictionary where keys correspond to the placeholders and values are the replacements.

    Returns
    -------
    str
        The input string with placeholders replaced by corresponding values from the dictionary.

    Examples
    --------
    >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    >>> var_dict = {'df': df, 'name': 'Alice', 'age': 30}
    >>> replace_bracket_placeholders("{{name}} is {{age}} years old. DataFrame mean: {{df.mean()}}", var_dict)
    'Alice is 30 years old. DataFrame mean: A    2.0\nB    5.0\ndtype: float64'
    >>> replace_bracket_placeholders("1 + 1 = {{1+1}}", var_dict)
    '1 + 1 = 2'
    """

    # def evaluate_expression(expr: str) -> Any:
    #     return eval(expr, {"__builtins__": None}, var_dict)

    def evaluate_expression(expr: str) -> Any:
        try:
            return eval(expr, {"__builtins__": None}, var_dict)
        except Exception as e:
            error_message = f"Error evaluating '{expr}': {str(e)}"
            raise type(e)(error_message) from None

    # Pattern to match content inside {{ }}
    pattern = r"\{\{(.*?)\}\}"

    # Find all placeholders
    placeholders = re.findall(pattern, text)

    # Replace each placeholder with the evaluated expression
    for placeholder in placeholders:
        evaluated = evaluate_expression(placeholder)
        text = text.replace(f"{{{{{placeholder}}}}}", str(evaluated))

    return text


def editable_input(prompt_text: str, default_value: str, color: str = "ansicyan") -> str:
    """
    Displays a prompt with a pre-filled editable string and custom color for the default value.

    Parameters
    ----------
    prompt_text : str
        The prompt message shown before the editable string.
    default_value : str
        The string that will be pre-filled and editable by the user.
    color : str, optional
        The color to apply to the default value in the prompt message, default is 'ansicyan'.

    Examples
    --------
    >>> editable_input("Enter your name: ", "John")
    Enter your name: "John" -> Enter your name: "Johnny"
    'Johnny'

    Returns
    -------
    str
        The string edited by the user.
    """
    style = Style.from_dict({"prompt_text": color})

    # Prepare the prompt text with custom color using HTML
    formatted_prompt = HTML(f"<ansicyan>{prompt_text}</ansicyan>")

    # Get the result from the prompt (default value is shown but not styled)
    result = prompt(formatted_prompt, default=default_value, style=style)

    return result.strip()


def force_delete(temp_dir: str) -> None:
    """Forcefully deletes a directory if it exists."""
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            logger.error(f"Error deleting directory {temp_dir}:\n{traceback.format_exc()}")


def remove_temp_directories(lib_path: str) -> None:
    """Removes lingering temporary directories in the virtual environment's library path."""
    for d in os.listdir(lib_path):
        if d.startswith("tmp"):
            logger.info(f"Removing temporary directory: {d}")
            force_delete(os.path.join(lib_path, d))


def format_error_message(e: Exception) -> str:
    """
    Format an error message to be displayed to the user.

    Parameters
    ----------
    error : Exception
        The exception that occurred.

    Returns
    -------
    str
        The formatted error message.
    """
    return "{e.__class__.__name__}: {e}".format(e=e)


def convert_to_real_type(value):
    """
    Convert a string to its real type if possible (e.g., 'True' -> True, '3.14' -> 3.14).
    """
    if not isinstance(value, str):
        return value

    # Try to evaluate the string and return the result only if it's not a string
    try:
        evaluated_value = ast.literal_eval(value)
        # Only return the evaluated value if it is not a string
        if not isinstance(evaluated_value, str):
            return evaluated_value
    except (ValueError, SyntaxError):
        pass  # Return original string if evaluation fails

    return value  # Return the original string if it's not evaluable


def os_is_windows():
    return os.name == "nt"


def check_invalid_input_parameters(func: callable, kwargs: dict):
    """
    Validate the keyword arguments passed to a class against the __init__ signature.

    Parameters
    ----------
    func : callable
        The callable of which arguments are being validated.
    kwargs : dict
        A dictionary of keyword arguments to validate.

    Raises
    ------
    ValueError
        If there are invalid parameters.
    """
    # Extract the parameters from the __init__ method of the class
    sig = inspect.signature(func)
    sig_params = sig.parameters

    valid_params = [param_name for param_name in sig_params if param_name != "self"]

    # Check for any extra parameters in kwargs that are not in the __init__ signature
    for key in kwargs:
        if key not in sig_params:
            raise ValueError(
                f"Invalid argument: '{key}' is not a valid parameter for '{func.__name__}'\nValid parameters: {valid_params}"
            )


def flatten_dict(d, parent_key="", sep=".") -> dict:
    """Flatten a nested dictionary."""
    flattened = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            flattened.update(flatten_dict(v, new_key, sep=sep))
        else:
            flattened[new_key] = v
    return flattened
