import string
import csv
import os

# load passwords into a set for O(1) lookups
def load_passwords():
    common_passwords = set()

    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "top-10-million-passwords.csv")

    with open(file_path, mode='r', encoding='utf-8') as file:
        for line in file:
            common_passwords.add(line.strip().split(",")[1])

    return common_passwords


def read_input():
    return input("Enter your password: ")


def password_analysis(password_dict, common_passwords):
    password = password_dict["password"]
    score = 0
    reasons = []

    # Length
    if len(password) < 12:
        reasons.append("be at least 12 characters long")
    else:
        score += 20

    # Digit
    if not any(char.isdigit() for char in password):
        reasons.append("contain at least one digit")
    else:
        score += 20

    # Uppercase
    if not any(char.isupper() for char in password):
        reasons.append("contain at least one uppercase letter")
    else:
        score += 20

    # Lowercase
    if not any(char.islower() for char in password):
        reasons.append("contain at least one lowercase letter")
    else:
        score += 20

    # Special character
    if not any(char in string.punctuation for char in password):
        reasons.append("contain at least one special character")
    else:
        score += 20

    # Common password check (FAST now)
    if password in common_passwords:
        reasons.append("not be a commonly used password")
        score -= 40

    # Clamp score
    score = max(0, min(score, 100))

    # Strength classification
    if score < 60:
        strength = "Weak"
        suggestions = ["Use at least 12 characters with a mix of letters, numbers, and symbols."]
    elif score < 100:
        strength = "Medium"
        suggestions = ["Increase complexity and avoid predictable patterns."]
    else:
        strength = "Strong"
        suggestions = []

    # Final structured output
    return {
        "password": password,
        "score": score,
        "strength": strength,
        "issues": reasons,
        "suggestions": suggestions
    }


def main():
    print("Password Strength Checker")

    # Load dataset
    common_passwords = load_passwords()

    input_password = read_input()

    password_dict = {
        "password": input_password
    }

    result = password_analysis(password_dict, common_passwords)

    print("\nResult:")
    print(result)


if __name__ == "__main__":
    main()