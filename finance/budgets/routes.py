from flask import Blueprint,render_template,redirect,url_for,flash
from flask_login import login_required,current_user
from finance.models import Budget, Transaction
from finance.extensions import db
from finance.budgets.forms import BudgetForm
from sqlalchemy import func
from datetime import datetime


budgets = Blueprint('budgets',__name__,template_folder='templates')


@budgets.route('/list')
@login_required
def list_budgets():
    budget_list = Budget.query.filter_by(user_id=current_user.uid).all()

    # Compute current month window [start, next_month_start)
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1)

    # Count current month expense transactions per category for this user
    counts = (
        db.session.query(Transaction.category, func.count(Transaction.tid))
        .filter(
            Transaction.user_id == current_user.uid,
            Transaction.type == 'expense',
            Transaction.date >= month_start,
            Transaction.date < next_month_start,
        )
        .group_by(Transaction.category)
        .all()
    )
    current_month_counts = {category: count for category, count in counts}

    return render_template('budgets/listbudget.html',budget_list=budget_list,current_month_counts=current_month_counts)


@budgets.route('/add', methods=['GET','POST'])
@login_required
def add_budgets():
    form = BudgetForm()

    used_cats = [b.category for b in Budget.query.filter_by(user_id=current_user.uid).all()]

    form.category.choices = [(c,c.capitalize()) for c,_ in form.category.choices if c not in used_cats ]


    if form.validate_on_submit():
        existing = Budget.query.filter_by(user_id=current_user.uid, category=form.category.data).first()
        if existing:
            flash('budget already exists please edit the existing budget or delete it!!')
            return redirect(url_for('budgets.list_budgets'))
        from datetime import datetime
        current_month = datetime.now().strftime('%Y-%m')
        newbudget = Budget(
            user_id=current_user.uid,
            category=form.category.data,
            month=current_month,
            amount=form.amount.data
        )

        db.session.add(newbudget)
        db.session.commit()

        flash('Budget added successfully!!')
        return redirect(url_for('budgets.list_budgets'))

    return render_template('budgets/setbudget.html', form=form)

@budgets.route('/edit/<int:budget_id>',methods=['GET','POST'])
@login_required
def edit_budgets(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.user_id != current_user.uid:
        flash('Error Budget Unavailable!!')
        return redirect(url_for('budgets.list_budgets'))

    form = BudgetForm(obj=budget)

    used_cats = [b.category for b in Budget.query.filter_by(user_id=current_user.uid).all()]

    form.category.choices = [(c, c.capitalize()) for c, _ in form.category.choices if c not in used_cats]

    if form.validate_on_submit():

        existing = Budget.query.filter_by(user_id=current_user.uid,category=form.category.data).first()

        if existing:
            flash('budget already exists please edit the existing budget or delete it!!')
            return redirect(url_for('budgets.list_budgets'))

        budget.category = form.category.data
        budget.amount = form.amount.data

        db.session.commit()

        flash('budget added successfully!!')

        return redirect(url_for('budgets.list_budgets'))

    return render_template('budgets/editbudget.html',form=form,budget=budget)


@budgets.route('/delete/<int:budget_id>')
@login_required
def delete_budgets(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    if budget.user_id != current_user.uid:
        flash('Error Budget Unavailable!!')
        return redirect(url_for('budgets.list_budgets'))

    db.session.delete(budget)
    db.session.commit()
    flash('Budget deleted Sucessfully!!')
    return redirect(url_for('budgets.list_budgets'))