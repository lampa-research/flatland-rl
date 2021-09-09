from enum import IntEnum

class TrainState(IntEnum):
    WAITING = 0
    READY_TO_DEPART = 1
    MALFUNCTION_OFF_MAP = 2
    MOVING = 3
    STOPPED = 4
    MALFUNCTION = 5
    DONE = 6

    @classmethod
    def check_valid_state(cls, state):
        return state in cls._value2member_map_

    def is_malfunction_state(self):
        return self.value in [self.MALFUNCTION, self.MALFUNCTION_OFF_MAP]

    def is_off_map_state(self):
        return self.value in [self.WAITING, self.READY_TO_DEPART, self.MALFUNCTION_OFF_MAP]
    
    def is_on_map_state(self):
        return self.value in [self.MOVING, self.STOPPED, self.MALFUNCTION]

    


