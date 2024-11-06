import uuid
from typing import Union
from fastapi import status

from ..utils.service_provider import ServiceProvider


class PracticeService:
    def __init__(self, service_provider: ServiceProvider):
        self.service_provider = service_provider

    def get_expert(
            self,
            expert_id: Union[uuid.UUID, None] = None,
            user_id: Union[uuid.UUID, None] = None
    ) -> dict:
        if expert_id is None and user_id is None:
            raise ValueError("Either expert_id or user_id must be provided")
        if expert_id is not None and user_id is not None:
            raise ValueError(
                "Only one of expert_id or user_id should be provided")

        if expert_id is not None:
            request_path = f"/experts/{str(expert_id)}"
        else:
            request_path = f"/experts/by_user_id/{str(user_id)}"

        return self.service_provider.fetch_data(request_path).data

    def is_practice_active(self, practice_id: uuid.UUID) -> bool:
        request_path = f"/practices/{str(practice_id)}/is_active"
        response_code = self.service_provider.fetch_data(request_path).code

        return response_code == status.HTTP_200_OK
