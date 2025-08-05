from services.database import Database
from datetime import datetime

class IncomeManager:
    def __init__(self):
        self.db = Database.get_instance()

    def add_income(self, category, amount, income_date, description=None):
        query = """
            INSERT INTO Income (Category, Amount, IncomeDate, Description)
            VALUES (%s, %s, %s, %s)
        """
        params = (category, amount, income_date, description)
        return self.db.execute_query(query, params)

    def get_all_incomes(self):
        query = "SELECT * FROM Income ORDER BY IncomeDate DESC"
        return self.db.execute_query(query, fetchall=True)

    def get_income_by_id(self, income_id):
        query = "SELECT * FROM Income WHERE IncomeID = %s"
        return self.db.execute_query(query, (income_id,), fetchone=True)

    def update_income(self, income_id, category, amount, income_date, description):
        query = """
            UPDATE Income
            SET Category = %s, Amount = %s, IncomeDate = %s, Description = %s
            WHERE IncomeID = %s
        """
        params = (category, amount, income_date, description, income_id)
        return self.db.execute_query(query, params)

    def delete_income(self, income_id):
        query = "DELETE FROM Income WHERE IncomeID = %s"
        return self.db.execute_query(query, (income_id,))

    def get_total_income(self):
        query = "SELECT SUM(Amount) AS Total FROM Income"
        result = self.db.execute_query(query, fetchone=True)
        return result['Total'] if result and result['Total'] is not None else 0.00

    def get_incomes_by_category(self, start_date, end_date):
        query = """
            SELECT Category, SUM(Amount) AS Total
            FROM Income
            WHERE IncomeDate BETWEEN %s AND %s
            GROUP BY Category
            ORDER BY Total DESC
        """
        return self.db.execute_query(query, (start_date, end_date), fetchall=True)

    def get_incomes_between_dates(self, start_date, end_date):
        query = """
            SELECT * FROM Income
            WHERE IncomeDate BETWEEN %s AND %s
            ORDER BY IncomeDate DESC
        """
        return self.db.execute_query(query, (start_date, end_date), fetchall=True)