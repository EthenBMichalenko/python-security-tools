# Cybersecurity Python Projects

Security tools I'm building in Python while studying cybersecurity.

| # | Project | Status |
|---|---------|--------|
| 1 | [Password Strength Checker](01-password-checker/) | Done |
| 2 | File Integrity Monitor | Planned |
| 3 | Log Analyzer | Planned |
| 4 | Port Scanner | Planned |
| 5 | Cipher Toolkit | Planned |
| 6 | Mini Intrusion Detection System | Planned |

## 1. Password Strength Checker

Rates a password and explains how to improve it:

- Scores length and character variety (uppercase, lowercase, digits, symbols)
- Flags passwords found in the 10,000 most common leaked passwords (case-insensitive), using the list from [SecLists](https://github.com/danielmiessler/SecLists)
- Estimates brute-force crack time at 10 billion guesses per second
- Checks the password against [Have I Been Pwned](https://haveibeenpwned.com/Passwords) and reports how many times it has appeared in data breaches
- Any password found in a breach or in the common list is rated **Weak**, whatever its score

### How the breach check keeps your password private

The password never leaves your computer. The script hashes it with SHA-1 and sends only the **first 5 characters** of the hash to HIBP (k-anonymity). HIBP replies with every hash suffix that starts with those 5 characters (around 2,000 of them), and the script looks for a match locally. HIBP never learns which password, or even which full hash, you checked.

### Failing safely

If HIBP can't be reached (no internet, a timeout, or a server error), the script says the password **could not be checked** instead of reporting it as safe. The local common-password list still runs offline.

### Run it

```bash
pip install -r requirements.txt
python 01-password-checker/password_checker.py
```

### Limitations

- **Brute-force estimates are a best case.** Real attackers use dictionary and rule-based attacks, so predictable passwords like `Password1!` fall in seconds despite a "170 years" estimate. HIBP has seen `Password1!` more than 500,000 times.
- **Composition rules can mislead.** A long passphrase like `correct horse battery staple` scores Weak because it has no uppercase letters, digits or symbols, while `Password1!` scores 5/5. NIST SP 800-63B recommends length and breach checks over composition rules.
- **The breach check needs internet.** Offline, only the 10,000-password list is checked.
- **"Not found" doesn't mean safe.** A password can be weak or easy to guess without ever having appeared in a known breach.

## Ethics

These tools are for learning and for systems I own or have permission to test.
