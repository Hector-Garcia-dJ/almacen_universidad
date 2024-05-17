from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class SolicitudCommand(Command):
    def __init__(self, solicitud):
        self.solicitud = solicitud

    def execute(self):
        # Aquí va la lógica específica para procesar la solicitud
        self.solicitud.save()
        # Puedes agregar más lógica según sea necesario




