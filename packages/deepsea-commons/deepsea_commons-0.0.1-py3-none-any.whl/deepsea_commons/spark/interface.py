from typing import List
from abc import ABC, abstractmethod

##########################################################################
# Application       Represent a spark application
# Run               Represent a run of a spark application
##########################################################################

class Run(ABC):
    @abstractmethod
    def stop(self):
        pass

class Application(ABC):
    id: str  # application's unique ID

    @abstractmethod
    def start(self) -> Run:
        pass

class SparkProvider(ABC):
    def create_application(self) -> Application:
        pass

    def list_application(self) -> List[Application]:
        pass

    def delete_application(self, application_id: str):
        pass
