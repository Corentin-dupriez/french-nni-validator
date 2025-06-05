# French National Security Number validator

This Python script serves two purposes: 
- **Calculate** the control key (last two digits) of a French national security number 
- **Validate** a given number (with or without the key) for correctness

## What it does 

- Given a 13-chars long national security number, it can check its correctness and generate the two digits key at the end, returning a 15-chars number. 
- Provided with a 15 characters number, it can check correctness of the structure and control key. 

## Why this matters 

In France, the national security number is a unique identifier based on personal information (gender, year/month of birth, place of birth, etc.). Ensuring its validity is useful for:

- Data verification in administrative or HR systems
- Pre-validation before database insertion
- Educational or learning purposes (e.g., understanding Luhn-type checks)

## How to use
i. Clone repo or copy the script 
```bash
    git clone https://github.com/Corentin-dupriez/french-nni-validator.git
    cd french-nni-validator
```
ii. Use the functions placed in the `national_security_number_validator.py` file
