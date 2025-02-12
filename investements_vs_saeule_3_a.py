import matplotlib.pyplot as plt
import random

def calculate_wealth_tax(wealth):
    """Calculate wealth tax ('Vermögenssteuer') for Canton Bern."""
    if wealth <= 97000:  # Freibetrag
        return 0
    
    # Tax brackets in CHF and their rates in permille (‰)
    brackets = [
        (35000, 0),
        (40000, 0.4),
        (135000, 0.7),
        (215000, 0.8),
        (360000, 1.0),
        (535000, 1.2),
        (2300000, 1.3),
        (2500000, 1.35)
    ]
    
    tax = 0
    remaining_wealth = wealth
    current_base = 0
    
    # Calculate for each bracket
    for bracket_size, rate in brackets:
        if remaining_wealth <= 0:
            break
            
        taxable_in_bracket = min(remaining_wealth, bracket_size)
        tax += taxable_in_bracket * (rate / 1000)  # Convert permille to decimal
        remaining_wealth -= bracket_size
        current_base += bracket_size
    
    # Calculate remaining wealth at highest rate
    if remaining_wealth > 0:
        tax += remaining_wealth * (1.25 / 1000)  # Final rate of 1.25‰
    
    return tax

def calculate_income_tax(income):
    """Calculate income tax ('Einkommenssteuer') for Canton Bern - Single person."""
    # Tax brackets in CHF and their rates in percent
    brackets = [
        (17800, 0),
        (35600, 0.44),
        (58400, 0.88),
        (89200, 1.32),
        (116900, 1.76),
        (176800, 2.20),
        (351600, 2.64)
    ]
    
    tax = 0
    remaining_income = income
    current_base = 0
    
    # Calculate for each bracket
    for bracket_limit, rate in brackets:
        if remaining_income <= 0:
            break
            
        if current_base < remaining_income:
            taxable_in_bracket = min(remaining_income - current_base, bracket_limit - current_base)
            tax += taxable_in_bracket * (rate / 100)  # Convert percent to decimal
        
        current_base = bracket_limit
    
    # Calculate remaining income at highest rate
    if remaining_income > bracket_limit:
        tax += (remaining_income - bracket_limit) * (2.97 / 100)
    
    return tax

def calculate_total_tax(income, wealth):
    """Calculate total tax including cantonal and municipal multipliers."""
    # Tax multipliers
    CANTON_MULTIPLIER = 3.025
    MUNICIPAL_MULTIPLIER = 1.54
    TOTAL_MULTIPLIER = CANTON_MULTIPLIER + MUNICIPAL_MULTIPLIER
    
    # Calculate base taxes
    income_tax = calculate_income_tax(income)
    wealth_tax = calculate_wealth_tax(wealth)
    
    # Apply multipliers
    total_tax = (income_tax + wealth_tax) * TOTAL_MULTIPLIER
    
    return total_tax

# Example usage and testing
def print_tax_analysis(income, wealth):
    """Print detailed tax analysis for given income and wealth."""
    base_income_tax = calculate_income_tax(income)
    base_wealth_tax = calculate_wealth_tax(wealth)
    total_tax = calculate_total_tax(income, wealth)
    
    print(f"\nTax Analysis for Income: {income:,.2f} CHF and Wealth: {wealth:,.2f} CHF")
    print("-" * 70)
    print(f"Base Income Tax: {base_income_tax:,.2f} CHF")
    print(f"Base Wealth Tax: {base_wealth_tax:,.2f} CHF")
    print(f"Total Base Tax: {(base_income_tax + base_wealth_tax):,.2f} CHF")
    print(f"Final Tax (with multipliers): {total_tax:,.2f} CHF")

# Test the calculations with some example values
if __name__ == "__main__":
    test_cases = [
        #(80000, 100000),    # Middle income, modest wealth
        #(150000, 500000),   # Higher income, substantial wealth
        #(50000, 90000),     # Lower income, below wealth tax threshold
        #(200000, 1000000),   # High income, high wealth
        #(100000, 127000),
        (93000, 120000)
    ]
    
    for income, wealth in test_cases:
        print_tax_analysis(income, wealth)

def calculate_3a_contribution(base_contribution, year):
    """Calculate 3a contribution limit for a given year with 2% ± 0.5% biennial increase."""
    if year <= 1:
        return base_contribution
        
    # Calculate number of 2-year periods since start
    periods = (year - 1) // 2
    
    # Generate random variations for each period
    variations = [2 + random.uniform(-0.5, 0.5) for _ in range(periods)]
    
    # Calculate cumulative increase
    total_increase = 1.0
    for variation in variations:
        total_increase *= (1 + variation/100)
    
    # Calculate new contribution, capped at yearly_investment
    new_contribution = min(base_contribution * total_increase, 20000)
    return new_contribution

