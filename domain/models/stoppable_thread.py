from threading import Thread, Event


class StoppableThread(Thread):
    def __init__(self, target = None):
        super().__init__()
        self._stop_event = Event()
        self.target = target

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
        if self.target is not None:
            self.target(self._stop_event)
