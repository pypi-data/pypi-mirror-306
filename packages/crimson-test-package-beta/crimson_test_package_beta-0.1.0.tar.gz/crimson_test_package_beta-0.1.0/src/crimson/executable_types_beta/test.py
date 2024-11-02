from typing import Any, List, Dict
from crimson.executable_types_beta.types import (
    MetaAnnotations_,
    ArgumentName_,
    TestResult_,
    MetaDict_,
    ComparisonExpression_,
    MetaAnnotation_,
)
from crimson.ast_dev_tool import collect_nodes
import ast


def test_meta_dict_unit(
    meta_dict: MetaDict_[Dict[str, Any]],
    meta_annotation: MetaAnnotation_[List[str]],
    result_key: str = "_result",
) -> MetaDict_[Dict[str, int]]:
    comparison_result = {}
    for unit_meta in meta_annotation:
        compare_nodes = collect_nodes(unit_meta, ast.Compare)
        for compare_node in compare_nodes:
            comparison_code = ast.unparse(compare_node)
            comparison_execution_code = f"{result_key} = " + comparison_code
            exec(comparison_execution_code, {}, meta_dict)
            comparison_result[comparison_code] = meta_dict[result_key]
            del meta_dict[result_key]

    return comparison_result


def test_meta_dict(
    meta_dict: MetaDict_[Dict[str, Any]],
    meta_annotations: MetaAnnotations_[
        Dict[ArgumentName_[str], MetaAnnotation_[List[str]]] | None
    ],
) -> TestResult_[Dict[ComparisonExpression_[str], bool]]:
    """
    If a unit in `MetaAnnotation` is categorized as a comparison expression(`ast.Compare`), <br/>
    the comparison expression is executed.

    The `meta_dict` is used as the locals of the execution, <br/>
    meaning all the names in the comparison expressions must be in `meta_dict.keys()`.
    """
    comparison_result = {}

    for _, meta_annotation in meta_annotations.items():
        if meta_annotation is not None:
            comparison_result_unit = test_meta_dict_unit(
                meta_dict=meta_dict, meta_annotation=meta_annotation
            )
            comparison_result.update(comparison_result_unit)
    return comparison_result
