class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    def __init__(self, mensaje="Ha ocurrido un error general en el sistema."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple el formato o está vacío."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un argumento obligatorio para crear o procesar algo."""
    pass
    


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio ocupado o inactivo."""
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta realizar una acción inválida (ej. cancelar una reserva ya cancelada)."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo arroja valores negativos o incoherentes."""
    pass
