from abc import abstractmethod
from modelos_base import EntidadSistema
from excepciones import DatoInvalidoError, ServicioNoDisponibleError, CalculoInconsistenteError
from logger_config import log

# Clase abstracta para los servicios de la empresa Software FJ
class Servicio(EntidadSistema):
    def __init__(self, id_servicio, nombre, tarifa_base, disponible=True):
        super().__init__(id_servicio)
        if not nombre or nombre.strip() == "":
            raise DatoInvalidoError("El nombre del servicio no puede estar vacio.")
        if tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor a 0.")
        
        self.__nombre = nombre.strip()
        self.__tarifa_base = float(tarifa_base)
        self.__disponible = disponible

    def get_nombre(self):
        return self.__nombre

    def get_tarifa_base(self):
        return self.__tarifa_base

    def esta_disponible(self):
        return self.__disponible

    def set_disponible(self, estado):
        self.__disponible = estado

    # Revisa si el servicio se puede reservar
    def verificar_disponibilidad(self):
        if not self.__disponible:
            raise ServicioNoDisponibleError("El servicio " + self.__nombre + " no esta disponible.")

    # Metodo abstracto que simula sobrecarga usando parametros opcionales (descuento e iva)
    @abstractmethod
    def calcular_costo(self, horas, descuento=0, incluir_iva=False):
        pass

    # Metodo de ayuda para aplicar descuentos e IVA a cualquier servicio
    def aplicar_descuento_e_iva(self, subtotal, descuento, incluir_iva):
        if descuento < 0 or descuento > 100:
            raise CalculoInconsistenteError("El descuento debe estar entre 0 y 100.")
        
        total = subtotal - (subtotal * (descuento / 100))
        if incluir_iva:
            total = total * 1.19  # Se suma el 19% de IVA
        
        if total < 0:
            raise CalculoInconsistenteError("El total calculado no puede ser negativo.")
        
        return round(total, 2)

    def validar(self):
        if self.__tarifa_base <= 0:
            raise CalculoInconsistenteError("Tarifa invalida.")
        return True


# 1. Servicio especializado: Reserva de Salas
class ReservaSala(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0.")
        self.__capacidad = capacidad
        log.info("Sala creada: " + self.get_nombre())

    def calcular_costo(self, horas, descuento=0, incluir_iva=False):
        if horas <= 0:
            raise DatoInvalidoError("Las horas deben ser mayores a 0.")
        subtotal = self.get_tarifa_base() * horas
        # Si caben mas de 20 personas se cobra un 10% adicional
        if self.__capacidad > 20:
            subtotal = subtotal * 1.10
        return self.aplicar_descuento_e_iva(subtotal, descuento, incluir_iva)

    def obtener_resumen(self):
        estado = "Disponible" if self.esta_disponible() else "Ocupada"
        return f"Sala [{self.get_id()}]: {self.get_nombre()} (Capacidad: {self.__capacidad}) - ${self.get_tarifa_base()}/h - {estado}"


# 2. Servicio especializado: Alquiler de Equipos
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_base, marca, seguro=True, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not marca or marca.strip() == "":
            raise DatoInvalidoError("Falta la marca del equipo.")
        self.__marca = marca.strip()
        self.__seguro = seguro
        log.info("Equipo creado: " + self.get_nombre())

    def calcular_costo(self, horas, descuento=0, incluir_iva=False):
        if horas <= 0:
            raise DatoInvalidoError("Las horas deben ser mayores a 0.")
        subtotal = self.get_tarifa_base() * horas
        # Se suman 15000 pesos si el equipo lleva seguro
        if self.__seguro:
            subtotal = subtotal + 15000
        return self.aplicar_descuento_e_iva(subtotal, descuento, incluir_iva)

    def obtener_resumen(self):
        estado = "Disponible" if self.esta_disponible() else "Alquilado"
        return f"Equipo [{self.get_id()}]: {self.get_nombre()} ({self.__marca}) - ${self.get_tarifa_base()}/h - {estado}"


# 3. Servicio especializado: Asesoria Especializada
class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio, nombre, tarifa_base, tema, es_senior=True, disponible=True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not tema or tema.strip() == "":
            raise DatoInvalidoError("Falta el tema de la asesoria.")
        self.__tema = tema.strip()
        self.__es_senior = es_senior
        log.info("Asesoria creada: " + self.get_nombre())

    def calcular_costo(self, horas, descuento=0, incluir_iva=False):
        if horas <= 0:
            raise DatoInvalidoError("Las horas deben ser mayores a 0.")
        subtotal = self.get_tarifa_base() * horas
        # Si el asesor es senior se cobra 25% mas
        if self.__es_senior:
            subtotal = subtotal * 1.25
        return self.aplicar_descuento_e_iva(subtotal, descuento, incluir_iva)

    def obtener_resumen(self):
        estado = "Disponible" if self.esta_disponible() else "No disponible"
        return f"Asesoria [{self.get_id()}]: {self.get_nombre()} ({self.__tema}) - ${self.get_tarifa_base()}/h - {estado}"
