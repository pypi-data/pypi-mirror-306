import re
import os
from typing import Dict, List, Any
from email_validator import validate_email, EmailNotValidError


class ValidatorUtils:
    def __init__(self):
        self.phone_pattern = r'^\d{2}9\d{8}$'
        self.password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}:;"\'<>,.?/~`-]).{8,}$'

    def phone_number_validator(self, phone_number: str) -> bool:
        """
        Validates a given phone number against a regular expression pattern.

        :param phone_number: A string representing the phone number to be validated.
        :return: A boolean value indicating whether the phone number is valid (True) or not (False).
        """
        return re.match(self.phone_pattern, phone_number) is not None

    def validate_password(self, password: str) -> bool:
        """
        Validates a given password against a regular expression pattern.

        :param password: A string representing the password to be validated.
        :return: A boolean value indicating whether the password is valid (True) or not (False).
        """
        return bool(re.match(self.password_regex, password))

    def validate_input(self, data: Dict[str, Any], required_fields: Dict[str, type]) -> List[str]:
        """
        Validates the presence and type of required fields in the input data.

        :param data: A dictionary containing the actual data to validate.
        :param required_fields: A dictionary specifying required fields as keys and their expected types as values.
        :return: A list of error messages indicating missing fields or type mismatches.
        """
        errors = []

        for field, expected_type in required_fields.items():
            if field not in data:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(data[field], expected_type):
                errors.append(
                    f"Incorrect type for field '{field}': expected {expected_type.__name__}, got {type(data[field]).__name__}")

        return errors

    def validate_email(self, email: str) -> bool:
        """
        Validates an email address using the email-validator library.

        :param email: A string representing the email address to be validated.
        :return: True if the email address is valid.
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            return False

    def validate_cpf(self, cpf: str) -> bool:
        """
        Validates a Brazilian CPF (Cadastro de Pessoas Físicas).
        """
        cpf = re.sub(r'\D', '', cpf)

        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        digit1 = self._calculate_cpf_digit(cpf[:-2])
        digit2 = self._calculate_cpf_digit(cpf[:-1], second=True)

        return cpf[-2:] == f"{digit1}{digit2}"

    def validate_cnpj(self, cnpj: str) -> bool:
        """
        Validates a Brazilian CNPJ (Cadastro Nacional da Pessoa Jurídica).
        """
        cnpj = re.sub(r'\D', '', cnpj)

        if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
            return False

        digit1 = self._calculate_cnpj_digit(cnpj[:-2])
        digit2 = self._calculate_cnpj_digit(cnpj[:-1], second=True)

        return cnpj[-2:] == f"{digit1}{digit2}"

    def _calculate_cpf_digit(self, number: str, second: bool = False) -> int:
        """
        Calculates the verification digit for CPF.
        """
        factor = 10 if not second else 11
        total = sum(int(digit) * factor for digit, factor in zip(number, range(factor, 1, -1)))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    def _calculate_cnpj_digit(self, number: str, second: bool = False) -> int:
        """
        Calculates the verification digit for CNPJ.
        """
        factors = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2] if not second else [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        total = sum(int(digit) * factor for digit, factor in zip(number, factors))

        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
