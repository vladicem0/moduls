import os


def get_current_packages() -> None:
    os.system('pip list > versions.txt')


def check_updates() -> list[str]:
    os.system('pip list --outdated > outdated.txt')
    outdated = []
    with open('outdated.txt', 'r') as file:
        rows = file.readlines()
        for row in rows:
            outdated.append(row)
    os.remove('outdated.txt')
    if not outdated:
        outdated.append('No updates found')
    return outdated


def upgrade() -> None:
    os.system('python -m pip install --upgrade pip')
    os.system('pip list > installed_packages')
    with open('installed_packages', 'r') as file:
        rows = file.readlines()
        for row in rows[2:]:
            os.system(f'pip install --upgrade {row.split()[0]}')
    os.remove('installed_packages')
