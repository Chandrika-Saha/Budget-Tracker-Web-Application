from services.database import Database
from datetime import datetime

class ExpenseManager:
    def __init__(self):
        self.db = Database.get_instance()

    def add_expense(self, category, amount, expense_date, description=None):
        query = """
            INSERT INTO Expense (Category, Amount, ExpenseDate, Description)
            VALUES (%s, %s, %s, %s)
        """
        params = (category, amount, expense_date, description)
        return self.db.execute_query(query, params)

    def get_all_expenses(self):
        query = "SELECT * FROM Expense ORDER BY ExpenseDate DESC"
        return self.db.execute_query(query, fetchall=True)

    def get_expense_by_id(self, expense_id):
        query = "SELECT * FROM Expense WHERE ExpenseID = %s"
        return self.db.execute_query(query, (expense_id,), fetchone=True)

    def update_expense(self, expense_id, category, amount, expense_date, description):
        query = """
            UPDATE Expense
            SET Category = %s, Amount = %s, ExpenseDate = %s, Description = %s
            WHERE ExpenseID = %s
        """
        params = (category, amount, expense_date, description, expense_id)
        return self.db.execute_query(query, params)

    def delete_expense(self, expense_id):
        query = "DELETE FROM Expense WHERE ExpenseID = %s"
        return self.db.execute_query(query, (expense_id,))

    def get_total_expense(self):
        query = "SELECT SUM(Amount) AS Total FROM Expense"
        result = self.db.execute_query(query, fetchone=True)
        return result['Total'] if result and result['Total'] is not None else 0.00

    def get_expenses_by_category(self, start_date, end_date):
        query = """
            SELECT Category, SUM(Amount) AS Total
            FROM Expense
            WHERE ExpenseDate BETWEEN %s AND %s
            GROUP BY Category
            ORDER BY Total DESC
        """
        return self.db.execute_query(query, (start_date, end_date), fetchall=True)

    def get_expenses_between_dates(self, start_date, end_date):
        query = """
            SELECT * FROM Expense
            WHERE ExpenseDate BETWEEN %s AND %s
            ORDER BY ExpenseDate DESC
        """
        return self.db.execute_query(query, (start_date, end_date), fetchall=True)
