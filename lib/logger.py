import time

class Logger:
    def __init__(self, filename="log.txt"):
        self.filename = filename

    def log(self, level, message):
        timestamp = time.localtime()
        timestr = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            timestamp[0], timestamp[1], timestamp[2],
            timestamp[3], timestamp[4], timestamp[5]
        )
        log_entry = "[{}] {}: {}\n".format(timestr, level.upper(), message)
        try:
            with open(self.filename, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print("Logger error:", e)

    def debug(self, message):
        self.log("debug", message)

    def info(self, message):
        self.log("info", message)

    def warning(self, message):
        self.log("warning", message)

    def error(self, message):
        self.log("error", message)