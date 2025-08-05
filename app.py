# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from services.IncomeManager import IncomeManager
from services.ExpenseManager import ExpenseManager
from datetime import datetime, date
from functools import wraps
from decimal import Decimal
from datetime import datetime
from flask import jsonify  # For API responses
import requests           # For Ollama communication
import json              # For JSON handling

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Sample categories data (in a real app, this would come from a database)
categories = [
    {'CategoryID': 1, 'CategoryName': 'Salary'},
    {'CategoryID': 2, 'CategoryName': 'Freelance'},
    {'CategoryID': 3, 'CategoryName': 'Investment'},
    {'CategoryID': 4, 'CategoryName': 'Groceries'},
    {'CategoryID': 5, 'CategoryName': 'Dining Out'},
    {'CategoryID': 6, 'CategoryName': 'Transportation'},
    {'CategoryID': 7, 'CategoryName': 'Entertainment'},
    {'CategoryID': 8, 'CategoryName': 'Travel'},
    {'CategoryID': 9, 'CategoryName': 'Rent or Mortgage'},
    {'CategoryID': 10, 'CategoryName': 'Utilities'},
    {'CategoryID': 11, 'CategoryName': 'Health'},
    {'CategoryID': 12, 'CategoryName': 'Insurance'},
    {'CategoryID': 13, 'CategoryName': 'Education'},
    {'CategoryID': 14, 'CategoryName': 'Personal Care'},
    {'CategoryID': 15, 'CategoryName': 'Clothing'},
    {'CategoryID': 17, 'CategoryName': 'Taxes'},
    {'CategoryID': 18, 'CategoryName': 'Pets'},
    {'CategoryID': 19, 'CategoryName': 'Subscriptions'},
    {'CategoryID': 20, 'CategoryName': 'Debt Payments'},
    {'CategoryID': 21, 'CategoryName': 'Savings'},
    {'CategoryID': 22, 'CategoryName': 'Other'}
]


@app.route('/', methods=['GET', 'POST'])
def index():
    income_manager = IncomeManager()
    expense_manager = ExpenseManager()

    # Default date range (current month)
    start_date = request.form.get('start_date', date.today().replace(day=1).strftime('%Y-%m-%d'))
    end_date = request.form.get('end_date', date.today().strftime('%Y-%m-%d'))

    # Get filtered data
    incomes = income_manager.get_incomes_between_dates(start_date, end_date)
    expenses = expense_manager.get_expenses_between_dates(start_date, end_date)

    # Add this right after getting the data to see what columns you have:
    if incomes:
        print("First income record:", incomes[0])
    if expenses:
        print("First expense record:", expenses[0])

    # Calculate totals
    total_income = sum(income['Amount'] for income in incomes) if incomes else 0
    total_expenses = sum(expense['Amount'] for expense in expenses) if expenses else 0
    balance = total_income - total_expenses

    # Get category breakdowns for charts
    income_by_category = income_manager.get_incomes_by_category(start_date, end_date)
    expense_by_category = expense_manager.get_expenses_by_category(start_date, end_date)

    # Prepare data for pie charts
    income_categories = [item['Category'] for item in income_by_category] if income_by_category else []
    income_amounts = [float(item['Total']) for item in income_by_category] if income_by_category else []

    expense_categories = [item['Category'] for item in expense_by_category] if expense_by_category else []
    expense_amounts = [float(item['Total']) for item in expense_by_category] if expense_by_category else []

    # Combine transactions for the list
    # Combine transactions for the list
    all_transactions = []
    if incomes:
        for income in incomes:
            # Find category ID for this income
            category_id = next((cat['CategoryID'] for cat in categories if cat['CategoryName'] == income['Category']),
                               1)
            all_transactions.append({
                'id': income['IncomeID'],  # ← ADD THIS LINE
                'date': income['IncomeDate'],
                'type': 'Income',
                'category': income['Category'],
                'category_id': category_id,  # ← ADD THIS LINE
                'description': income['Description'] or '',
                'amount': float(income['Amount'])
            })

    if expenses:
        for expense in expenses:
            # Find category ID for this expense
            category_id = next((cat['CategoryID'] for cat in categories if cat['CategoryName'] == expense['Category']),
                               4)
            all_transactions.append({
                'id': expense['ExpenseID'],  # ← ADD THIS LINE
                'date': expense['ExpenseDate'],
                'type': 'Expense',
                'category': expense['Category'],
                'category_id': category_id,  # ← ADD THIS LINE
                'description': expense['Description'] or '',
                'amount': float(expense['Amount'])
            })

    # Sort by date (newest first)
    all_transactions.sort(key=lambda x: x['date'], reverse=True)

    return render_template('index.html',
                           categories=categories,
                           total_income=total_income,
                           total_expenses=total_expenses,
                           balance=balance,
                           income_categories=income_categories,
                           income_amounts=income_amounts,
                           expense_categories=expense_categories,
                           expense_amounts=expense_amounts,
                           all_transactions=all_transactions,
                           start_date=start_date,
                           end_date=end_date)

