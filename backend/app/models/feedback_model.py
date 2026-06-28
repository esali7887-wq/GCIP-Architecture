from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackModel(BaseModel):
    id: Optional[str] = Field(None, description="Düzeltme olayının UUID v4 kimliği (Boşsa otonom atanır)")
    project_id: str = Field(..., description="İşlemin yapıldığı proje kimliği")
    user_id: str = Field(..., description="Düzeltmeyi yapan mühendis/kullanıcı kimliği")
    boq_id: str = Field(..., description="Müdahale edilen Keşif/BOQ pozunun ID'si")
    adjusted_field: str = Field(..., description="Düzeltilen alan adı (Örn: quantity_verified, unit_price)")
    old_value: str = Field(..., description="Yapay zeka tarafından üretilen eski değer")
    new_value: str = Field(..., description="Mühendis tarafından el ile girilen yeni değer")
    reason: str = Field(..., description="Düzeltme/Müdahale gerekçesi (RLHF eğitim girdisi)")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Düzeltmenin yapıldığı tarih/saat"
    )
