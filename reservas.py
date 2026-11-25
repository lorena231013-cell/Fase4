from modelos_base import EntidadSistema, Cliente
from servicios import Servicio
from excepciones import (
    ErrorSistemaFJ,
    DatoInvalidoError,
    ParametroFaltanteError,
    OperacionNoPermitidaError
)
from logger_config import log


# Clase Reserva que une a un Cliente con un Servicio
class Reserva(EntidadSistema):
    def __init__(self, id_reserva, cliente, servicio, horas):
        super().__init__(id_reserva)
        # Validamos que cliente y servicio sean objetos validos
        if not isinstance(cliente, Cliente):
            raise ParametroFaltanteError("Se requiere un cliente valido para la reserva.")
        if not isinstance(servicio, Servicio):
            raise ParametroFaltanteError("Se requiere un servicio valido para la reserva.")
        if horas <= 0:
            raise DatoInvalidoError("La duracion de la reserva debe ser mayor a 0 horas.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__estado = "Pendiente"
        self.__costo_total = 0.0
        self.validar()

    def get_estado(self):
        return self.__estado

    def get_costo_total(self):
        return self.__costo_total

    # Procesa el calculo y confirma la reserva usando encadenamiento de excepciones
    def confirmar_y_procesar(self, descuento=0, incluir_iva=False):
        if self.__estado == "Confirmada":
            raise OperacionNoPermitidaError("Esta reserva ya fue confirmada antes.")
        if self.__estado == "Cancelada":
            raise OperacionNoPermitidaError("No se puede confirmar una reserva cancelada.")

        try:
            # Revisamos si el servicio esta libre y calculamos el precio
            self.__servicio.verificar_disponibilidad()
            self.__costo_total = self.__servicio.calcular_costo(self.__horas, descuento, incluir_iva)
        except Exception as error_original:
            # Encadenamiento de excepciones: guardamos el motivo real del fallo
            raise ErrorSistemaFJ(f"No se pudo procesar la reserva {self.get_id()}") from error_original
        else:
            # El bloque else se ejecuta solo si el try no tuvo errores
            self.__estado = "Confirmada"
            self.__servicio.set_disponible(False)  # Marcamos el servicio como ocupado
            log.info(f"Reserva {self.get_id()} confirmada para {self.__cliente.get_nombre()} - Total: ${self.__costo_total}")

    # Cancela una reserva y libera el servicio
    def cancelar(self):
        if self.__estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")
        
        estado_anterior = self.__estado
        self.__estado = "Cancelada"
        # Si estaba confirmada, volvemos a dejar el servicio disponible
        if estado_anterior == "Confirmada":
            self.__servicio.set_disponible(True)
        log.info(f"Reserva {self.get_id()} ha sido cancelada.")

    def validar(self):
        if self.__horas <= 0:
            raise DatoInvalidoError("Horas invalidas en la reserva.")
        return True

    def obtener_resumen(self):
        return (f"Reserva [{self.get_id()}] | Cliente: {self.__cliente.get_nombre()} | "
                f"Servicio: {self.__servicio.get_nombre()} | Horas: {self.__horas} | "
                f"Estado: {self.__estado} | Total: ${self.__costo_total}")


# Clase principal que maneja las listas en memoria (sin base de datos)
class SistemaSoftwareFJ:
    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        log.info("Sistema Software FJ iniciado correctamente.")

    def agregar_cliente(self, cliente):
        # Evitamos IDs repetidos
        for c in self.__clientes:
            if c.get_id() == cliente.get_id():
                raise OperacionNoPermitidaError("Ya existe un cliente con el ID " + cliente.get_id())
        self.__clientes.append(cliente)

    def agregar_servicio(self, servicio):
        for s in self.__servicios:
            if s.get_id() == servicio.get_id():
                raise OperacionNoPermitidaError("Ya existe un servicio con el ID " + servicio.get_id())
        self.__servicios.append(servicio)

    def agregar_reserva(self, reserva):
        for r in self.__reservas:
            if r.get_id() == reserva.get_id():
                raise OperacionNoPermitidaError("Ya existe una reserva con el ID " + reserva.get_id())
        self.__reservas.append(reserva)

    def mostrar_resumen_general(self):
        print("\n--- RESUMEN ACTUAL DEL SISTEMA SOFTWARE FJ ---")
        print(f"Total Clientes: {len(self.__clientes)}")
        for c in self.__clientes:
            print("  *", c.obtener_resumen())
            
        print(f"\nTotal Servicios: {len(self.__servicios)}")
        for s in self.__servicios:
            print("  *", s.obtener_resumen())
            
        print(f"\nTotal Reservas: {len(self.__reservas)}")
        for r in self.__reservas:
            print("  *", r.obtener_resumen())