def simulate_investment_strategies(initial_income=100000, initial_wealth=120000,
                                yearly_investment=20000, saeule_3a_contribution=7258,
                                wealth_growth_rate=0.04, saeule_3a_growth_rate=0.04, 
                                wealth_ter=0.001, saeule_3a_ter=0.004, years=42, num_3a_accounts=11):
    """Simulate and compare four investment strategies over time."""
    
    # Person 1: Alice - Uses 10 Säule 3a accounts, starting withdrawal at year 32
    p1_income = initial_income
    p1_wealth = initial_wealth
    p1_saeule_3a_accounts = [0] * num_3a_accounts  # Use the parameter here
    p1_active_accounts = list(range(num_3a_accounts))
    p1_total_taxes = 0
    p1_history = []
    withdrawal_history = []
    
    # Person 2: Bob - Only standard investments
    p2_income = initial_income
    p2_wealth = initial_wealth
    p2_total_taxes = 0
    p2_history = []
    
    # Person 3: Charly - Single Säule 3a account, withdrawal at retirement
    p3_income = initial_income
    p3_wealth = initial_wealth
    p3_saeule_3a_accounts = [0]  # Charly has 1 account
    p3_active_accounts = [0]
    p3_total_taxes = 0
    p3_history = []

    # Person 4: Dominic - 5 Säule 3a accounts, withdrawal starting at retirement
    p4_income = initial_income
    p4_wealth = initial_wealth
    p4_saeule_3a_accounts = [0] * 5  # Dominic has 5 accounts
    p4_active_accounts = list(range(5))
    p4_total_taxes = 0
    p4_history = []

    # Add withdrawal tracking for Person 2, 3 and 4
    p2_withdrawals = []
    p3_withdrawals = []
    p4_withdrawals = []

    # Person 5: Emily - Dynamic 3a accounts based on 50k threshold
    p5_income = initial_income
    p5_wealth = initial_wealth
    p5_saeule_3a_accounts = [0]  # Start with one account
    p5_active_accounts = [0]
    p5_total_taxes = 0
    p5_history = []
    p5_withdrawals = []

    # Initialize Alice_adjusted similar to Alice
    p6_income = initial_income
    p6_wealth = initial_wealth
    p6_saeule_3a_accounts = [0] * num_3a_accounts
    p6_active_accounts = list(range(num_3a_accounts))
    p6_total_taxes = 0
    p6_history = []

    # Set random seed for reproducibility
    random.seed(42)
    
    for year in range(1, years + 1):
        # Determine income and investment amounts based on retirement
        current_income = initial_income if year < 37 else 0
        current_investment = yearly_investment if year < 37 else 0
        current_3a = saeule_3a_contribution if year < 37 else 0 
        
        yearly_withdrawal_amount = 0  # Track withdrawals for Person 1
        
        # Handle Säule 3a account withdrawal and reinvestment for Alice
        if year >= 32 and len(p1_active_accounts) > 0 :
            account_to_close = p1_active_accounts[0]
            account_balance = p1_saeule_3a_accounts[account_to_close]
            withdrawal_tax = calculate_saeule_3a_withdrawal_tax(account_balance)
            after_tax_amount = account_balance - withdrawal_tax
            
            # Add withdrawal to wealth directly
            if year < 37:
                p1_wealth += after_tax_amount
            
            withdrawal_history.append({
                'Year': year,
                'Account': account_to_close + 1,
                'Balance': account_balance,
                'Tax': withdrawal_tax,
                'After_Tax': after_tax_amount
            })
            
            p1_saeule_3a_accounts[account_to_close] = 0
            p1_active_accounts.pop(0)
        
        # Calculate and subtract taxes for Alice
        p1_tax = calculate_total_tax(current_income - current_3a, p1_wealth)
        p1_total_taxes += p1_tax
        p1_wealth -= p1_tax  # Subtract taxes from wealth
        
        # Handle active 3a accounts
        if len(p1_active_accounts) > 0 and year < 37:
            contribution_per_account = current_3a / len(p1_active_accounts)
        else:
            contribution_per_account = 0
            
        for acc_idx in p1_active_accounts:
            p1_saeule_3a_accounts[acc_idx] = p1_saeule_3a_accounts[acc_idx] * (1 - saeule_3a_ter)
            p1_saeule_3a_accounts[acc_idx] = p1_saeule_3a_accounts[acc_idx] * (1 + saeule_3a_growth_rate)
            p1_saeule_3a_accounts[acc_idx] += contribution_per_account * (1 - saeule_3a_ter)
        
        # Apply TER and growth to regular wealth for Person 1
        p1_wealth = p1_wealth * (1 - wealth_ter)
        p1_wealth = p1_wealth * (1 + wealth_growth_rate)
        p1_wealth += (current_investment - current_3a if current_3a > 0 else current_investment)
        
        # Calculate and subtract taxes for Bob (Person 2)
        p2_tax = calculate_total_tax(current_income, p2_wealth)
        p2_total_taxes += p2_tax
        p2_wealth -= p2_tax  # Subtract taxes from wealth
        
        # Apply TER and growth to wealth for Person 2
        p2_wealth = p2_wealth * (1 - wealth_ter)
        p2_wealth = p2_wealth * (1 + wealth_growth_rate)
        p2_wealth += current_investment * (1 - wealth_ter)
        
        # Handle retirement withdrawals (starting year 37)
        if year >= 37:
            # Get Person 1's withdrawal amount for this year
            p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
            
            if p1_withdrawal > 0:
                # Person 2 (Bob) - Always withdraws from wealth to match Alice
                p2_wealth -= p1_withdrawal
                p2_withdrawals.append({
                    'Year': year,
                    'Amount': p1_withdrawal
                })
                
                # Person 3 (Charly) - Special handling for year 37
                if year == 37:
                    # Withdraw entire 3a account
                    account_balance = p3_saeule_3a_accounts[0]
                    withdrawal_tax = calculate_saeule_3a_withdrawal_tax(account_balance)
                    after_tax_amount = account_balance - withdrawal_tax
                    
                    # Match Alice's withdrawal and add excess to wealth
                    p3_wealth += (after_tax_amount - p1_withdrawal)
                    p3_withdrawals.append({
                        'Year': year,
                        'Amount': p1_withdrawal,
                        'From_3a': after_tax_amount,
                        'To_Wealth': after_tax_amount - p1_withdrawal
                    })
                    
                    p3_saeule_3a_accounts[0] = 0
                else:
                    # Years 38-42: withdraw from wealth to match Alice
                    p3_wealth -= p1_withdrawal
                    p3_withdrawals.append({
                        'Year': year,
                        'Amount': p1_withdrawal,
                        'From_Wealth': p1_withdrawal
                    })

        # Handle Person 4 (Dominic)
        if year >= 37 and year <= 41 and len(p4_active_accounts) > 0:
            # Process one 3a account per year
            account_to_close = p4_active_accounts[0]
            account_balance = p4_saeule_3a_accounts[account_to_close]
            withdrawal_tax = calculate_saeule_3a_withdrawal_tax(account_balance)
            after_tax_amount = account_balance - withdrawal_tax
            
            # Get Person 1's withdrawal for comparison
            p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
            
            # Match Alice's withdrawal and add excess to wealth
            p4_wealth += (after_tax_amount - p1_withdrawal)
            p4_withdrawals.append({
                'Year': year,
                'Amount': p1_withdrawal,
                'From_3a': after_tax_amount,
                'To_Wealth': after_tax_amount - p1_withdrawal
            })
            
            p4_saeule_3a_accounts[account_to_close] = 0
            p4_active_accounts.pop(0)
        
        elif year == 42:
            # In year 42, withdraw from wealth to match Alice
            p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
            if p1_withdrawal > 0:
                p4_wealth -= p1_withdrawal
                p4_withdrawals.append({
                    'Year': year,
                    'Amount': p1_withdrawal,
                    'From_Wealth': p1_withdrawal
                })
        
        # Handle regular investments and taxes for Charly and Dominic
        for person_idx, (income, wealth, active_accounts, saeule_3a_accounts) in enumerate(
            [(p3_income, p3_wealth, p3_active_accounts, p3_saeule_3a_accounts),
             (p4_income, p4_wealth, p4_active_accounts, p4_saeule_3a_accounts)]):
            
            # Calculate and subtract taxes
            tax = calculate_total_tax(current_income - (current_3a if len(active_accounts) > 0 else 0), wealth)
            if person_idx == 0:  # Charly
                p3_total_taxes += tax
                p3_wealth -= tax
            else:  # Dominic
                p4_total_taxes += tax
                p4_wealth -= tax
            
            # Handle active 3a accounts
            if len(active_accounts) > 0:
                contribution = current_3a if year < 37 else 0
                for acc_idx in active_accounts:
                    saeule_3a_accounts[acc_idx] *= (1 - saeule_3a_ter)
                    saeule_3a_accounts[acc_idx] *= (1 + saeule_3a_growth_rate)
                    saeule_3a_accounts[acc_idx] += contribution / len(active_accounts) * (1 - saeule_3a_ter)
            
            # Apply TER and growth to regular wealth
            if person_idx == 0:  # Charly
                p3_wealth *= (1 - wealth_ter)
                p3_wealth *= (1 + wealth_growth_rate)
                p3_wealth += (current_investment - (current_3a if len(p3_active_accounts) > 0 else 0))
            else:  # Dominic
                p4_wealth *= (1 - wealth_ter)
                p4_wealth *= (1 + wealth_growth_rate)
                p4_wealth += (current_investment - (current_3a if len(p4_active_accounts) > 0 else 0))

        # Store history for all persons
        total_3a = sum(p1_saeule_3a_accounts)
        p1_history.append({
            'Year': year,
            'Wealth': p1_wealth,
            'Saeule_3a': total_3a,
            'Saeule_3a_Accounts': p1_saeule_3a_accounts.copy(),
            'Active_Accounts': len(p1_active_accounts),
            'Yearly_Tax': p1_tax,
            'Cumulative_Tax': p1_total_taxes,
            'Yearly_Withdrawal': yearly_withdrawal_amount
        })
        
        p2_history.append({
            'Year': year,
            'Wealth': p2_wealth,
            'Yearly_Tax': p2_tax,
            'Cumulative_Tax': p2_total_taxes,
            'Withdrawal': next((w['Amount'] for w in p2_withdrawals if w['Year'] == year), 0)
        })
        
        p3_history.append({
            'Year': year,
            'Wealth': p3_wealth,
            'Saeule_3a': sum(p3_saeule_3a_accounts),
            'Yearly_Tax': tax,
            'Cumulative_Tax': p3_total_taxes,
            'Withdrawal': next((w['Amount'] for w in p3_withdrawals if w['Year'] == year), 0)
        })
        
        p4_history.append({
            'Year': year,
            'Wealth': p4_wealth,
            'Saeule_3a': sum(p4_saeule_3a_accounts),
            'Saeule_3a_Accounts': p4_saeule_3a_accounts.copy(),  # Store individual account balances
            'Yearly_Tax': tax,
            'Cumulative_Tax': p4_total_taxes,
            'Withdrawal': next((w['Amount'] for w in p4_withdrawals if w['Year'] == year), 0)
        })

        # Handle Emily's strategy
        if year < 37:
            # Calculate and subtract taxes
            p5_tax = calculate_total_tax(current_income - current_3a, p5_wealth)
            p5_total_taxes += p5_tax
            p5_wealth -= p5_tax

            # Handle 3a accounts growth and contributions
            for acc_idx in p5_active_accounts:
                p5_saeule_3a_accounts[acc_idx] *= (1 - saeule_3a_ter)
                p5_saeule_3a_accounts[acc_idx] *= (1 + saeule_3a_growth_rate)

            # Check if current active account reaches 50k
            current_account = p5_active_accounts[-1]
            remaining_space = 50000 - p5_saeule_3a_accounts[current_account]
            
            if remaining_space > 0:
                # Add contribution to current account
                contribution = min(current_3a, remaining_space)
                p5_saeule_3a_accounts[current_account] += contribution * (1 - saeule_3a_ter)
                
                # If there's remaining contribution, start new account
                remaining_contribution = current_3a - contribution
                if remaining_contribution > 0:
                    p5_saeule_3a_accounts.append(remaining_contribution * (1 - saeule_3a_ter))
                    p5_active_accounts.append(len(p5_saeule_3a_accounts) - 1)
            else:
                # Start new account
                p5_saeule_3a_accounts.append(current_3a * (1 - saeule_3a_ter))
                p5_active_accounts.append(len(p5_saeule_3a_accounts) - 1)

            # Apply TER and growth to regular wealth
            p5_wealth *= (1 - wealth_ter)
            p5_wealth *= (1 + wealth_growth_rate)
            p5_wealth += (current_investment - current_3a)

        elif year >= 37:  # Retirement phase
            # Apply TER and growth to regular wealth first
            p5_wealth *= (1 - wealth_ter)
            p5_wealth *= (1 + wealth_growth_rate)
            
            if len(p5_active_accounts) > 0:
                # Still have 3a accounts to withdraw from
                account_to_close = p5_active_accounts[0]
                account_balance = p5_saeule_3a_accounts[account_to_close]
                withdrawal_tax = calculate_saeule_3a_withdrawal_tax(account_balance)
                after_tax_amount = account_balance - withdrawal_tax
                
                # Get Person 1's withdrawal for comparison
                p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
                
                # Add excess to wealth
                p5_wealth += (after_tax_amount - p1_withdrawal)
                p5_withdrawals.append({
                    'Year': year,
                    'Amount': p1_withdrawal,
                    'From_3a': after_tax_amount,
                    'To_Wealth': after_tax_amount - p1_withdrawal
                })
                
                p5_saeule_3a_accounts[account_to_close] = 0
                p5_active_accounts.pop(0)
            else:
                # No more 3a accounts, withdraw from wealth
                p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
                if p1_withdrawal > 0:
                    p5_wealth -= p1_withdrawal
                    p5_withdrawals.append({
                        'Year': year,
                        'Amount': p1_withdrawal,
                        'From_Wealth': p1_withdrawal
                    })

        # Store Emily's history
        p5_history.append({
            'Year': year,
            'Wealth': p5_wealth,
            'Saeule_3a': sum(p5_saeule_3a_accounts),
            'Saeule_3a_Accounts': p5_saeule_3a_accounts.copy(),
            'Yearly_Tax': p5_tax if year < 37 else 0,
            'Cumulative_Tax': p5_total_taxes,
            'Withdrawal': next((w['Amount'] for w in p5_withdrawals if w['Year'] == year), 0)
        })

        # Handle Alice_adjusted similar to Alice but with adjusted contribution
        if year < 37:
            # Calculate and subtract taxes
            p6_tax = calculate_total_tax(current_income - current_3a, p6_wealth)
            p6_total_taxes += p6_tax
            p6_wealth -= p6_tax
            
            # Handle active 3a accounts with adjusted contribution
            if len(p6_active_accounts) > 0:
                contribution_per_account = current_3a / len(p6_active_accounts)
            else:
                contribution_per_account = 0
                
            for acc_idx in p6_active_accounts:
                p6_saeule_3a_accounts[acc_idx] *= (1 - saeule_3a_ter)
                p6_saeule_3a_accounts[acc_idx] *= (1 + saeule_3a_growth_rate)
                p6_saeule_3a_accounts[acc_idx] += contribution_per_account * (1 - saeule_3a_ter)
            
            # Apply TER and growth to regular wealth
            p6_wealth *= (1 - wealth_ter)
            p6_wealth *= (1 + wealth_growth_rate)
            p6_wealth += (current_investment - current_3a)
        
        # Store history for Alice_adjusted
        p6_history.append({
            'Year': year,
            'Wealth': p6_wealth,
            'Saeule_3a': sum(p6_saeule_3a_accounts),
            'Saeule_3a_Accounts': p6_saeule_3a_accounts.copy(),
            'Active_Accounts': len(p6_active_accounts),
            'Yearly_Tax': p6_tax if year < 37 else 0,
            'Cumulative_Tax': p6_total_taxes,
            'Yearly_Withdrawal': 0,
            '3a_Contribution': current_3a
        })

    return p1_history, p2_history, p3_history, p4_history, p5_history, p6_history, withdrawal_history, p3_withdrawals, p4_withdrawals, p5_withdrawals

