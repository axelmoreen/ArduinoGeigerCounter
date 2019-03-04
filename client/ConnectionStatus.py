from ctypes import Structure, c_bool, c_int

class ConnectionStatus(Structure):
#    _fields_ = [("connected", c_bool), ("collecting", c_bool), ("counts", c_int), ("elapsed", c_int), ("duration", c_int)]
    def __init__(self, connected=False, collecting=False, counts=0, time_elapsed=0, collection_duration=0, connection_string= "COM3"):
        self.connected = connected
        self.collecting = collecting
        self.counts = counts
        self.time_elapsed = time_elapsed
        self.collection_duration = collection_duration
        self.connection_string = connection_string

    def get_is_connected(self):
        return self.connected

    def get_is_collecting(self):
        return self.collecting

    def get_num_counts(self):
        return self.counts

    def get_time_elapsed(self):
        return self.time_elapsed

    def get_collection_duration(self):
        return self.collection_duration

    def get_connection_string(self):
        return self.connection_string

    def set_is_connected(self, connected):
        self.connected = connected

    def set_is_collecting(self, collecting):
        self.collecting = collecting

    def add_count(self):
        self.counts += 1

    def set_time_elapsed(self, time):
        self.time_elasped = time

    def set_collection_duration(self, duration):
        self.collection_duration = duration

    def set_connection_string(self, connection_string):
        self.connection_string = connection_string