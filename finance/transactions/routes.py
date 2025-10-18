from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_required,current_user
from finance.transactions.forms import TransactionForm
from finance.models import Transaction
from finance.extensions import db

transbp = Blueprint('transactions',__name__,template_folder='templates')

@transbp.route('/add', methods=['GET','POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    
    if form.validate_on_submit():
        transaction = Transaction(
            user_id=current_user.uid,
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data,
            is_recurring=form.is_recurring.data
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!!')
        return redirect(url_for('transactions.list_transaction'))
    return render_template('transactions/addtransactions.html',form=form)

@transbp.route('/list')
@login_required
def list_transaction():
    transactions = Transaction.query.filter_by(user_id=current_user.uid).order_by(Transaction.date.desc()).all()
    return render_template("transactions/listtransactions.html", transactions=transactions)

@transbp.route('/edit/<int:transaction_id>',methods=['GET','POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)

    if transaction.user_id != current_user.uid:
        flash('Error Transaction unavailable!',)
        return redirect(url_for('transactions.list_transaction'))

    form = TransactionForm(obj=transaction)

    if form.validate_on_submit():
        transaction.type = form.type.data
        transaction.category = form.category.data
        transaction.amount = form.amount.data
        transaction.description = form.description.data
        transaction.is_recurring = form.is_recurring.data
        db.session.commit()
        flash('Transaction updated Successfully!!')
        return redirect(url_for('transactions.list_transaction'))

    return render_template('transactions/edittransactions.html',form=form,transaction=transaction)

@transbp.route('/delete/<int:transaction_id>')
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)

    if transaction.user_id != current_user.uid:
        flash('Error Transaction unavailable!')
        return redirect(url_for('transactions.list_transaction'))

    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted Successfully!!')
    return redirect(url_for('transactions.list_transaction'))