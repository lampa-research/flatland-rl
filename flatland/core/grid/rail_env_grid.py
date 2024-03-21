from flatland.core.grid.grid4 import Grid4Transitions
from flatland.utils.ordered_set import OrderedSet
from flatland.utils.directed_tiles import DirectedTiles

class RailEnvTransitions(Grid4Transitions):
    """
    Special case of `GridTransitions` over a 2D-grid, with a pre-defined set
    of transitions mimicking the types of real Swiss rail connections.

    As no diagonal transitions are allowed in the RailEnv environment, the
    possible transitions for RailEnv from a cell to its neighboring ones
    are represented over 16 bits.

    The 16 bits are organized in 4 blocks of 4 bits each, the direction that
    the agent is facing.
    E.g., the most-significant 4-bits represent the possible movements (NESW)
    if the agent is facing North, etc...

    agent's direction:          North    East   South   West
    agent's allowed movements:  [nesw]   [nesw] [nesw]  [nesw]
    example:                     1000     0000   0010    0000

    In the example, the agent can move from North to South and viceversa.
    """

    # Contains the basic transitions;
    # the set of all valid transitions is obtained by successive 90-degree rotation of one of these basic transitions.
    transition_list = [int('0000000000000000', 2),  # empty cell - Case 0
                       int('1000000000100000', 2),  # Case 1 - straight
                       int('1000000000000000', 2),  # Case 2 - straight directed
                       int('0010000000000000', 2),  # Case 3 - deadend
                       int('1000010000100001', 2),  # Case 4 - diamond crossing
                       int('0100000000000010', 2),  # Case 5 - simple turn
                       int('0101001000000010', 2),  # Case 6 - symmetrical switch
                       int('0001001001001000', 2),  # Case 7 - asymetrical switch
                       int('1001001000100000', 2),  # Case 8 - simple switch a
                       int('1100000000100010', 2),  # Case 9 - simple switch b
                       int('0101011000000011', 2),  # Case 10 - T switch
                       int('1101001000100010', 2),  # Case 11 - arrow switch
                       int('1001001001101000', 2),  # Case 12 - double x switch a
                       int('1100100000110010', 2),  # Case 13 - double x switch b
                       int('1001011000100001', 2),  # Case 14 - single slip switch
                       int('1101011000100011', 2),  # Case 15 - double slip switch a
                       int('1001011001101001', 2),  # Case 16 - double slip switch b
                       int('0101001001001010', 2),  # Case 17 - simple triple switch
                       int('0101011001001011', 2),  # Case 18 - triple x switch a
                       int('1101001001101010', 2),  # Case 19 - triple x switch b
                       int('1101011001101011', 2),  # Case 20 - triple slip switch
                       int('1101101001111010', 2),  # Case 21  - quadruple x switch
                       int('0101101001011010', 2),  # Case 22  - all turns
                       int('1101111001111011', 2)]  # Case 23 - all directions
    dt = DirectedTiles()
    transition_list.extend(dt.get_extra_transition_list())

    def __init__(self):
        super(RailEnvTransitions, self).__init__(
            transitions=self.transition_list
        )

        # create this to make validation faster
        self.transitions_all = OrderedSet()
        for index, trans in enumerate(self.transitions):
            self.transitions_all.add(trans)
            if index in (2, 3, 5, 6, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20):
                for _ in range(3):
                    trans = self.rotate_transition(trans, rotation=90)
                    self.transitions_all.add(trans)
            elif index in (1, 7, 12, 13, 16, 21):
                trans = self.rotate_transition(trans, rotation=90)
                self.transitions_all.add(trans)
            elif index > 23:
                trans = self.rotate_transition(trans, rotation=90)
                self.transitions_all.add(trans)

    def print(self, cell_transition):
        print("  NESW")
        print("N", format(cell_transition >> (3 * 4) & 0xF, '04b'))
        print("E", format(cell_transition >> (2 * 4) & 0xF, '04b'))
        print("S", format(cell_transition >> (1 * 4) & 0xF, '04b'))
        print("W", format(cell_transition >> (0 * 4) & 0xF, '04b'))

    def is_valid(self, cell_transition):
        """
        Checks if a cell transition is a valid cell setup.

        Parameters
        ----------
        cell_transition : int
            64 bits used to encode the valid transitions for a cell.

        Returns
        -------
        Boolean
            True or False
        """
        return cell_transition in self.transitions_all
