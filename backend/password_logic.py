import string
import os
import math
from datetime import date


# load common passwords from the CSV file into a set for O(1) lookups

def load_passwords():
    common_passwords = set()
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "top-10-million-passwords.csv")
    with open(file_path, mode='r', encoding='utf-8') as file:
        for line in file:
            common_passwords.add(line.strip().split(",")[1])
    return common_passwords


# entropy calculation based on character sets and length

def password_entropy(password, is_common):
    if is_common:
        return 1  # extremely weak — skip real calc

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


# crack time estimation

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
        "online":  1_000,
        "offline": 1_000_000_000,
        "gpu":     10_000_000_000,
    }
    results = []
    for label, speed in attack_speeds.items():
        guesses = min(2 ** entropy_bits, 1e18)
        seconds = guesses / speed
        results.append({"attack_type": label, "time": format_time(seconds)})
    return results


# Strength classification better than previous version, now we are calculating just entropy and not score 
# plus progress bar relies on entropy thresholds. Also, if the password is common, we classify it as "Compromised" 
# regardless of entropy. This is more accurate and user-friendly. 

def classify_strength(entropy_bits, is_common):
    if is_common:
        return "Compromised"
    if entropy_bits < 28:
        return "Very Weak"
    elif entropy_bits < 36:
        return "Weak"
    elif entropy_bits < 60:
        return "Fair"
    elif entropy_bits < 128:
        return "Strong"
    else:
        return "Very Strong"


#main analysis 

def password_analysis(password, common_passwords):
    reasons = []

    if len(password) < 12:
        reasons.append("be at least 12 characters long")
    if not any(c.isdigit() for c in password):
        reasons.append("contain at least one digit")
    if not any(c.isupper() for c in password):
        reasons.append("contain at least one uppercase letter")
    if not any(c.islower() for c in password):
        reasons.append("contain at least one lowercase letter")
    if not any(c in string.punctuation for c in password):
        reasons.append("contain at least one special character")

    is_common = password in common_passwords
    if is_common:
        reasons.append("not be a commonly used password")

    entropy = password_entropy(password, is_common)
    crack_time = estimate_crack_time(entropy)
    strength = classify_strength(entropy, is_common)

    return {
        "password": password,
        "strength": strength,
        "issues": reasons,
        "entropy": entropy,
        "crack_time": crack_time,
    }


# personal info attack candidates

def _cap(s):
    """Capitalise first letter, lowercase the rest."""
    return s.strip().capitalize() if s and s.strip() else None


def build_personal_candidates(first_name, last_name, birthdate, pet_name, city_name):
    """
    Generate passwords an attacker might craft from personal information.
    birthdate is expected as a string 'YYYY-MM-DD' or None.
    Returns a list of dicts: {password, reason}
    """
    results = []

    # Parse date parts
    day = month = year2 = year4 = None
    if birthdate:
        try:
            bd = date.fromisoformat(birthdate)
            day   = f"{bd.day:02d}"
            month = f"{bd.month:02d}"
            year2 = str(bd.year)[2:] #for example 1990 -> "90" because it can be something like "Nick90"
            year4 = str(bd.year)
        except ValueError:
            pass

    fn = _cap(first_name)
    ln = _cap(last_name)
    pn = _cap(pet_name)
    cn = _cap(city_name)

    def add(pwd, reason):
        if pwd and len(pwd) >= 3:
            results.append({"password": pwd, "reason": reason})

    # First name combos
    if fn:
        add(fn,                              "First name alone")
        if year2: add(f"{fn}{year2}",        "First name + short year")
        if year4: add(f"{fn}{year4}",        "First name + full year")
        if day and month:
            add(f"{fn}{day}{month}",         "First name + day/month")
            add(f"{fn}{month}{year2}",       "First name + month + short year") if year2 else None
            add(f"{fn}{day}{month}{year2}",  "First name + full date (short)") if year2 else None

    # Last name combos
    if ln:
        add(ln,                              "Last name alone")
        if year4: add(f"{ln}{year4}",        "Last name + full year")
        if fn:
            add(f"{fn}{ln}",                 "Full name combined")
            if year2: add(f"{fn}.{ln}{year2}", "Name.Surname + short year")

    # Pet name combos
    if pn:
        add(pn,                              "Pet name alone")
        if year2: add(f"{pn}{year2}",        "Pet name + short year")
        if day and month: add(f"{pn}{day}{month}", "Pet name + birthday day/month")
        if fn: add(f"{fn}{pn}",              "First name + pet name")

    # City combos
    if cn:
        add(cn,                              "City name alone")
        if year4: add(f"{cn}{year4}",        "City + full year")
        if fn: add(f"{fn}{cn}",              "First name + city")

    # Date-only combos
    if day and month and year4:
        add(f"{day}/{month}/{year4}",        "Full date dd/mm/yyyy")
        add(f"{day}{month}{year2}",          "Compact date ddmmyy")
    if year4:
        add(year4,                           "Birth year alone")

    return results


def analyze_personal_candidates(candidates, common_passwords):
    """Run password_analysis on each candidate and return enriched results."""
    results = []
    for c in candidates:
        pwd = c["password"]
        analysis = password_analysis(pwd, common_passwords)
        results.append({
            "password":  pwd,
            "reason":    c["reason"],
            "strength":  analysis["strength"],
            "entropy":   analysis["entropy"],
            "crack_time": analysis["crack_time"],
        })
    return results