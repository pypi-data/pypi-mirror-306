from fastapi import Depends

from .services import DictionaryService, PracticeService
from .utils.service_provider import ServiceProvider, get_dictionary_service_provider, get_practice_service_provider


def get_dictionary_service(service_provider: ServiceProvider = Depends(
        get_dictionary_service_provider)) -> DictionaryService:
    return DictionaryService(service_provider=service_provider)


def get_practice_service(service_provider: ServiceProvider = Depends(
        get_practice_service_provider)) -> PracticeService:
    return PracticeService(service_provider=service_provider)
