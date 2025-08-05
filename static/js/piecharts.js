    // Income Breakdown Chart
    const incomeCtx = document.getElementById('incomePieChart').getContext('2d');
    new Chart(incomeCtx, {
        type: 'pie',
        data: {
            labels: {{ income_categories|tojson }},
            datasets: [{
                data: {{ income_amounts|tojson }},
                backgroundColor: ['#28a745', '#17a2b8', '#ffc107', '#dc3545', '#6610f2']
            }]
        }
    });

    // Expense Breakdown Chart
    const expenseCtx = document.getElementById('expensePieChart').getContext('2d');
    new Chart(expenseCtx, {
        type: 'pie',
        data: {
            labels: {{ expense_categories|tojson }},
            datasets: [{
                data: {{ expense_amounts|tojson }},
                backgroundColor: ['#dc3545', '#ffc107', '#17a2b8', '#28a745', '#6610f2']
            }]
        }
    });
