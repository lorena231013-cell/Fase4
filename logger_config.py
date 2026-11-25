import logging

def configurar_logger():
    """
    Configura el sistema de registro (logs) para guardar tanto eventos 
    informativos como errores en un archivo de texto plano.
    """
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evita duplicar mensajes si se llama varias veces
    if not logger.handlers:
        # Formato: Fecha y hora | Nivel (INFO, ERROR) | Mensaje
        formato = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Manejador para guardar en archivo (usa utf-8 para tildes y eñes)
        archivo_handler = logging.FileHandler("sistema_fj.log", encoding="utf-8")
        archivo_handler.setFormatter(formato)
        logger.addHandler(archivo_handler)

    return logger

# Instancia global que importaremos en los demás archivos
log = configurar_logger()
