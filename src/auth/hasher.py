import bcrypt
import logging

logger = logging.getLogger(__name__)


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        try:
            check_password = bcrypt.checkpw(
                plain_password.encode("utf-8"), hashed_password.encode("utf-8")
            )
            return check_password
        except Exception:
            logger.error("Error verifying password", exc_info=True)
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        salt = bcrypt.gensalt()
        try:
            hash_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
                "utf-8"
            )
            return hash_password
        except Exception:
            logger.error("Error hashing password", exc_info=True)
            raise ValueError("Failed to hash the password") from None
