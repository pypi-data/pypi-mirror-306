from typing import Literal, Dict
from functools import wraps
from crimson.executable_types_beta.data_model import ExecutionResult
from crimson.auto_pydantic import generate_inputprops_model

from crimson.executable_types_beta.utils import (
    delegate_func_returning_args_details,
    push_execution_result,
    generate_meta_dict,
    get_meta_annotations,
    GenerateMetaDict,
    GetMetaAnnotations,
    PushExecutionResult,
)
from crimson.executable_types_beta.test import test_meta_dict


class AnnotationExecutor:
    mode: Literal["on", "off"] = "on"
    raise_error: bool = True
    push_result: bool = False
    env = {}

    last_execution_result: ExecutionResult
    execution_results: Dict[str, ExecutionResult] = {}

    get_meta_annotations = get_meta_annotations
    push_execution_result = push_execution_result
    generate_meta_dict = generate_meta_dict

    @staticmethod
    def get_field(name: Literal["last_execution_result", "execution_results"]):
        """
        Fields:
                last_execution_result: ExecutionResult = Last `ExecutionResult`
                execution_results: Dict[str, ExecutionResult] = Pushed `ExecutionResult`s by `push_execution_result` function.
        """
        return getattr(name)

    @staticmethod
    def with_executable(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if AnnotationExecutor.mode == "off":
                return AnnotationExecutor.wrapper_off(func, *args, **kwargs)
            elif AnnotationExecutor.mode == "on":
                return AnnotationExecutor.wrapper_on(func, *args, **kwargs)

        return wrapper

    @staticmethod
    def wrapper_off(func, *args, **kwargs):
        return func(*args, **kwargs)

    @staticmethod
    def wrapper_on(func, *args, **kwargs):
        meta_annotations = AnnotationExecutor.get_meta_annotations(func)

        output, args_details, args_fields = delegate_func_returning_args_details(
            func, AnnotationExecutor.env, *args, **kwargs
        )

        meta_dict = AnnotationExecutor.generate_meta_dict(
            args_details, meta_annotations, args_fields
        )
        test_result = test_meta_dict(meta_dict, meta_annotations)

        last_execution_result = ExecutionResult(
            meta_annotations=meta_annotations,
            args_detail=args_details,
            meta_dict=meta_dict,
            test_result=test_result,
        )

        if AnnotationExecutor.push_result is True:
            AnnotationExecutor.push_execution_result(
                func, AnnotationExecutor.execution_results, last_execution_result
            )

        AnnotationExecutor.last_execution_result = last_execution_result

        if AnnotationExecutor.raise_error is True:
            for result in test_result.values():
                if result is False:
                    raise Exception(
                        "test_meta_dict failed. Check fields in AnnotationExecutor.test_result."
                    )
        return output

    @staticmethod
    def set_config(
        mode: Literal["on", "off"] | None = None,
        raise_error: bool | None = None,
        push_result: bool | None = None,
    ):
        """
        Arguments:
                mode: If `on`, the annotation codes are executed.
                raise_error: If True, the failure of the test raise an error.
                push_result: If True, the tested results are stored to AnnotationExecutor.execution_results. It depends on the `push_execution_result` function
        """
        args = {"mode": mode, "raise_error": raise_error, "push_result": push_result}

        for key, value in args.items():
            if value is not None:
                setattr(AnnotationExecutor, key, value)

    @staticmethod
    def set_functions(
        get_meta_annotations: GetMetaAnnotations = None,
        push_execution_result: PushExecutionResult = None,
        generate_meta_dict: GenerateMetaDict = None,
    ):
        """
        The main purpose of this function is to expose the functions, that are recommended to customize if you want more flexible experience.

        While the roles of `GetMetaAnnotations_` and `GenerateMetaDict_` functions are clear, <br/>
        the implementation of them won't be that simple.

        Before you try the customization, you might need to study <br/>
        what the default `ArgsDetails_`, `MetaAnnotations_`, `MetaDict_` and `ExecutionResult` look like.
        """
        inputs = {
            "get_meta_annotations": get_meta_annotations,
            "push_execution_result": push_execution_result,
            "generate_meta_dict": generate_meta_dict,
        }

        for key, value in inputs.items():
            if value is not None:
                setattr(AnnotationExecutor, key, value)


with_executable = AnnotationExecutor.with_executable
