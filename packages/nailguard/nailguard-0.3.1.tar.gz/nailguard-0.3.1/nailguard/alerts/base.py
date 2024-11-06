class Alert:
    
    def __init__(self):
        self.last_detected = False
    
    def handle(self, detected: bool):
        if detected and not self.last_detected:
            self.on_start()
        elif not detected and self.last_detected:
            self.on_stop()
        elif detected:
            self.on_active()
        self.last_detected = detected
    
    def on_start(self):
        pass

    def on_stop(self):
        pass
    
    def on_active(self):
        pass
