
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv("ecommerce_sales.csv")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# ============================================================
# TITLE
# ============================================================

st.title("🛒 E-Commerce Sales Analytics Dashboard")
st.markdown(
    "### Interactive analysis of sales, products, customers and regions"
)

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

products = st.sidebar.multiselect(
    "Product",
    sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

payment_methods = st.sidebar.multiselect(
    "Payment Method",
    sorted(df["Payment_Method"].unique()),
    default=sorted(df["Payment_Method"].unique())
)

# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories)) &
    (df["Product"].isin(products)) &
    (df["Payment_Method"].isin(payment_methods))
]

# ============================================================
# KPI CALCULATIONS
# ============================================================

total_revenue = filtered_df["Revenue"].sum()

total_orders = filtered_df["Order_ID"].nunique()

total_quantity = filtered_df["Quantity"].sum()

total_customers = filtered_df["Customer_ID"].nunique()

average_order_value = (
    filtered_df["Revenue"].mean()
    if len(filtered_df) > 0
    else 0
)

# ============================================================
# KPI DISPLAY
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "🛒 Total Orders",
    f"{total_orders:,}"
)

col3.metric(
    "📦 Quantity Sold",
    f"{total_quantity:,}"
)

col4.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

col5.metric(
    "💵 Avg Order Value",
    f"₹{average_order_value:,.0f}"
)

st.divider()

# ============================================================
# MONTHLY REVENUE
# ============================================================

st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = (
    filtered_df
    .groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue (₹)")
ax.set_title("Monthly Revenue")

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# ============================================================
# CATEGORY + REGION
# ============================================================

col1, col2 = st.columns(2)

# ---------------- CATEGORY ----------------

with col1:

    st.subheader("📊 Revenue by Category")

    category_revenue = (
        filtered_df
        .groupby("Category")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(category_revenue)

# ---------------- REGION ----------------

with col2:

    st.subheader("🌍 Revenue by Region")

    region_revenue = (
        filtered_df
        .groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(region_revenue)

# ============================================================
# PRODUCT PERFORMANCE
# ============================================================

st.subheader("🏆 Product Performance")

product_revenue = (
    filtered_df
    .groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_revenue)

# ============================================================
# PAYMENT METHOD
# ============================================================

st.subheader("💳 Revenue by Payment Method")

payment_revenue = (
    filtered_df
    .groupby("Payment_Method")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(payment_revenue)

# ============================================================
# TOP CUSTOMERS
# ============================================================

st.subheader("👑 Top 10 Customers")

top_customers = (
    filtered_df
    .groupby("Customer_ID")
    .agg(
        Total_Revenue=("Revenue", "sum"),
        Orders=("Order_ID", "nunique"),
        Quantity=("Quantity", "sum")
    )
    .sort_values(
        "Total_Revenue",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customers,
    use_container_width=True
)

# ============================================================
# AUTOMATIC BUSINESS INSIGHTS
# ============================================================

st.subheader("💡 Key Business Insights")

if len(filtered_df) > 0:

    best_product = product_revenue.idxmax()
    best_product_value = product_revenue.max()

    best_category = category_revenue.idxmax()
    best_category_value = category_revenue.max()

    best_region = region_revenue.idxmax()
    best_region_value = region_revenue.max()

    best_payment = payment_revenue.idxmax()

    best_month = monthly_revenue.idxmax()
    best_month_value = monthly_revenue.max()

    st.success(
        f"🏆 **Best Product:** {best_product} "
        f"generated ₹{best_product_value:,.0f} in revenue."
    )

    st.info(
        f"📊 **Best Category:** {best_category} "
        f"generated ₹{best_category_value:,.0f}."
    )

    st.warning(
        f"🌍 **Best Region:** {best_region} "
        f"generated ₹{best_region_value:,.0f}."
    )

    st.info(
        f"📅 **Best Month:** {best_month} "
        f"with ₹{best_month_value:,.0f} in revenue."
    )

    st.success(
        f"💳 **Most Used Revenue-Generating Payment Method:** "
        f"{best_payment}."
    )

else:

    st.warning("No data available for the selected filters.")

# ============================================================
# FILTERED DATA
# ============================================================

with st.expander("🔍 View Filtered Sales Data"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "E-Commerce Sales Analytics Dashboard | "
    "Python • Pandas • Matplotlib • Streamlit"
)
st.caption(
    "E-Commerce Sales Analytics Dashboard | "
    "Python • Pandas • Matplotlib • Streamlit"
)
