import utils

class TapHandler:
    def __init__(self, id) -> None:
        self.id = id
        self.message_in_buffer = []
        self.tap_buffer = []
        self.message_out_buffer = []
    
    
