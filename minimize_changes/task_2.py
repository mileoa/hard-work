from abc import ABC, abstractmethod


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
    def __init__(self, is_valid: bool, errors: list[str], strength: str):
        self._is_valid: bool = is_valid
        self._errors: list[str] = errors
        self._strength: str = strength

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def errors(self) -> list[str]:
        return self._errors

    @property
    def strength(self) -> str:
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

    def validate(self, password):
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

    def validate(self, password):
        errors: list[str] = []

        is_valid: bool = any(char.islower() for char in password)
        if not is_valid:
            errors.append("must contain lowercase letter")

        return ValidationResult(is_valid, errors)


class UpperCaseValidation(ValidateStrategy):

    def validate(self, password):
        errors: list[str] = []

        is_valid: bool = any(char.isupper() for char in password)
        if not is_valid:
            errors.append("must contain uppercase letter")

        return ValidationResult(is_valid, errors)


class PasswordValidator:

    def __init__(self):
        self._validations: list[ValidateStrategy] = [
            LengthValidation(8, 12),
            LowerCaseValidation(),
            UpperCaseValidation(),
        ]

    def validate(self, password: str) -> ValidationResult:
        is_valid: bool = True
        errors: list[str] = []

        for validation in self._validations:
            validation_result: ValidationResult = validation.validate(password)
            errors.extend(validation_result.errors)
            is_valid = validation_result.is_valid and is_valid

        return PasswordValidationResult(is_valid, errors, "")
