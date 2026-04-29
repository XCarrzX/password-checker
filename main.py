import argparse
import getpass
import sys
from src.checker import analyze_password
from src.display import display_result


def check_single(password: str) -> None:
    """Analisis satu password."""
    result = analyze_password(password)
    display_result(result)


def check_batch(filepath: str) -> None:
    """
    Analisis banyak password dari file teks.
    Format file: satu password per baris.
    """
    try:
        with open(filepath, "r") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File '{filepath}' tidak ditemukan!")
        sys.exit(1)

    print(f"\n📋 Menganalisis {len(passwords)} password dari '{filepath}'...\n")

    for i, pwd in enumerate(passwords, 1):
        print(f"── Password #{i} ──")
        result = analyze_password(pwd)
        display_result(result)


def main():
    parser = argparse.ArgumentParser(
        description="🔐 Password Strength Checker — Analisis kekuatan password kamu!",
        epilog="Contoh: python main.py | python main.py --batch passwords.txt"
    )
    parser.add_argument(
        "--password", "-p",
        help="Password yang ingin dicek (langsung via argumen)"
    )
    parser.add_argument(
        "--batch", "-b",
        metavar="FILE",
        help="Cek banyak password dari file teks (1 password per baris)"
    )

    args = parser.parse_args()

    # Mode batch
    if args.batch:
        check_batch(args.batch)
        return

    # Mode single dengan argumen
    if args.password:
        check_single(args.password)
        return

    # Mode interaktif (default) — password disembunyikan saat diketik
    print("\n🔐 Password Strength Checker")
    print("=" * 32)
    try:
        password = getpass.getpass("   Masukkan password: ")
    except KeyboardInterrupt:
        print("\n\n👋 Dibatalkan.")
        sys.exit(0)

    if not password:
        print("❌ Password tidak boleh kosong!")
        sys.exit(1)

    check_single(password)


if __name__ == "__main__":
    main()
