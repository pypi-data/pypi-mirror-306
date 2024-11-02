from typing import Any, List, Dict, Callable
from crimson.types_beta.addon import TypesPack, T


class MetaAnnotation_(List[str], TypesPack[T]):
    """
    ``` python
    MetaAnnotation_[List[str]]
    ```
    ---
    MetaAnnotation: The string values in the subscription of the annotated type<br/>
    MetaAnnotation is ["meta_info1", "meta_info2"] in the example below:

    ``` python
    arg: CustomType[List[str], "meta_info1", "meta_info2"]
    ```
    """


class ArgumentName_(str, TypesPack[T]):
    """
    ---
    ``` python
    ArgumentName_[str]
    ```
    ---
    The name of an argument your target function uses.
    """


class MetaAnnotations_(
    Dict[ArgumentName_[str], MetaAnnotation_[List[str]] | None], TypesPack[T]
):
    """
    ---
    ``` python
    MetaAnnotations_[Dict[ArgumentName_[str], MetaAnnotation_[List[str]] | None]]
    ```
    ---
    Each argument of your target function can have its own `MetaAnnotation`.<br/>
    Therefore, the `MetaAnnotation`s are provided in the dictionary form with their `ArgumentName`.
    """


class MetaDict_(Dict[str, Any], TypesPack[T]):
    """
    ---
    ``` python
    MetaDict_[Dict[str, Any]]
    ```
    ---
    The locals used during the dynamic execution.
    """


class ArgsDetails_(Dict[str, Any], TypesPack[T]):
    """
    ---
    ``` python
    ArgsDetails_[Dict[str, Any]]
    ```
    ---
    The arguments details your target function received.
    It is provided in the dictionaty form, meaning you can track the name of arguments as well.
    """


class GenerateMetaDict_(
    Callable[
        [ArgsDetails_[Dict[str, Any]], Dict[str, MetaAnnotation_[List[str]]]],
        MetaDict_[Dict[str, Any]],
    ],
    TypesPack[T],
):
    """
    ---
    ``` python
    GenerateMetaDict_[
        Callable[
                        [ArgsDetails_[Dict[str, Any]], Dict[str, MetaAnnotation_[List[str]]]],
                        MetaDict_[Dict[str, Any]]]
    ]
    ```
    ---
    A function to generate `MetaDict`
    """


class ComparisonExpression_(str, TypesPack[T]):
    """
    ---
    ``` python
    ComparisonExpression_[str]
    ```
    ---

    Test cases are defined by `ComparisonExpression`s.

    See the example here: [link](https://github.com/crimson206/executable-types/blob/main/example/types/types.ipynb), ## Comparison Expression

    """


class TestResult_(Dict[ComparisonExpression_[str], bool], TypesPack[T]):
    """
    ---
    ``` python
    TestResult_[Dict[ComparisonExpression_[str], bool]]
    ```
    ---
    `ComparisonExpression_`s are dynamically tested, and stored with the result here.
    """
