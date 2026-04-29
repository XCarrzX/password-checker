def display_result(result: dict) -> None:
    """Tampilkan hasil analisis password dalam format kotak rapi."""
    width        = 46
    border       = "═" * width
    score        = result["score"]
    strength     = result["strength"]
    masked       = _mask_password(result["password"])

    # Warna strength
    strength_display = _get_strength_display(score, strength)

    # Progress bar
    bar = _make_progress_bar(score, bar_length=16)

    print(f"\n╔{border}╗")
    print(f"║{'🔐 PASSWORD STRENGTH CHECKER':^{width}}║")
    print(f"╠{border}╣")
    print(f"║  Password : {masked:<34}║")
    print(f"║  Strength : {bar} {strength_display:<14}║")
    print(f"╠{border}╣")

    # Detail analisis
    checks = [
        ("Length",    f"{result['length']} chars",  result['length'] >= 8),
        ("Uppercase", "Yes" if result['has_upper'] else "No",  result['has_upper']),
        ("Lowercase", "Yes" if result['has_lower'] else "No",  result['has_lower']),
        ("Numbers",   "Yes" if result['has_digit'] else "No",  result['has_digit']),
        ("Symbols",   "Yes" if result['has_symbol'] else "Add !@#$",  result['has_symbol']),
        ("Common pwd","No ✅" if not result['is_common'] else "Detected! ⚠️", not result['is_common']),
        ("Repeated",  "None ✅" if not result['has_repeat'] else "Found! ⚠️",  not result['has_repeat']),
    ]

    for label, value, passed in checks:
        icon = "✅" if passed else "❌"
        print(f"║  {icon} {label:<12}: {value:<27}║")

    # Tips
    if result["tips"]:
        print(f"╠{border}╣")
        print(f"║  💡 Tips:{' ' * 37}║")
        for tip in result["tips"][:4]:          # max 4 tips
            tip_text = tip[:43]
            print(f"║   {tip_text:<45}║")

    print(f"╚{border}╝\n")


def _mask_password(password: str) -> str:
    """Sembunyikan sebagian karakter password."""
    if len(password) <= 2:
        return "*" * len(password)
    return password[0] + "*" * (len(password) - 2) + password[-1]


def _make_progress_bar(score: int, bar_length: int = 16) -> str:
    """Buat progress bar visual berdasarkan skor."""
    filled = round((score / 100) * bar_length)
    empty  = bar_length - filled
    return f"{'█' * filled}{'░' * empty}"


def _get_strength_display(score: int, label: str) -> str:
    """Format label kekuatan dengan skor."""
    return f"{label} ({score}%)"
