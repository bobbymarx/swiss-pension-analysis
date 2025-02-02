import matplotlib.pyplot as plt

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
        (100000, 127000),
        (93000, 120000)
    ]
    
    for income, wealth in test_cases:
        print_tax_analysis(income, wealth)

def simulate_investment_strategies(initial_income=100000, initial_wealth=120000,
                                yearly_investment=20000, saeule_3a_contribution=7258,
                                wealth_growth_rate=0.04, saeule_3a_growth_rate=0.04, 
                                wealth_ter=0.001, saeule_3a_ter=0.004, years=42, num_3a_accounts=10):
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

    for year in range(1, years + 1):
        # Determine income and investment amounts based on retirement
        current_income = initial_income if year < 37 else 0
        current_investment = yearly_investment if year < 37 else 0
        current_3a = saeule_3a_contribution if year <= 37 else 0
        
        yearly_withdrawal_amount = 0  # Track withdrawals for Person 1
        
        # Handle Säule 3a account withdrawal and reinvestment
        if year >= 32 and len(p1_active_accounts) > 0:
            account_to_close = p1_active_accounts[0]
            account_balance = p1_saeule_3a_accounts[account_to_close]
            withdrawal_tax = calculate_saeule_3a_withdrawal_tax(account_balance)
            after_tax_amount = account_balance - withdrawal_tax
            
            yearly_withdrawal_amount = after_tax_amount  # Store withdrawal amount
            
            withdrawal_history.append({
                'Year': year,
                'Account': account_to_close + 1,
                'Balance': account_balance,
                'Tax': withdrawal_tax,
                'After_Tax': after_tax_amount
            })
            
            # Only reinvest if not retired
            if year < 37:
                p1_wealth += after_tax_amount
            
            p1_saeule_3a_accounts[account_to_close] = 0
            p1_active_accounts.pop(0)
        
        # Calculate and subtract taxes for Alice
        p1_tax = calculate_total_tax(current_income - current_3a, p1_wealth)
        p1_total_taxes += p1_tax
        p1_wealth -= p1_tax  # Subtract taxes from wealth
        
        # Handle active 3a accounts
        if len(p1_active_accounts) > 0 and year <= 37:
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
        
        # Handle retirement withdrawals for Person 2 and 3
        if year >= 37:
            # Get Person 1's withdrawal amount for this year
            p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
            
            if p1_withdrawal > 0:
                # Person 2 withdraws the same amount
                p2_wealth -= p1_withdrawal
                if p2_wealth < 0:
                    print(f"Warning: Person 2 depleted wealth in year {year}")
                    p2_wealth = 0
                
                # Person 3 withdraws the same amount
                p3_wealth -= p1_withdrawal
                if p3_wealth < 0:
                    print(f"Warning: Person 3 depleted wealth in year {year}")
                    p3_wealth = 0

        # Handle Person 3 (Charly)
        if year == 37 and len(p3_active_accounts) > 0:
            # Withdraw entire Säule 3a amount at retirement
            account_balance = p3_saeule_3a_accounts[0]
            withdrawal_tax = calculate_saeule_3a_withdrawal_tax(account_balance)
            after_tax_amount = account_balance - withdrawal_tax
            
            # Add the entire amount to wealth (excess will be handled by retirement withdrawals)
            p3_wealth += after_tax_amount
            
            p3_saeule_3a_accounts[0] = 0
            p3_active_accounts = []

        # Handle Person 4 (Dominic)
        if year >= 37 and len(p4_active_accounts) > 0:
            # Withdraw one account per year starting at retirement
            account_to_close = p4_active_accounts[0]
            account_balance = p4_saeule_3a_accounts[account_to_close]
            withdrawal_tax = calculate_saeule_3a_withdrawal_tax(account_balance)
            after_tax_amount = account_balance - withdrawal_tax
            
            # Compare with Person 1's withdrawal and add excess to wealth
            p1_withdrawal = next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
            if after_tax_amount > p1_withdrawal:
                p4_wealth += (after_tax_amount - p1_withdrawal)
            
            p4_saeule_3a_accounts[account_to_close] = 0
            p4_active_accounts.pop(0)

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
            if len(active_accounts) > 0 and year <= 37:
                contribution = current_3a
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
            'Cumulative_Tax': p2_total_taxes
        })
        
        p3_history.append({
            'Year': year,
            'Wealth': p3_wealth,
            'Saeule_3a': sum(p3_saeule_3a_accounts),
            'Yearly_Tax': tax,
            'Cumulative_Tax': p3_total_taxes
        })
        
        p4_history.append({
            'Year': year,
            'Wealth': p4_wealth,
            'Saeule_3a': sum(p4_saeule_3a_accounts),
            'Yearly_Tax': tax,
            'Cumulative_Tax': p4_total_taxes
        })
    
    return p1_history, p2_history, p3_history, p4_history, withdrawal_history

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

