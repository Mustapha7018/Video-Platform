import random
from django.utils import timezone


def generate_activation_code():
    return int("".join([str(random.randint(1, 9)) for _ in range(6)]))


def is_expired(expiration_date):
    return timezone.now() > expiration_date


def combine_code(request):
    try:
        code = (
            (request.POST.get("input1") or '') +
            (request.POST.get("input2") or '') +
            (request.POST.get("input3") or '') +
            (request.POST.get("input4") or '') +
            (request.POST.get("input5") or '') +
            (request.POST.get("input6") or '')
        )
        if not code.isdigit():
            raise ValueError("Verification code must be numeric.")
        return int(code)
    except ValueError as e:
        raise ValueError("Invalid verification code.")



