from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class OrchestratorStateModel(BaseModel):
    project_id: str = Field(..., description="Projenin benzersiz kimliği (UUID veya Kod)")
    tenant_id: str = Field(..., description="Kiracı/Holding kimliği")
    current_node: str = Field("init", description="LangGraph içerisindeki aktif düğüm adı")
    messages: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Ajanlar arası kronolojik mesajlaşma geçmişi"
    )
    quantity_survey: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Ölçülen ve AutoCAD/BIM projelerinden doğrulanan metraj verileri"
    )
    billing_data: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Aktif dönem hakediş ödeme ve ceza kesinti verileri"
    )
    disputes: List[Dict[str, Any]] = Field(
        default_factory=list, 
        description="Aktif uyuşmazlık, kilitlenme ve ortak kurul kararları listesi"
    )
    risk_metrics: Dict[str, Any] = Field(
        default_factory=dict, 
        description="EVM (Kazanılmış Değer), zaman sapması ve maliyet öngörüleri"
    )
