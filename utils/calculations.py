def calculate_corpus(age, retirement_age, expense, current_savings, monthly_saving, inflation=0.06, return_rate=0.08):
    years_to_retire = retirement_age - age
    annual_expense = expense * 12
    inflated_expense = annual_expense * ((1 + inflation) ** years_to_retire)
    corpus_needed = inflated_expense * 20

    total_saving = current_savings
    for _ in range(years_to_retire):
        total_saving += monthly_saving * 12
        total_saving *= (1 + return_rate)

    return corpus_needed

# --- Simulate Savings Growth ---
def simulate_savings_growth(current_savings, monthly_saving, years, interest_rate=0.07):
    balance = current_savings
    yearly_balances = []

    for year in range(1, years + 1):
        balance += (monthly_saving * 12)
        balance *= (1 + interest_rate)
        yearly_balances.append(round(balance))

    return yearly_balances
