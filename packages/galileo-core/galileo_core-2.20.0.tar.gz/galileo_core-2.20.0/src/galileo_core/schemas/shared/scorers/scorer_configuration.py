from typing import List

from pydantic import BaseModel, Field

from galileo_core.schemas.shared.scorers.base_configs import RegisteredScorerConfig
from galileo_core.schemas.shared.scorers.scorers import GalileoScorer


class ScorerConfiguration(BaseModel):
    scorers: List[GalileoScorer] = Field(default_factory=list, description="List of Galileo scorers to enable.")
    registered_scorers: List[RegisteredScorerConfig] = Field(
        default_factory=list, description="List of registered scorers to enable."
    )
