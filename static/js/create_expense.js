// const form = document.getElementById('expense-form');

// form.addEventListener('submit', (e) => {
// e.preventDefault();

// const expenseName = document.getElementById('expense-name').value;
// const expenseValue = document.getElementById('expense-value').value;
// const expenseMonthly = document.getElementById('expense-monthly').checked;
// const expenseDaily = document.getElementById('expense-daily').checked;
// const expenseDate = document.getElementById('expense-date').value;
// const expenseType = document.getElementById('expense-type').value;

// const data = {
// expense_name: expenseName,
// expense_value: expenseValue,
// expense_monthly: expenseMonthly,
// expense_daily: expenseDaily,
// expense_date: expenseDate,
// expense_type: expenseType
// };

// fetch('http://127.0.0.1:5000/create_expense', {
// method: 'POST',
// headers: {
// 'Content-Type': 'applhication/json'
// },
// body: JSON.stringify(data)
// })
// .then(response => response.json())
// .then(data => {
// console.log('Success:', data);
// })
// .catch((error) => {
// console.error('Error:', error);
// });
// });