@app.route('/add_income', methods=['POST'])
def add_income():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        category = categories[int(category) - 1]['CategoryName']
        date = request.form.get('date')
        description = request.form.get('description')

        # Here you would typically save to a database
        income_manager = IncomeManager()
        result = income_manager.add_income(category, amount, date, description)
        print(result)

        if result:
            flash(f'Income of ${amount} added successfully!', 'success')
            # Add a flag for popup
            session['show_popup'] = f'Income of ${amount} ({category}) added successfully to database!'
        else:
            flash('Failed to add income to database. Please try again.', 'error')
        # For now, we'll just flash a success message
        # flash(f'Income of ${amount} added successfully!', 'success')

        return redirect(url_for('index'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        category = categories[int(category) - 1]['CategoryName']
        date = request.form.get('date')
        # payment_method = request.form.get('payment_method')
        description = request.form.get('description')

        # Here you would typically save to a database
        expense_manager = ExpenseManager()
        result = expense_manager.add_expense(category, amount, date, description)
        print(result)

        if result:
            flash(f'Income of ${amount} added successfully!', 'success')
            # Add a flag for popup
            session['show_popup'] = f'Income of ${amount} ({category}) added successfully to database!'
        else:
            flash('Failed to add income to database. Please try again.', 'error')

        return redirect(url_for('index'))


# ================================
# CHATBOT FUNCTIONALITY - NEW CODE
# ================================

@app.route('/api/chatbot', methods=['POST'])
def chatbot_api():
    """
    API endpoint for chatbot communication
    """
    try:
        # Get user message from request
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Get current budget data for context
        income_manager = IncomeManager()
        expense_manager = ExpenseManager()


        # Get data from managers
        incomes = income_manager.get_all_incomes()
        expenses = expense_manager.get_all_expenses()

        # Calculate totals
        total_income = sum(income['Amount'] for income in incomes) if incomes else 0
        total_expenses = sum(expense['Amount'] for expense in expenses) if expenses else 0
        balance = total_income - total_expenses

        all_transactions = []
        if incomes:
            for income in incomes:
                all_transactions.append({
                    'date': income['IncomeDate'],
                    'type': 'Income',
                    'category': income['Category'],
                    'description': income['Description'] or '',
                    'amount': float(income['Amount'])
                })

        if expenses:
            for expense in expenses:
                all_transactions.append({
                    'date': expense['ExpenseDate'],
                    'type': 'Expense',
                    'category': expense['Category'],
                    'description': expense['Description'] or '',
                    'amount': float(expense['Amount'])
                })

        # Sort by date (newest first)
        all_transactions.sort(key=lambda x: x['date'], reverse=True)
        # Create structured context for the AI
        budget_context = f"""
FINANCIAL SUMMARY:
• All Incomes: {incomes}
• All Expenses: {expenses}
• Total Income: ${total_income:.2f}
• Total Expenses: ${total_expenses:.2f}
• Current Balance: ${balance:.2f}
• Financial Status: {'Positive' if balance >= 0 else 'Negative'}

RECENT ACTIVITY: {all_transactions}"""

        # Add top categories if available
        if incomes:
            income_by_category = {}
            for income in incomes:
                category = income['Category']
                income_by_category[category] = income_by_category.get(category, 0) + income['Amount']
            if income_by_category:
                top_income = max(income_by_category.items(), key=lambda x: x[1])
                budget_context += f"\n• Top Income Source: {top_income[0]} (${top_income[1]:.2f})"

        if expenses:
            expense_by_category = {}
            for expense in expenses:
                category = expense['Category']
                expense_by_category[category] = expense_by_category.get(category, 0) + expense['Amount']
            if expense_by_category:
                top_expense = max(expense_by_category.items(), key=lambda x: x[1])
                budget_context += f"\n• Top Expense Category: {top_expense[0]} (${top_expense[1]:.2f})"

        # Get AI response
        ollama_response = chat_with_ollama(user_message, budget_context)

        return jsonify({
            'response': ollama_response,
            'status': 'success'
        })

    except Exception as e:
        print(f"Error in chatbot API: {str(e)}")
        return jsonify({
            'response': "I'm having trouble processing your request right now. Please try again later.",
            'status': 'error'
        }), 500


def chat_with_ollama(user_message, budget_context):
    """
    Send message to Ollama using Qwen2.5:0.5b model
    """
    try:
        # Qwen2.5 works well with structured prompts
        system_prompt = f"""<|im_start|>system
You are a helpful personal finance assistant. Help users with their budget management.

Current Budget Data:
{budget_context}

Guidelines:
- Be concise but helpful
- Use the provided budget data for accurate responses
- Use the budget data as the context and only respond to the user_message
- Give practical financial advice
- Be encouraging and supportive
- Keep responses under 100 words
- Be friendly with the user and conversational
- Do not provide unnecessary information, unnecessary information refers to the information not asked by the user
<|im_end|>

<|im_start|>user
{user_message}
<|im_end|>

<|im_start|>assistant
"""

        # Ollama API request
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": system_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 200,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1,
                    "stop": ["<|im_end|>", "<|im_start|>"]
                }
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            bot_response = result.get('response', '').strip()

            # Clean up any remaining tokens
            if bot_response.endswith('<|im_end|>'):
                bot_response = bot_response[:-10].strip()
            if bot_response.startswith('<|im_start|>assistant'):
                bot_response = bot_response[21:].strip()

            return bot_response if bot_response else "I'm sorry, I couldn't generate a response."
        else:
            print(f"Ollama API error: {response.status_code}, {response.text}")
            return "I'm having trouble connecting to the AI service right now."

    except requests.exceptions.ConnectionError:
        return "Please make sure Ollama is running. Try running 'ollama serve' in your terminal."
    except requests.exceptions.Timeout:
        return "The AI is taking too long to respond. Please try a shorter question."
    except Exception as e:
        print(f"Error in chat_with_ollama: {str(e)}")
        return "I encountered an error while processing your request. Please try again."


@app.route('/edit_income', methods=['POST'])
def edit_income():
    try:
        transaction_id = request.form.get('transaction_id')
        amount = request.form.get('amount')
        category_id = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')

        # Get category name from ID
        category_name = next((cat['CategoryName'] for cat in categories if str(cat['CategoryID']) == str(category_id)),
                             None)

        if not category_name:
            flash('Invalid category selected.', 'error')
            return redirect(url_for('index'))

        income_manager = IncomeManager()
        result = income_manager.update_income(transaction_id, category_name, amount, date, description)

        if result:
            flash(f'Income updated successfully!', 'success')
        else:
            flash('Failed to update income. Please try again.', 'error')

    except Exception as e:
        print(f"Error updating income: {str(e)}")
        flash('An error occurred while updating income.', 'error')

    return redirect(url_for('index'))


@app.route('/edit_expense', methods=['POST'])
def edit_expense():
    try:
        transaction_id = request.form.get('transaction_id')
        amount = request.form.get('amount')
        category_id = request.form.get('category')
        date = request.form.get('date')
        description = request.form.get('description')

        # Get category name from ID
        category_name = next((cat['CategoryName'] for cat in categories if str(cat['CategoryID']) == str(category_id)),
                             None)

        if not category_name:
            flash('Invalid category selected.', 'error')
            return redirect(url_for('index'))

        expense_manager = ExpenseManager()
        result = expense_manager.update_expense(transaction_id, category_name, amount, date, description)

        if result:
            flash(f'Expense updated successfully!', 'success')
        else:
            flash('Failed to update expense. Please try again.', 'error')

    except Exception as e:
        print(f"Error updating expense: {str(e)}")
        flash('An error occurred while updating expense.', 'error')

    return redirect(url_for('index'))


@app.route('/delete_income', methods=['POST'])
def delete_income():
    try:
        transaction_id = request.form.get('transaction_id')

        income_manager = IncomeManager()
        result = income_manager.delete_income(transaction_id)

        if result:
            flash('Income deleted successfully!', 'success')
        else:
            flash('Failed to delete income. Please try again.', 'error')

    except Exception as e:
        print(f"Error deleting income: {str(e)}")
        flash('An error occurred while deleting income.', 'error')

    return redirect(url_for('index'))


@app.route('/delete_expense', methods=['POST'])
def delete_expense():
    try:
        transaction_id = request.form.get('transaction_id')

        expense_manager = ExpenseManager()
        result = expense_manager.delete_expense(transaction_id)

        if result:
            flash('Expense deleted successfully!', 'success')
        else:
            flash('Failed to delete expense. Please try again.', 'error')

    except Exception as e:
        print(f"Error deleting expense: {str(e)}")
        flash('An error occurred while deleting expense.', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
