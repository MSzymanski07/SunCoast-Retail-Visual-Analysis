# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# First, we create a line graph depicting total sales across each quarter
# We also create custom labels to make the graph look more professional
def plot_quarterly_sales_trend():
    fig, ax = plt.subplots()
    quarterly_sales = sales_df.groupby("Quarter")["Sales"].sum().sort_index()
    ax.plot(range(len(quarterly_sales)), quarterly_sales.values)
    labels = sales_df.sort_values("Quarter")["QuarterLabel"].unique()
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_title("Quarterly Sales Trends")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales (in millions)")
    ax.grid(True, linestyle="--", alpha=0.3)
    return fig

# Next we make a multi-line chart with sales trends for each location
def plot_location_sales_comparison():
    fig, ax = plt.subplots()
    quarterly_location = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()
    for location in quarterly_location:
        ax.plot(quarterly_location.index, quarterly_location[location], label=location)
    ax.set_title("Location Sales Comparison by Quarter")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales")
    ax.legend()
    return fig

# TODO 2: Categorical Comparison - Product Performance by Location
# We make grouped bar chart comparing category performance by location
def plot_category_performance_by_location():
    fig, ax = plt.subplots()
    loc_category = sales_df.groupby(["Location", "Category"])["Sales"].sum().unstack()
    locations = loc_category.index
    categories = loc_category.columns
    x = range(len(locations))
    bar_width = 0.20
    for i, category in enumerate(categories):
        ax.bar(
            [pos + i * bar_width for pos in x],
            loc_category[category],
            width=bar_width,
            label=category
        )
    ax.set_title("Category Performance by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Sales (in millions)")
    ax.set_xticks([pos + bar_width * 2 for pos in x])
    ax.set_xticklabels(locations)
    ax.legend()
    return fig

# Now we make a stacked bar chart to show sales composition by location
def plot_sales_composition_by_location():
    fig, ax = plt.subplots()
    loc_category = sales_df.groupby(["Location", "Category"])["Sales"].sum().unstack()
    bottom = None
    for category in loc_category.columns:
        ax.bar(
            loc_category.index,
            loc_category[category],
            bottom=bottom,
            label=category
            )
        if bottom is None:
            bottom = loc_category[category].copy()
        else:
            bottom += loc_category[category]
    ax.set_title("Location Sales Composition")
    ax.set_xlabel("Location")
    ax.set_ylabel("Sales (in millions)")
    ax.legend()
    return fig

# TODO 3: Relationship Analysis - Advertising and Sales
# This scatter plot analyzes the relationship between ad spending and sales
# Also includes a line of best fit, and an annotation about the outlier
def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots()
    ax.scatter(
        sales_df["AdSpend"],
        sales_df["Sales"],
        alpha=0.6
        )
    slope, intercept = np.polyfit(sales_df["AdSpend"], sales_df["Sales"], 1)
    ax.plot(sales_df["AdSpend"], slope * sales_df["AdSpend"] + intercept, color="red")
    high = sales_df.loc[sales_df["Sales"].idxmax()]
    ax.annotate(
        "Outlier",
        xy=(high["AdSpend"], high["Sales"]),
        xytext=(2, 2),
        textcoords="offset points"
        )
    ax.set_title("Correlation between Advertising Spending and Sales Revenue")
    ax.set_xlabel("Advert. Spending")
    ax.set_ylabel("Sales Revenue")
    return fig

# Line Chart showing sales per dollar spent on ads
# Includes annotations on low and high efficiency
def plot_ad_efficiency_over_time():
    fig, ax = plt.subplots()
    efficiency = sales_df.groupby("QuarterLabel")["SalesPerDollarSpent"].mean()
    ax.plot(
        efficiency.index,
        efficiency.values
        )
    max_idx = np.argmax(efficiency.values)
    min_idx = np.argmin(efficiency.values)
    ax.annotate(
        "High Efficiency",
        xy=(max_idx, efficiency.values[max_idx]),
        xytext=(max_idx, efficiency.values[max_idx] + 0.2)
    )
    ax.annotate(
        "Low Efficiency",
        xy=(min_idx, efficiency.values[min_idx]),
        xytext=(min_idx, efficiency.values[min_idx] - 0.2)
    )
    ax.set_title("Advertising Efficiency Over Time")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales per Dollar Spent on Advertising")
    return fig

