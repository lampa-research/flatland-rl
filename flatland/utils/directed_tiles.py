from itertools import combinations


class DirectedTiles():
    def __init__(self) -> None:
        # Initialize the list of substrings in a sorted way
        substrings = ["NN", "NE", "NW", "EN", "EE",
                      "ES", "SE", "SS", "SW", "WN", "WS", "WW"]

        rail_files = {
            "": "case_0_empty.png",
            "NN SS": "case_1_straight.png",
            "NN": "case_2_straight_directed.png",
            "NS": "case_3_deadend.png",
            "NN EE SS WW": "case_4_diamond_crossing.png",
            "NE WS": "case_5_simple_turn.png",
            "NE NW ES WS": "case_6_symetrical_switch.png",
            "NW ES SE WN": "case_7_asymetrical_switch.png",
            "NN NW ES SS": "case_8_simple_switch_a.png",
            "NN NE SS WS": "case_9_simple_switch_b.png",
            "NE NW EE ES WS WW": "case_10_T_switch.png",
            "NN NE NW ES SS WS": "case_11_arrow_switch.png",
            "NN NW ES SE SS WN": "case_12_double_x_switch_a.png",
            "NN NE EN SS SW WS": "case_13_double_x_switch_b.png",
            "NN NW EE ES SS WW": "case_14_single_slip_switch.png",
            "NN NE NW EE ES SS WS WW": "case_15_double_slip_switch_a.png",
            "NN NW EE ES SE SS WN WW": "case_16_double_slip_switch_b.png",
            "NE NW ES SE WN WS": "case_17_simple_triple_switch.png",
            "NE NW EE ES SE WN WS WW": "case_18_triple_x_switch_a.png",
            "NN NE NW ES SE SS WN WS": "case_19_triple_x_switch_b.png",
            "NN NE NW EE ES SE SS WN WS WW": "case_20_triple_slip_switch.png",
            "NN NE NW EN ES SE SS SW WN WS": "case_21_quadruple_x_switch.png",
            "NE NW EN ES SE SW WN WS": "case_22_all_turns.png",
            "NN NE NW EN EE ES SE SS SW WN WS WW": "case_23_all_directions.png"
        }

        # generate all possible transitions and their binary versions
        transitions = self.generate_strings(substrings)
        transitions_binary = [self.transition_to_binary(
            transition) for transition in transitions]

        # enumerate existing transitions and their binary versions, remember pngs
        existing_transitions = [
            transition for transition, png in rail_files.items()]
        existing_transitions_binary = [self.transition_to_binary(
            transition) for transition in existing_transitions]
        existing_rotations = [0 for transition in existing_transitions]
        existing_pngs = [png for transition, png in rail_files.items()]

        # add the rotations
        for index, trans in enumerate(existing_transitions_binary):
            if index in (2, 3, 5, 6, 8, 9, 10, 11, 14, 15, 17, 18, 19, 20):
                for rot in range(3):
                    trans = self.fast_grid4_rotate_transition(
                        trans, rotation=90)
                    existing_transitions_binary.append(trans)
                    existing_rotations.append((rot + 1) * 90)
                    existing_pngs.append(existing_pngs[index])
            elif index in (1, 7, 12, 13, 16, 21):
                trans = self.fast_grid4_rotate_transition(trans, rotation=90)
                existing_transitions_binary.append(trans)
                existing_rotations.append(90)
                existing_pngs.append(existing_pngs[index])

        # remove existing transitions from all transitions
        indices = [i for i, element in enumerate(
            transitions_binary) if element in existing_transitions_binary]
        transitions = [transition for i, transition in enumerate(
            transitions) if i not in indices]
        transitions_binary = [transition for i, transition in enumerate(
            transitions_binary) if i not in indices]

        # sort the existing transition list, return sorted indices
        sorted_indices = sorted(range(len(existing_transitions_binary)), key=lambda i: bin(
            existing_transitions_binary[i])[2:].count('1'))

        # match the transitions to existing transitions
        # for each transition, go through the sorted existing transitions and figure out whether the transition can be obtained by removing 1s
        # if so, associate it with the corresponding png and export to the final list
        # generate the transition_list (rail_env_grid)
        # generate the rail_files (graphics_pil)
        self.transition_list_extra = []
        self.binary_transitions_extra = []
        self.rail_files_extra = {}
        self.rail_file_rotations = {}
        for i, transition in enumerate(transitions_binary):
            self.transition_list_extra.append(transition)
            for index in sorted_indices:
                if self.can_construct_by_removing_ones(transition, existing_transitions_binary[index]):
                    self.binary_transitions_extra.append(transition)
                    self.rail_files_extra[transitions_binary[i]
                                          ] = existing_pngs[index]
                    self.rail_file_rotations[transitions_binary[i]
                                             ] = existing_rotations[index]
                    break

        # add rotated versions?

    def get_extra_transition_list(self):
        return self.transition_list_extra

    def get_extra_binary_transitions(self):
        return self.binary_transitions_extra

    def get_extra_rail_files(self):
        return self.rail_files_extra

    def get_rail_file_rotations(self):
        return self.rail_file_rotations

    def generate_strings(self, substrings):
        # Container for the results
        result = []

        # Generate combinations
        for r in range(1, len(substrings) + 1):
            for comb in combinations(substrings, r):
                # Check if the combinations starts with an "N" substring
                if comb[0] in {"NN", "NE", "NW"}:
                    result.append(" ".join(comb))

        # Sort the strings by the length
        result.sort(key=lambda s: (len(s.split()),
                    substrings.index(s.split()[0])))
        return result

    def transition_to_binary(self, transition):
        # Translate the ascii transition description in the format  "NE WS" to the
        # binary list of transitions as per RailEnv - NESW (in) x NESW (out)
        directions = list("NESW")
        transition_16_bit = ["0"] * 16
        for sTran in transition.split(" "):
            if len(sTran) == 2:
                in_direction = directions.index(sTran[0])
                out_direction = directions.index(sTran[1])
                transition_idx = 4 * in_direction + out_direction
                transition_16_bit[transition_idx] = "1"
        transition_16_bit_string = "".join(transition_16_bit)
        return int(transition_16_bit_string, 2)

    def fast_grid4_get_transitions(self, cell_transition, orientation):
        bits = (cell_transition >> ((3 - orientation) * 4))
        return ((bits >> 3) & 1, (bits >> 2) & 1, (bits >> 1) & 1, (bits) & 1)

    def fast_grid4_set_transitions(self, cell_transition, orientation, new_transitions):
        mask = (1 << ((4 - orientation) * 4)) - (1 << ((3 - orientation) * 4))
        negmask = ~mask

        new_transitions = \
            (new_transitions[0] & 1) << 3 | \
            (new_transitions[1] & 1) << 2 | \
            (new_transitions[2] & 1) << 1 | \
            (new_transitions[3] & 1)

        cell_transition = (cell_transition & negmask) | (
            new_transitions << ((3 - orientation) * 4))

        return cell_transition

    def fast_grid4_rotate_transition(self, cell_transition, rotation=0):
        value = cell_transition
        rotation = rotation // 90
        for i in range(4):
            block_tuple = self.fast_grid4_get_transitions(value, i)
            block_tuple = block_tuple[(4 - rotation):] + \
                block_tuple[:(4 - rotation)]
            value = self.fast_grid4_set_transitions(value, i, block_tuple)

        # Rotate the 4-bits blocks
        value = ((value & (2 ** (rotation * 4) - 1)) << ((4 - rotation) * 4)) | (
            value >> (rotation * 4))

        cell_transition = value
        return cell_transition

    def can_construct_by_removing_ones(self, x, y):
        """
        Check if x can be constructed by only removing 1s from the binary representation of y.
        """
        return (x & y) == x
