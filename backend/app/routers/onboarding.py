from fastapi import APIRouter, Depends, HTTPException, status
from app.models.onboarding_model import OnboardingModel
from app.middlewares.tenant_validator import get_current_tenant
from app.database.interfaces import BaseProjectRepository
from app.database.dependency import get_project_repository
import logging

logger = logging.getLogger("gcip-onboarding-router")

router = APIRouter(
    prefix="/onboarding",
    tags=["onboarding"]
)

@router.post("/start", status_code=status.HTTP_201_CREATED)
async def start_onboarding(
    payload: OnboardingModel,
    tenant_id: str = Depends(get_current_tenant),
    repo: BaseProjectRepository = Depends(get_project_repository)
):
    logger.info(f"Onboarding started for Tenant: {tenant_id}, Project ID: {payload.project_id}")
    
    # Save the project onboarding data using the abstraction layer
    repo.save_onboarding(tenant_id, payload)
    
    audit_results = {}
    
    if payload.is_takeover:
        logger.info("Executing Mid-Project Takeover flow...")
        # Step 24.3 takeover sanity checks sequence (mocked triggers)
        audit_results = {
            "onboarding_mode": "MID_PROJECT_TAKEOVER",
            "historical_leakage_audit": "ENABLED" if payload.historical_leakage_audit else "DISABLED",
            "metraj_sanity_check": "PENDING_VERIFICATION",
            "avans_mahsup_balance": "PENDING_AUDIT",
            "baseline_calibration": "SCHEDULED"
        }
    else:
        logger.info("Executing New Project Setup flow...")
        audit_results = {
            "onboarding_mode": "NEW_PROJECT_SETUP",
            "baseline_calibration": "ACTIVE"
        }

    return {
        "status": "success",
        "message": "Project onboarding sequence initiated and mock-saved.",
        "project_id": payload.project_id,
        "tenant_id": tenant_id,
        "payload_summary": {
            "project_name": payload.project_name,
            "total_budget_usd": payload.total_budget_usd,
            "boq_items_received": len(payload.boq_items),
            "subcontractors_registered": len(payload.subcontractors)
        },
        "takeover_audit": audit_results
    }

@router.get("/{project_id}", status_code=status.HTTP_200_OK)
async def get_onboarding(
    project_id: str,
    tenant_id: str = Depends(get_current_tenant),
    repo: BaseProjectRepository = Depends(get_project_repository)
):
    project_data = repo.get_project(tenant_id, project_id)
    if not project_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found under tenant context '{tenant_id}'."
        )
    return {
        "status": "success",
        "tenant_id": tenant_id,
        "project_id": project_id,
        "project_data": project_data
    }

