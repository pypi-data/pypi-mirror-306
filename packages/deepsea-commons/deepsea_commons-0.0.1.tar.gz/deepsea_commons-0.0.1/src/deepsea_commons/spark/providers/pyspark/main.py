from deepsea_commons.spark.interface import Application, Run, SparkProvider

class PysparkApplication(Application):
    pass

class PySparkRun(Run):
    pass

class PySparkProvider(SparkProvider):
    def create_application(self):
        pass

    def list_application(self):
        pass

    def delete_application(self, application_id: str):
        pass
    