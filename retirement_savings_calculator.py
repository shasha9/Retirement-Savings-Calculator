import matplotlib.pyplot as plt
import pandas as pd

# Function to calculate retirement savings
def calculate_retirement_savings(current_savings, annual_contribution, years_until_retirement, annual_return_rate, retirement_expenses):
    savings_progress = []
    adjusted_retirement_expenses = retirement_expenses * ((1 + 0.02) ** years_until_retirement)
    
    savings = current_savings
    for year in range(1, years_until_retirement + 1):
        # Compound the savings with the expected annual return and add annual contributions after tax
        annual_contribution_after_tax = annual_contribution * (1 - 0.15)  # Assuming 15% tax on contributions
        savings = savings * (1 + annual_return_rate) + annual_contribution_after_tax
        savings_progress.append(savings)

    # Calculate final savings and post-retirement balance
    final_savings = savings
    post_retirement_balance = final_savings - (adjusted_retirement_expenses * (1 + 0.10))  # Assuming 10% tax on withdrawals

    return savings_progress, final_savings, adjusted_retirement_expenses, post_retirement_balance

# Function to calculate different investment strategies
def calculate_investment_strategy(current_savings, annual_contribution, years_until_retirement, strategies):
    strategy_results = {}
    for strategy_name, return_rate in strategies.items():
        savings_progress, final_savings, adjusted_expenses, post_retirement_balance = calculate_retirement_savings(
            current_savings, annual_contribution, years_until_retirement, return_rate, retirement_expenses=40000
        )
        strategy_results[strategy_name] = {
            "Final Savings": final_savings,
            "Adjusted Expenses": adjusted_expenses,
            "Post Retirement Balance": post_retirement_balance,
            "Savings Progress": savings_progress
        }
    return strategy_results

# Function to visualize savings growth for different strategies
def plot_strategy_comparison(strategy_results, years_until_retirement):
    plt.figure(figsize=(10, 6))
    for strategy, data in strategy_results.items():
        plt.plot(range(1, years_until_retirement + 1), data["Savings Progress"], label=strategy)
    plt.title('Comparison of Savings Growth by Strategy')
    plt.xlabel('Years until Retirement')
    plt.ylabel('Savings Amount ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to generate a report and save to file
def generate_report(strategy_results, years_until_retirement):
    report = pd.DataFrame({
        "Strategy": [],
        "Final Savings": [],
        "Adjusted Expenses": [],
        "Post Retirement Balance": []
    })

    # Update with `pd.concat()` instead of `DataFrame.append()`
    rows = []
    for strategy, data in strategy_results.items():
        row = {
            "Strategy": strategy,
            "Final Savings": data["Final Savings"],
            "Adjusted Expenses": data["Adjusted Expenses"],
            "Post Retirement Balance": data["Post Retirement Balance"]
        }
        rows.append(row)

    # Convert rows to DataFrame and concatenate to report
    report = pd.concat([report, pd.DataFrame(rows)], ignore_index=True)

    report_file = "retirement_savings_report.csv"
    report.to_csv(report_file, index=False)
    print(f"\nReport saved as {report_file}")

# Main function to get user input and run the calculator
def main():
    print("Welcome to the Retirement Savings Calculator!")

    # Input: Collect user details
    current_savings = float(input("Enter your current savings amount (in dollars): "))
    annual_contribution = float(input("Enter your annual contribution (in dollars): "))
    years_until_retirement = int(input("Enter the number of years until retirement: "))
    
    # Define multiple investment strategies with different return rates
    strategies = {
        "Conservative (3%)": 0.03,
        "Balanced (5%)": 0.05,
        "Aggressive (7%)": 0.07
    }

    # Calculate savings for each strategy
    strategy_results = calculate_investment_strategy(current_savings, annual_contribution, years_until_retirement, strategies)

    # Display results for each strategy
    for strategy, data in strategy_results.items():
        print(f"\nStrategy: {strategy}")
        print(f"Final Savings: ${data['Final Savings']:,.2f}")
        print(f"Adjusted Retirement Expenses (with inflation): ${data['Adjusted Expenses']:,.2f}")
        print(f"Post Retirement Balance (after expenses and tax): ${data['Post Retirement Balance']:,.2f}")

    # Visualize savings growth comparison
    plot_strategy_comparison(strategy_results, years_until_retirement)

    # Generate a report summary
    generate_report(strategy_results, years_until_retirement)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
