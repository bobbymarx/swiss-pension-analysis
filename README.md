# swiss-pension-analysis
Analysis of Säule 3a vs Direct Investment in Switzerland

## Key Findings

The simulation reveals several interesting insights about the Swiss pension system:

1. **Tax Benefits**: 
   - Immediate tax savings during the contribution phase
   - Impact of wealth tax differences
   - Special withdrawal tax considerations

2. **Growth Comparison**:
   - Effect of different TER rates on long-term growth
   - Impact of tax-privileged growth in Säule 3a
   - Compound interest effects over 42 years

3. **Retirement Phase**:
   - Sequential withdrawal strategy benefits
   - Post-retirement wealth comparison
   - Withdrawal tax implications

## Visualization

The code generates two main visualizations:
1. Wealth development over time for both strategies
2. Retirement phase withdrawal comparison

## Limitations and Assumptions

- Based on Canton Bern tax rates
- Assumes stable investment returns
- Does not account for inflation
- Uses current (2024) Säule 3a contribution limits
- Assumes consistent yearly investments
- Does not consider market volatility

## Configuration Parameters

The `simulate_investment_strategies` function accepts the following parameters:

### Basic Parameters
| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `initial_income` | 100,000 CHF | Starting annual income |
| `initial_wealth` | 120,000 CHF | Starting wealth/savings |
| `yearly_investment` | 20,000 CHF | Total amount invested per year |
| `saeule_3a_contribution` | 7,258 CHF | Yearly Säule 3a contribution (2024 maximum) |

### Investment Parameters
| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `wealth_growth_rate` | 0.04 (4%) | Annual return rate for regular investments |
| `saeule_3a_growth_rate` | 0.04 (4%) | Annual return rate for Säule 3a accounts |
| `wealth_ter` | 0.001 (0.1%) | Total Expense Ratio for regular investments |
| `saeule_3a_ter` | 0.004 (0.4%) | Total Expense Ratio for Säule 3a funds |

### Simulation Settings
| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| `years` | 42 | Total simulation period in years |
| `num_3a_accounts` | 10 | Number of Säule 3a accounts to open |

### Important Notes:
- All monetary values are in CHF
- Growth rates and TER should be provided as decimals (e.g., 0.04 for 4%)
- The simulation assumes:
  * Retirement starts at year 37
  * Säule 3a withdrawals begin at year 32
  * No more contributions after retirement
  * Withdrawals match between both strategies during retirement

## Further Reading

For a detailed analysis of the results, check out our [Medium article](YOUR_ARTICLE_LINK).

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or find any bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Swiss Federal Tax Administration for tax rate information
- Canton Bern for cantonal tax rates
- Swiss banking regulations for Säule 3a rules and limits
