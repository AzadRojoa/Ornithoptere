try:
    import _thread
except ImportError:
    _thread = None


class TableauTerminal:
    def __init__(self, data, refresh=0.1, titre=None):
        self._data = data.copy()
        self._refresh = refresh
        self._titre = titre
        self._running = False
        self._lock = None
        if _thread:
            import time

            self._lock = _thread.allocate_lock()
        else:
            import threading

            self._lock = threading.Lock()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        if self._lock:
            self._lock.acquire()
        self._data = new_data.copy()
        if self._lock:
            self._lock.release()

    def _afficher_tableau(self):
        while self._running:
            if self._lock:
                self._lock.acquire()
            data = self._data.copy()
            if self._lock:
                self._lock.release()
            # Efface l'écran et remet le curseur en haut
            print("\033[2J\033[H", end="")

            # Afficher le titre s'il existe
            if self._titre:
                print(f"\n{self._titre}")
                print("=" * len(self._titre))
                print()

            keys = list(data.keys())
            values = [str(data[k]) for k in keys]
            col_widths = [
                max(len(str(k)), len(str(v))) + 2 for k, v in zip(keys, values)
            ]
            line = "+"
            for w in col_widths:
                line += "-" * w + "+"
            print(line)
            row = "|"
            for k, w in zip(keys, col_widths):
                row += f" {str(k).ljust(w-1)}|"
            print(row)
            row = "|"
            for v, w in zip(values, col_widths):
                row += f" {str(v).ljust(w-1)}|"
            print(row)
            print(line)
            print("(Ctrl+C pour quitter)")
            import time

            time.sleep(self._refresh)

    def start(self):
        self._running = True
        if _thread:
            _thread.start_new_thread(self._afficher_tableau, ())
        else:
            import threading

            t = threading.Thread(target=self._afficher_tableau)
            t.daemon = True
            t.start()

    def stop(self):
        self._running = False
