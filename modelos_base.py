from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError, ParametroFaltanteError
from logger_config import log

# Clase abstracta base para todas las entidades del sistema
class EntidadSistema(ABC):
    def __init__(self, id_entidad):
        # Verificamos que el ID no venga vacio
        if not id_entidad or str(id_entidad).strip() == "":
            raise ParametroFaltanteError("El ID no puede estar vacio.")
        self.__id_entidad = str(id_entidad).strip()

    # Metodo get para leer el ID privado
    def get_id(self):
        return self.__id_entidad

    # Metodos obligatorios para las clases hijas
    @abstractmethod
    def validar(self):
        pass

    @abstractmethod
    def obtener_resumen(self):
        pass


# Clase Cliente que hereda de EntidadSistema
class Cliente(EntidadSistema):
    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)
        # Usamos los metodos set para validar los datos desde el inicio
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)
        self.validar()
        log.info("Cliente registrado: " + self.__nombre + " con ID " + self.get_id())

    # Metodos get y set para encapsular los datos del cliente
    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if not nombre or len(nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 letras.")
        self.__nombre = nombre.strip()

    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        if not correo or "@" not in correo or "." not in correo:
            raise DatoInvalidoError("El correo ingresado no es valido.")
        self.__correo = correo.strip().lower()

    def get_telefono(self):
        return self.__telefono

    def set_telefono(self, telefono):
        tel = str(telefono).strip()
        if not tel.isdigit() or len(tel) < 7:
            raise DatoInvalidoError("El telefono debe tener solo numeros y minimo 7 digitos.")
        self.__telefono = tel

    def validar(self):
        if not self.__nombre or not self.__correo or not self.__telefono:
            raise ParametroFaltanteError("Faltan datos obligatorios del cliente.")
        return True

    def obtener_resumen(self):
        return f"Cliente [{self.get_id()}]: {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono}"