# TODO 4: Distribution Analysis - Customer Demographics
# These two histograms show customer age distribution, and then age distribution by location
# Also includes lines to show the mean and median ages
def plot_customer_age_distribution():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    mean_age = customer_df["Age"].mean()
    median_age = customer_df["Age"].median()
    
    # First Plot
    axes[0].hist(customer_df["Age"], bins=15, color="blue", edgecolor="black")
    axes[0].axvline(mean_age, color="red", linestyle="-", label="Mean Age")
    axes[0].axvline(median_age, color="purple", linestyle="-", label="Median Age")
    axes[0].set_title("General Customer Age Distribution")
    axes[0].set_xlabel("Age")
    axes[0].set_ylabel("Number of Customers")
    axes[0].legend()
    
    # Second Plot
    locations = customer_df["Location"].unique()
    for location in locations:
        subset = customer_df[customer_df["Location"] == location]
        axes[1].hist(subset["Age"], bins=15, alpha=0.6, label=location)
    axes[1].axvline(mean_age, color="red", linestyle="-", label="Mean Age")
    axes[1].axvline(median_age, color="purple", linestyle="-", label="Median Age")
    axes[1].set_title("Customer Age Distribution by Location")
    axes[1].set_xlabel("Age")
    axes[1].set_ylabel("Number of Customers")
    axes[1].legend()
    plt.tight_layout()
    return fig

# Here we create a boxplot showing purchases per age group
# We define the bins and labels before we create the figure...
# ...and also create an age group column in our customer DataFrame to work with the data better
def plot_purchase_by_age_group():
    fig, ax = plt.subplots()
    bins = [18, 30, 40, 50, 80]
    labels = ["18-29", "30-39", "40-49", "50+"]
    customer_df["AgeGroup"] = pd.cut(customer_df["Age"], bins=bins, labels=labels, right=False)
    grouped_data = [
        customer_df[customer_df["AgeGroup"] == group]["PurchaseAmount"]
        for group in labels
    ]
    ax.boxplot(grouped_data, tick_labels=labels)
    ax.set_title("Purchase Amounts by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Amount of Purchases")
    return fig

# TODO 5: Sales Distribution - Pricing Tiers
# This code creates a histogram that shows the number of customers per purchase amounts
def plot_purchase_amount_distribution():
    fig, ax = plt.subplots()
    ax.hist(customer_df["PurchaseAmount"], bins=20, color="red", edgecolor="black")
    ax.set_title("Distribution of Purchase Amounts")
    ax.set_xlabel("Purchase Amount")
    ax.set_ylabel("Number of Customers")
    return fig

# Now we make a pie chart that shows the sales by price tier, including percentages and exploding the largest slice
def plot_sales_by_price_tier():
    fig, ax = plt.subplots()
    sales_by_tier = customer_df.groupby("PriceTier")["PurchaseAmount"].sum()
    maxidx = np.argmax(sales_by_tier.values)
    explode = [0] * len(sales_by_tier)
    explode[maxidx] = 0.1
    ax.pie(
        sales_by_tier.values,
        labels=sales_by_tier.index,
        autopct="%1.2f%%",
        explode=explode
        )
    ax.set_title("Sales Breakdown by Price Tier")
    return fig

# TODO 6: Market Share Analysis
# The pie chart created here shows the sales by category, including percentages
# Also pulls out the largest slice
def plot_category_market_share():
    fig, ax = plt.subplots()
    category_sales = sales_df.groupby("Category")["Sales"].sum()
    maxidx = np.argmax(category_sales.values)
    explode = [0] * len(category_sales)
    explode[maxidx] = 0.1
    ax.pie(
        category_sales.values,
        labels=category_sales.index,
        autopct="%1.2f%%",
        explode=explode
        )
    ax.set_title("Sales Breakdown by Category")
    return fig

