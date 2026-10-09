
import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Cart2Insights | E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Cart2Insights")
st.caption("Decoding E-Commerce Performance | SQL Analytics Dashboard")

# ==========================================
# 2. DATABASE CONNECTION
# ==========================================
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
         host=st.secrets["mysql"]["host"],
        port=st.secrets["mysql"]["port"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )


def run_query(query):
    conn = get_connection()

    if not conn.is_connected():
        conn.reconnect(attempts=3, delay=2)

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)
        return pd.DataFrame(cursor.fetchall())
    finally:
        cursor.close()


# ==========================================
# 3. RADIO BUTTON NAVIGATION
# ==========================================
st.sidebar.title("📊 Dashboard Navigation")

section = st.sidebar.radio(
    "Choose an analysis section",
    [
        "Business Overview",
        "Sales Analysis",
        "Customer Analysis",
        "Seller & Product Analysis",
        "Delivery Analysis",
        "Customer Experience"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Data source: MySQL | Olist E-Commerce")


# ==========================================
# 4. REUSABLE CHART FUNCTIONS
# ==========================================
def show_chart(fig):
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        title_x=0.02,
        legend_title_text=""
    )
    st.plotly_chart(fig, use_container_width=True)


def show_error(error):
    st.error("Unable to load this analysis.")
    st.code(str(error))


# ==========================================
# 5. BUSINESS OVERVIEW
# ==========================================
if section == "Business Overview":

    st.header("Business Overview")

    query = """
    SELECT
        (SELECT COALESCE(SUM(price + freight_value), 0)
         FROM order_items) AS total_revenue,

        (SELECT COUNT(*) FROM orders) AS total_orders,

        (SELECT COUNT(*) FROM customers) AS total_customers,

        (SELECT COUNT(*) FROM sellers) AS total_sellers,

        (SELECT AVG(order_total)
         FROM (
             SELECT order_id,
                    SUM(price + freight_value) AS order_total
             FROM order_items
             GROUP BY order_id
         ) AS order_values) AS average_order_value,

        (SELECT AVG(review_score)
         FROM order_reviews) AS average_review_score;
    """

    try:
        df = run_query(query)
        m = df.iloc[0]

        a, b, c = st.columns(3)

        a.metric("Total Revenue", f"R$ {m['total_revenue']:,.2f}")
        b.metric("Total Orders", f"{int(m['total_orders']):,}")
        c.metric("Total Customers", f"{int(m['total_customers']):,}")

        d, e, f = st.columns(3)

        d.metric("Total Sellers", f"{int(m['total_sellers']):,}")
        e.metric(
            "Average Order Value",
            f"R$ {m['average_order_value']:,.2f}"
        )
        f.metric(
            "Average Review Score",
            f"{m['average_review_score']:.2f} / 5"
        )

        st.subheader("Revenue Trend")

        trend = run_query("""
            SELECT DATE_FORMAT(
                       o.order_purchase_timestamp, '%Y-%m'
                   ) AS order_month,
                   SUM(oi.price + oi.freight_value) AS revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY order_month
            ORDER BY order_month;
        """)

        if not trend.empty:
            fig = px.line(
                trend,
                x="order_month",
                y="revenue",
                markers=True,
                title="Monthly Revenue Trend",
                labels={
                    "order_month": "Month",
                    "revenue": "Revenue (R$)"
                }
            )
            show_chart(fig)

        st.caption(
            "Revenue includes item prices and freight. "
            "The figures cover the available dataset."
        )

    except Exception as e:
        show_error(e)


# ==========================================
# 6. SALES ANALYSIS
# ==========================================
elif section == "Sales Analysis":

    st.header("Sales Analysis")

    try:
        monthly = run_query("""
            SELECT DATE_FORMAT(
                       o.order_purchase_timestamp, '%Y-%m'
                   ) AS order_month,
                   SUM(oi.price + oi.freight_value) AS revenue
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY order_month
            ORDER BY order_month;
        """)

        category = run_query("""
            SELECT COALESCE(
                       p.product_category_name, 'Unknown'
                   ) AS category,
                   SUM(oi.price + oi.freight_value) AS revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY category
            ORDER BY revenue DESC
            LIMIT 10;
        """)

        products = run_query("""
            SELECT oi.product_id,
                   COUNT(*) AS units_sold,
                   SUM(oi.price) AS product_sales
            FROM order_items oi
            GROUP BY oi.product_id
            ORDER BY units_sold DESC
            LIMIT 10;
        """)

        location = run_query("""
            SELECT c.customer_state AS state,
                   SUM(oi.price + oi.freight_value) AS revenue
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY c.customer_state
            ORDER BY revenue DESC
            LIMIT 15;
        """)

        left, right = st.columns(2)

        with left:
            show_chart(px.line(
                monthly,
                x="order_month",
                y="revenue",
                markers=True,
                title="Monthly Revenue",
                labels={
                    "order_month": "Month",
                    "revenue": "Revenue (R$)"
                }
            ))

        with right:
            show_chart(px.bar(
                category.sort_values("revenue"),
                x="revenue",
                y="category",
                orientation="h",
                title="Top 10 Categories by Revenue",
                labels={
                    "revenue": "Revenue (R$)",
                    "category": "Category"
                }
            ))

        left, right = st.columns(2)

        with left:
            show_chart(px.bar(
                products.sort_values("units_sold"),
                x="units_sold",
                y="product_id",
                orientation="h",
                title="Top 10 Products by Units Sold",
                labels={
                    "units_sold": "Items Sold",
                    "product_id": "Product ID"
                }
            ))

        with right:
            show_chart(px.bar(
                location.sort_values("revenue"),
                x="revenue",
                y="state",
                orientation="h",
                title="Revenue by Customer State",
                labels={
                    "revenue": "Revenue (R$)",
                    "state": "State"
                }
            ))

    except Exception as e:
        show_error(e)


# ==========================================
# 7. CUSTOMER ANALYSIS
# ==========================================
elif section == "Customer Analysis":

    st.header("Customer Analysis")

    try:
        distribution = run_query("""
            SELECT customer_state AS state,
                   COUNT(*) AS customers
            FROM customers
            GROUP BY customer_state
            ORDER BY customers DESC
            LIMIT 15;
        """)

        spending = run_query("""
            WITH customer_spending AS (
                SELECT c.customer_unique_id,
                       COUNT(DISTINCT o.order_id) AS total_orders,
                       SUM(oi.price + oi.freight_value) AS spending
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                JOIN order_items oi ON o.order_id = oi.order_id
                GROUP BY c.customer_unique_id
            )
            SELECT customer_unique_id, total_orders, spending
            FROM customer_spending
            ORDER BY spending DESC
            LIMIT 10;
        """)

        repeat = run_query("""
            SELECT
                CASE
                    WHEN order_count = 1 THEN 'One order'
                    ELSE 'Repeat customer'
                END AS customer_type,
                COUNT(*) AS customers
            FROM (
                SELECT c.customer_unique_id,
                       COUNT(DISTINCT o.order_id) AS order_count
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_unique_id
            ) AS customer_orders
            GROUP BY customer_type;
        """)

        left, right = st.columns(2)

        with left:
            show_chart(px.bar(
                distribution.sort_values("customers"),
                x="customers",
                y="state",
                orientation="h",
                title="Customer Distribution by State",
                labels={
                    "customers": "Customers",
                    "state": "State"
                }
            ))

        with right:
            show_chart(px.pie(
                repeat,
                names="customer_type",
                values="customers",
                title="One-Order vs Repeat Customers",
                hole=0.45
            ))

        show_chart(px.bar(
            spending.sort_values("spending"),
            x="spending",
            y="customer_unique_id",
            orientation="h",
            title="Top 10 Customers by Spending",
            labels={
                "spending": "Spending (R$)",
                "customer_unique_id": "Customer"
            }
        ))

    except Exception as e:
        show_error(e)


# ==========================================
# 8. SELLER & PRODUCT ANALYSIS
# ==========================================
elif section == "Seller & Product Analysis":

    st.header("Seller & Product Analysis")

    try:
        sellers = run_query("""
            WITH seller_totals AS (
                SELECT seller_id,
                       COUNT(DISTINCT order_id) AS orders_handled,
                       SUM(price + freight_value) AS revenue
                FROM order_items
                GROUP BY seller_id
                HAVING COUNT(DISTINCT order_id) > 0
            )
            SELECT seller_id,
                   orders_handled,
                   revenue,
                   RANK() OVER (ORDER BY revenue DESC) AS seller_rank
            FROM seller_totals
            ORDER BY seller_rank
            LIMIT 10;
        """)

        categories = run_query("""
            SELECT COALESCE(
                       p.product_category_name, 'Unknown'
                   ) AS category,
                   COUNT(*) AS items_sold,
                   SUM(oi.price) AS product_sales
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY category
            ORDER BY product_sales DESC
            LIMIT 10;
        """)

        ratings = run_query("""
            SELECT oi.seller_id,
                   ROUND(AVG(r.review_score), 2) AS average_rating,
                   COUNT(*) AS review_count
            FROM order_items oi
            JOIN order_reviews r ON oi.order_id = r.order_id
            GROUP BY oi.seller_id
            HAVING COUNT(*) >= 5
            ORDER BY average_rating DESC, review_count DESC
            LIMIT 10;
        """)

        left, right = st.columns(2)

        with left:
            show_chart(px.bar(
                sellers.sort_values("revenue"),
                x="revenue",
                y="seller_id",
                orientation="h",
                title="Top 10 Sellers by Revenue",
                labels={
                    "revenue": "Revenue (R$)",
                    "seller_id": "Seller ID"
                }
            ))

        with right:
            show_chart(px.bar(
                categories.sort_values("product_sales"),
                x="product_sales",
                y="category",
                orientation="h",
                title="Top Categories by Product Sales",
                labels={
                    "product_sales": "Product Sales (R$)",
                    "category": "Category"
                }
            ))

        show_chart(px.bar(
            ratings.sort_values("average_rating"),
            x="average_rating",
            y="seller_id",
            orientation="h",
            title="Highest-Rated Sellers (Minimum 5 Reviews)",
            labels={
                "average_rating": "Average Review Score",
                "seller_id": "Seller ID"
            },
            hover_data=["review_count"]
        ))

    except Exception as e:
        show_error(e)


# ==========================================
# 9. DELIVERY ANALYSIS
# ==========================================
elif section == "Delivery Analysis":

    st.header("Delivery Analysis")

    try:
        delivery = run_query("""
            SELECT
                CASE
                    WHEN order_delivered_customer_date
                         <= order_estimated_delivery_date
                    THEN 'On time'
                    ELSE 'Delayed'
                END AS delivery_status,
                COUNT(*) AS total_orders
            FROM orders
            WHERE order_delivered_customer_date IS NOT NULL
              AND order_estimated_delivery_date IS NOT NULL
            GROUP BY delivery_status;
        """)

        duration = run_query("""
            SELECT DATE_FORMAT(
                       order_purchase_timestamp, '%Y-%m'
                   ) AS order_month,
                   ROUND(AVG(DATEDIFF(
                       order_delivered_customer_date,
                       order_purchase_timestamp
                   )), 2) AS average_delivery_days
            FROM orders
            WHERE order_delivered_customer_date IS NOT NULL
            GROUP BY order_month
            ORDER BY order_month;
        """)

        state_delivery = run_query("""
            SELECT c.customer_state AS state,
                   ROUND(AVG(DATEDIFF(
                       o.order_delivered_customer_date,
                       o.order_purchase_timestamp
                   )), 2) AS average_delivery_days
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_delivered_customer_date IS NOT NULL
            GROUP BY c.customer_state
            ORDER BY average_delivery_days DESC
            LIMIT 15;
        """)

        left, right = st.columns(2)

        with left:
            show_chart(px.pie(
                delivery,
                names="delivery_status",
                values="total_orders",
                title="On-Time vs Delayed Orders",
                hole=0.45
            ))

        with right:
            show_chart(px.line(
                duration,
                x="order_month",
                y="average_delivery_days",
                markers=True,
                title="Average Delivery Time by Month",
                labels={
                    "order_month": "Month",
                    "average_delivery_days": "Days"
                }
            ))

        show_chart(px.bar(
            state_delivery.sort_values("average_delivery_days"),
            x="average_delivery_days",
            y="state",
            orientation="h",
            title="Average Delivery Time by State",
            labels={
                "average_delivery_days": "Days",
                "state": "State"
            }
        ))

    except Exception as e:
        show_error(e)


# ==========================================
# 10. CUSTOMER EXPERIENCE
# ==========================================
elif section == "Customer Experience":

    st.header("Customer Experience")

    try:
        reviews = run_query("""
            SELECT review_score,
                   COUNT(*) AS review_count
            FROM order_reviews
            GROUP BY review_score
            ORDER BY review_score;
        """)

        category_reviews = run_query("""
            SELECT COALESCE(
                       p.product_category_name, 'Unknown'
                   ) AS category,
                   ROUND(AVG(r.review_score), 2) AS average_rating,
                   COUNT(*) AS review_count
            FROM order_reviews r
            JOIN order_items oi ON r.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            GROUP BY category
            HAVING COUNT(*) >= 20
            ORDER BY average_rating DESC
            LIMIT 15;
        """)

        rating_delivery = run_query("""
            SELECT r.review_score,
                   ROUND(AVG(DATEDIFF(
                       o.order_delivered_customer_date,
                       o.order_purchase_timestamp
                   )), 2) AS average_delivery_days,
                   COUNT(*) AS review_count
            FROM order_reviews r
            JOIN orders o ON r.order_id = o.order_id
            WHERE o.order_delivered_customer_date IS NOT NULL
            GROUP BY r.review_score
            ORDER BY r.review_score;
        """)

        # ------------------------------------------
        # CUSTOMER EXPERIENCE CHARTS
        # ------------------------------------------
        left, right = st.columns(2)

        with left:
            show_chart(px.bar(
                reviews,
                x="review_score",
                y="review_count",
                title="Review Score Distribution",
                labels={
                    "review_score": "Review Score",
                    "review_count": "Reviews"
                }
            ))

        with right:
            show_chart(px.bar(
                category_reviews.sort_values("average_rating"),
                x="average_rating",
                y="category",
                orientation="h",
                title="Category Ratings (Minimum 20 Reviews)",
                labels={
                    "average_rating": "Average Rating",
                    "category": "Category"
                },
                hover_data=["review_count"]
            ))

        show_chart(px.scatter(
            rating_delivery,
            x="average_delivery_days",
            y="review_score",
            size="review_count",
            title="Delivery Time vs Review Score",
            labels={
                "average_delivery_days": "Average Delivery Time (Days)",
                "review_score": "Review Score",
                "review_count": "Number of Reviews"
            },
            hover_data=["review_count"]
        ))

        # ------------------------------------------
        # BUSINESS INSIGHTS
        # ------------------------------------------
        st.divider()
        st.subheader("💡 Business Insights")

        if not rating_delivery.empty:

            fastest = rating_delivery.loc[
                rating_delivery["average_delivery_days"].idxmin()
            ]

            slowest = rating_delivery.loc[
                rating_delivery["average_delivery_days"].idxmax()
            ]

            fastest_days = fastest["average_delivery_days"]
            slowest_days = slowest["average_delivery_days"]
            fastest_score = int(fastest["review_score"])
            slowest_score = int(slowest["review_score"])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### 🔍 Observation")
                st.write(
                    f"The fastest delivery group averaged "
                    f"{fastest_days:.2f} days and had a review score "
                    f"of {fastest_score}/5. The slowest delivery group "
                    f"averaged {slowest_days:.2f} days and had a review "
                    f"score of {slowest_score}/5."
                )

            with col2:
                st.markdown("#### 🧠 Interpretation")
                st.write(
                    "Compare the delivery times and review scores to "
                    "understand whether slower deliveries coincide "
                    "with lower ratings. This comparison shows an "
                    "association, not proof of cause and effect."
                )

            with col3:
                st.markdown("#### 🎯 Business Impact")
                st.write(
                    "Review delayed orders and low-rated customer "
                    "experiences to identify delivery issues and "
                    "prioritize service improvements."
                )

        else:
            st.info(
                "Not enough delivery and review data to generate "
                "this insight."
            )

    except Exception as e:
        show_error(e)


# ==========================================
# 11. DASHBOARD FOOTER
# ==========================================
st.divider()
st.caption("Cart2Insights | E-Commerce Performance Analytics")
