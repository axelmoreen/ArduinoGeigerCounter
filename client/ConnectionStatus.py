class ConnectionStatus:
    def __init__(self):
        self.connected = False
        self.collecting = False
        self.counts = 0
        self.time_elapsed = 0
        self.collection_duration = 0
        self.connection_string = "COM3"