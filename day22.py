import unittest
import re

TEST_INSTRUCTIONS = """
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""

TEST_INSTRUCTIONS2 = """
deal with increment 7
deal into new stack
deal into new stack
"""

TEST_INSTRUCTIONS3 = """
cut 6
deal with increment 7
deal into new stack
"""


def deal_new_stack(cards):
    return list(reversed(cards))


def cut_deck(cards, position):
    result = cards[position:] + cards[:position]
    return result


def deal_increment(cards, increment):
    num_cards = len(cards)
    result = [0] * num_cards
    for index, card in enumerate(cards):
        position = (increment * index) % num_cards
        result[position] = card
    return result


def parse_instructions(instructions):
    patterns = {r'cut (-?[0-9]*)': cut_deck,
                r'deal into new stack' : deal_new_stack,
                r'deal with increment (-?[0-9]*)' : deal_increment}
    result = []
    for line in instructions.splitlines():
        for pattern, fun_name in patterns.items():
            match = re.match(pattern, line)
            if match:
                groups = match.groups()
                this_result = [fun_name]
                for group in groups:
                    this_result.append(int(group))
                result.append(tuple(this_result))
    return result


def run_instructions(instructions, cards):
    to_do = parse_instructions(instructions)
    for fun_name, *args in to_do:
        cards = fun_name(cards, *args)
    return cards


def evaluate_state(state, card_value):
    slope, intercept, length = state
    return (slope * card_value + intercept) % length


def apply_instructions_to_state(instructions, state):
    todo = parse_instructions_state(instructions)
    for fun_name, *args in todo:
        state = fun_name(state, *args)
    return state


def cut_deck_state(state, position):
    slope, intercept, length = state
    new_slope = slope
    new_intercept = (intercept + position * slope) % length
    return new_slope, new_intercept, length


def deal_new_stack_state(state):
    slope, intercept, length = state
    new_slope = -slope % length
    new_intercept = (intercept - slope) % length
    return new_slope, new_intercept, length


def deal_increment_state(state, increment):
    slope, intercept, length = state
    new_slope = (slope * pow(increment, -1, length)) % length
    new_intercept = intercept
    return new_slope, new_intercept, length

def parse_instructions_state(instructions):
    patterns = {r'cut (-?[0-9]*)': cut_deck_state,
                r'deal into new stack' : deal_new_stack_state,
                r'deal with increment (-?[0-9]*)' : deal_increment_state}
    result = []
    for line in instructions.splitlines():
        for pattern, fun_name in patterns.items():
            match = re.match(pattern, line)
            if match:
                groups = match.groups()
                this_result = [fun_name]
                for group in groups:
                    this_result.append(int(group))
                result.append(tuple(this_result))
    return result


def apply_many_times(state, num_times):
    slope, intercept, length = state
    new_slope = int(pow(slope, num_times, length))
    new_intercept = intercept * ((1 - new_slope) * pow(1 - slope, -1, length))
    return new_slope, new_intercept, length


class TestShuffle(unittest.TestCase):
    def test_deal_new_stack(self):
        cards = list(range(10))
        result = deal_new_stack(cards)
        expected_result = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.assertEqual(expected_result, list(result))

    def test_deal_new_stack_state(self):
        state = deal_new_stack_state((1, 0, 10))
        expected_result = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        self.compare_to_expected(expected_result, state)

    def compare_to_expected(self, expected_result, state):
        for index, expected in enumerate(expected_result):
            result = evaluate_state(state, index)
            self.assertEqual(expected, result)

    def test_cut_positive(self):
        cards = list(range(10))
        result = cut_deck(cards, 3)
        expected_result = [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
        self.assertEqual(expected_result, result)

    def test_cut_positive_state(self):
        state = cut_deck_state((1, 0, 10), 3)
        expected_result = [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
        self.compare_to_expected(expected_result, state)

    def test_cut_negative(self):
        cards = list(range(10))
        result = cut_deck(cards, -4)
        expected_result = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
        self.assertEqual(expected_result, result)

    def test_cut_negative_state(self):
        state = cut_deck_state((1, 0, 10), -4)
        expected_result = [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
        self.compare_to_expected(expected_result, state)

    def test_deal_increment(self):
        cards = list(range(10))
        result = deal_increment(cards, 3)
        expected_result = [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
        self.assertEqual(expected_result, result)

    def test_deal_increment_state(self):
        state = deal_increment_state((1, 0, 10), 3)
        expected_result = [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
        self.compare_to_expected(expected_result, state)

    def test_deal_increment_state2(self):
        state = deal_increment_state((1, 1, 10), 3)
        expected_result = [1, 8, 5, 2, 9, 6, 3, 0, 7, 4]
        self.compare_to_expected(expected_result, state)

    def test_parse_instructions(self):
        result = parse_instructions(TEST_INSTRUCTIONS)
        expected_result = [(deal_new_stack,),
                           (cut_deck, -2),
                           (deal_increment, 7),
                           (cut_deck, 8),
                           (cut_deck, -4),
                           (deal_increment, 7),
                           (cut_deck, 3),
                           (deal_increment, 9),
                           (deal_increment, 3),
                           (cut_deck, -1)]
        self.assertEqual(expected_result, result)

    def test_run_instructions(self):
        cards = list(range(10))
        result = run_instructions(TEST_INSTRUCTIONS, cards)
        expected_result = [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
        self.assertEqual(expected_result, result)

    def test_run_instructions_compare(self):
        cards = list(range(10))
        state =(1, 0, 10)
        base_cards = cards
        instructions = TEST_INSTRUCTIONS
        to_do = parse_instructions(instructions)
        to_do_state = parse_instructions_state(instructions)
        for ((fun_name, *args), (fun_state, *state_args)) in zip(to_do, to_do_state):
            print('----------------------')
            print(fun_name)
            print(fun_state)
            cards = fun_name(cards, *args)
            state = fun_state(state, *state_args)
            self.compare_to_expected(cards, state)

    def test_increment_state_different(self):
        state = (9, 1, 10)
        new_state = deal_increment_state(state, 7)
        expected_result = [1, 8, 5, 2, 9, 6, 3, 0, 7, 4]
        self.compare_to_expected(expected_result, new_state)

    def test_run_instructions_state(self):
        state = apply_instructions_to_state(TEST_INSTRUCTIONS, (1, 0, 10))
        expected_result = [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
        self.compare_to_expected(expected_result, state)

    def test_run_instructions_state2(self):
        state = apply_instructions_to_state(TEST_INSTRUCTIONS2, (1, 0, 10))
        expected_result = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
        self.compare_to_expected(expected_result, state)

    def test_run_instructions_state3(self):
        state = apply_instructions_to_state(TEST_INSTRUCTIONS3, (1, 0, 10))
        expected_result = [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
        self.compare_to_expected(expected_result, state)

    def test_run_part_1(self):
        cards = range(10007)
        with open('day22_input.txt') as infile:
            instructions = infile.read()
        cards = run_instructions(instructions, cards)
        index = cards.index(2019)
        self.assertEqual(8502, index)

    def test_evaluate_state(self):
        state = (2, 1, 10)
        index = evaluate_state(state, 4)
        self.assertEqual(index, 9)

    def test_run_part_1v2(self):
        with open('day22_input.txt') as infile:
            instructions = infile.read()
        final_state = apply_instructions_to_state(instructions, (1, 0, 10007))
        index = evaluate_state(final_state, 8502)
        self.assertEqual(2019, index)

    def test_run_part_2(self):
        state = (1, 0, 119315717514047)
        with open('day22_input.txt') as infile:
            instructions = infile.read()
        inst_state = apply_instructions_to_state(instructions, state)
        final_state = apply_many_times(inst_state, 101741582076661)
        result = evaluate_state(final_state, 2020)
        self.assertEqual(41685581334351, result)

if __name__ == '__main__':
    unittest.main()
