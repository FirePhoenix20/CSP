
def main():
    accounts = {}

    while True:
        action = input("Would you like to (1) Create an account or (2) Sign in? (Enter 1 or 2): ")

        if action == '1':
            create_account(accounts)
        elif action == '2':
            sign_in(accounts)
        else:
            print("Invalid option. Please try again.")

def create_account(accounts):
    username = input("Enter a username: ")
    if username in accounts:
        print("Username already exists. Please choose a different username.")
    else:
        password = input("Enter a password: ")
        accounts[username] = password
        print("Account created successfully!")

def sign_in(accounts):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in accounts and accounts[username] == password:
        print("Login successful!")
    else:
        print("Invalid username or password.")

if __name__ == "__main__":
    main()
