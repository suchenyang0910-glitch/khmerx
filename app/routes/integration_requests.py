from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.integration_request import IntegrationRequest
from app.api_v1.errors import ApiError
from app.schemas import IntegrationRequestCreate, IntegrationRequestCreateResponse

router = APIRouter(prefix="/api", tags=["integration"])


@router.post("/integration-requests", response_model=IntegrationRequestCreateResponse)
def create_integration_request(payload: IntegrationRequestCreate, request: Request, db: Session = Depends(get_db)):
    if not payload._is_email(payload.email):
        raise ApiError(code="invalid_email", message="invalid_email", status_code=400)
    if not payload.phone and not payload.telegram:
        raise ApiError(code="phone_or_telegram_required", message="phone_or_telegram_required", status_code=400)
    if not payload.consent:
        raise ApiError(code="consent_required", message="consent_required", status_code=400)
    if not payload.interestedApis:
        raise ApiError(code="interested_apis_required", message="interested_apis_required", status_code=400)

    row = IntegrationRequest(
        applicant_type=payload.applicantType,
        org_name=payload.orgName,
        contact_name=payload.contactName,
        email=payload.email,
        phone=payload.phone,
        telegram=payload.telegram,
        country_or_region=payload.countryOrRegion,
        use_case=payload.useCase,
        interested_apis=payload.interestedApis,
        expected_volume_range=payload.expectedVolumeRange,
        expected_launch_time=payload.expectedLaunchTime,
        notes=payload.notes,
        source=payload.source or request.headers.get("referer"),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return IntegrationRequestCreateResponse(ok=True, requestId=str(row.id))
