import string
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

    if  any(char.islower() for char in password):
        score += 1
    else: 
        feedback.append("Add a lowercase letter")

    if any(char.isdigit() for char in password):
        score += 1
    else: 
        feedback.append("Add a digit")

    if any (char in string.punctuation for char in password):
        score += 1
    else: 
        feedback.append("Add a special character")


    return score, feedback

def load_common_password(filename):
    with open(filename) as file:
        bad_passwords = set()
        for line in file:
            word = line.strip()
            bad_passwords.add(word.lower())
    return bad_passwords

def estimate_crack_time(password):
    MINIUTE = 60
    HOUR = 60 * MINIUTE
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
    
    if any (char in string.punctuation for char in password):
        pool += SPECIAL

    combination = pool ** len(password)

    seconds = combination / GUESSES_PER_SECOND

    if seconds <= MINIUTE:
        return f"Time to crack: {seconds} seconds"
    elif seconds <= HOUR:
        return f"Time to crack: {seconds / MINIUTE:.1f} minutes" 
    elif seconds <= DAY:
        return f"Time to crack: {seconds / HOUR:.1f} hours"
    elif seconds <= YEAR:
        return f"Time to crack: {seconds / DAY:.1f} days"
    else:
        return f"Time to crack: {seconds / YEAR:.1f} years" 

SCRIPT_DIR = Path(__file__).parent
bad_passwords = load_common_password(SCRIPT_DIR / "common_passwords.txt")

password = input("Enter a password to check: ")
score, feedback = check_password(password)

if score < 3:
    label = "Weak"
elif score < 5:
    label = "Medium"
else: 
    label = "Strong"

if password.lower() in bad_passwords:
    label = "Weak"
    score = 0
    print("⚠️ This password is in a list of commonly leaked passwords!")



print(f"Score: {score} / 5 ({label})")
print(estimate_crack_time(password))
for word in feedback:
    print("-", word)