def plot_retirement_phase(withdrawal_history, p2_history, p3_history, p4_history):
    """Create a visualization of retirement phase withdrawals."""
    retirement_years = range(37, 43)
    
    # Collect withdrawal data
    p1_withdrawals = [next((w['After_Tax'] for w in withdrawal_history if w['Year'] == year), 0)
                     for year in retirement_years]
    
    # Fixed withdrawal calculations for persons 2-4
    p2_withdrawals = []
    p3_withdrawals = []
    p4_withdrawals = []
    
    for year in retirement_years:
        # Person 2 withdrawals
        p2_current = next((h for h in p2_history if h['Year'] == year), None)
        p2_next = next((h for h in p2_history if h['Year'] == year + 1), None) if year < 42 else None
        p2_withdrawal = p2_current['Wealth'] - (p2_next['Wealth'] if p2_next else 0) if p2_current else 0
        p2_withdrawals.append(max(0, p2_withdrawal))
        
        # Person 3 withdrawals
        p3_current = next((h for h in p3_history if h['Year'] == year), None)
        p3_next = next((h for h in p3_history if h['Year'] == year + 1), None) if year < 42 else None
        p3_withdrawal = p3_current['Wealth'] - (p3_next['Wealth'] if p3_next else 0) if p3_current else 0
        p3_withdrawals.append(max(0, p3_withdrawal))
        
        # Person 4 withdrawals
        p4_current = next((h for h in p4_history if h['Year'] == year), None)
        p4_next = next((h for h in p4_history if h['Year'] == year + 1), None) if year < 42 else None
        p4_withdrawal = p4_current['Wealth'] - (p4_next['Wealth'] if p4_next else 0) if p4_current else 0
        p4_withdrawals.append(max(0, p4_withdrawal))
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot bars side by side
    x = range(len(retirement_years))
    width = 0.2  # Reduced width to accommodate more bars
    
    # Plot bars for each person
    plt.bar([i - 1.5*width for i in x], p1_withdrawals, width, 
            label='Alice (10 accounts)', color='skyblue', alpha=0.7)
    plt.bar([i - 0.5*width for i in x], p2_withdrawals, width,
            label='Bob (Direct Investment)', color='lightcoral', alpha=0.7)
    plt.bar([i + 0.5*width for i in x], p3_withdrawals, width,
            label='Charly (Single account)', color='lightgreen', alpha=0.7)
    plt.bar([i + 1.5*width for i in x], p4_withdrawals, width,
            label='Dominic (5 accounts)', color='purple', alpha=0.7)
    
    # Customize the plot
    plt.xlabel('Year')
    plt.ylabel('Withdrawal Amount (CHF)')
    plt.title('Retirement Phase Withdrawals Comparison')
    plt.legend()
    
    # Set x-axis labels to actual years
    plt.xticks(x, retirement_years)
    
    # Add value labels on top of bars
    for i, (v1, v2, v3, v4) in enumerate(zip(p1_withdrawals, p2_withdrawals, p3_withdrawals, p4_withdrawals)):
        plt.text(i - 1.5*width, v1, f'{v1:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        plt.text(i - 0.5*width, v2, f'{v2:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        plt.text(i + 0.5*width, v3, f'{v3:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
        plt.text(i + 1.5*width, v4, f'{v4:,.0f}', ha='center', va='bottom', rotation=45, fontsize=8)
    
    # Add grid for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return plt.gcf()  # Return the figure for potential further use

def plot_wealth_development(p1_history, p2_history, p3_history, p4_history):
    """Create a visualization of total wealth development over time."""
    years = [entry['Year'] for entry in p1_history]
    
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
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot lines
    plt.plot(years, p1_total_wealth, label='Alice (Total)', color='blue', linewidth=2)
    plt.plot(years, p1_regular_wealth, label='Alice (Regular Wealth)', color='skyblue', linestyle='--')
    plt.plot(years, p1_saeule_3a, label='Alice (Säule 3a)', color='lightblue', linestyle=':')
    plt.plot(years, p2_wealth, label='Bob (Total)', color='red', linewidth=2)
    plt.plot(years, p3_total_wealth, label='Charly (Single 3a)', color='green', linewidth=2)
    plt.plot(years, p4_total_wealth, label='Dominic (5 accounts)', color='purple', linewidth=2)
    
    # Add vertical lines for key events
    plt.axvline(x=32, color='gray', linestyle='--', alpha=0.5, label='Start of 3a Withdrawals')
    plt.axvline(x=37, color='gray', linestyle=':', alpha=0.5, label='Retirement')
    
    # Customize the plot
    plt.xlabel('Year')
    plt.ylabel('Wealth (CHF)')
    plt.title('Wealth Development Comparison Over Time')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format y-axis with thousands separator
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    # Add annotations for key events
    plt.text(32, plt.ylim()[0], 'Start 3a\nWithdrawals', 
             rotation=90, verticalalignment='bottom')
    plt.text(37, plt.ylim()[0], 'Retirement', 
             rotation=90, verticalalignment='bottom')
    
    plt.tight_layout()
    
    return plt.gcf()

def print_comparison(p1_history, p2_history, p3_history, p4_history, withdrawal_history):
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
    
    for year in range(37, 43):
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

    # Add both visualizations
    plot_retirement_phase(withdrawal_history, p2_history, p3_history, p4_history)
    plot_wealth_development(p1_history, p2_history, p3_history, p4_history)
    plt.show()

if __name__ == "__main__":
    # Run the simulation with 10 Säule 3a accounts
    p1_history, p2_history, p3_history, p4_history, withdrawal_history = simulate_investment_strategies(num_3a_accounts=10)
    print_comparison(p1_history, p2_history, p3_history, p4_history, withdrawal_history)
