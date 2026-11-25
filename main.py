from modelos_base import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva, SistemaSoftwareFJ
from excepciones import ErrorSistemaFJ
from logger_config import log


# Funcion auxiliar para ejecutar cada prueba de forma segura y registrar errores
def ejecutar_operacion(numero, descripcion, funcion_prueba):
    print(f"\n[Operacion {numero}] {descripcion}...")
    try:
        funcion_prueba()
    except ErrorSistemaFJ as error:
        # Si el error tiene una causa encadenada (__cause__), tambien la mostramos
        detalle = f"{error}"
        if error.__cause__:
            detalle += f" | Causa original: {error.__cause__}"
        print(f"  -> ERROR CONTROLADO: {detalle}")
        log.error(f"Operacion {numero} fallida: {detalle}")
    except Exception as error_inesperado:
        print(f"  -> ERROR INESPERADO: {error_inesperado}")
        log.critical(f"Operacion {numero} error critico: {error_inesperado}")
    else:
        print("  -> EXITO: Operacion realizada correctamente.")
    finally:
        # El bloque finally siempre se ejecuta para confirmar que el sistema sigue estable
        print("  -> Estado del sistema: Activo y estable.")


def main():
    print("==========================================================")
    print("   INICIANDO SISTEMA DE GESTION - SOFTWARE FJ")
    print("==========================================================")

    sistema = SistemaSoftwareFJ()

    # Variables para guardar referencias y usarlas en las reservas
    clientes_creados = {}
    servicios_creados = {}
    reservas_creadas = {}

    # --- OPERACION 1: Registro valido de cliente ---
    def op1():
        c1 = Cliente("C001", "Laura Gomez", "laura.gomez@correo.com", "3104567890")
        sistema.agregar_cliente(c1)
        clientes_creados["c1"] = c1

    ejecutar_operacion(1, "Registrar cliente valido (Laura Gomez)", op1)

    # --- OPERACION 2: Registro valido de segundo cliente ---
    def op2():
        c2 = Cliente("C002", "Carlos Perez", "carlos.perez@empresa.co", "3209876543")
        sistema.agregar_cliente(c2)
        clientes_creados["c2"] = c2

    ejecutar_operacion(2, "Registrar segundo cliente valido (Carlos Perez)", op2)

    # --- OPERACION 3: Registro invalido de cliente (correo sin @ y telefono corto) ---
    def op3():
        c_malo = Cliente("C003", "Ana", "anacorreo.com", "123")
        sistema.agregar_cliente(c_malo)

    ejecutar_operacion(3, "Intentar registrar cliente con datos invalidos", op3)

    # --- OPERACION 4: Creacion valida de servicio Reserva de Sala ---
    def op4():
        s1 = ReservaSala("S001", "Sala Juntas Norte", 50000, capacidad=25)
        sistema.agregar_servicio(s1)
        servicios_creados["sala"] = s1

    ejecutar_operacion(4, "Crear servicio valido: Reserva de Sala", op4)

    # --- OPERACION 5: Creacion valida de servicio Alquiler de Equipo ---
    def op5():
        s2 = AlquilerEquipo("S002", "Portatil Workstation", 30000, marca="Dell", seguro=True)
        sistema.agregar_servicio(s2)
        servicios_creados["equipo"] = s2

    ejecutar_operacion(5, "Crear servicio valido: Alquiler de Equipo", op5)

    # --- OPERACION 6: Creacion valida de servicio Asesoria Especializada ---
    def op6():
        s3 = AsesoriaEspecializada("S003", "Arquitectura Cloud", 80000, tema="AWS y Python", es_senior=True)
        sistema.agregar_servicio(s3)
        servicios_creados["asesoria"] = s3

    ejecutar_operacion(6, "Crear servicio valido: Asesoria Especializada", op6)

    # --- OPERACION 7: Creacion invalida de servicio (tarifa negativa) ---
    def op7():
        s_malo = ReservaSala("S004", "Sala Sur", -20000, capacidad=10)
        sistema.agregar_servicio(s_malo)

    ejecutar_operacion(7, "Intentar crear servicio con tarifa negativa", op7)

    # --- OPERACION 8: Reserva exitosa usando sobrecarga (con 10% descuento e IVA) ---
    def op8():
        r1 = Reserva("R001", clientes_creados["c1"], servicios_creados["sala"], horas=3)
        r1.confirmar_y_procesar(descuento=10, incluir_iva=True)
        sistema.agregar_reserva(r1)
        reservas_creadas["r1"] = r1

    ejecutar_operacion(8, "Crear y confirmar reserva de sala (con descuento e IVA)", op8)

    # --- OPERACION 9: Reserva fallida (intentar reservar la misma sala ya ocupada) ---
    def op9():
        r2 = Reserva("R002", clientes_creados["c2"], servicios_creados["sala"], horas=2)
        sistema.agregar_reserva(r2)
        # Esto lanzara una excepcion encadenada porque la sala quedo ocupada en la op8
        r2.confirmar_y_procesar()

    ejecutar_operacion(9, "Intentar confirmar reserva sobre sala ya ocupada", op9)

    # --- OPERACION 10: Reserva exitosa de equipo (solo tarifa base + seguro, sin IVA) ---
    def op10():
        r3 = Reserva("R003", clientes_creados["c2"], servicios_creados["equipo"], horas=4)
        r3.confirmar_y_procesar()
        sistema.agregar_reserva(r3)
        reservas_creadas["r3"] = r3

    ejecutar_operacion(10, "Crear y confirmar reserva de equipo tecnologico", op10)

    # --- OPERACION 11: Reserva fallida por calculo inconsistente (descuento del 150%) ---
    def op11():
        r4 = Reserva("R004", clientes_creados["c1"], servicios_creados["asesoria"], horas=2)
        r4.confirmar_y_procesar(descuento=150)

    ejecutar_operacion(11, "Intentar confirmar asesoria con descuento invalido (150%)", op11)

    # --- OPERACION 12: Cancelar una reserva confirmada y luego intentar cancelarla otra vez ---
    def op12():
        reservas_creadas["r1"].cancelar()
        # Intentamos cancelar por segunda vez para probar OperacionNoPermitidaError
        reservas_creadas["r1"].cancelar()

    ejecutar_operacion(12, "Cancelar reserva R001 y probar doble cancelacion", op12)

    # Mostramos el estado final de todas las listas del sistema
    sistema.mostrar_resumen_general()
    print("\n==========================================================")
    print("   FIN DE LA SIMULACION - REVISE EL ARCHIVO sistema_fj.log")
    print("==========================================================")

if __name__ == "__main__":
    main()
