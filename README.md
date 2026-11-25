# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

**Curso:** Programación (213023) - Fase 4 (Componente Práctico)  
**Estudiante:** Silvia Lorena Carreño Acosta  

---

## Descripción del Proyecto
Aplicación desarrollada en **Python** utilizando los principios de la **Programación Orientada a Objetos (POO)** (abstracción, herencia, encapsulación, polimorfismo y sobrecarga) junto con un sistema robusto de **manejo de excepciones personalizadas y encadenadas**.

El sistema gestiona clientes, servicios especializados y reservas en memoria (sin uso de bases de datos), garantizando la continuidad operativa ante fallos y registrando todos los eventos y errores en un archivo de logs (`sistema_fj.log`).

---

## Estructura de Archivos del Repositorio
* **`logger_config.py`**: Configura el sistema de registro (`logging`) para almacenar eventos e incidencias en `sistema_fj.log`.
* **`excepciones.py`**: Define la jerarquía de excepciones personalizadas (`ErrorSistemaFJ`, `DatoInvalidoError`, `ParametroFaltanteError`, `ServicioNoDisponibleError`, `OperacionNoPermitidaError` y `CalculoInconsistenteError`).
* **`modelos_base.py`**: Contiene la clase abstracta `EntidadSistema` y la clase `Cliente` con encapsulación (`get_` / `set_`) y validaciones.
* **`servicios.py`**: Implementa la clase abstracta `Servicio` y las tres clases hijas (`ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`) aplicando polimorfismo y sobrecarga de métodos para el cálculo de tarifas.
* **`reservas.py`**: Contiene la clase `Reserva` (con bloques `try/except/else` y encadenamiento de excepciones `raise ... from`) y la clase controladora `SistemaSoftwareFJ`.
* **`main.py`**: Archivo principal que ejecuta una simulación de 12 operaciones completas (casos exitosos y fallos controlados) demostrando la estabilidad del sistema.
* **`sistema_fj.log`**: Archivo de evidencia generado tras la ejecución con el historial completo de eventos y errores capturados.

---

## Cómo ejecutar el proyecto
1. Clonar o descargar los archivos del repositorio en una misma carpeta.
2. Abrir una terminal dentro de la carpeta del proyecto.
3. Ejecutar el archivo principal con el comando:
   ```bash
   python main.py
