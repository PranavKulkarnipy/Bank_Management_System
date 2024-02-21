import mysql.connector as c

class BankManagementSystem:
    Bank_Name="Bank of Maharashta"
    Branch_Name="Branch : Khatav"


    def __init__(self, host, port, user, password, database):
        self.con = c.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        self.cur = self.con.cursor()
        self.create_table()
        self.last_account_number = self.get_last_account_number()
        print("="*65)
        print(" "*25,end='')
        print(BankManagementSystem.Bank_Name)
        print(" "*25,end='')
        print(BankManagementSystem.Branch_Name)
        print("="*65)


    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS bank (
            acno INT PRIMARY KEY,
            name VARCHAR(255),
            mob VARCHAR(15),
            balance INT
        )
        """
        self.cur.execute(query)
        self.con.commit()

    def get_last_account_number(self):
        query = "SELECT MAX(acno) FROM bank"
        self.cur.execute(query)
        last_account_number = self.cur.fetchone()[0]
        return 0 if last_account_number is None else last_account_number

    def open_account(self, name, mob, balance):
        self.last_account_number += 1
        acno = self.last_account_number

        query = "INSERT INTO bank (acno, name, mob, balance) VALUES (%s, %s, %s, %s)"
        values = (acno, name, mob, balance)

        try:
            self.cur.execute(query, values)
            self.con.commit()
            print("Account opened successfully! Account Number:", acno)
        except Exception as e:
            print(f"Error opening account: {e}")

    def cash_withdrawal(self, acno, amount):
        query = "SELECT balance FROM bank WHERE acno=%s"
        self.cur.execute(query, (acno,))
        data = self.cur.fetchone()

        if data:
            current_balance = data[0]

            if current_balance >= amount:
                new_balance = current_balance - amount
                update_query = "UPDATE bank SET balance=%s WHERE acno=%s"
                self.cur.execute(update_query, (new_balance, acno))
                self.con.commit()
                print("Cash withdrawal successful. Updated balance:", new_balance)
            else:
                print("Insufficient funds for withdrawal.")
        else:
            print("Account not found.")

    def cash_deposit(self, acno, amount):
        query = "SELECT balance FROM bank WHERE acno=%s"
        self.cur.execute(query, (acno,))
        data = self.cur.fetchone()

        if data:
            current_balance = data[0]
            new_balance = current_balance + amount

            update_query = "UPDATE bank SET balance=%s WHERE acno=%s"
            self.cur.execute(update_query, (new_balance, acno))
            self.con.commit()
            print("Cash deposit successful. Updated balance:", new_balance)
        else:
            print("Account not found.")

    def display_statement(self, acno):
        query = "SELECT * FROM bank WHERE acno=%s"
        self.cur.execute(query, (acno,))
        data = self.cur.fetchone()

        if data:
            print("=" * 65)
            print("Account Number is =", data[0])
            print("Account holder name is =", data[1])
            print("Mobile number of account holder is =", data[2])
            print("Balance of account holder =", data[3])
            print("=" * 65)
        else:
            print("Account not found.")


if __name__ == "__main__":
    
    host = 'localhost'
    port = 3306
    user = 'root'
    password = 'pranav29'
    database = 'project'

    bank_system = BankManagementSystem(host, port, user, password, database)

    while True:
        try:
            choice = int(input("1. Open Account\n2. Cash Withdraw\n3. Cash Deposit\n4. Statement\n0. Exit\nEnter your choice: "))

            if choice == 1:
                name = input("Enter a name: ")
                mob = input("Enter mobile number: ")
                balance = int(input("Enter opening balance: "))
                bank_system.open_account(name, mob, balance)

            elif choice == 2:
                acno = int(input("Enter your account number: "))
                amount = int(input("Enter amount to withdraw: "))
                bank_system.cash_withdrawal(acno, amount)

            elif choice == 3:
                acno = int(input("Enter your account number: "))
                amount = int(input("Enter amount to deposit: "))
                bank_system.cash_deposit(acno, amount)

            elif choice == 4:
                acno = int(input("Enter an account number: "))
                bank_system.display_statement(acno)

            elif choice == 0:
                print("Exiting Bank Management System. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")
