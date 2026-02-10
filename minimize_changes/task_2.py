from abc import ABC, abstractmethod
from enum import IntEnum


class ValidationResult:
    def __init__(self, is_valid: bool, errors: list[str]):
        self._is_valid: bool = is_valid
        self._errors: list[str] = errors

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def errors(self) -> list[str]:
        return self._errors


class PasswordValidationResult:
    def __init__(self, is_valid: bool, errors: list[str], strength: int):
        self._is_valid: bool = is_valid
        self._errors: list[str] = errors
        self._strength: int = strength

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def errors(self) -> list[str]:
        return self._errors

    @property
    def strength(self) -> int:
        return self._strength


class ValidateStrategy(ABC):

    @abstractmethod
    def validate(self, password: str) -> ValidationResult:
        pass


class LengthValidation(ValidateStrategy):

    def __init__(self, min_length: int, max_length: int):
        if min_length <= 0:
            raise ValueError("Length must be > 0")
        if max_length < min_length:
            raise ValueError("max_length must be > min_length")
        self._min_length: int = min_length
        self._max_length: int = max_length

    def validate(self, password: str) -> ValidationResult:
        errors: list[str] = []

        password_len: int = len(password)
        is_short: bool = password_len < self._min_length
        is_long: bool = password_len > self._max_length

        if is_short:
            errors.append(f"must contain at least {self._min_length} characters")
        if is_long:
            errors.append(f"must contain not more than {self._max_length} characters")

        is_valid: bool = not is_short and not is_long

        return ValidationResult(is_valid, errors)


class LowerCaseValidation(ValidateStrategy):

    def validate(self, password) -> ValidationResult:
        errors: list[str] = []

        is_valid: bool = any(char.islower() for char in password)
        if not is_valid:
            errors.append("must contain lowercase letter")

        return ValidationResult(is_valid, errors)


class UpperCaseValidation(ValidateStrategy):

    def validate(self, password) -> ValidationResult:
        errors: list[str] = []

        is_valid: bool = any(char.isupper() for char in password)
        if not is_valid:
            errors.append("must contain uppercase letter")

        return ValidationResult(is_valid, errors)


class DigitsValidation(ValidateStrategy):

    def validate(self, password) -> ValidationResult:
        errors: list[str] = []

        is_valid: bool = any(char.isdigit() for char in password)
        if not is_valid:
            errors.append("must contain digit")

        return ValidationResult(is_valid, errors)


class SpecialCharsValidation(ValidateStrategy):

    def validate(self, password) -> ValidationResult:
        special_chars: str = "(!@#$%^&*)"
        errors: list[str] = []

        is_valid: bool = set(special_chars) & set(password) != set("")
        if not is_valid:
            errors.append("must contain special chars")

        return ValidationResult(is_valid, errors)


class AlwaysTrueValidation(ValidateStrategy):

    def validate(self, password) -> ValidationResult:
        return ValidationResult(True, [])


class PasswordStrength(IntEnum):
    WEAK = 1
    MEDIUM = 2
    STRONG = 3


class PasswordValidator:

    def __init__(self) -> None:
        self._validations: list[ValidateStrategy] = [
            LengthValidation(8, 12),
            UpperCaseValidation(),
            LowerCaseValidation(),
            DigitsValidation(),
        ]

        self._strength_rules: dict[PasswordStrength, list[ValidateStrategy]] = {
            PasswordStrength.WEAK: [AlwaysTrueValidation()],
            PasswordStrength.MEDIUM: [SpecialCharsValidation()],
            PasswordStrength.STRONG: [
                SpecialCharsValidation(),
                LengthValidation(10, 12),
            ],
        }

    def validate(self, password: str) -> PasswordValidationResult:
        is_valid: bool = True
        errors: list[str] = []

        for validation in self._validations:
            validation_result: ValidationResult = validation.validate(password)
            errors.extend(validation_result.errors)
            is_valid = validation_result.is_valid and is_valid

        strength: int = PasswordStrength.WEAK
        if is_valid:
            strength = self._check_strength(password)

        return PasswordValidationResult(is_valid, errors, strength)

    def _check_strength(self, password: str) -> int:
        for strength in sorted(self._strength_rules.keys(), reverse=True):
            validators = self._strength_rules[strength]
            if all(validator.validate(password).is_valid for validator in validators):
                return strength
        return PasswordStrength.WEAK
