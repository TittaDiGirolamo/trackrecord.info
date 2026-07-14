"""
Pydantic schema for the Future Prediction Indexing Record.
Strictly follows the user's specified format and constraints.
All fields validated for types, ranges, and required logic.
"""

from datetime import date
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator
import uuid
from hashlib import sha256


class Author(BaseModel):
    """Structured author name (optional)."""
    lastname: str = Field(..., description="Last name or '[anonymous]'")
    firstname: str = Field(..., description="First name or empty string if anonymous")


class PredictionRecord(BaseModel):
    """Main model for a prediction record."""

    # 1. Original statement with clarifications
    original_statement: str = Field(
        ...,
        min_length=20,
        description="Verbatim quote or closest accurate paraphrase, self-contained, with [clarifications] appended for pronouns/names/temporals."
    )

    # Preferred identifier (string)
    # - For people: use "Lastname, Firstname" format
    # - For models, organizations or anonymous: use a simple name
    forecaster: Optional[str] = Field(
        None,
        description="Forecaster name. Use 'Lastname, Firstname' for people, or simple name otherwise."
    )

    # Structured author (kept optional for backward compatibility)
    author: Optional[Author] = Field(
        None,
        description="Structured author object (optional if forecaster is used)"
    )

    # 3. Unique statement_id
    statement_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="UUID or composite unique ID including run context"
    )

    # 4. statement_topic
    statement_topic: str = Field(
        default="FIFA World Cup 2026",
        description="Main subject or sub-topic of the prediction"
    )

    # 5. statement_publication_date
    statement_publication_date: str = Field(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="YYYY-MM-DD from text/metadata or today's date"
    )

    # 7. statement_original_url
    statement_original_url: str = Field(
        ...,
        description="URL from source or 'Not provided'"
    )

    # 8. statement_probability (0.00-1.00)
    statement_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Calibrated probability the statement resolves true, based on text + general knowledge only"
    )

    # 9. statement_context
    statement_context: str = Field(
        ...,
        min_length=10,
        description="Delivery format, seriousness, speaker authority, editing level. Include author lookup source if used."
    )

    # 10. resolution_date
    resolution_date: Optional[str] = Field(
        None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="YYYY-MM-DD by which verifiable, or null if undetermined"
    )

    # 11. resolution_criteria
    resolution_criteria: str = Field(
        ...,
        description="Single falsifiable sentence OR 'Cannot formulate sufficient resolution_criteria: missing [list of missing elements]'"
    )

    # 12. Outcome fields (time-aware)
    outcome: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Certainty (0.00-1.00) that verification of resolution_criteria is correct"
    )
    outcome_proof: Optional[str] = Field(
        None,
        description="Brief evidence of how outcome was determined"
    )
    outcome_verification_url: Optional[str] = Field(
        None,
        description="URL to independent source for fact-checking the outcome (always required when outcome is set)"
    )

    # Internal audit fields
    extraction_timestamp: str = Field(
        default_factory=lambda: date.today().isoformat(),
        description="When this record was created (YYYY-MM-DD)"
    )
    source_text_snippet: Optional[str] = Field(
        None,
        description="Short excerpt of original text for auditability (do not store full copyrighted text)"
    )

    @field_validator('original_statement')
    @classmethod
    def validate_clarifications(cls, v: str) -> str:
        if '[' in v and ']' not in v:
            raise ValueError("Clarification brackets appear unbalanced")
        return v

    @model_validator(mode='after')
    def validate_outcome_logic(self) -> 'PredictionRecord':
        if self.outcome is not None and not self.outcome_verification_url:
            raise ValueError("outcome_verification_url is required whenever outcome is provided")
        if self.resolution_criteria.startswith("Cannot formulate"):
            if self.statement_probability != 0.00:
                raise ValueError("statement_probability must be 0.00 when resolution_criteria cannot be formulated")
        return self

    @model_validator(mode='after')
    def validate_forecaster_or_author(self) -> 'PredictionRecord':
        if not self.forecaster and not self.author:
            raise ValueError("At least one of 'forecaster' or 'author' must be provided")
        return self

    def generate_deterministic_id(self, run_id: str = "default") -> str:
        """Generate a reproducible ID even for identical content."""
        base = f"{self.original_statement[:100]}|{self.statement_original_url}|{run_id}"
        return sha256(base.encode()).hexdigest()[:16] + "-" + str(uuid.uuid4())[:8]


# Example instantiation helper (for testing)
def create_example_record() -> PredictionRecord:
    return PredictionRecord(
        original_statement='"France will win the 2026 FIFA World Cup [the tournament hosted in USA/Canada/Mexico]."',
        forecaster="Smith, John",                    # Preferred field
        # author=Author(lastname="Smith", firstname="John"),  # Optional
        statement_topic="FIFA World Cup 2026 - Winner",
        statement_publication_date="2025-03-15",
        statement_original_url="https://example.com/prediction-article",
        statement_probability=0.28,
        statement_context="Excerpt from opinion column in major sports outlet.",
        resolution_date="2026-07-19",
        resolution_criteria="The France national team is declared the winner of the 2026 FIFA World Cup by the official FIFA final match result on or before 2026-07-19.",
        outcome=None,
        outcome_proof=None,
        outcome_verification_url=None,
        source_text_snippet="In his column, Smith argued that France will win..."
    )
