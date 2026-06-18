from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from app.concept_seed import CONCEPTS_BY_ID, SEEDED_CONCEPTS
from app.models import ApiError, ConceptListResponse, ConceptResponse, HealthResponse


app = FastAPI(
    title="Productive Failure Study Mode API",
    description=(
        "Backend contract for an Attempt First Mode learning flow: concept selection, "
        "pre-instruction challenge, typed failure analysis, consolidation, retrieval quiz, "
        "and learning-event dashboard."
    ),
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="productive-failure-api")


@app.get("/concepts", response_model=ConceptListResponse)
def list_concepts() -> ConceptListResponse:
    return ConceptListResponse(concepts=list(SEEDED_CONCEPTS))


@app.get(
    "/concepts/{concept_id}",
    response_model=ConceptResponse,
    responses={404: {"model": ApiError}},
)
def get_concept(concept_id: str) -> ConceptResponse:
    concept = CONCEPTS_BY_ID.get(concept_id)
    if concept is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error_code": "concept_not_found",
                "message": f"No seeded concept exists for concept_id '{concept_id}'.",
            },
        )

    return ConceptResponse(concept=concept)
