class AppBaseException(Exception):
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.status_code = error_code
        super().__init__(f"[{error_code}] {message}")
