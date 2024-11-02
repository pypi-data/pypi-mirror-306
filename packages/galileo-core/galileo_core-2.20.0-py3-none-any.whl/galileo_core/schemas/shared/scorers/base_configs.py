from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator

from galileo_core.schemas.shared.scorers.scorer_name import ScorerName
from galileo_core.schemas.shared.scorers.scorer_type import LunaOrPlusScorerType, PlusScorerType, ScorerType


class BaseScorerConfig(BaseModel):
    name: str = Field(..., description="Name of the scorer to enable.")


class GalileoScorerConfig(BaseScorerConfig):
    name: ScorerName = Field(..., description="Name of the scorer to enable.")


class LunaOrPlusScorerTypeConfig(BaseModel):
    type: LunaOrPlusScorerType = ScorerType.luna


class PlusScorerTypeConfig(BaseModel):
    type: PlusScorerType = ScorerType.plus


class PlusScorerConfig(GalileoScorerConfig):
    type: ScorerType
    model_name: Optional[str] = Field(default=None, description="Alias of the model to use for the scorer.")

    model_config = ConfigDict(
        # Avoid Pydantic's protected namespace warning since we want to use
        # `model_alias` as a field name.
        protected_namespaces=(),
    )

    @field_validator("model_name", mode="before")
    def validate_model_alias(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        name = info.data["name"]
        scorer_type = info.data.get("type", ScorerType.luna)
        if value is not None and scorer_type != ScorerType.plus:
            raise ValueError(f"Model alias is not allowed for {name} scorer if type is not set to plus.")
        return value


class PlusScorerWithNumJudgesConfig(PlusScorerConfig):
    num_judges: Optional[int] = Field(default=None, ge=1, le=10, description="Number of judges for the scorer.")

    @field_validator("num_judges", mode="before")
    def validate_num_judges(cls, value: Optional[int], info: ValidationInfo) -> Optional[int]:
        name = info.data["name"]
        scorer_type = info.data.get("type", ScorerType.luna)
        if value is not None and scorer_type != ScorerType.plus:
            raise ValueError(f"Number of judges is not allowed for {name} scorer if type is not set to plus.")
        return value


class RegisteredScorerConfig(BaseScorerConfig): ...


class GeneratedScorerConfig(BaseScorerConfig):
    model_name: Optional[str] = Field(default=None, description="Alias of the model to use for the scorer.")
    num_judges: Optional[int] = Field(default=None, ge=1, le=10, description="Number of judges for the scorer.")

    model_config = ConfigDict(
        # Avoid Pydantic's protected namespace warning since we want to use
        # `model_name` as a field name.
        protected_namespaces=(),
    )
