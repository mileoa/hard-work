import unittest
from task_2 import ValidationResult, PasswordValidator


class TestPasswordValidator(unittest.TestCase):

    def test_validate_is_valid(self):
        validator = PasswordValidator()
        password = "Aa0Aa0Aa0A"

        result = validator.validate(password)

        assert result.errors == []
        assert result.is_valid

    def test_validate_is_not_valid_no_digits(self):
        validator = PasswordValidator()
        password = "AaaAaaAaaA"

        result = validator.validate(password)

        assert result.errors == ["must contain digits"]
        assert not result.is_valid

    def test_validate_is_not_valid_no_lowercase(self):
        validator = PasswordValidator()
        password = "AA0AA0AA0A"

        result = validator.validate(password)

        assert result.errors == ["must contain lowercase letter"]
        assert not result.is_valid

    def test_validate_is_not_valid_no_uppercase(self):
        validator = PasswordValidator()
        password = "aa0aa0aa0a"

        result = validator.validate(password)

        assert result.errors == ["must contain uppercase letter"]
        assert not result.is_valid

    def test_validate_is_not_valid_short(self):
        validator = PasswordValidator()
        password = "Aa0Aa0Aa0"

        result = validator.validate(password)

        assert result.errors == ["must contain at least 8 characters"]
        assert not result.is_valid

    def test_validate_is_not_valid_all_errors(self):
        validator = PasswordValidator()
        password = "abc"

        result = validator.validate(password)

        assert result.errors == [
            "must contain at least 8 characters",
            "must contain uppercase letter",
            "must contain lowercase letter",
        ]
        assert not result.is_valid


if __name__ == "__main__":
    unittest.main()
