import string
import os
import math

# Load passwords into a set for O(1) lookups
def load_passwords():
    common_passwords = set()

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "top-10-million-passwords.csv")

    with open(file_path, mode='r', encoding='utf-8') as file:
        for line in file:
            common_passwords.add(line.strip().split(",")[1])

    return common_passwords



# ---------------- ENTROPY ---------------- #

def password_entropy(password, is_common):
    #If common do not even calculate entropy
    if is_common:
        return 5  # extremely weak

    charset_size = 0

    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += len(string.punctuation)

    if charset_size == 0:
        return 0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)


def format_time(seconds):
    intervals = [
        ("years",   365.25 * 24 * 3600),
        ("days",    24 * 3600),
        ("hours",   3600),
        ("minutes", 60),
        ("seconds", 1),
    ]
    for name, count in intervals:
        value = seconds / count
        if value >= 1:
            return f"{value:,.1f} {name}"
    return "less than a second"


def estimate_crack_time(entropy_bits):
    attack_speeds = {
        "online": 1_000,
        "offline": 1_000_000_000,
        "gpu": 10_000_000_000,
    }

    results = []

    for label, speed in attack_speeds.items():
        # avoid huge numbers
        guesses = min(2 ** entropy_bits, 1e18)
        seconds = guesses / speed

        results.append({
            "attack_type": label,
            "time": format_time(seconds)
        })

    return results


# ---------------- MAIN ANALYSIS ---------------- #

def password_analysis(password, common_passwords):
    score = 0
    reasons = []

    # Checks
    if len(password) < 12:
        reasons.append("be at least 12 characters long")
    else:
        score += 20

    if not any(c.isdigit() for c in password):
        reasons.append("contain at least one digit")
    else:
        score += 20

    if not any(c.isupper() for c in password):
        reasons.append("contain at least one uppercase letter")
    else:
        score += 20

    if not any(c.islower() for c in password):
        reasons.append("contain at least one lowercase letter")
    else:
        score += 20

    if not any(c in string.punctuation for c in password):
        reasons.append("contain at least one special character")
    else:
        score += 20

    # Common password check
    is_common = password in common_passwords
    if is_common:
        reasons.append("not be a commonly used password")
        score -= 40

    score = max(0, min(score, 100))

    # Strength
    if score < 60:
        strength = "Weak"
    elif score < 100:
        strength = "Medium"
    else:
        strength = "Strong"

    # Entropy + crack time
    entropy = password_entropy(password, is_common)
    crack_time = estimate_crack_time(entropy)

    return {
        "password": password,
        "score": score,
        "strength": strength,
        "issues": reasons,
        "entropy": entropy,
        "crack_time": crack_time
    }




def main():
    common_passwords = load_passwords()

    password = input("Enter password: ")

    result = password_analysis(password, common_passwords)

    print("\nResult:")
    print(result)


if __name__ == "__main__":
    main()