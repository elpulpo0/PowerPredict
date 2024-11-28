from loguru import logger
import sys

def configure_logging():
    """
    Configure Loguru avec un format, descouleurs et un niveau de log uniformes pour l'ensemble de l'application.
    """
    # Supprimer le gestionnaire par défaut
    logger.remove()

    # Ajouter un gestionnaire pour la console
    logger.add(sys.stderr, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | <green>{level}</green> | <cyan>{message}</cyan>")
