import utils

class TapHandler:
    def __init__(self, id) -> None:
        self.id = id
        self.message_in_buffer = []
        self.tap_buffer = []
        self.message_out_buffer = []
    
    def word_finished(self):
        if len(self.tap_buffer) > 2:
            start_time = self.tap_buffer[-2]
            end_time = self.tap_buffer[-1]
            