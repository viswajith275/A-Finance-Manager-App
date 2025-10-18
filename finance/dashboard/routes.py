from flask import  Blueprint,render_template
from flask_login import login_required,current_user
from finance.utils import process_recurring_bills
from finance.models import Transaction,Budget,RecurringBills
from datetime import datetime
from finance.extensions import db

dashboard = Blueprint('dashboard',__name__,template_folder='templates')

@dashboard.route('/')
@login_required
def dashboards():

    process_recurring_bills(current_user.uid)

    usrtranc = Transaction.query.filter_by(user_id=current_user.uid).all()

    income_list = [i for i in usrtranc if i.type=='income']
    expense_list = [e for e in usrtranc if e.type == 'expense']

    total_income = sum(i.amount for i in income_list)
    total_expense = sum(i.amount for i in expense_list)
    net_save = total_income-total_expense

    month = datetime.now().strftime('%Y-%m')
    budgets = Budget.query.filter_by(user_id=current_user.uid,month=month).all()

    spentpercat = {}

    # Restrict spending counts to current month only for budget tab
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1)

    expense_list_current_month = [
        e for e in expense_list if month_start <= e.date < next_month_start
    ]

    for b in budgets:
        spentpercat[b.category] = sum(
            e.amount for e in expense_list_current_month if e.category == b.category
        )


    chartdata = {
            'labels': list(spentpercat.keys()),  #only show the spended categories in chart
            'spent': list(spentpercat.values()),#only get the spended values
            'budget': [b.amount for b in budgets]
        }

    curbudsstat = {}
    for b in budgets:
        spent = spentpercat.get(b.category,0)
        if spent > b.amount:
            curbudsstat[b.category] = 'Over Budget'
        elif spent > 0.9*b.amount:
            curbudsstat[b.category] = 'Nearing budget careful'
        else:
            curbudsstat[b.category] = 'within budget'
    return render_template('dashboard/index.html',
                           total_income=total_income,
                           total_expense=total_expense,
                           net_save=net_save,
                           chartdata=chartdata,
                           curbudsstat=curbudsstat
                           )