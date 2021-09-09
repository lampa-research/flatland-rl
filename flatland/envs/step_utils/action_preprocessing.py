from flatland.core.grid.grid_utils import position_to_coordinate
from flatland.envs.agent_utils import TrainState
from flatland.envs.rail_env_action import RailEnvActions
from flatland.envs.step_utils.transition_utils import check_valid_action


def process_illegal_action(action: RailEnvActions):
	if not RailEnvActions.check_valid_action(action): 
		return RailEnvActions.DO_NOTHING
	else:
		return RailEnvActions(action)


def process_do_nothing(state: TrainState):
    if state == TrainState.MOVING:
        action = RailEnvActions.MOVE_FORWARD
    else:
        action = RailEnvActions.STOP_MOVING
    return action


def process_left_right(action, rail, position, direction):
    if not check_valid_action(action, rail, position, direction):
        action = RailEnvActions.MOVE_FORWARD
    return action


def preprocess_action_when_waiting(action, state):
    """
    Set action to DO_NOTHING if in waiting state
    """
    if state == TrainState.WAITING:
        action = RailEnvActions.DO_NOTHING
    return action


def preprocess_raw_action(action, state):
    """
    Preprocesses actions to handle different situations of usage of action based on context
        - DO_NOTHING is converted to FORWARD if train is moving
        - DO_NOTHING is converted to STOP_MOVING if train is moving
    """
    action = process_illegal_action(action)

    if action == RailEnvActions.DO_NOTHING:
        action = process_do_nothing(state)

    return action

def preprocess_moving_action(action, rail, position, direction):
    """
    LEFT/RIGHT is converted to FORWARD if left/right is not available and train is moving
    FORWARD is converted to STOP_MOVING if leading to dead end?
    """
    if action in [RailEnvActions.MOVE_LEFT, RailEnvActions.MOVE_RIGHT]:
        action = process_left_right(action, rail, position, direction)

    if not check_valid_action(action, rail, position, direction): # TODO: Dipam - Not sure if this is needed
        action = RailEnvActions.STOP_MOVING
    return action