from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class OnboardingModel(BaseModel):
    project_id: str = Field(..., description="Kurulum yapılacak yeni veya devralınan proje kimliği (UUID veya Kod)")
    project_name: str = Field(..., description="Proje adı")
    total_budget_usd: float = Field(..., description="Toplam keşif/sözleşme bütçesi (USD)")
    is_takeover: bool = Field(
        False, 
        description="Projenin yarıda devralınıp devralınmadığı (Mid-Project Takeover) bilgisi"
    )
    historical_leakage_audit: bool = Field(
        True, 
        description="Geçmiş dönem hakediş kaçak denetiminin (Historical Leakage Audit) tetiklenmesi seçeneği"
    )
    boq_items: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Proje keşif (BOQ) pozlarının listesi"
    )
    subcontractors: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Projeye atanmış aktif alt yüklenici (taşeron) tanımları listesi"
    )
    baseline_version: str = Field(
        "Rev0", 
        description="İlk hedef iş programı revizyon adı (örn: Rev0, Rev1)"
    )
