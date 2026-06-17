from pydantic import BaseModel, Field

# Schema for any additional conditions, too defined, not broad enough. 
# Pydantic Model for Optional Dictionaries does not translate well with Gemini 2.5, cant parse additional properties.
class AnalyticalConditionals(BaseModel):
    timeframe: Optional[str] = Field(default=None, description="E.g., 'Q2', '2025-H1'")
    threshold: Optional[float] = Field(default=None, description="Numerical thresholds or cuts")
    segment: Optional[str] = Field(default=None, description="Customer or geographic segment")

# Schema for reasoning, what track and what to analyze.
class IngestionRoutingSchema(BaseModel):
    reasoning_chain: str = Field(
        description="A short, internal step-by-step logic detailing why this track and intent were selected."
    )
    track: Literal["Financial", "Operational", "People", "Product", "Growth", "Unknown"] = Field(
        description="The primary target analytics track."
    )
    analytical_intent: str = Field(
        description="The precise name of the target deterministic metric/function to execute."
    )
    # Explicit additional's model added.
    conditionals: Optional[AnalyticalConditionals] = Field(
        default=None,
        description="Extra parameters or filters extracted from the input."
    )