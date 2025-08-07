import time


class Logger:
    def __init__(self, filename: str = "log.txt") -> None:
        self.filename = filename

    def log(self, level: str, message: str) -> None:
        timestamp = time.localtime()
        timestr = (
            f"{timestamp[0]:04d}-{timestamp[1]:02d}-{timestamp[2]:02d} "
            f"{timestamp[3]:02d}:{timestamp[4]:02d}:{timestamp[5]:02d}"
        )
        log_entry = f"[{timestr}] {level.upper()}: {message}\n"
        try:
            with open(self.filename, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print("Logger error:", e)

    def debug(self, message: str) -> None:
        self.log("debug", message)

    def info(self, message: str) -> None:
        self.log("info", message)

    def warning(self, message: str) -> None:
        self.log("warning", message)

    def error(self, message: str) -> None:
        self.log("error", message)
