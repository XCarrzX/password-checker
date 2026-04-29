import re
from src.wordlist import is_common_password


def analyze_password(password: str) -> dict:
    """
    Analisis kekuatan password secara menyeluruh.

    Args:
        password: Password yang akan dianalisis

    Returns:
        Dictionary berisi hasil analisis lengkap
    """
    length         = len(password)
    has_upper      = bool(re.search(r'[A-Z]', password))
    has_lower      = bool(re.search(r'[a-z]', password))
    has_digit      = bool(re.search(r'\d', password))
    has_symbol     = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>\/?]', password))
    is_common      = is_common_password(password)
    has_repeat     = bool(re.search(r'(.)\1{2,}', password))   # 3+ karakter berulang
    has_sequence   = _has_sequence(password)

    score = _calculate_score(
        length, has_upper, has_lower,
        has_digit, has_symbol, is_common,
        has_repeat, has_sequence
    )

    tips = _generate_tips(
        length, has_upper, has_lower,
        has_digit, has_symbol, is_common,
        has_repeat, has_sequence
    )

    return {
        "password":      password,
        "length":        length,
        "has_upper":     has_upper,
        "has_lower":     has_lower,
        "has_digit":     has_digit,
        "has_symbol":    has_symbol,
        "is_common":     is_common,
        "has_repeat":    has_repeat,
        "has_sequence":  has_sequence,
        "score":         score,
        "strength":      _get_strength_label(score),
        "tips":          tips,
    }


def _calculate_score(length, has_upper, has_lower,
                     has_digit, has_symbol,
                     is_common, has_repeat, has_sequence) -> int:
    """Hitung skor kekuatan password (0-100)."""
    score = 0

    # Panjang password (max 35 poin)
    if length >= 16:  score += 35
    elif length >= 12: score += 25
    elif length >= 8:  score += 15
    elif length >= 6:  score += 5

    # Variasi karakter (masing-masing 15 poin)
    if has_upper:  score += 15
    if has_lower:  score += 15
    if has_digit:  score += 15
    if has_symbol: score += 20  # simbol paling kuat

    # Penalti
    if is_common:    score -= 40
    if has_repeat:   score -= 10
    if has_sequence: score -= 10

    return max(0, min(100, score))


def _get_strength_label(score: int) -> str:
    """Konversi skor ke label kekuatan."""
    if score >= 80: return "VERY STRONG"
    if score >= 60: return "STRONG"
    if score >= 40: return "MODERATE"
    if score >= 20: return "WEAK"
    return "VERY WEAK"


def _has_sequence(password: str) -> bool:
    """Deteksi pola urutan seperti 'abc', '123', 'qwerty'."""
    sequences = ["abcdefghijklmnopqrstuvwxyz", "0123456789", "qwertyuiop", "asdfghjkl"]
    pwd_lower = password.lower()
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in pwd_lower:
                return True
    return False


def _generate_tips(length, has_upper, has_lower,
                   has_digit, has_symbol,
                   is_common, has_repeat, has_sequence) -> list:
    """Generate tips perbaikan yang spesifik."""
    tips = []

    if is_common:
        tips.append("❌ Password ini terlalu umum — segera ganti!")
    if length < 12:
        tips.append(f"📏 Tambah panjang password (sekarang {length}, ideal 12+)")
    if not has_upper:
        tips.append("🔠 Tambahkan huruf kapital (A-Z)")
    if not has_lower:
        tips.append("🔡 Tambahkan huruf kecil (a-z)")
    if not has_digit:
        tips.append("🔢 Tambahkan angka (0-9)")
    if not has_symbol:
        tips.append("🔣 Tambahkan simbol seperti !@#$%^&*")
    if has_repeat:
        tips.append("🔁 Hindari karakter berulang (aaa, 111)")
    if has_sequence:
        tips.append("📶 Hindari urutan seperti 'abc', '123', 'qwerty'")

    if not tips:
        tips.append("✅ Password kamu sudah sangat kuat!")

    return tips
