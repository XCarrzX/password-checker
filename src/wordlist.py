from pathlib import Path

WORDLIST_PATH = Path(__file__).parent.parent / "data" / "common_passwords.txt"


def load_common_passwords() -> set:
    """
    Load daftar password umum dari file wordlist.

    Returns:
        Set berisi password-password yang dianggap lemah/umum
    """
    if not WORDLIST_PATH.exists():
        return set()

    with open(WORDLIST_PATH, "r") as f:
        return {line.strip().lower() for line in f if line.strip()}


def is_common_password(password: str) -> bool:
    """
    Cek apakah password termasuk dalam daftar password umum.

    Args:
        password: Password yang akan dicek

    Returns:
        True jika password termasuk common password
    """
    common = load_common_passwords()
    return password.lower() in common
