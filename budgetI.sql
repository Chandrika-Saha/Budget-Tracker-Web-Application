DROP DATABASE IF EXISTS personal_budget_tracker;
CREATE DATABASE personal_budget_tracker;

USE personal_budget_tracker;

CREATE TABLE Income (
    IncomeID INT AUTO_INCREMENT PRIMARY KEY,
	Category VARCHAR(100) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    IncomeDate DATE NOT NULL,
    Description VARCHAR(255)
);

CREATE TABLE Expense (
    ExpenseID INT AUTO_INCREMENT PRIMARY KEY,
	Category VARCHAR(100) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    ExpenseDate DATE NOT NULL,
    Description VARCHAR(255)
);

INSERT INTO Income (Category, Amount, IncomeDate, Description) VALUES
('Salary', 4500.00, '2025-05-01', 'Monthly salary from company'),
('Freelance', 750.00, '2025-05-05', 'Freelance web development project'),
('Investment', 200.00, '2025-05-10', 'Stock dividends'),
('Gift', 100.00, '2025-05-12', 'Birthday gift from friend'),
('Rental Income', 1200.00, '2025-05-15', 'Apartment rental payment'),
('Bonus', 500.00, '2025-05-20', 'Quarterly performance bonus'),
('Interest', 50.00, '2025-05-22', 'Bank interest'),
('Cashback', 30.00, '2025-05-25', 'Credit card cashback'),
('Online Sales', 300.00, '2025-05-27', 'Etsy store sales'),
('Refund', 80.00, '2025-05-28', 'Tax refund adjustment');

INSERT INTO Expense (Category, Amount, ExpenseDate, Description) VALUES
('Groceries', 150.00, '2025-05-02', 'Weekly grocery shopping'),
('Rent', 1200.00, '2025-05-03', 'Monthly apartment rent'),
('Utilities', 180.00, '2025-05-04', 'Electricity and water bill'),
('Dining Out', 60.00, '2025-05-06', 'Dinner at restaurant'),
('Transport', 100.00, '2025-05-08', 'Monthly transit pass'),
('Internet', 70.00, '2025-05-09', 'Wi-Fi and phone bill'),
('Subscription', 15.00, '2025-05-13', 'Netflix subscription'),
('Healthcare', 90.00, '2025-05-16', 'Dental check-up'),
('Clothing', 120.00, '2025-05-18', 'New summer clothes'),
('Gift', 50.00, '2025-05-21', 'Friend’s birthday present');

SELECT * FROM Income;