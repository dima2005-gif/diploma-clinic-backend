from main.models import CustomUser


def generate_username(email):
    base = email.split("@")[0].lower()
    username = base
    counter = 1

    while CustomUser.objects.filter(username=username).exists():
        username = f"{base}{counter}"
        counter += 1

    return username
