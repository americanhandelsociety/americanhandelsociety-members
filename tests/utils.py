import re

from captcha.models import CaptchaStore

# Utility test function from django-simple-captcha
# https://github.com/mbi/django-simple-captcha/blob/8129ef0276de3c099e838d00f44a102243e2db91/captcha/tests/tests.py#L72-L75
def extract_hash_and_response(response):
    hash = re.findall(r'value="([0-9a-f]+)"', str(response.content))[0]
    captcha = CaptchaStore.objects.get(hashkey=hash).response
    return hash, captcha


def post_valid_user(client):
    response = client.get("/join/")
    hash, captcha = extract_hash_and_response(response)

    data = {
        "first_name": "Queen",
        "last_name": "Cleopatra",
        "email": "cleo@egypt.ico",
        "password1": "1724handel",
        "password2": "1724handel",
        "captcha_0": hash,
        "captcha_1": captcha,
    }

    return client.post("/join/", data=data)