from enum import Enum


class ScorerName(str, Enum):
    bleu = "bleu"
    chunk_attribution_utilization = "chunk_attribution_utilization"
    completeness = "completeness"
    context_adherence = "context_adherence"
    context_relevance = "context_relevance"
    correctness = "correctness"
    input_pii = "input_pii"
    input_sexist = "input_sexist"
    input_tone = "input_tone"
    input_toxicity = "input_toxicity"
    instruction_adherence = "instruction_adherence"
    output_pii = "output_pii"
    output_sexist = "output_sexist"
    output_tone = "output_tone"
    output_toxicity = "output_toxicity"
    prompt_injection = "prompt_injection"
    prompt_perplexity = "prompt_perplexity"
    rouge = "rouge"
    uncertainty = "uncertainty"
