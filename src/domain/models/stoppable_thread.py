from threading import Thread, Event


class StoppableThread(Thread):
    def __init__(self, *args, **kargs):
        super(StoppableThread, self).__init__(*args, **kargs)
        self._stop_event = Event()

    def stop(self):
        self.status = False
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
