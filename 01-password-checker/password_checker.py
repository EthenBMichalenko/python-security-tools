import string
import hashlib
import requests
from pathlib import Path

def check_password(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add an uppercase letter")

    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add a lowercase letter")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add a digit")

    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add a special character")
    return score, feedback

def load_common_passwords(filename):
    with open(filename) as file:
        bad_passwords = set()
        for line in file:
            word = line.strip()
            bad_passwords.add(word.lower())
    return bad_passwords

def estimate_crack_time(password):
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    YEAR = 365 * DAY
    LOWERCASE = 26
    UPPERCASE = 26
    DIGIT = 10
    SPECIAL = 32
    GUESSES_PER_SECOND = 10_000_000_000

    pool = 0

    if any(char.isupper() for char in password):
        pool += UPPERCASE
    
    if any(char.islower() for char in password):
        pool += LOWERCASE
    
    if any(char.isdigit() for char in password):
        pool += DIGIT
    
    if any(char in string.punctuation for char in password):
        pool += SPECIAL

    combination = pool ** len(password)
    seconds = combination / GUESSES_PER_SECOND

    if seconds < 1:
        return "Time to crack: Less than a second"
    elif seconds <= MINUTE:
        return f"Time to crack: {seconds:.1f} seconds"
    elif seconds <= HOUR:
        return f"Time to crack: {seconds / MINUTE:.1f} minutes" 
    elif seconds <= DAY:
        return f"Time to crack: {seconds / HOUR:.1f} hours"
    elif seconds <= YEAR:
        return f"Time to crack: {seconds / DAY:.1f} days"
    else:
        return f"Time to crack: {seconds / YEAR:.1f} years" 
    
def hash_password(password):
    password_bytes = password.encode()
    hashed = hashlib.sha1()
    hashed.update(password_bytes)
    finalhashed = hashed.hexdigest().upper()
    prefix = finalhashed[:5]
    suffix = finalhashed[5:]
    return prefix, suffix

def check_pwned(prefix, suffix):
    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None
    response = response.text.split()
    for line in response:
        hash_suffix, count = line.split(":") 
        if hash_suffix == suffix:
            return int(count)
    return 0

def main():
    SCRIPT_DIR = Path(__file__).parent
    bad_passwords = load_common_passwords(SCRIPT_DIR / "common_passwords.txt")

    password = input("Enter a password to check: ")
    score, feedback = check_password(password)

    if score < 3:
        label = "Weak"
    elif score < 5:
        label = "Medium"
    else:
        label = "Strong"

    if len(password) == 0:
        print("Please enter a password")
    else:
        if password.lower() in bad_passwords:
            label = "Weak"
            score = 0
            print("This password is in a list of commonly leaked passwords!")
        
        print(f"Score: {score} / 5 ({label})")
        print(estimate_crack_time(password))
        for word in feedback:
            print("-", word)
        prefix, suffix = hash_password(password)
        print(f"Hash Prefix: {prefix}\nHash Suffix: {suffix}")

        pwned_check = check_pwned(prefix, suffix)

        if pwned_check == 0:
            print("Your password was not seen in checked data breaches")
        elif pwned_check == 1:
            print(f"Your password was seen {pwned_check} time in a data breach")
        elif pwned_check is None:
            print("Your password was not able to be checked because of an error")
        else:
            print(f"Your password was seen {pwned_check:,} times in data breaches")

if __name__ == "__main__":
    main()