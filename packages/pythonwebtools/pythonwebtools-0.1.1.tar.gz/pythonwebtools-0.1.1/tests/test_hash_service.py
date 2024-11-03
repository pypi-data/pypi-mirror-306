import pytest
from src.services.HashService import HashService
from tests.mock import generate_strong_password

@pytest.mark.hash
def test_hash_password():
    hash_service = HashService()
    password = generate_strong_password(length=8)
    
    # Hash the password
    hashed_password = hash_service.hash_password(password)
    
    # Verify that the hashed password is not empty
    assert hashed_password is not None
    assert hashed_password != password  # The hashed password should not match the original

    # Verify that the hashed password can be verified correctly
    is_valid = hash_service.verify_password(hashed_password=hashed_password, provided_password=password)
    assert is_valid == True

    # Verify that  an invalid password is rejected
    is_valid = hash_service.verify_password(hashed_password=hashed_password, provided_password='wrong_password5')
    assert is_valid == False
