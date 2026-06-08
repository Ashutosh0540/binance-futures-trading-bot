import streamlit as st
import pandas as pd

from bot.client import get_client
from bot.orders import OrderManager

st.set_page_config(
    page_title="Binance Futures Trading Bot",
    page_icon="📈",
    layout="wide"
)

# -------------------------------
# Header
# -------------------------------

st.title("📈 Binance Futures Trading Bot")

client = get_client()
manager = OrderManager(client)

tab1, tab2, tab3 = st.tabs(
    [
        "🚀 Place Order",
        "💰 Account Balance",
        "📋 Order History"
    ]
)

# ==========================
# TAB 1 - PLACE ORDER
# ==========================

with tab1:

    st.subheader("Place a Futures Order")

    col1, col2 = st.columns(2)

    with col1:
        symbol = st.selectbox(
            "Symbol",
            ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
        )

        side = st.selectbox(
            "Side",
            ["BUY", "SELL"]
        )

    with col2:
        order_type = st.selectbox(
            "Order Type",
            ["MARKET", "LIMIT"]
        )

        quantity = st.number_input(
            "Quantity",
            min_value=0.001,
            value=0.001,
            step=0.001
        )

    price = None

    if order_type == "LIMIT":
        price = st.number_input(
            "Limit Price",
            min_value=1.0,
            value=200000.0
        )

    if st.button("🚀 Place Order", use_container_width=True):

        try:

            if order_type == "MARKET":

                response = manager.place_market_order(
                    symbol,
                    side,
                    quantity
                )

            else:

                response = manager.place_limit_order(
                    symbol,
                    side,
                    quantity,
                    price
                )

            st.success("Order submitted successfully!")

            st.subheader("Order Response")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Order ID",
                    response.get("orderId")
                )

                st.metric(
                    "Status",
                    response.get("status")
                )

                st.metric(
                    "Side",
                    response.get("side")
                )

            with col2:
                st.metric(
                    "Type",
                    response.get("type")
                )

                st.metric(
                    "Executed Qty",
                    response.get("executedQty")
                )

                st.metric(
                    "Avg Price",
                    response.get("avgPrice")
                )

            with st.expander("View Full Response"):
                st.json(response)

        except Exception as e:
            st.error(str(e))

# ==========================
# TAB 2 - BALANCE
# ==========================

with tab2:

    st.subheader("Futures Account Balance")

    try:

        balances = client.futures_account_balance()

        balance_df = pd.DataFrame(balances)

        st.dataframe(
            balance_df,
            use_container_width=True
        )

    except Exception as e:

        st.error(str(e))

# ==========================
# TAB 3 - ORDER HISTORY
# ==========================

with tab3:

    st.subheader("Recent BTCUSDT Orders")

    try:

        orders = client.futures_get_all_orders(
            symbol="BTCUSDT"
        )

        if orders:

            order_df = pd.DataFrame(orders)

            columns_to_show = [
                "orderId",
                "symbol",
                "side",
                "type",
                "status",
                "price",
                "executedQty",
                "avgPrice"
            ]

            available_columns = [
                col for col in columns_to_show
                if col in order_df.columns
            ]

            st.dataframe(
                order_df[available_columns].tail(20),
                use_container_width=True
            )

        else:

            st.info("No orders found.")

    except Exception as e:

        st.error(str(e))

# -------------------------------
# Footer
# -------------------------------

st.markdown("---")
st.caption(
    "Binance Futures Demo Trading | Built using Python, Streamlit, and Binance API"
)