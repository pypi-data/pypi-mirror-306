from fwdi.Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI


from Application.Abstractions.base_llm_service import BaseLlmService
from Application.Abstractions.base_service_search import BaseServiceSearch
from Application.Abstractions.base_task_manager import BaseTaskManager
from Application.Abstractions.base_usecase_context_data_base import BaseUsecaseContextDataBase
from Application.Abstractions.base_usecase_task_manager import BaseUsecaseTaskManager
from Application.Config.service_congif import ServiceConfig
from Application.TaskManager.task_manager import TaskManager
from Application.Usecases.usecase_context_database import UsecaseContextDataBase
from Application.Usecases.usecase_search import ServiceSearch
from Application.Usecases.usecase_task_manager import UsecaseTaskManager
from Infrastructure.rag_llm_service import LLMService

class DependencyInjection():
    def AddApplicationInteractors(services:BaseServiceCollectionFWDI):
        services.AddTransient(BaseServiceSearch, ServiceSearch)
        services.AddTransient(BaseLlmService, LLMService)
        services.AddSingleton(BaseTaskManager, TaskManager)
        services.AddTransient(BaseUsecaseContextDataBase, UsecaseContextDataBase)
        services.AddTransient(BaseUsecaseTaskManager, UsecaseTaskManager)

    def AddConfig(services:BaseServiceCollectionFWDI):
        ServiceConfig.service_avaible = True
        services.AddSingleton(ServiceConfig)
        
