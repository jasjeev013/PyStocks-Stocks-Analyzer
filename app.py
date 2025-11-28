import streamlit as st
from streamlit_option_menu import option_menu
from utils import get_stock_list,get_stock_data,download_stock_data,plot_trend_using_close_price,plot_trend_using_moving_averages,plot_volume_trend,plot_macd,get_multiple_stock_data,plot_multiple_stocks,plot_multiple_volumes
import time
import yfinance as yf
import pandas as pd


# -----------------------------
# Basic Page Config
# -----------------------------
st.set_page_config(
    page_title="Stock Analyzer App",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("Navigation")

    option = option_menu(
        menu_title="",         
        options=["Single Stock Analysis", "Multi Stock Evaluation", "Stream Stock Data", "About"], 
        icons=["align-center", "graph-up-arrow", "cast","info-circle-fill"],  # Optional icons
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
    )

    st.markdown("---")
    debug = st.checkbox("Enable debug mode")

# -----------------------------
# Main App
# -----------------------------
if option == "Single Stock Analysis":
    st.title("Single Stock Analysis")
    st.write("Enter your stock symbol below to get started & analyze its performance.")
    
    stock_list = get_stock_list()
    formatted_options = [f"{item[0]} - {item[1]}" for item in stock_list]

    # Searchable dropdown
    selected = st.selectbox(
        "Search & select a stock:",
        formatted_options,
        index=None,
        placeholder="Type to search..."
    )

    # Extract ticker
    if selected:
        ticker = selected.split(" - ")[0]
        st.write(f"### Selected Stock: **{ticker}**")
        
        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input("Start Date")

        with col2:
            end_date = st.date_input("End Date")

        col11, col12 = st.columns(2)
        # Display chosen dates
        with col11:
            st.write(f"**Start Date:** {start_date}")
        with col12:
            st.write(f"**End Date:** {end_date}")
       
        # Initialize session state to store data
        if "stock_data" not in st.session_state:
            st.session_state.stock_data = None

        # Analyze & Download buttons side by side
        btn_col1, btn_col2 = st.columns([1, 1])

        with btn_col1:
            analyze = st.button("Analyze Stock")

        # If analyze clicked, fetch data and store in session state
        if analyze:
            st.session_state.stock_data = get_stock_data(ticker, start_date, end_date)

        # Show download button only if data exists
        if st.session_state.stock_data is not None:
            with btn_col2:
                csv_data = download_stock_data(st.session_state.stock_data)
                st.download_button(
                    label="Download Data as CSV",
                    data=csv_data,
                    file_name=f"{ticker}_data.csv",
                    mime="text/csv"
                )

           
            col1, col2 = st.columns(2)

            # ----------- Column 1: Close Price Trend -----------
            with col1:
                st.write("Close Price Trend Analysis")
                
                # Plot using your function
                fig1 = plot_trend_using_close_price(st.session_state.stock_data)
                st.pyplot(fig1)
                st.caption("Trend Analyzing using Closing Prices over time.")

            # ----------- Column 2: Placeholder -----------
            with col2:
                st.write("Moving Averages Analysis")
                # You can add a graph later
                fig2 = plot_trend_using_moving_averages(st.session_state.stock_data)
                st.pyplot(fig2)
                st.caption("Trend Analyzing using Moving Averages (MA50 & MA200).")

                
            col1, col2 = st.columns(2)
            with col1:
                st.write("MACD Analysis")
                fig3 = plot_macd(st.session_state.stock_data)
                st.pyplot(fig3)
                st.caption("Compares two exponential moving averages to see if the price trend is strengthening or weakening.")
            
            with col2:
                st.write("Volume Analysis")
                fig4 = plot_volume_trend(st.session_state.stock_data)
                st.pyplot(fig4)
                st.caption("Shows volume of shares traded over time. Spikes can indicate strong investor interest.")
                
             # Display DataFrame below buttons
            st.dataframe(st.session_state.stock_data)
    
elif option == "Multi Stock Evaluation":
    st.title("Multi Stock Evaluation")
    st.write("Compare multiple stocks side by side.")
    
    stock_list = get_stock_list()   # Example format: [("AAPL", "Apple Inc"), ("MSFT", "Microsoft Corp")]
    formatted_options = [f"{item[0]} - {item[1]}" for item in stock_list]

    # --- Multiselect ---
    selected_stock_labels = st.multiselect(
        "Select stocks to compare:",
        options=formatted_options
    )

    # Convert "AAPL - Apple Inc" → "AAPL"
    selected_symbols = [item.split(" - ")[0] for item in selected_stock_labels]
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    col1, col2 = st.columns(2)
    # Display chosen dates
    with col1:
        st.write(f"**Start Date:** {start_date}")
    with col2:
        st.write(f"**End Date:** {end_date}")
    # --- Compare Button ---
    if st.button("Compare Stocks"):
        if not selected_symbols:
            st.warning("Please select at least one stock.")
        else:
            st.success(f"Comparing: {', '.join(selected_symbols)}")
            
            all_data = get_multiple_stock_data(selected_symbols, start_date, end_date)
            fig = plot_multiple_stocks(all_data)
            st.pyplot(fig)
            fig2 = plot_multiple_volumes(all_data)
            st.pyplot(fig2)
            
            tabs = st.tabs(list(all_data.keys()))

            for tab, (ticker, df) in zip(tabs, all_data.items()):
                with tab:
                    st.dataframe(df)
    
elif option == "Stream Stock Data":
    st.title("Stream Stock Data")
    st.write("Live streaming of stock data.")
    
    stock_list = get_stock_list()
    formatted_options = [f"{item[0]} - {item[1]}" for item in stock_list]

    selected = st.selectbox(
        "Search & select a stock:",
        formatted_options,
        placeholder="Type to search..."
    )

    if selected:
        ticker = selected.split(" - ")[0]
        st.write(f"### Selected Stock: **{ticker}**")

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        refresh_rate = st.slider("Refresh every (seconds)", 2, 60, 5)

        # Placeholders for live updating
        price_placeholder = st.empty()
        chart_placeholder = st.empty()
        table_placeholder = st.empty()
        download_placeholder = st.empty()

        # ------------------- Live Streaming Loop -------------------
        for _ in range(10000):  # large number to simulate continuous streaming
            data = get_stock_data(ticker, start_date, end_date)

            if not data.empty:
                latest_price = data["Close"].iloc[-1]

                # Update metric
                price_placeholder.metric("Latest Price", f"${latest_price:.2f}")

                # Update chart
                chart_placeholder.line_chart(data.set_index("Date")["Close"])

                # Update table
                with table_placeholder.container():
                    st.write("Latest Data")
                    st.dataframe(data)

                # Update download button
                csv_data = download_stock_data(data)
                download_placeholder.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"{ticker}_data.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data found for this ticker/interval.")

            time.sleep(refresh_rate)

elif option == "About":
    st.title("About")
    st.write("Get details about this app.")
    
    st.markdown("""
    This app is stock analyzer built using Streamlit and yFinance.
    - **Single Stock Analysis:** Analyze individual stocks with various technical indicators.
    - **Multi Stock Evaluation:** Compare multiple stocks side by side.
    - **Stream Stock Data:** Live streaming of stock data with periodic updates.
    
    It uses various financial methods and anlysis like closing price trends, moving averages, MACD, and volume analysis to provide insights into stock performance.With that for multi stock evaulation it uses graphs to compare stocks side by side.
    For live streaming it uses yfinance to fetch data and plot it in real time. 
    
    """)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write("Made with ❤️ using Streamlit")
