
"""
This Python script simulates a basic banking system with account creation, login, deposit, withdrawal, transfer, and deletion functionalities. It stores account information in a text file ("accounts.txt").

Sources:
  [1] Python Data Structures (Docs): https://docs.python.org/3/tutorial/datastructures.html
"""

class Account:
    def __init__(self, accountNumber, accountType, balance=0):
        self.accountNumber = accountNumber
        self.accountType = accountType
        self.balance = balance
        self.password = self.generatePassword()
    
    def generatePassword(self):
        import random
        import string
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(4))
        return password

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}.")
    
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}.")
    
    def displayBalance(self):
        print(f"Account Balance: {self.balance}")
    
    def transfer(self, amount, targetAccount):
        if amount > self.balance:
            print("Insufficient funds for transfer.")
        else:
            self.balance -= amount
            targetAccount.deposit(amount)
            print(f"Transferred {amount} to Account {targetAccount.accountNumber}. New balance is {self.balance}.")

class BusinessAccount(Account):
    def __init__(self, accountNumber, balance=0):
        super().__init__(accountNumber, "Business", balance)

class PersonalAccount(Account):
    def __init__(self, accountNumber, balance=0):
        super().__init__(accountNumber, "Personal", balance)

def saveAccount(account):
    with open("accounts.txt", "a") as file:
        account_data = f'{{"accountNumber": "{account.accountNumber}", "accountType": "{account.accountType}", "balance": {account.balance}, "password": "{account.password}"}}\n'
        file.write(account_data)

def loadAccounts():
    accounts = []
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                try:
                    if not line.strip():
                        continue  # Skip empty lines
                    accountNumber, accountType, balance, password = line.strip().split(',')
                    balance = float(balance)
                    if accountType == "Business":
                        account = BusinessAccount(accountNumber, balance)
                    elif accountType == "Personal":
                        account = PersonalAccount(accountNumber, balance)
                    else:
                        print(f"Unknown account type: {accountType}")
                        continue
                    account.password = password
                    accounts.append(account)
                except ValueError as e:
                    print(f"Error loading account: {e}")
                    continue
    except FileNotFoundError:
        pass
    return accounts

def deleteAccount(accounts, account):
  """
  This function removes the account object from the accounts list 
  and rewrites the "accounts.txt" file without the deleted account data.
  """
  confirmation = input(f"Are you sure you want to delete account {account.accountNumber}? (y/n): ")
  if confirmation.lower() == 'y':
    accounts.remove(account)
    with open("accounts.txt", "w") as file:  # Open in write mode to overwrite
      for remainingAccount in accounts:
        account_data = f'{{"accountNumber": "{remainingAccount.accountNumber}", "accountType": "{remainingAccount.accountType}", "balance": {remainingAccount.balance}, "password": "{remainingAccount.password}"}}\n'
        file.write(account_data)
    print(f"Account {account.accountNumber} has been deleted.")


def login(accounts):
    accountNumber = input("Enter your account number: ")
    password = input("Enter your password: ")
    for account in accounts:
        if account.accountNumber == accountNumber and account.password == password:
            return account
    print("Invalid account number or password.")
    return None

def main():
    accounts = loadAccounts()
    
    while True:
        print("\nBanking System")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            print("Enter account type: 1 for Business, 2 for Personal")
            accountTypeChoice = input()
            if accountTypeChoice == "1":
                account = BusinessAccount(str(len(accounts) + 1))
            elif accountTypeChoice == "2":
                account = PersonalAccount(str(len(accounts) + 1))
            else:
                print("Invalid account type. Please enter '1' for Business or '2' for Personal.")
                continue
            accounts.append(account)
            saveAccount(account)
            print(f"Account created. Your account number is {account.accountNumber} and password is {account.password}.")
        
        elif choice == "2":
            account = login(accounts)
            if account:
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transfer")
                    print("5. Delete Account")
                    print("6. Logout")
                    userChoice = input("Choose an option: ")

                    if userChoice == "1":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif userChoice == "2":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif userChoice == "3":
                        account.displayBalance()
                    elif userChoice == "4":
                        targetAccountNumber = input("Enter target account number: ")
                        targetAccount = next((acc for acc in accounts if acc.accountNumber == targetAccountNumber), None)
                        if targetAccount:
                            amount = float(input("Enter amount to transfer: "))
                            account.transfer(amount, targetAccount)
                        else:
                            print("Target account not found.")
                        
                    elif userChoice == "5":
                        deleteAccount(accounts, account)  # Call delete function
                        break  # Exit inner loop after deletion
                  
                    elif userChoice == "6":
                        break
                    else:
                        print("Invalid option.")
        
        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
