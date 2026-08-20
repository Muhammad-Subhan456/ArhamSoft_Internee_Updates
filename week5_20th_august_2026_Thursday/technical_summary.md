# Technical Summary — Orders EDA

This summary presents the key observations from the exploratory data analysis performed on the orders dataset.

## Dataset Overview

The dataset contains order-level transaction information, including order dates, customer identifiers, product categories, quantities, unit prices, and customer regions.

The original dataset contained 5,015 records across 7 columns. Before analysis, the data was diagnosed for missing values, inconsistent categories, invalid quantities, extreme prices, and duplicate records.

The identified quality issues were addressed individually before performing the final analysis.

## Data Quality Handling

Several data-quality issues were identified in the original dataset.

- Orders without a customer identifier were removed because a missing identifier could not be reliably inferred.
- Missing regions were retained and labeled as `Unknown` rather than assigning an unsupported region.
- Product category names were standardized so that differently capitalized versions of the same category were treated consistently.
- Negative quantities were treated as returns. Return information was preserved using a separate indicator while the quantity value was normalized.
- Extreme unit-price values identified as data-entry outliers were removed.
- Exact duplicate records were removed to prevent transactions from being counted more than once.

The cleaned dataset was then used for visualization and analysis.

## Key Findings

### 1. Unit Price Distribution

Most orders fall within the normal unit-price range of the cleaned dataset. The extreme data-entry values identified during diagnosis were removed before the final analysis, resulting in a more representative price distribution.

### 2. Product Category Quantity

The **electronics** category has the highest total quantity ordered, with **7818 units** in the cleaned dataset. This result was obtained from the category-level aggregation and supported by the corresponding comparison chart.

### 3. Quantity and Unit Price

There is no clear linear relationship between order quantity and unit price in the cleaned dataset. The Pearson correlation is approximately **-0.009**, which indicates a negligible linear association between the two variables.

## Limitations

The dataset is artificially generated rather than collected from real customer transactions. Therefore, the observed patterns should not be interpreted as representative of real-world customer or business behavior.

The dataset is also limited to a relatively small set of variables and a fixed generated time period. Additional information such as product-level details, actual customer demographics, discounts, payment methods, and return reasons would be required for deeper business analysis.

Finally, the analysis identifies associations and patterns in the available data but does not establish causal relationships between variables.

## Conclusion

The analysis demonstrates a complete EDA workflow from raw-data diagnosis through cleaning, visualization, and interpretation.

The main value of the analysis is not only the resulting charts, but also the systematic identification and handling of data-quality issues before drawing conclusions from the dataset.