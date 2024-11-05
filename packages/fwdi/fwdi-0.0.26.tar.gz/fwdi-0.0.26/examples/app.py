import sys
from pathlib import Path
sys.path.insert(0,str(Path(sys.path[0]).parent))

#======= Package library ============================
from fwdi.WebApp.web_application import WebApplication
from fwdi.WebApp.web_application_builder import WebApplicationBuilder
#----------------------------------------------------
from Application.dependency_injection import DependencyInjection as ApplicationDependencyInjection
from Persistance.dependency_injection import DependencyInjection as PersistanceDependencyInjection
from Presentation.dependency_injection import DependencyInjection as PresentationDependencyInjection
from Utilites.dependency_injection import DependencyInjection as UtilitesDependencyInjection
from Infrastructure.dependency_injection  import DependencyInjection as InfrastructureDependencyInjection
#----------------------------------------------------
def start_web_service():
    server_param = {
        'name':'Rest Inference service',
        'debug':'False'
    }
    builder:WebApplicationBuilder = WebApplication.create_builder(**server_param)

    #------------------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------------------
    UtilitesDependencyInjection.AddUtils(builder.services)
    ApplicationDependencyInjection.AddConfig(builder.services)
    InfrastructureDependencyInjection.AddConfigs(builder.services)
    InfrastructureDependencyInjection.AddInfrastructure(builder.services)
    ApplicationDependencyInjection.AddApplicationInteractors(builder.services)
    PersistanceDependencyInjection.AddPersistance(builder.services)
    #------------------------------------------------------------------------------------------
    PresentationDependencyInjection.AddScope(builder)   
    app:WebApplication = builder.build()
    #------------------------------------------------------------------------------------------
    PresentationDependencyInjection.AddEndpoints(app)
    #------------------------------------------------------------------------------------------
    kwargs = {
            'host': "0.0.0.0",
            'port': 5000
        }
    app.run(**kwargs)
if __name__ == "__main__":
    start_web_service()