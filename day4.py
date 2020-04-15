import unittest

def double_digit(dig):
    match = [(dig[i] == dig[i+1]) for i in range(len(dig) - 1)]
    return any(match)

def no_decrease(dig):
    match = [dig[i] <= dig[i+1] for i in range(len(dig) - 1)]
    return all(match)

def check_password(password):
    digits = [int(dig) for dig in str(password)]
    result = ((len(digits) == 6) and double_digit(digits)
              and no_decrease(digits))
    return result

def count_passwords(min_val, max_val):
    checks = [check_password(val) for val in range(min_val, max_val + 1)]
    return sum(checks)

def count_consecutive(digits):
    result = []
    count = 1
    for i in range(len(digits) - 1):
        if digits[i] == digits[i+1]:
            count = count + 1
        else:
            result.append(count)
            count = 1
    result.append(count)
    return result

def has_two_in_a_row(digits):
    return 2 in count_consecutive(digits)

def check_password_part_two(password):
    digits = [int(dig) for dig in str(password)]
    result = ((len(digits) == 6) and has_two_in_a_row(digits)
              and no_decrease(digits))
    return result

def count_passwords_part_two(min_val, max_val):
    checks = [check_password_part_two(val) for val in range(min_val, max_val + 1)]
    return sum(checks)

class TestPasswordCheck(unittest.TestCase):

    def run_password_check_test(self, password, expected):
        result = check_password(password)
        self.assertEqual(expected, result)

    def test_check_password(self):
        self.run_password_check_test(111111, True)
        self.run_password_check_test(223450, False)
        self.run_password_check_test(123789, False)

    def test_count_in_range(self):
        self.assertEqual(3, count_passwords(111109, 111113))

    def test_right_answer(self):
        self.assertEqual(1694, count_passwords(156218, 652527))

    def run_count_consecutive(self, password, expected):
        digits = [int(dig) for dig in str(password)]
        result = count_consecutive(digits)
        self.assertEqual(expected, result)

    def test_count_consecutive(self):
        self.run_count_consecutive(111111, [6])
        self.run_count_consecutive(111222, [3, 3])
        self.run_count_consecutive(445200, [2, 1, 1, 2])

    def run_password_check_part_two(self, password, expected):
        result = check_password_part_two(password)
        self.assertEqual(expected, result)

    def test_check_password(self):
        self.run_password_check_part_two(111111, False)
        self.run_password_check_part_two(223450, False)
        self.run_password_check_part_two(123789, False)
        self.run_password_check_part_two(112233, True)
        self.run_password_check_part_two(123444, False)
        self.run_password_check_part_two(111122, True)

    def test_right_answer_part_two(self):
        self.assertEqual(1148, count_passwords_part_two(156218, 652527))

if __name__ == '__main__':
    unittest.main()
