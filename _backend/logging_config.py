from loguru import logger
import sys

def configure_logging():
    """
    Configure Loguru avec des couleurs spécifiques pour chaque niveau de log
    et un fichier pour enregistrer les logs.
    """
    logger.remove()

    logger.add(sys.stderr, 
               level="DEBUG",
               format="{time:YYYY-MM-DD HH:mm:ss} | <green>{level}</green> | <cyan>{message}</cyan>")

    # Ajouter un gestionnaire pour les logs dans un fichier
    logger.add("app.log", 
               level="DEBUG",
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
               rotation="1 week",
               compression="zip")