from loguru import logger
import sys

def configure_logging():
    """
    Configure Loguru avec des couleurs spécifiques pour chaque niveau de log
    et un fichier pour enregistrer les logs.
    """
    logger.remove()

    # Configuration pour l'affichage des logs dans la console
    logger.add(sys.stderr, 
               level="DEBUG",
               format=("{time:YYYY-MM-DD HH:mm:ss} | "
                       "<level>{level}</level> | "
                       "<cyan>{message}</cyan>"),
               colorize=True)

    # Configuration pour écrire les logs dans un fichier
    logger.add("app.log", 
               level="DEBUG",
               format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
               rotation="1 week",
               compression="zip")

# Personnalisation des couleurs par niveau
logger.level("DEBUG", color="<green>")
logger.level("INFO", color="<blue>")
logger.level("WARNING", color="<red>")
logger.level("ERROR", color="<magenta>")
logger.level("CRITICAL", color="<yellow>")