def calculate_saeule_3a_withdrawal_tax(amount):
    """Calculate tax due on Säule 3a withdrawal."""
    tax_brackets = [
        (50000, 0.047),
        (100000, 0.056),
        (150000, 0.066),
        (200000, 0.075),
        (250000, 0.084),
        (300000, 0.093),
        (350000, 0.102),
        (400000, 0.111),
        (450000, 0.120),
        (500000, 0.129)
    ]
    
    # Find applicable tax rate
    tax_rate = tax_brackets[-1][1]  # Default to highest rate
    for threshold, rate in tax_brackets:
        if amount <= threshold:
            tax_rate = rate
            break
    
    return amount * tax_rate

def plot_retirement_phase(withdrawal_history, p2_history, p3_history, p4_history, p5_history, p3_withdrawals, p4_withdrawals, p5_withdrawals):
    """Create a visualization of retirement phase withdrawals."""
    retirement_years = range(37, 43)
    retirement_ages = [year + 28 for year in retirement_years]
    
    # Collect withdrawal data
    p1_withdrawals = [next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
                     for year in retirement_years]
    
    # Get actual withdrawal amounts from history
    p2_withdrawals = [next((h['Withdrawal'] for h in p2_history if h['Year'] == year), 0)
                     for year in retirement_years]
    
    # For Charly, get both matched withdrawals and additional money to wealth
    p3_matched = []
    p3_additional = []
    for year in retirement_years:
        withdrawal = next((h['Withdrawal'] for h in p3_history if h['Year'] == year), 0)
        p3_matched.append(withdrawal)
        
        # Get the additional amount that goes to wealth (if any)
        if year == 37:  # Only in first retirement year
            from_3a = next((w['From_3a'] for w in p3_withdrawals if w['Year'] == year), 0)
            to_wealth = from_3a - withdrawal if from_3a > withdrawal else 0
            p3_additional.append(to_wealth)
        else:
            p3_additional.append(0)
    
    # For Dominic, get both matched withdrawals and additional money to wealth
    p4_matched = []
    p4_additional = []
    for year in retirement_years:
        withdrawal = next((h['Withdrawal'] for h in p4_history if h['Year'] == year), 0)
        p4_matched.append(withdrawal)
        
        # Get the additional amount that goes to wealth (if any)
        p4_withdrawal = next((w for w in p4_withdrawals if w['Year'] == year), None)
        if p4_withdrawal and 'From_3a' in p4_withdrawal:
            from_3a = p4_withdrawal['From_3a']
            to_wealth = from_3a - withdrawal if from_3a > withdrawal else 0
        else:
            to_wealth = 0
        p4_additional.append(to_wealth)
    
    # For Emily, get matched withdrawals and additional money to wealth
    p5_matched = []
    p5_additional = []
    for year in retirement_years:
        withdrawal = next((h['Withdrawal'] for h in p5_history if h['Year'] == year), 0)
        p5_matched.append(withdrawal)
        
        # Get the additional amount that goes to wealth (if any)
        p5_withdrawal = next((w for w in p5_withdrawals if w['Year'] == year), None)
        if p5_withdrawal and 'From_3a' in p5_withdrawal:
            from_3a = p5_withdrawal['From_3a']
            to_wealth = from_3a - withdrawal if from_3a > withdrawal else 0
        else:
            to_wealth = 0
        p5_additional.append(to_wealth)
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot bars side by side
    x = range(len(retirement_ages))
    width = 0.2
    
    # Plot bars for each person
    plt.bar([i - 1.5*width for i in x], p1_withdrawals, width, 
            label='Alice (11 accounts)', color='skyblue', alpha=0.7)
    plt.bar([i - 0.5*width for i in x], p2_withdrawals, width,
            label='Bob (Direct Investment)', color='lightcoral', alpha=0.7)
    
    # Plot Charly's bars: matched withdrawals and additional money stacked
    plt.bar([i + 0.5*width for i in x], p3_matched, width,
            label='Charly (Matched)', color='lightgreen', alpha=0.7)
    plt.bar([i + 0.5*width for i in x], p3_additional, width,
            bottom=p3_matched,
            label='Charly (To Wealth)', color='palegreen', alpha=0.7)
    
    # Plot Dominic's bars: matched withdrawals and additional money stacked
    plt.bar([i + 1.5*width for i in x], p4_matched, width,
            label='Dominic (Matched)', color='purple', alpha=0.7)
    plt.bar([i + 1.5*width for i in x], p4_additional, width,
            bottom=p4_matched,
            label='Dominic (To Wealth)', color='lavender', alpha=0.7)
    
    # Plot Emily's bars: matched withdrawals and additional money stacked
    plt.bar([i + 2.5*width for i in x], p5_matched, width,
            label='Emily (Dynamic)', color='orange', alpha=0.7)
    plt.bar([i + 2.5*width for i in x], p5_additional, width,
            bottom=p5_matched,
            label='Emily (To Wealth)', color='moccasin', alpha=0.7)
    
    # Customize the plot
    plt.xlabel('Age')
    plt.ylabel('Amount (CHF)')
    plt.title('Retirement Phase Withdrawals Comparison')
    plt.legend()
    
    # Set x-axis labels to actual ages
    plt.xticks(x, retirement_ages)
    
    # Add value labels on top of bars
    for i, (v1, v2, v3, v3a, v4, v4a, v5, v5a) in enumerate(zip(p1_withdrawals, p2_withdrawals, 
                                                       p3_matched, p3_additional,
                                                       p4_matched, p4_additional,
                                                       p5_matched, p5_additional)):
        plt.text(i - 1.5*width, v1, f'{v1:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        plt.text(i - 0.5*width, v2, f'{v2:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        if v3a > 0:
            plt.text(i + 0.5*width, v3 + v3a, f'+{v3a:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        plt.text(i + 0.5*width, v3/2, f'{v3:,.0f}', ha='center', va='center', rotation=45, fontsize=8)
        if v4a > 0:
            plt.text(i + 1.5*width, v4 + v4a, f'+{v4a:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        plt.text(i + 1.5*width, v4/2, f'{v4:,.0f}', ha='center', va='center', rotation=45, fontsize=8)
        if v5a > 0:
            plt.text(i + 2.5*width, v5 + v5a, f'+{v5a:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        plt.text(i + 2.5*width, v5/2, f'{v5:,.0f}', ha='center', va='center', rotation=45, fontsize=8)
    
    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return plt.gcf()

def plot_wealth_development(p1_history, p2_history, p3_history, p4_history, p5_history, p6_history):
    """Create a visualization of total wealth development over time."""
    years = [entry['Year'] for entry in p1_history]
    ages = [year + 28 for year in years]  # Convert years to ages
    
    # Calculate total wealth for Person 1 (including Säule 3a)
    p1_total_wealth = [entry['Wealth'] + entry['Saeule_3a'] for entry in p1_history]
    p1_regular_wealth = [entry['Wealth'] for entry in p1_history]
    p1_saeule_3a = [entry['Saeule_3a'] for entry in p1_history]
    
    # Get wealth for Person 2
    p2_wealth = [entry['Wealth'] for entry in p2_history]
    
    # Calculate total wealth for Person 3 (Charly)
    p3_total_wealth = [entry['Wealth'] + entry['Saeule_3a'] for entry in p3_history]
    
    # Calculate total wealth for Person 4 (Dominic)
    p4_total_wealth = [entry['Wealth'] + entry['Saeule_3a'] for entry in p4_history]
    
    # Calculate total wealth for Person 5 (Emily)
    p5_total_wealth = [entry['Wealth'] + entry['Saeule_3a'] for entry in p5_history]
    
    # Calculate total wealth for Alice_adjusted
    p6_total_wealth = [entry['Wealth'] + entry['Saeule_3a'] for entry in p6_history]
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot lines using ages instead of years
    plt.plot(ages, p1_total_wealth, label='Alice (Total)', color='blue', linewidth=2)
    plt.plot(ages, p1_regular_wealth, label='Alice (Regular Wealth)', color='skyblue', linestyle='--')
    plt.plot(ages, p1_saeule_3a, label='Alice (pillar 3a total)', color='lightblue', linestyle=':')
    plt.plot(ages, p2_wealth, label='Bob (Total)', color='red', linewidth=2)
    plt.plot(ages, p3_total_wealth, label='Charly (Single pillar 3a)', color='green', linewidth=2)
    plt.plot(ages, p4_total_wealth, label='Dominic (5 accounts pillar 3a)', color='purple', linewidth=2)
    plt.plot(ages, p5_total_wealth, label='Emily (Dynamic pillar 3a)', color='orange', linewidth=2)
    plt.plot(ages, p6_total_wealth, label='Alice_adjusted (Dynamic 3a limit)', color='magenta', linewidth=2)
    
    # Add vertical lines for key events (convert years to ages)
    plt.axvline(x=60, color='gray', linestyle='--', alpha=0.5, label='Start of 3a Withdrawals')  # year 32 -> age 60
    plt.axvline(x=65, color='gray', linestyle=':', alpha=0.5, label='Retirement')  # year 37 -> age 65
    
    # Customize the plot
    plt.xlabel('Age')
    plt.ylabel('Wealth (CHF)')
    plt.title('Wealth Development Comparison Over Time')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format y-axis with thousands separator
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # Add annotations for key events (using ages)
    plt.text(60, plt.ylim()[0], 'Start 3a\nWithdrawals', 
             rotation=90, verticalalignment='bottom')
    plt.text(65, plt.ylim()[0], 'Retirement', 
             rotation=90, verticalalignment='bottom')
    
    plt.tight_layout()
    
    return plt.gcf()

def plot_final_years(p1_history, p2_history, p3_history, p4_history, p5_history, p6_history):
    """Create a visualization focusing on the final two years of wealth differences compared to Bob."""
    final_years = [41, 42]
    ages = [year + 28 for year in final_years]
    
    # Get wealth data for final years
    def get_final_wealth(history, has_3a=True):
        if has_3a:
            return [next((entry['Wealth'] + entry['Saeule_3a'] 
                         for entry in history if entry['Year'] == year), 0)
                    for year in final_years]
        else:
            return [next((entry['Wealth']
                         for entry in history if entry['Year'] == year), 0)
                    for year in final_years]
    
    # Get wealth values for all strategies
    p1_wealth = get_final_wealth(p1_history, has_3a=True)
    p2_wealth = get_final_wealth(p2_history, has_3a=False)  # Bob's wealth (reference)
    p3_wealth = get_final_wealth(p3_history, has_3a=True)
    p4_wealth = get_final_wealth(p4_history, has_3a=True)
    p5_wealth = get_final_wealth(p5_history, has_3a=True)
    p6_wealth = get_final_wealth(p6_history, has_3a=True)
    
    # Calculate differences compared to Bob
    p1_diff = [p1 - p2 for p1, p2 in zip(p1_wealth, p2_wealth)]
    p3_diff = [p3 - p2 for p3, p2 in zip(p3_wealth, p2_wealth)]
    p4_diff = [p4 - p2 for p4, p2 in zip(p4_wealth, p2_wealth)]
    p5_diff = [p5 - p2 for p5, p2 in zip(p5_wealth, p2_wealth)]
    p6_diff = [p6 - p2 for p6, p2 in zip(p6_wealth, p2_wealth)]
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot bars for each person with increased spacing between years
    width = 0.15
    x = [0, 1]  # Increase spacing between year groups (was: range(len(final_years)))
    
    plt.bar([i - 2*width for i in x], p1_diff, width, 
            label='Alice vs Bob', color='skyblue', alpha=0.7)
    plt.bar([i - width for i in x], p3_diff, width,
            label='Charly vs Bob', color='lightgreen', alpha=0.7)
    plt.bar([i for i in x], p4_diff, width,
            label='Dominic vs Bob', color='purple', alpha=0.7)
    plt.bar([i + width for i in x], p5_diff, width,
            label='Emily vs Bob', color='orange', alpha=0.7)
    plt.bar([i + 2*width for i in x], p6_diff, width,
            label='Alice_adjusted vs Bob', color='magenta', alpha=0.7)
    
    # Add reference line for Bob (at 0)
    plt.axhline(y=0, color='lightcoral', linestyle='-', alpha=0.5, label='Bob (reference)')
    
    # Customize the plot
    plt.xlabel('Age')
    plt.ylabel('Wealth Difference vs Bob (CHF)')
    plt.title('Final Years Wealth Comparison (Relative to Bob)')
    plt.legend()
    
    # Set x-axis labels to ages with adjusted positions
    plt.xticks(x, ages)
    
    # Add value labels on top of bars with adjusted positions
    for i, (v1, v3, v4, v5, v6) in enumerate(zip(p1_diff, p3_diff, p4_diff, p5_diff, p6_diff)):
        x_pos = x[i]  # Use new x positions
        plt.text(x_pos - 2*width, v1, f'{v1:+,.0f}', ha='center', va='bottom' if v1 > 0 else 'top', rotation=45, fontsize=8)
        plt.text(x_pos - width, v3, f'{v3:+,.0f}', ha='center', va='bottom' if v3 > 0 else 'top', rotation=45, fontsize=8)
        plt.text(x_pos, v4, f'{v4:+,.0f}', ha='center', va='bottom' if v4 > 0 else 'top', rotation=45, fontsize=8)
        plt.text(x_pos + width, v5, f'{v5:+,.0f}', ha='center', va='bottom' if v5 > 0 else 'top', rotation=45, fontsize=8)
        plt.text(x_pos + 2*width, v6, f'{v6:+,.0f}', ha='center', va='bottom' if v6 > 0 else 'top', rotation=45, fontsize=8)
    
    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Format y-axis with thousands separator
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), '+,') if x != 0 else '0'))
    
    plt.tight_layout()
    
    return plt.gcf()

def print_comparison(p1_history, p2_history, p3_history, p4_history, p5_history, p6_history, withdrawal_history, p3_withdrawals, p4_withdrawals, p5_withdrawals, saeule_3a_contribution=7258):
    """Print detailed comparison of both strategies."""
    print("\n=== Investment Strategy Comparison (0.39% TER only on Säule 3a) ===")
    print("-" * 100)
    print(f"{'Year':^6} | {'Alice (with Säule 3a)':^45} | {'Bob (without Säule 3a)':^45}")
    print(f"{'':6} | {'Wealth':^12} {'Säule 3a':^12} {'Total':^12} {'Tax':^7} | {'Wealth':^12} {'Tax':^7}")
    print("-" * 100)
    
    for p1, p2 in zip(p1_history, p2_history):
        if p1['Year'] % 5 == 0 or p1['Year'] == 1 or p1['Year'] == len(p1_history):
            print(f"{p1['Year']:4}   | "
                  f"{p1['Wealth']:11,.0f} "
                  f"{p1['Saeule_3a']:11,.0f} "
                  f"{(p1['Wealth'] + p1['Saeule_3a']):11,.0f} "
                  f"{p1['Yearly_Tax']:6,.0f} | "
                  f"{p2['Wealth']:11,.0f} "
                  f"{p2['Yearly_Tax']:6,.0f}")
    
    print("-" * 100)
    last_p1 = p1_history[-1]
    last_p2 = p2_history[-1]
    
    print("\n=== Retirement Phase Details (Years 37-42) ===")
    print("-" * 100)
    print(f"{'Year':^6} | {'Alice Withdrawal':^20} | {'Bob Withdrawal':^20} | {'Bob Remaining Wealth':^20}")
    print("-" * 100)
    
    for year in range(30, 43):
        p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
        p2_data = next((h for h in p2_history if h['Year'] == year), None)
        p2_withdrawal = p2_data['Yearly_Tax'] if p2_data else 0
        p2_wealth = p2_data['Wealth'] if p2_data else 0
        
        print(f"{year:4}   | "
              f"{p1_withdrawal:18,.2f} | "
              f"{p2_withdrawal:18,.2f} | "
              f"{p2_wealth:18,.2f}")
    
    print("\n=== Säule 3a Account Withdrawal History ===")
    total_withdrawal_tax = 0
    for withdrawal in withdrawal_history:
        print(f"Year {withdrawal['Year']}: Account {withdrawal['Account']}")
        print(f"  Balance: {withdrawal['Balance']:,.2f} CHF")
        print(f"  Tax: {withdrawal['Tax']:,.2f} CHF")
        print(f"  After Tax: {withdrawal['After_Tax']:,.2f} CHF")
        total_withdrawal_tax += withdrawal['Tax']
    
    print(f"\n=== Final Results (after {len(p1_history)} years, including all taxes) ===")
    print(f"Alice (with Säule 3a):")
    print(f"  Final Wealth (including reinvested 3a): {last_p1['Wealth']:,.2f} CHF")
    print(f"  Remaining Säule 3a: {last_p1['Saeule_3a']:,.2f} CHF")
    print(f"  Total Assets: {(last_p1['Wealth'] + last_p1['Saeule_3a']):,.2f} CHF")
    print(f"  Total Regular Taxes Paid: {last_p1['Cumulative_Tax']:,.2f} CHF")
    print(f"  Total 3a Withdrawal Taxes Paid: {total_withdrawal_tax:,.2f} CHF")
    print(f"  Total Taxes Paid: {(last_p1['Cumulative_Tax']):,.2f} CHF")
    
    print(f"\nBob (without Säule 3a):")
    print(f"  Final Wealth: {last_p2['Wealth']:,.2f} CHF")
    print(f"  Total Taxes Paid: {last_p2['Cumulative_Tax']:,.2f} CHF")
    
    tax_difference = last_p2['Cumulative_Tax'] - (last_p1['Cumulative_Tax'] + 0)
    asset_difference = (last_p1['Wealth'] + last_p1['Saeule_3a']) - last_p2['Wealth']
    total = tax_difference + asset_difference
    
    print(f"\nComparison (including all taxes):")
    print(f"  Total Tax Difference: {tax_difference:,.2f} CHF")
    print(f"  Final Asset Difference: {asset_difference:,.2f} CHF")
    print(f"  Total advantage of Säule 3a strategy: {total:,.2f} CHF")

    print("\n=== Alice's Retirement Phase Details (Years 37-42) ===")
    print("-" * 120)
    print(f"{'Year':^6} | {'3a Withdrawal':^20} | {'After Tax':^20} | {'To Wealth':^20} | {'Wealth':^20}")
    print("-" * 120)
    
    for year in range(30, 43):
        p1_data = next((h for h in p1_history if h['Year'] == year), None)
        withdrawal = next((w for w in withdrawal_history if w['Year'] == year), None)
        
        if p1_data:
            before_tax = withdrawal['Balance'] if withdrawal else 0
            after_tax = withdrawal['After_Tax'] if withdrawal else 0
            
            print(f"{year:4}   | "
                  f"{before_tax:18,.2f} | "
                  f"{after_tax:18,.2f} | "
                  f"{0:18,.2f} | "  # Alice doesn't add to wealth during retirement
                  f"{p1_data['Wealth']:18,.2f}")

    print("\n=== Bob's Retirement Phase Details (Years 37-42) ===")
    print("-" * 120)
    print(f"{'Year':^6} | {'From Wealth':^20} | {'Matches Alice':^20} | {'Remaining Wealth':^20}")
    print("-" * 120)
    
    for year in range(30, 43):
        p2_data = next((h for h in p2_history if h['Year'] == year), None)
        p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
        
        if p2_data:
            # Only show withdrawals during retirement
            from_wealth = p1_withdrawal if year >= 37 else 0
            matches_alice = p1_withdrawal if year >= 37 else 0
            
            print(f"{year:4}   | "
                  f"{from_wealth:18,.2f} | "
                  f"{matches_alice:18,.2f} | "
                  f"{p2_data['Wealth']:18,.2f}")

    print("\n=== Charly's Retirement Phase Details (Years 37-42) ===")
    print("-" * 140)
    print(f"{'Year':^6} | {'3a Withdrawal':^20} | {'From Wealth':^20} | {'Matches Alice':^20} | {'To Wealth':^20} | {'Wealth':^20}")
    print("-" * 140)
    
    for year in range(30, 43):
        p3_data = next((h for h in p3_history if h['Year'] == year), None)
        p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
        
        if p3_data:
            # Only show withdrawals during retirement
            from_3a = p3_data['Saeule_3a'] if year == 37 else 0
            from_wealth = p1_withdrawal if year >= 37 else 0
            matches_alice = p1_withdrawal if year >= 37 else 0
            to_wealth = from_3a - from_wealth if year == 37 else 0
            
            print(f"{year:4}   | "
                  f"{from_3a:18,.2f} | "
                  f"{from_wealth:18,.2f} | "
                  f"{matches_alice:18,.2f} | "
                  f"{to_wealth:18,.2f} | "
                  f"{p3_data['Wealth']:18,.2f}")

    print("\n=== Dominic's Detailed Retirement Phase Analysis (Years 37-42) ===")
    print("-" * 160)
    print(f"{'Year':^6} | {'3a Balance':^15} | {'3a After Tax':^15} | {'Alice Gets':^15} | {'To Wealth':^15} | {'Wealth Before':^15} | {'Expected After':^15} | {'Actual After':^15}")
    print("-" * 160)
    
    for year in range(37, 43):
        p4_data = next((h for h in p4_history if h['Year'] == year), None)
        prev_p4_data = next((h for h in p4_history if h['Year'] == year-1), None)
        p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
        p4_withdrawal = next((w for w in p4_withdrawals if w['Year'] == year), None)
        
        if p4_data and prev_p4_data:
            if year <= 41:  # Years with 3a withdrawals
                from_3a = p4_withdrawal['From_3a'] if p4_withdrawal else 0
                to_wealth = p4_withdrawal['To_Wealth'] if p4_withdrawal else 0
                expected_after = prev_p4_data['Wealth'] + to_wealth
                print(f"{year:4}   | "
                      f"{p4_data['Saeule_3a']:14,.2f} | "
                      f"{from_3a:14,.2f} | "
                      f"{p1_withdrawal:14,.2f} | "
                      f"{to_wealth:14,.2f} | "
                      f"{prev_p4_data['Wealth']:14,.2f} | "
                      f"{expected_after:14,.2f} | "
                      f"{p4_data['Wealth']:14,.2f}")
            else:  # Year 42 - withdrawal from wealth only
                expected_after = prev_p4_data['Wealth'] - p1_withdrawal
                print(f"{year:4}   | "
                      f"{'0':>14} | "
                      f"{'0':>14} | "
                      f"{p1_withdrawal:14,.2f} | "
                      f"{'0':>14} | "
                      f"{prev_p4_data['Wealth']:14,.2f} | "
                      f"{expected_after:14,.2f} | "
                      f"{p4_data['Wealth']:14,.2f}")
    
    print("\n=== Dominic's 3a Accounts Details ===")
    print("-" * 160)
    print(f"{'Year':^6} | {'Account 1':^15} | {'Account 2':^15} | {'Account 3':^15} | {'Account 4':^15} | {'Account 5':^15} | {'Total 3a':^15} | {'Contributions':^15}")
    print("-" * 160)
    
    for year in range(30, 43):
        p4_data = next((h for h in p4_history if h['Year'] == year), None)
        if p4_data:
            accounts = p4_data.get('Saeule_3a_Accounts', [0, 0, 0, 0, 0])  # Get individual account balances
            total_3a = sum(accounts)
            contributions = saeule_3a_contribution if year < 37 else 0
            
            print(f"{year:4}   | "
                  f"{accounts[0]:14,.2f} | "
                  f"{accounts[1]:14,.2f} | "
                  f"{accounts[2]:14,.2f} | "
                  f"{accounts[3]:14,.2f} | "
                  f"{accounts[4]:14,.2f} | "
                  f"{total_3a:14,.2f} | "
                  f"{contributions:14,.2f}")

    print("\n=== Emily's Detailed Retirement Phase Analysis (Years 37-42) ===")
    print("-" * 160)
    print(f"{'Year':^6} | {'3a Balance':^15} | {'3a After Tax':^15} | {'Alice Gets':^15} | {'To Wealth':^15} | {'Wealth Before':^15} | {'Expected After':^15} | {'Actual After':^15}")
    print("-" * 160)
    
    for year in range(37, 43):
        p5_data = next((h for h in p5_history if h['Year'] == year), None)
        prev_p5_data = next((h for h in p5_history if h['Year'] == year-1), None)
        p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
        p5_withdrawal = next((w for w in p5_withdrawals if w['Year'] == year), None)
        
        if p5_data and prev_p5_data:
            if p5_withdrawal and 'From_3a' in p5_withdrawal:  # Years with 3a withdrawals
                from_3a = p5_withdrawal['From_3a']
                to_wealth = p5_withdrawal['To_Wealth']
                expected_after = prev_p5_data['Wealth'] + to_wealth
                print(f"{year:4}   | "
                      f"{p5_data['Saeule_3a']:14,.2f} | "
                      f"{from_3a:14,.2f} | "
                      f"{p1_withdrawal:14,.2f} | "
                      f"{to_wealth:14,.2f} | "
                      f"{prev_p5_data['Wealth']:14,.2f} | "
                      f"{expected_after:14,.2f} | "
                      f"{p5_data['Wealth']:14,.2f}")
            else:  # Years withdrawing from wealth
                expected_after = prev_p5_data['Wealth'] - p1_withdrawal
                print(f"{year:4}   | "
                      f"{'0':>14} | "
                      f"{'0':>14} | "
                      f"{p1_withdrawal:14,.2f} | "
                      f"{'0':>14} | "
                      f"{prev_p5_data['Wealth']:14,.2f} | "
                      f"{expected_after:14,.2f} | "
                      f"{p5_data['Wealth']:14,.2f}")

    print("\n=== Emily's 3a Accounts Details ===")
    print("-" * 160)
    print(f"{'Year':^6} | {'Account 1':^15} | {'Account 2':^15} | {'Account 3':^15} | {'Account 4':^15} | {'Account 5':^15} | {'Total 3a':^15} | {'Contributions':^15}")
    print("-" * 160)
    
    for year in range(30, 43):
        p5_data = next((h for h in p5_history if h['Year'] == year), None)
        if p5_data:
            accounts = p5_data.get('Saeule_3a_Accounts', [])  # Get individual account balances
            # Pad with zeros if less than 5 accounts
            accounts = accounts + [0] * (5 - len(accounts))
            total_3a = sum(accounts)
            contributions = saeule_3a_contribution if year < 37 else 0
            
            print(f"{year:4}   | "
                  f"{accounts[0]:14,.2f} | "
                  f"{accounts[1]:14,.2f} | "
                  f"{accounts[2]:14,.2f} | "
                  f"{accounts[3]:14,.2f} | "
                  f"{accounts[4]:14,.2f} | "
                  f"{total_3a:14,.2f} | "
                  f"{contributions:14,.2f}")

    print("\n=== Alice_adjusted's 3a Contribution Analysis ===")
    print("-" * 160)
    print(f"{'Year':^6} | {'Base Contribution':^15} | {'Adjusted Contribution':^20} | {'Increase %':^12} | {'Total 3a':^15} | {'Wealth':^15}")
    print("-" * 160)
    
    base_contribution = saeule_3a_contribution
    for year in range(30, 43):
        p6_data = next((h for h in p6_history if h['Year'] == year), None)
        if p6_data:
            adjusted_contribution = p6_data.get('3a_Contribution', 0)
            increase_percent = ((adjusted_contribution / base_contribution) - 1) * 100 if adjusted_contribution > 0 else 0
            
            print(f"{year:4}   | "
                  f"{base_contribution:14,.2f} | "
                  f"{adjusted_contribution:19,.2f} | "
                  f"{increase_percent:11.2f} | "
                  f"{p6_data['Saeule_3a']:14,.2f} | "
                  f"{p6_data['Wealth']:14,.2f}")
    
    # Keep the visualization calls
    plot_retirement_phase(withdrawal_history, p2_history, p3_history, p4_history, p5_history, p3_withdrawals, p4_withdrawals, p5_withdrawals)
    plot_wealth_development(p1_history, p2_history, p3_history, p4_history, p5_history, p6_history)
    plot_final_years(p1_history, p2_history, p3_history, p4_history, p5_history, p6_history)
    plt.show()

if __name__ == "__main__":
    # Run the simulation with 11 Säule 3a accounts
    p1_history, p2_history, p3_history, p4_history, p5_history, p6_history, withdrawal_history, p3_withdrawals, p4_withdrawals, p5_withdrawals = simulate_investment_strategies(num_3a_accounts=11)
    print_comparison(p1_history, p2_history, p3_history, p4_history, p5_history, p6_history, withdrawal_history, p3_withdrawals, p4_withdrawals, p5_withdrawals, saeule_3a_contribution=7258)
