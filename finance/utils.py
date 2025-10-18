from finance.models import RecurringBills,Transaction, Budget
from finance.extensions import db
import os,json,requests
from datetime import datetime
import pandas as pd
from prophet import Prophet
import google.generativeai as genai


def process_recurring_bills(uid):

    recbills = RecurringBills.query.filter_by(user_id=uid,active=True)
    today = datetime.utcnow().date()

    for bill in recbills:
        if bill.next_due_date <= today:

            newtranc = Transaction(user_id=uid,
                                   type='expense',
                                   category=bill.category,
                                   amount=bill.amount,
                                   description=f'Bill deducted: {bill.category}',
                                   date=datetime.utcnow()
                                   )
            db.session.add(newtranc)
            nxtmnt = bill.next_due_date.month + 1 if bill.next_due_date.month < 12 else 1
            nxtyr = bill.next_due_date.year if bill.next_due_date.month < 12 else bill.next_due_date.year + 1
            bill.next_due_date = bill.next_due_date.replace(year=nxtyr,month=nxtmnt)
    db.session.commit()

def get_insights(transactions,budgets):
    
    df = pd.DataFrame(transactions)
    
    # Check if DataFrame is empty
    if df.empty:
        return ['No transactions found for the current month.']
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Restrict to current month only
    current_month = datetime.utcnow().strftime('%Y-%m')
    df = df[df['date'].dt.to_period('M').astype(str) == current_month]
    if df.empty:
        return ['No transactions found for the current month.']
    
    df['month'] = current_month

    # Only consider budgets for the current month
    budget_map = {(b['category'], b['month']): b['amount'] for b in budgets if b.get('month') == current_month}

    insights = []

    grouped = df.groupby(['month','category'])['amount'].sum().reset_index()
    for _,row in grouped.iterrows():
        key = (row['category'],row['month'])

        if key in budget_map:
            budget_amount = budget_map[key]

            if row['amount'] > budget_amount:
                insights.append(f'Overspent on {row["category"]} by {row["amount"] - budget_amount}.')
            elif row['amount'] > 0.8 * budget_amount:
                insights.append(f'Used 80% of {row["category"]} budget in {row["month"]}.')

    
    for category in df['category'].unique():
        cat_df = df[df['category'] == category]
        monthly = cat_df.groupby(cat_df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        monthly['ds'] = monthly['date'].dt.to_timestamp()
        monthly['y'] = monthly['amount']

        if len(monthly) >= 3:
            try:
                model = Prophet()
                model.fit(monthly[['ds','y']])
                future = model.make_future_dataframe(periods=30, freq='D')
                forecast = model.predict(future)
                forecast['month'] = forecast['ds'].dt.to_period('M')
                forecast_monthly = forecast.groupby('month')['yhat'].sum().reset_index()

                latest_month = monthly['date'].max()
                next_month = latest_month + 1
                prev_spend = monthly[monthly['date'] == latest_month]['amount'].values[0]
                next_forecast = forecast_monthly[forecast_monthly['month'] == next_month]['yhat'].values[0]

                if next_forecast > 1.2 * prev_spend:
                    insights.append(f'{category} forecast to rise {round((next_forecast - prev_spend)/prev_spend * 100)} in {next_month}.')
            except Exception as e:
                # Skip forecasting if there's an error
                continue

    today = datetime.today().day
    recurring = df[df['is_recurring'] == True]
    for _,row in recurring.iterrows():
        try:
            if abs(row['date'].day - today) <= 3:
                insights.append(f'Recurring {row["category"]} charge around {row["date"].strftime("%d %b")}.')
        except Exception as e:
            # Skip if there's an error with date processing
            continue

    if not insights:
        insights.append('No issues detected, All spending within budget.')
    
    return insights

def get_from_ai(insights):
    # If AI isn't configured or fails, return the provided insights directly
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        notifications = insights if insights else ["No financial insights available."]
        return {"notifications": notifications}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Convert these financial insights into JSON with 3-5 clear notifications strictly in this schema:
        {{"notifications": ["msg1", "msg2", "msg3"]}}
        Insights: {insights}
        """

        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception:
        notifications = insights if insights else ["No financial insights available."]
        return {"notifications": notifications}

def get_news(limit=9):
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    if not NEWS_API_KEY:
        return []

    PRIORITY_KEYWORDS = [
        "recession", "inflation", "interest rate", "rate hike", "rate cut",
        "stock crash", "market crash", "selloff", "volatility", "vol spike",
        "crypto", "bitcoin", "ethereum", "fed", "federal reserve", "nasdaq",
        "layoffs", "earnings", "economy", "gdp", "cpi", "ppi", "gst",'financial literacy',
        'money management','budgeting tips','investing basics','cost of living','scholarships',
        'student loans','education budget','digital payment','UPI', 'fintech','mobile banking'
    ]

    SOURCE_REPUTATION = {
        "reuters": 3,
        "bloomberg": 3,
        "cnbc": 2,
        "financial times": 3,
        "wsj": 3,
        "the wall street journal": 3,
        "the economist": 2,
        "yahoo finance": 1,
        "marketwatch": 1,
    }

    try:
        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"category=business&language=en&pageSize=50&apiKey={NEWS_API_KEY}"
        )
        response = requests.get(url, timeout=10)
        data = response.json()
        articles = data.get("articles", [])
    except Exception:
        return []

    seen_urls = set()
    scored_news = []

    for a in articles:
        url = a.get("url")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        title = (a.get("title") or "").strip()
        description = (a.get("description") or "").strip()
        full_text = f"{title} {description}".lower()
        source_name = (a.get("source", {}).get("name") or "").strip()
        published_at = a.get("publishedAt")

        score = 0

        # keyword scoring (title weighted higher than description)
        for kw in PRIORITY_KEYWORDS:
            if kw in title.lower():
                score += 6
            elif kw in full_text:
                score += 3

        # source reputation
        rep = SOURCE_REPUTATION.get(source_name.lower(), 0)
        score += rep

        # recency boost
        try:
            if published_at:
                # expected ISO8601; recent articles get a small boost
                dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                age_hours = (datetime.utcnow().replace(tzinfo=None) - dt.replace(tzinfo=None)).total_seconds() / 3600.0
                if age_hours <= 6:
                    score += 3
                elif age_hours <= 24:
                    score += 2
                elif age_hours <= 72:
                    score += 1
        except Exception:
            pass

        severity = "high" if score >= 9 else ("medium" if score >= 4 else "low")

        scored_news.append({
            "message": title if title else (description[:120] + "…" if description else "Untitled"),
            "source": source_name or "Unknown",
            "url": url,
            "severity": severity,
            "score": score,
            "published_at": published_at,
        })

    scored_news.sort(key=lambda x: (x["severity"] != "high", -x["score"]))
    return scored_news[:limit]

def delete_previous_month_budgets():
    """Delete all budgets for the immediately previous month (format yyyy-mm).

    This is intended to be invoked once at the start of a new month. It is
    idempotent for the month boundary: calling it multiple times within the
    same month will have no additional effect after the first successful run.
    """
    # Compute previous month in yyyy-mm format
    today = datetime.utcnow().date()
    prev_month_year = today.year if today.month > 1 else today.year - 1
    prev_month_num = today.month - 1 if today.month > 1 else 12
    prev_month_str = f"{prev_month_year:04d}-{prev_month_num:02d}"

    # If there are any budgets for prev_month, delete them in a single query
    try:
        (
            Budget.query
            .filter(Budget.month == prev_month_str)
            .delete(synchronize_session=False)
        )
        db.session.commit()
    except Exception:
        db.session.rollback()