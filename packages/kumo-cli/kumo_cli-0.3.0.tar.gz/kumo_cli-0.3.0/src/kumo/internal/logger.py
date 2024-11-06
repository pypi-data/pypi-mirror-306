import logging


class KumoLogger:
    def __init__(self, name, log_file="deploy.log", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Criar um manipulador de arquivo
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Criar um manipulador de console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Criar um formatador detalhado para o arquivo
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)

        # Criar um formatador resumido para o console
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)

        # Adicionar os manipuladores ao logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
