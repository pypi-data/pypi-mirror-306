import random
from tabulate import tabulate

lower_alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
capital_alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
special = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_"]

class Password:
    def __init__(self, password) -> None:
        self.password = password
        self.strength_score = 0

    def generate(self):
        self.password = " "
        for i in range(3):
            if i == 0:
                self.password += random.choice(capital_alphabets)
            self.password += random.choice(lower_alphabets)
            self.password += random.choice(special)
            self.password += random.choice(numbers)
        
        return self.password

    def check_strength(self):
        self.strength_score = 0
        score_capital = 0
        score_lower = 0
        score_number = 0
        score_special = 0
        score_length = max(0, min(10, len(self.password) // 4))

        for char in self.password:
            if char in capital_alphabets:
                score_capital = 1
            if char in lower_alphabets:
                score_lower = 1
            if char in numbers:
                score_number = 1
            if char in special:
                score_special = 1

        self.strength_score = score_capital + score_lower + score_number + score_special + score_length

    def status_declaration(self):
        self.check_strength()
        if self.strength_score <= 4:
            return "weak"
        if self.strength_score > 4 and self.strength_score < 8:
            return "moderate"
        else:
            return "strong"
        
    def print_password_table_format(self, passwords_array):
        passwords = passwords_array
        headers = ["ID", "Destination", "Password", "Strength"]
        data = [[password.get("_id", "N/A"), password.get("destination", "N/A"), password.get("password", "N/A"), password.get("strength", "N/A")] for password in passwords]
        print(tabulate(data, headers=headers, tablefmt="grid"))

    def caesar_cipher(self, shift):
        cipher_password = ""

        for char in self.password:
            if char in lower_alphabets:
                shifted_index = (lower_alphabets.index(char) + shift) % 26
                shifted_char = lower_alphabets[shifted_index]
                cipher_password += shifted_char
            if char in capital_alphabets:
                shifted_index = (capital_alphabets.index(char) + shift) % 26
                shifted_char = capital_alphabets[shifted_index]
                cipher_password += shifted_char
            if char in numbers:
                shifted_index = (numbers.index(char) + shift) % 10
                shifted_char = numbers[shifted_index]
                cipher_password += shifted_char
            if char in special:
                shifted_index = (special.index(char) + shift) % 12
                shifted_char = special[shifted_index]
                cipher_password += shifted_char

        self.password = cipher_password

    def caesar_decipher(self, shift, passwords):
        decipher_password = ""

        for password in passwords:
            for char in password["password"]:
                if char in lower_alphabets:
                    shifted_index = (lower_alphabets.index(char) - shift) % 26
                    shifted_char = lower_alphabets[shifted_index]
                    decipher_password += shifted_char
                if char in capital_alphabets:
                    shifted_index = (capital_alphabets.index(char) - shift) % 26
                    shifted_char = capital_alphabets[shifted_index]
                    decipher_password += shifted_char
                if char in numbers:
                    shifted_index = (numbers.index(char) - shift) % 10
                    shifted_char = numbers[shifted_index]
                    decipher_password += shifted_char
                if char in special:
                    shifted_index = (special.index(char) - shift) % 12
                    shifted_char = special[shifted_index]
                    decipher_password += shifted_char
            password["password"] = decipher_password
            decipher_password = ""
        return passwords

            