from argon2 import PasswordHasher, exceptions


class HashService:
    def __init__(self):
        self.ph = PasswordHasher(
            time_cost=2,
            memory_cost=102400,
            parallelism=8)
    
    def hash_password(self, password):
        return self.ph.hash(password)
    
    def verify_password(self, hashed_password, provided_password):
        try:
            self.ph.verify(hashed_password, provided_password)
            return True
        except exceptions.VerifyMismatchError:
            return False
