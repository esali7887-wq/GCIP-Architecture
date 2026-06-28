from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from app.models.onboarding_model import OnboardingModel

class BaseProjectRepository(ABC):
    @abstractmethod
    def save_onboarding(self, tenant_id: str, onboarding_data: OnboardingModel) -> bool:
        """
        Saves the project onboarding details for a given tenant.
        """
        pass

    @abstractmethod
    def get_project(self, tenant_id: str, project_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a project onboarding payload by tenant_id and project_id.
        """
        pass
