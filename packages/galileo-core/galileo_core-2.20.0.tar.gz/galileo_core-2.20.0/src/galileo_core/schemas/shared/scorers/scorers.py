from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from galileo_core.schemas.shared.scorers.base_configs import (
    GalileoScorerConfig,
    LunaOrPlusScorerTypeConfig,
    PlusScorerConfig,
    PlusScorerTypeConfig,
    PlusScorerWithNumJudgesConfig,
)
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName


class BleuScorer(GalileoScorerConfig):
    name: Literal[ScorerName.bleu] = ScorerName.bleu


class ChunkAttributionUtilizationScorer(LunaOrPlusScorerTypeConfig, PlusScorerConfig):
    name: Literal[ScorerName.chunk_attribution_utilization] = ScorerName.chunk_attribution_utilization


class CompletenessScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.completeness] = ScorerName.completeness


class ContextAdherenceScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.context_adherence] = ScorerName.context_adherence


class ContextRelevanceScorer(GalileoScorerConfig):
    name: Literal[ScorerName.context_relevance] = ScorerName.context_relevance


class CorrectnessScorer(PlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.correctness] = ScorerName.correctness


class InputPIIScorer(GalileoScorerConfig):
    name: Literal[ScorerName.input_pii] = ScorerName.input_pii


class InputSexistScorer(GalileoScorerConfig):
    name: Literal[ScorerName.input_sexist] = ScorerName.input_sexist


class InputToneScorer(GalileoScorerConfig):
    name: Literal[ScorerName.input_tone] = ScorerName.input_tone


class InputToxicityScorer(GalileoScorerConfig):
    name: Literal[ScorerName.input_toxicity] = ScorerName.input_toxicity


class InstructionAdherenceScorer(PlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.instruction_adherence] = ScorerName.instruction_adherence


class OutputPIIScorer(GalileoScorerConfig):
    name: Literal[ScorerName.output_pii] = ScorerName.output_pii


class OutputSexistScorer(GalileoScorerConfig):
    name: Literal[ScorerName.output_sexist] = ScorerName.output_sexist


class OutputToneScorer(GalileoScorerConfig):
    name: Literal[ScorerName.output_tone] = ScorerName.output_tone


class OutputToxicityScorer(GalileoScorerConfig):
    name: Literal[ScorerName.output_toxicity] = ScorerName.output_toxicity


class PromptInjectionScorer(GalileoScorerConfig):
    name: Literal[ScorerName.prompt_injection] = ScorerName.prompt_injection


class PromptPerplexityScorer(GalileoScorerConfig):
    name: Literal[ScorerName.prompt_perplexity] = ScorerName.prompt_perplexity


class RougeScorer(GalileoScorerConfig):
    name: Literal[ScorerName.rouge] = ScorerName.rouge


class UncertaintyScorer(GalileoScorerConfig):
    name: Literal[ScorerName.uncertainty] = ScorerName.uncertainty


GalileoScorer = Annotated[
    Union[
        BleuScorer,
        ChunkAttributionUtilizationScorer,
        CompletenessScorer,
        ContextAdherenceScorer,
        ContextRelevanceScorer,
        CorrectnessScorer,
        InputPIIScorer,
        InputSexistScorer,
        InputToneScorer,
        InputToxicityScorer,
        InstructionAdherenceScorer,
        OutputPIIScorer,
        OutputSexistScorer,
        OutputToneScorer,
        OutputToxicityScorer,
        PromptInjectionScorer,
        PromptPerplexityScorer,
        RougeScorer,
        UncertaintyScorer,
    ],
    Field(discriminator="name"),
]
