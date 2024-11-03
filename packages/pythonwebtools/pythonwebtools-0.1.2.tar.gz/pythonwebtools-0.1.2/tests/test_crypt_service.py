import pytest
from src.services.CryptService import CryptService
from tests.mock import generate_random_text, generate_faker_sentence

@pytest.mark.crypt
def test_encrypt_decrypt():
    crypt_service = CryptService()
    
    # Teste com texto aleatório
    random_text = generate_random_text(50)  # Generate a random text of 50 characters
    encrypted_text = crypt_service.encrypt(random_text)
    decrypted_text = crypt_service.decrypt(encrypted_text)
    
    # Verify if the decrypted text is the same as the original text
    assert decrypted_text == random_text
    
    # Test with a sentence
    faker_sentence = generate_faker_sentence()
    encrypted_sentence = crypt_service.encrypt(faker_sentence)
    decrypted_sentence = crypt_service.decrypt(encrypted_sentence)
    
    # Verify that the sentence is recovered correctly
    assert decrypted_sentence == faker_sentence
