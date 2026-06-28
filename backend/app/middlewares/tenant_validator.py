from contextvars import ContextVar
from fastapi import Request, HTTPException, Header
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger("gcip-tenant-validator")

# ContextVar to store the tenant_id thread/task-safely
tenant_context: ContextVar[str] = ContextVar("tenant_id", default="")

class TenantValidatorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude docs and root/health paths from tenant validation
        exempt_paths = ["/", "/health", "/docs", "/redoc", "/openapi.json"]
        if request.url.path in exempt_paths:
            return await call_next(request)

        tenant_id = request.headers.get("X-Tenant-ID")
        
        if not tenant_id:
            logger.warning(f"Request blocked: Missing X-Tenant-ID header on path {request.url.path}")
            return JSONResponse(
                status_code=400,
                content={"detail": "Missing X-Tenant-ID header."}
            )

        # Simple validation: Ensure tenant_id is alphanumeric with dashes (e.g. TR-IST-044)
        clean_tenant = tenant_id.strip()
        if not clean_tenant or len(clean_tenant) < 3 or not all(c.isalnum() or c in "-_" for c in clean_tenant):
            logger.warning(f"Request blocked: Invalid X-Tenant-ID format: '{tenant_id}'")
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid X-Tenant-ID format."}
            )

        # Set the ContextVar value for the duration of this request
        token = tenant_context.set(clean_tenant)
        try:
            response = await call_next(request)
            return response
        finally:
            # Reset ContextVar back to avoid memory leak / cross-context contamination
            tenant_context.reset(token)

def get_current_tenant(x_tenant_id: str = Header(..., alias="X-Tenant-ID", description="Tenant Identifier (e.g. TR-IST-044)")) -> str:
    """Dependency helper to retrieve the tenant_id and document it in OpenAPI/Swagger UI."""
    return x_tenant_id
