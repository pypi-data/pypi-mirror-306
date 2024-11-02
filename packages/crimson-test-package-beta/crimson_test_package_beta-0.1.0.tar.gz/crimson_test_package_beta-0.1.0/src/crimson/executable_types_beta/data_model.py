from typing import Any, List, Dict
from crimson.executable_types_beta.types import (
    ArgsDetails_,
    MetaAnnotations_,
    ArgumentName_,
    TestResult_,
    MetaDict_,
    ComparisonExpression_,
    MetaAnnotation_,
)
from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    custom_meta: Dict = Field(default_factory=dict)
    args_detail: ArgsDetails_[Dict[str, Any]]
    meta_annotations: MetaAnnotations_[
        Dict[ArgumentName_[str], MetaAnnotation_[List[str]] | None]
    ]
    meta_dict: MetaDict_[Dict[str, Any]]
    test_result: TestResult_[Dict[ComparisonExpression_[str], bool]]
