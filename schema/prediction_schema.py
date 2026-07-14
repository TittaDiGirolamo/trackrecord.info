"""
Pydantic schema for the Future Prediction Indexing Record.
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator
import uuid
from hashlib import sha256


class Author(BaseModel):
    lastname: str = Field(..., description="Last name or '[anonymous]'")
    firstname: str = Field(..., description="First name or empty string if anonymous")


class PredictionRecord(BaseModel):
    original_statement: str = Field(..., min_length=20)
    
    # New preferred field
    forecaster: Optional[str] = Field(
        None, 
        description="Forecaster name. Use 'Lastname, Firstname' for people."
    )
    
    # Old structured author (now optional)
    author: Optional[Author] = Field(None)
    
    statement_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    statement_topic: str = Field(default="FIFA World Cup 2026")
    statement_publication_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    statement_original_url: str = Field(...)
    statement_probability: float = Field(..., ge=0.0, le=1.0)
    statement_context: str = Field(..., min_length=10)
    resolution_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    resolution_criteria: str = Field(...)
    outcome: Optional[float] = Field(None, ge=0.0, le=1.0)
    outcome_proof: Optional[str] = Field(None)
    outcome_verification_url: Optional[str] = Field(None)
    extraction_timestamp: str = Field(default_factory=lambda: date.today().isoformat())
    source_text_snippet: Optional[str] = Field(None)

    @model_validator(mode='after')
    def validate_forecaster_or_author(self) -> 'PredictionRecord':
        if not self.forecaster and not self.author:
            raise ValueError("Either 'forecaster' or 'author' must be provided")
        return self

    def generate_deterministic_id(self, run_id: str = "default") -> str:
        base = f"{self.original_statement[:100]}|{self.statement_original_url}|{run_id}"
        return sha256(base.encode()).hexdigest()[:16] + "-" + str(uuid.uuid4())[:8]