# While this pie chart shows sales by locations
def plot_location_sales_distribution():
    fig, ax = plt.subplots()
    location_sales = sales_df.groupby("Location")["Sales"].sum()
    ax.pie(
        location_sales.values,
        labels=location_sales.index,
        autopct="%1.2f%%"
        )
    ax.set_title("Sales Breakdown by Location")
    return fig


# TODO 7: Comprehensive Dashboard
# This is the code for our comprehensive dashboard, which includes the following graphs:
# 1. Quarterly Sales line graph
# 2. Category Sales by Location stacked bar chart
# 3. Advertising and Sales Relationship scatter plot
# 4. Customer Age Distribution histogram
def create_business_dashboard():
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("SunCoast Retail Business Dashboard")
    
    # First Chart
    quarterly_sales = sales_df.groupby("Quarter")["Sales"].sum().sort_index()
    axes[0, 0].plot(range(len(quarterly_sales)), quarterly_sales.values)
    labels = sales_df.sort_values("Quarter")["QuarterLabel"].unique()
    axes[0, 0].set_xticks(range(len(labels)))
    axes[0, 0].set_xticklabels(labels)
    axes[0, 0].set_title("Quarterly Sales Trend")
    axes[0, 0].set_xlabel("Quarter")
    axes[0, 0].set_ylabel("Total Sales (in millions)")
    axes[0, 0].grid(True, linestyle="--", alpha=0.3)

    # Second Chart
    loc_category = sales_df.groupby(["Location", "Category"])["Sales"].sum().unstack()
    bottom = None
    for category in loc_category.columns:
        axes[0, 1].bar(loc_category.index, loc_category[category], bottom=bottom, label=category)
        if bottom is None:
            bottom = loc_category[category].copy()
        else:
            bottom += loc_category[category]
    axes[0, 1].set_title("Location Sales Composition")
    axes[0, 1].set_xlabel("Location")
    axes[0, 1].set_ylabel("Sales (in millions)")
    axes[0, 1].legend()

    # Third Chart
    axes[1, 0].scatter(
        sales_df["AdSpend"],
        sales_df["Sales"],
        alpha=0.6
    )
    slope, intercept = np.polyfit(sales_df["AdSpend"], sales_df["Sales"], 1)
    axes[1, 0].plot(sales_df["AdSpend"], slope * sales_df["AdSpend"] + intercept, color="red")
    high = sales_df.loc[sales_df["Sales"].idxmax()]
    axes[1, 0].annotate(
        "Outlier",
        xy=(high["AdSpend"], high["Sales"]),
        xytext=(2, 2),
        textcoords="offset points"
        )
    axes[1, 0].set_title("Correlation between Advertising Spending and Sales Revenue")
    axes[1, 0].set_xlabel("Advert. Spending")
    axes[1, 0].set_ylabel("Sales Revenue")

    # Fourth Chart
    mean_age = customer_df["Age"].mean()
    median_age = customer_df["Age"].median()
    axes[1, 1].hist(customer_df["Age"], bins=15, color="blue", edgecolor="black")
    axes[1, 1].axvline(mean_age, color="red", linestyle="-", label="Mean Age")
    axes[1, 1].axvline(median_age, color="purple", linestyle="-", label="Median Age")
    axes[1, 1].set_title("General Customer Age Distribution")
    axes[1, 1].set_xlabel("Age")
    axes[1, 1].set_ylabel("Number of Customers")
    axes[1, 1].legend()

    plt.tight_layout()
    return fig

# Main function to execute all visualizations
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # Business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    print("- Quarter 4 sales tend to be highest, while quarter 1 sales tend to be lowest")
    print("- Electronics takes up the largest percentage of sales across all locations")
    print("- Spending on advertising and sales revenue seem to have a positive correlation")
    print("- Most customer ages are split between people in their 20's and people in their middle-age")
    
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()