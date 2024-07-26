import logging

# Настройка логирования 
def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ])
def loggin():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', handlers=[
                            logging.FileHandler("logging.log"),
                            logging.StreamHandler()
                        ])