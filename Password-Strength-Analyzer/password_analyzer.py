import re
import math
import random
import string

# Check password strength
def check_password_strength(password):

    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    return score, suggestions


# Check common passwords
def is_common_password(password):

    with open("common_passwords.txt", "r") as file:
        common_passwords = file.read().splitlines()

    return password.lower() in common_passwords


# Calculate entropy
def calculate_entropy(password):

    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26

    if re.search(r"[A-Z]", password):
        charset += 26

    if re.search(r"\d", password):
        charset += 10

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0

    return round(len(password) * math.log2(charset), 2)


# Generate secure password
def generate_password(length=12):

    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*"
    )

    password = ''.join(random.choice(characters) for _ in range(length))

    return password


# Main Program
print("================================")
print(" PASSWORD STRENGTH ANALYZER ")
print("================================")

print("\n1. Analyze Password")
print("2. Generate Secure Password")

choice = input("\nChoose an option (1 or 2): ")

if choice == "2":
    password = generate_password()
    print("\nGenerated Secure Password:")
    print(password)
else:
    password = input("\nEnter password: ")

if is_common_password(password):
    print("\nWARNING: This is a commonly used password!")

score, suggestions = check_password_strength(password)
entropy = calculate_entropy(password)

print("\nPassword Analysis")
print("--------------------------")

if score <= 2:
    print("Strength : Weak")
elif score <= 4:
    print("Strength : Medium")
else:
    print("Strength : Strong")

print(f"Score    : {score}/5")
print(f"Entropy  : {entropy} bits")

if suggestions:
    print("\nSuggestions:")
    for suggestion in suggestions:
        print("-", suggestion)
else:
    print("\nExcellent password security!")