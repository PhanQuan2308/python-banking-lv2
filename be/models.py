import mysql.connector
from extensions import bcrypt
from flask import current_app


def get_db_connection():
    return mysql.connector.connect(
        host=current_app.config["MYSQL_HOST"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DB"],
    )


class User:
    @staticmethod
    def create_user(name, email, password):
        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                cursor.close()
                connection.close()
                return {"error": "Email already exists"}

            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password),
            )
            connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def verify_user_email(email):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        print(f"Checking email: {email}")  # In ra email để kiểm tra
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            print(f"User found: {user}")
            return user
        else:
            print("No user found")
        return None


    @staticmethod
    def verify_user(email, password):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user

    @staticmethod
    def update_password(user_id, new_password):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET password = %s WHERE id = %s", (new_password, user_id)
        )
        connection.commit()
        cursor.close()
        connection.close()


class Account:
    @staticmethod
    def get_balance(account_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT balance FROM accounts WHERE account_id = %s", (account_id,)
        )
        account = cursor.fetchone()
        cursor.close()
        connection.close()
        return account["balance"] if account else None

    @staticmethod
    def update_balance(account_id, amount, transaction_type):
        connection = get_db_connection()
        cursor = connection.cursor()

        if transaction_type == "deposit":
            cursor.execute(
                "UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
                (amount, account_id),
            )
        elif transaction_type == "withdraw":
            cursor.execute(
                "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
                (amount, account_id),
            )

        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_account_id_by_user(user_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT account_id FROM accounts WHERE user_id = %s", (user_id,))
        account = cursor.fetchone()
        cursor.close()
        connection.close()

        if account:
            return account["account_id"]
        return None

    @staticmethod
    def create_account_for_user(user_id):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO accounts (user_id, balance) VALUES (%s, %s)", (user_id, 0)
            )
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error creating account for user {user_id}: {e}")


class Transaction:
    @staticmethod
    def create_transaction(account_id, transaction_type, amount):
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, %s, %s)",
                (account_id, transaction_type, amount),
            )
            connection.commit()
            print(f"Transaction created: {transaction_type} of {amount}")
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"Error creating transaction: {e}")

    @staticmethod
    def get_transaction_history(account_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM transactions WHERE account_id = %s ORDER BY date DESC",
            (account_id,),
        )
        transactions = cursor.fetchall()
        cursor.close()
        connection.close()
        return transactions

    @staticmethod
    def get_today_transactions(account_id):
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
           "SELECT * FROM transactions WHERE account_id = %s AND DATE(date) = CURDATE()",
             (account_id,),
         )
        transactions = cursor.fetchall()
        cursor.close()
        connection.close()
        return transactions

