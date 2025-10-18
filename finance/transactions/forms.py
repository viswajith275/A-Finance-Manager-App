from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class TransactionForm(FlaskForm):
    type = SelectField('Type',choices=[('income','Income'),('expense','Expense')],validators=[DataRequired()])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than 0")])
    description = TextAreaField('Description')
    is_recurring = BooleanField('Mark as monthly recurring bill!')
    submit = SubmitField('Add Transaction')
    
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Set all possible categories to avoid validation errors
        self.category.choices = self.get_all_categories()
    
    def get_all_categories(self):
        #Return all possible categories for both income and expense
        return [
            # Income categories
            ("salary", "Salary"),
            ("freelance", "Freelance"),
            ("business", "Business"),
            ("investment", "Investment Returns"),
            ("rental", "Rental Income"),
            ("bonus", "Bonus"),
            ("gift", "Gift/Allowance"),
            ("other_income", "Other Income"),
            # Expense categories
            ("food", "Food & Dining"),
            ("rent", "Rent/Mortgage"),
            ("utilities", "Utilities"),
            ("transport", "Transportation"),
            ("entertainment", "Entertainment"),
            ("shopping", "Shopping"),
            ("healthcare", "Healthcare"),
            ("education", "Education"),
            ("insurance", "Insurance"),
            ("other_expense", "Other Expense")
        ]
    
    def get_categories_by_type(self, transaction_type):
        """Get categories filtered by transaction type for frontend display"""
        if transaction_type == 'income':
            return [
                ("salary", "Salary"),
                ("freelance", "Freelance"),
                ("business", "Business"),
                ("investment", "Investment Returns"),
                ("rental", "Rental Income"),
                ("bonus", "Bonus"),
                ("gift", "Gift/Allowance"),
                ("other_income", "Other Income")
            ]
        else:  # expense
            return [
                ("food", "Food & Dining"),
                ("rent", "Rent/Mortgage"),
                ("utilities", "Utilities"),
                ("transport", "Transportation"),
                ("entertainment", "Entertainment"),
                ("shopping", "Shopping"),
                ("healthcare", "Healthcare"),
                ("education", "Education"),
                ("insurance", "Insurance"),
                ("other_expense", "Other Expense")
            ]
