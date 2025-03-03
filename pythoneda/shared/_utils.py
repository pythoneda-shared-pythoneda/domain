# vim: set fileencoding=utf-8
"""
pythoneda/shared/_utils.py

This script defines some utility functions.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythonlang/domain

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import inspect
import re
from typing import Type


def full_class_name(target: Type = None) -> str:
    """
    Retrieves the full class name of given class.
    :param target: The class. If omitted, this very class.
    :type target: Class
    :return: The key.
    :rtype: str
    """
    actual_target = target
    if actual_target is None:
        actual_target = cls
    return f"{actual_target.__module__}.{actual_target.__name__}"


def snake_to_camel(inputText: str) -> str:
    """
    Converts a string in snake case to camel case.
    :param inputText: The snake-case input to convert.
    :type inputText: str
    :return: The camel-case version of the input.
    :rtype: str
    """
    components = inputText.split("_")
    return "".join(x.title() for x in components)


def camel_to_snake(inputText: str) -> str:
    """
    Converts a string in camel case, to snake case.
    :param inputText: The camel-case input to convert.
    :type inputText: str
    :return: The snake-case version of the input.
    :rtype: str
    """
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", inputText).lower()


def kebab_to_camel(txt: str) -> str:
    """
    Transforms given kebab-case value to camel case.
    :param txt: The value.
    :type txt: str
    :return: The value formatted in camel case.
    :rtype: str
    """
    words = txt.split("-")
    result = "".join(word.capitalize() for word in words)
    return result[0].lower() + result[1:]


def camel_to_kebab(txt: str) -> str:
    """
    Transforms given camel-case value to kebab case.
    :param txt: The value.
    :type txt: str
    :return: The value formatted in kebab case.
    :rtype: str
    """
    # Use regular expression to find capital letters and prepend them with a hyphen
    result = re.sub("([a-z0-9])([A-Z])", r"\1-\2", txt)
    # Convert the string to lowercase
    return result.lower()


def kebab_to_snake(txt: str) -> str:
    """
    Transforms given kebab-case value to snake case.
    :param txt: The value.
    :type txt: str
    :return: The value formatted in snake case.
    :rtype: str
    """
    return camel_to_snake(kebab_to_camel(txt))


def snake_to_kebab(txt: str) -> str:
    """
    Transforms given snake-case value to kebab case.
    :param txt: The value.
    :type txt: str
    :return: The value formatted in kebab case.
    :rtype: str
    """
    return camel_to_kebab(snake_to_camel(txt))


def simplify_class_name(inputText: str) -> str:
    """
    Simplifies given class name to remove the module if it's just a snake-case version of the actual class name.
    :param inputText: The class name to simplify.
    :type inputText: str
    :return: The simplified class name, or the input if it doesn't need to be simplified.
    :rtype: str
    """
    result = inputText
    if "." in inputText:
        # If there's no dot, it's not a fully qualified class name

        module_name, class_name = inputText.rsplit(".", 1)

        # Extract the last part of the module path (if it exists)
        last_module_name = (
            module_name.split(".")[-1] if "." in module_name else module_name
        )

        # Convert the last part of the module path to CamelCase
        camel_case_last_module = snake_to_camel(last_module_name)

        # Check if the class name is the CamelCase version of the last part of the module name
        if class_name == camel_case_last_module:
            # Remove the last part of the module name and append the class name
            result = ".".join(module_name.split(".")[:-1] + [class_name])

    return result


def has_method(cls, methodName: str) -> bool:
    """
    Checks if this class defines a given method or not.
    :param methodName: The method name.
    :type methodName: str
    :return: True if the class defines that method.
    :rtype: bool
    """
    return hasattr(cls, methodName) and callable(getattr(cls, methodName))


def has_class_method(cls, methodName: str) -> bool:
    """
    Checks if this class defines a given class method or not.
    :param methodName: The method name.
    :type methodName: str
    :return: True if the class defines that class method.
    :rtype: bool
    """
    result = False
    if has_method(cls, methodName):
        method = getattr(cls, methodName)
        result = isinstance(method, classmethod)
    return result


def sort_by_priority(otherClass) -> int:
    """
    Delegates the priority information to given primary port.
    :param otherClass: The primary port.
    :type otherClass: pythoneda.Port
    :return: Such priority.
    :rtype: int
    """
    return Ports.sort_by_priority(otherClass)


def method_has_no_parameters(cls, methodName: str) -> bool:
    """
    Checks if this class defines given method, and it doesn't define parameters.
    :return: True in such case.
    :rtype: bool
    """
    result = False
    if has_method(cls, methodName):
        method = getattr(cls, methodName)
        init_signature = inspect.signature(method)

        first_parameter = "self"
        if isinstance(method, classmethod):
            first_parameter = "cls"

        # Check if all parameters except 'self' (or 'cls' if class method) have defaults
        parameters = init_signature.parameters.values()
        result = all(
            p.default is not inspect.Parameter.empty or p.name == first_parameter
            for p in parameters
        )

    return result


def method_has_one_parameter(cls, methodName: str, paramType: Type) -> bool:
    """
    Checks if the given class defines a method with the specified name and if
    that method accepts exactly one parameter of the given type (excluding 'self').

    :param cls: The class to inspect.
    :param methodName: The name of the method to check.
    :param paramType: The type of the single parameter to verify.
    :return: True if the method exists, has one parameter of the specified type, False otherwise.
    """
    try:
        # Get the method from the class
        method = getattr(cls, methodName, None)
        if method is None:
            return False  # Method doesn't exist

        # Get the signature of the method
        sig = inspect.signature(method)
        params = list(sig.parameters.values())

        # Check for exactly one parameter (excluding 'self')
        if len(params) == 2:  # 'self' + one other parameter
            param = params[1]  # The actual parameter (after 'self')
            # Check the parameter's type annotation
            return param.annotation == paramType
        return False
    except (AttributeError, ValueError):
        # Handle cases where the method or signature cannot be retrieved
        return False

    return result


def has_default_constructor(cls) -> bool:
    """
    Checks if this class defines the default constructor or not.
    :return: True in such case.
    :rtype: bool
    """
    init_signature = inspect.signature(cls.__init__)

    # Check if all parameters except 'self' have defaults
    parameters = init_signature.parameters.values()
    result = all(
        p.default is not inspect.Parameter.empty or p.name == "self" for p in parameters
    )

    return result


def has_one_param_constructor(cls, paramType):
    try:
        constructor = cls.__init__
        sig = inspect.signature(constructor)
        params = list(sig.parameters.values())
        # Check if there's one parameter other than 'self' and it matches the type
        if len(params) == 2:  # 'self' + one other parameter
            param = params[1]
            return param.annotation == paramType
        return False
    except AttributeError:
        # No __init__ method
        return False


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
