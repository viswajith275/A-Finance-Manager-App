# A Finance Manager App

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()  
A Finance Manager Web App built with Flask. This project provides a responsive dashboard for managing personal finances, tracking transactions, forecasting expenses using machine learning, and accessing the latest financial news—all in one place.

---

## 🚀 What the Project Does

- **Expense Management:** Add, edit, categorize, and track your daily transactions.
- **Budgets:** Create and monitor financial budgets to maintain spending discipline.
- **AI-Powered Predictions:** Get expense predictions and trends using integrated ML & AI.
- **Financial News Aggregation:** Stay updated with relevant business and finance news.
- **Personal Dashboard:** Customizable dashboard with insights and summary statistics.
- **Secure Authentication:** Register and manage sessions for a personalized experience.

---

## 🌟 Why the Project is Useful

- **All-in-one Tool:** Combines budgeting, transaction monitoring, and financial news.
- **Data-driven Decisions:** Make smarter spending choices with visualizations and AI predictions.
- **Instant Insights:** Track your finances intuitively without spreadsheet hassle.
- **Learning Platform:** Open-source code for those interested in Flask, MVC, and applied ML.

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- (Recommended) Virtual Environment

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/viswajith275/A-Finance-Manager-App.git
   cd A-Finance-Manager-App
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - On Windows:
     ```cmd
     set FLASK_APP=finance
     ```
   - On Linux/Mac:
     ```bash
     export FLASK_APP=finance
     ```

4. **Initialize and migrate the database:**
   ```bash
   flask db init      # (only first time)
   flask db migrate
   flask db upgrade
   ```

5. **Run the app:**
   ```bash
   python run.py
   ```
   _or_
   ```bash
   flask run
   ```

### Usage Example

- Log in or register a new account.
- Start recording your expenses and incomes via the dashboard.
- Set up monthly or custom budgets.
- See trends and expense predictions in the dashboard.
- Check the “News” section for the latest financial news.

---

## 📂 Project Structure

```
A-Finance-Manager-App/
│
├── run.py                # App entry point
├── README.md             # Project overview (this file)
├── finance/              # Main Flask app package
│   ├── __init__.py       # App factory & routes
│   ├── models.py         # Database models (users, transactions, etc.)
│   ├── extensions.py     # Flask extensions (DB, Migrate, etc.)
│   ├── utils.py          # Utility modules & helpers
│   ├── aiandnews/        # Modules for ML predictions & news integration
│   ├── auth/             # User authentication
│   ├── budgets/          # Budget-related views and logic
│   ├── dashboard/        # Dashboard routes and templates
│   ├── transactions/     # CRUD for transaction records
│   └── templates/        # Jinja2 HTML templates
└── ...
```

---

## 🤝 Contributing

All contributions are welcome! Please read our [CONTRIBUTING.md](docs/CONTRIBUTING.md) for development workflow, code style, and submitting issues/PRs.

---

## 📖 Documentation & Help

- See [docs/](docs/) for more documentation, setup guides, and FAQs.
- For issues or feature requests, please open an issue in the [GitHub Issues](../../issues) tab.
- For usage or troubleshooting, check the project wiki or [contact the maintainer](#maintainers).

---

## 👨‍💻 Maintainers

- **viswajith275** - [GitHub Profile](https://github.com/viswajith275)

---

> **License:** See [LICENSE](LICENSE) for details.
