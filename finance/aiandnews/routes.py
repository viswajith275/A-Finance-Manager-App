from flask import Blueprint,render_template
from flask_login import login_required, current_user
from finance.models import Transaction,Budget
from finance.utils import get_insights, get_from_ai, get_news, delete_previous_month_budgets

aiandnews = Blueprint('aiandnews',__name__,template_folder='templates')

@aiandnews.route('/')
@login_required
def ai_and_news():
    # Cleanup previous month's budgets on first access in a new month
    delete_previous_month_budgets()

    transactions = Transaction.query.filter_by(user_id=current_user.uid).all()
    budgets = Budget.query.filter_by(user_id=current_user.uid).all()

    trans = [{'date': t.date.strftime('%Y-%m-%d'),
            'amount': t.amount,
            'category': t.category,
            'is_recurring': t.is_recurring,
            'desc': t.description
    } for t in transactions]

    buds = [{
            'category': b.category,
            'month': b.month,
            'amount': b.amount,
    } for b in budgets]

    insights = get_insights(trans,buds)

    ai_notifications = get_from_ai(insights)

    lat_news = get_news() #add finace news via api

    return render_template('aiandnews/index.html',ai_notifications=ai_notifications,get_news=lat_news)
