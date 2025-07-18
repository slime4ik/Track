import random
import string
from django.core.cache import cache
from django.core.mail import send_mail

EMAIL_CODE_TTL = 60 * 10

def generate_code(length: int = 6) -> int:
    return int(''.join(random.choices(string.digits, k=length)))

def set_code_in_redis(email: str) -> str:
    code = generate_code()
    key = f'verify_code:{email}'
    cache.set(key, code, timeout=EMAIL_CODE_TTL)  # перезапишет старый код
    return code


def check_code_in_redis(email: str, code: str) -> bool:
    key = f'verify_code:{email}'
    stored_code = cache.get(key)
    if stored_code == code:
        cache.delete(key)
        return True
    return False