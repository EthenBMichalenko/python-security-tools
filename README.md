# Cybersecurity Python Projects

Security tools I'm building in Python while studying cybersecurity.

| # | Project | Status |
|---|---------|--------|
| 1 | [Password Strength Checker](01-password-checker/) | In progress |
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
- *Coming next:* breach check against Have I Been Pwned using SHA-1 and k-anonymity

```bash
python 01-password-checker/password_checker.py
```

> **Note:** brute-force estimates are a best case. Real attackers use dictionary and rule-based attacks, so predictable passwords like `Password1!` fall in seconds despite a "170 years" estimate.

## Ethics

These tools are for learning and for systems I own or have permission to test.
