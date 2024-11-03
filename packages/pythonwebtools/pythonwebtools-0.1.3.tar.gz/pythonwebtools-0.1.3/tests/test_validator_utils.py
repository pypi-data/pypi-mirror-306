import pytest
from src.utils.ValidatorUtils import ValidatorsUtil
from tests.mock import *

@pytest.fixture
def validator():
    return ValidatorsUtil()

@pytest.mark.validators
def test_phone_number_validator(validator):
    valid_phone = generate_random_phone_number()
    invalid_phone = "(11) 8000-1234"
    
    assert validator.phone_number_validator(valid_phone) is True
    assert validator.phone_number_validator(invalid_phone) is False

@pytest.mark.validators
def test_validate_password(validator):
    valid_password = generate_strong_password()
    invalid_password = "wrong_password5"
    
    assert validator.validate_password(valid_password) is True
    assert validator.validate_password(invalid_password) is False

@pytest.mark.validators
def test_validate_input(validator):
    valid_data = {'username': 'test_user', 'age': 30}
    required_fields = {'username': str, 'age': int}
    
    assert validator.validate_input(valid_data, required_fields) == []

    invalid_data = {'username': 'test_user', 'age': 'not_a_number'}
    errors = validator.validate_input(invalid_data, required_fields)
    assert len(errors) == 1
    assert "Incorrect type for field 'age': expected int, got str" in errors

@pytest.mark.validators
def test_validate_email(validator):
    valid_email = 'valid-email@email.com'
    invalid_email = "invalid-email"
    
    assert validator.validate_email(valid_email) is None  # No exception should be raised
    with pytest.raises(Exception):
        validator.validate_email(invalid_email)

@pytest.mark.validators
def test_validate_cpf(validator):
    valid_cpf = generate_valid_cpf()
    invalid_cpf = generate_random_cpf()
    
    assert validator.validate_cpf(valid_cpf) is True
    assert validator.validate_cpf(invalid_cpf) is False

@pytest.mark.validators
def test_validate_cnpj(validator):
    valid_cnpj = generate_valid_cnpj()
    invalid_cnpj = generate_random_cnpj()
    
    assert validator.validate_cnpj(valid_cnpj) is True
    assert validator.validate_cnpj(invalid_cnpj) is False
