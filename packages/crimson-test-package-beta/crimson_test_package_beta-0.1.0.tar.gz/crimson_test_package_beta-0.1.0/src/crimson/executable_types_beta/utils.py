from typing import Any, List, Dict, Tuple, Callable
from crimson.ast_dev_tool import collect_nodes

# from crimson.executable_types_beta.mock import TensorMock
from crimson.auto_pydantic.generator_model import (
    generate_inputprops_model,
)
import ast
from inspect import currentframe
from types import FunctionType
from crimson.executable_types_beta.types import (
    ArgsDetails_,
    MetaAnnotations_,
    ArgumentName_,
    MetaDict_,
    MetaAnnotation_,
)
from crimson.executable_types_beta.data_model import ExecutionResult
from pydantic import BaseModel
from pydantic.fields import FieldInfo


def delegate_func_returning_args_details(
    func: FunctionType, env: Dict[str, Any] = {}, *args, **kwargs
) -> Tuple[Any, ArgsDetails_[Dict[str, Any]], Dict[str, FieldInfo]]:

    Model = generate_inputprops_model(func, currentframe(), env, *args, **kwargs)
    output = func(*args, **kwargs)
    model: BaseModel = Model(*args, **kwargs)
    args_details = model.__dict__
    args_details["return"] = output

    return output, args_details, model.model_fields


# Customization recommended
def push_execution_result(
    func: FunctionType,
    execution_results: Dict[str, ExecutionResult],
    execution_result: ExecutionResult,
    *args,
    **kwargs
):
    execution_results[func.__name__] = execution_result


def get_names(meta_annotation: MetaAnnotation_[List[str]]):
    names = []
    for unit in meta_annotation:
        name = collect_nodes(unit, ast.Name)[0].id
        names.append(name)
    return names


# Customization recommended
def generate_meta_dict(
    args_details: ArgsDetails_[Dict[str, Any]],
    meta_annotations: MetaAnnotations_[
        Dict[ArgumentName_[str], MetaAnnotation_[List[str]] | None]
    ],
    args_fields: Dict[str, FieldInfo] = {},
) -> MetaDict_[Dict[str, int]]:
    """
    You will want to implement this by yourself,
    for your customized use.
    """
    meta_dict = {}
    for name, arg in args_details.items():
        meta_annotation = meta_annotations[name]
        if meta_annotation is not None:
            names = get_names(meta_annotation=meta_annotation)
            for shape_unit, name in zip(arg.shape, names):
                if name not in meta_dict.keys():
                    meta_dict[name] = shape_unit
                else:
                    if meta_dict[name] != shape_unit:
                        raise Exception(
                            "Shape Units sharing same name don't have the same value."
                        )
    return meta_dict


def get_meta_annotation(
    subscript_node: ast.Subscript | Any,
) -> MetaAnnotation_[List[str]] | None:
    meta_annotation = []

    if not isinstance(subscript_node, ast.Subscript):
        return None

    if isinstance(subscript_node.slice, ast.Tuple):
        tuple_node = subscript_node.slice
        for elt in tuple_node.elts:
            if isinstance(elt, ast.Constant):
                meta_annotation.append(elt.value)
        return meta_annotation


# Customization recommended
def get_meta_annotations(
    func: ast.FunctionType,
) -> MetaAnnotations_[Dict[ArgumentName_[str], MetaAnnotation_[List[str] | None]]]:
    meta_annotations = {}
    func_node = collect_nodes(func, ast.FunctionDef)[0]
    arg_nodes = collect_nodes(func, ast.arg)
    for arg_node in arg_nodes:
        meta_annotations[arg_node.arg] = get_meta_annotation(arg_node.annotation)

    if hasattr(func_node, "returns"):
        meta_annotations["return"] = get_meta_annotation(func_node.returns)

    return meta_annotations


def get_return_meta_annotation(func: FunctionType):
    func_node = collect_nodes(func, ast.FunctionDef)[0]
    if hasattr(func_node, "returns"):
        meta_node = collect_nodes(func_node.returns, ast.Tuple)[0]
        constant_nodes = collect_nodes(meta_node, ast.Constant)
    meta_annotation = []
    for meta in constant_nodes:
        meta_annotation.append(meta.value)
    return meta_annotation


class GetMetaAnnotations(
    Callable[
        [FunctionType],
        MetaAnnotations_[Dict[ArgumentName_[str], MetaAnnotation_[List[str] | None]]],
    ]
):
    """
    ``` python
    GetMetaAnnotations_[Callable[
        [FunctionType],
        MetaAnnotations_[Dict[ArgumentName_[str], MetaAnnotation_[List[str] | None]]],
    ]]
    ```

    I need some args, and comparison expressions,
    in order to define tests to be executed by `AnnotationExecutor`.

    This function extracts the `str` type values in annotated types.

    """

    default = get_meta_annotations


class PushExecutionResult(
    Callable[[FunctionType, Dict[str, ExecutionResult], ExecutionResult], None]
):
    """
    ``` python
    PushExecutionResult_[Callable[[FunctionType, Dict[str, ExecutionResult], ExecutionResult], None]]
    ```

    `ExecutionResult` has the `custom_meta` field. <br/>
    If you want a customized `ExecutionResult`, you might customize the `push_execution_result` function.
    """

    default = push_execution_result


class GenerateMetaDict(
    Callable[
        [
            ArgsDetails_[Dict[str, Any]],
            MetaAnnotations_[
                Dict[ArgumentName_[str], MetaAnnotation_[List[str]] | None]
            ],
        ],
        MetaDict_[Dict[str, int]],
    ]
):
    """
    ``` python
    GenerateMetaDict[
        Callable[
            [
                ArgsDetails_[Dict[str, Any]],
                MetaAnnotations_[
                    Dict[ArgumentName_[str], MetaAnnotation_[List[str]] | None]
                ],
            ],
            MetaDict_[Dict[str, int]],
        ]
    ]
    ```

    It integrates the `ArgDetails_` and 'MetaAnnotation_`s.
    It means that, you will get all the information you want from the args in a function.

    I don't prefer to generalize the `test_meta_dict` function, which works based on the comparison expressions.

    You can instead customize this function.
    """

    default = generate_meta_dict
