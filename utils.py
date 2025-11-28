import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import time
from io import StringIO
import warnings
warnings.filterwarnings('ignore')

stocks = [
    ["AAPL", "Apple Inc."],
    ["MSFT", "Microsoft Corporation"],
    ["GOOGL", "Alphabet Inc."],
    ["AMZN", "Amazon.com, Inc."],
    ["NVDA", "NVIDIA Corporation"],
    ["META", "Meta Platforms, Inc."],
    ["TSLA", "Tesla, Inc."],
    ["BRK.B", "Berkshire Hathaway Inc. Class B"],
    ["BRK.A", "Berkshire Hathaway Inc. Class A"],
    ["LLY", "Eli Lilly & Company"],
    ["AVGO", "Broadcom Inc."],
    ["JPM", "JPMorgan Chase & Co."],
    ["WMT", "Walmart Inc."],
    ["ORCL", "Oracle Corporation"],
    ["V", "Visa Inc."],
    ["XOM", "Exxon Mobil Corporation"],
    ["PG", "Procter & Gamble Co."],
    ["UNH", "UnitedHealth Group Incorporated"],
    ["MA", "Mastercard Incorporated"],
    ["HD", "The Home Depot, Inc."],
    ["BAC", "Bank of America Corporation"],
    ["NFLX", "Netflix, Inc."],
    ["DIS", "Walt Disney Company"],
    ["COST", "Costco Wholesale Corporation"],
    ["PEP", "PepsiCo, Inc."],
    ["KO", "Coca-Cola Company"],
    ["CSCO", "Cisco Systems, Inc."],
    ["QCOM", "QUALCOMM, Inc."],
    ["MRK", "Merck & Co., Inc."],
    ["PFE", "Pfizer Inc."],
    ["ABNB", "Airbnb, Inc."],
    ["NKE", "Nike, Inc."],
    ["INTC", "Intel Corporation"],
    ["ADBE", "Adobe Inc."],
    ["CRM", "Salesforce, Inc."],
    ["MCD", "McDonald's Corporation"],
    ["IBM", "International Business Machines Corporation"],
    ["AMD", "Advanced Micro Devices, Inc."],
    ["PYPL", "PayPal Holdings, Inc."],
    ["CVX", "Chevron Corporation"],
    ["HON", "Honeywell International Inc."],
    ["T", "AT&T Inc."],
    ["VZ", "Verizon Communications Inc."],
    ["CAT", "Caterpillar Inc."],
    ["GE", "General Electric Company"],
    ["UPS", "United Parcel Service, Inc."],
    ["FDX", "FedEx Corporation"],
    ["SPGI", "S&P Global Inc."],
    ["PLTR", "Palantir Technologies Inc."],
    ["SO", "Southern Company"],
    ["NEE", "NextEra Energy, Inc."],
    ["SBUX", "Starbucks Corporation"],
    ["LMT", "Lockheed Martin Corporation"],
    ["BA", "Boeing Company"],
    ["MO", "Altria Group, Inc."],
    ["TGT", "Target Corporation"],
    ["LOW", "Lowe's Companies, Inc."],
    ["BMY", "Bristol-Myers Squibb Company"],
    ["AMGN", "Amgen Inc."],
    ["GILD", "Gilead Sciences, Inc."],
    ["MMM", "3M Company"],
    ["MDT", "Medtronic plc"],
    ["DE", "Deere & Company"],
    ["F", "Ford Motor Company"],
    ["GM", "General Motors Company"],
    ["UBER", "Uber Technologies, Inc."],
    ["LYFT", "Lyft, Inc."],
    ["SQ", "Block, Inc."],
    ["SHOP", "Shopify Inc."],
    ["ROKU", "Roku, Inc."],
    ["BYND", "Beyond Meat, Inc."],
    ["SNOW", "Snowflake Inc."],
    ["DKNG", "DraftKings Inc."],
    ["ROST", "Ross Stores, Inc."],
    ["TJX", "TJX Companies Inc."],
    ["SPOT", "Spotify Technology S.A."],
    ["YELP", "Yelp Inc."],
    ["EBAY", "eBay Inc."],
    ["DASH", "DoorDash, Inc."],
    ["TWLO", "Twilio Inc."],
    ["ZM", "Zoom Video Communications, Inc."],
    ["PANW", "Palo Alto Networks, Inc."],
    ["CRWD", "CrowdStrike Holdings, Inc."],
    ["NET", "Cloudflare, Inc."],
    ["DDOG", "Datadog, Inc."],
    ["OKTA", "Okta, Inc."],
    ["TEAM", "Atlassian Corporation"],
    ["WORK", "Slack Technologies, Inc."],
    ["HUBS", "HubSpot, Inc."],
    ["INTU", "Intuit Inc."],
    ["ADP", "Automatic Data Processing, Inc."],
    ["WBD", "Warner Bros. Discovery"],
    ["PARA", "Paramount Global"],
    ["FOX", "Fox Corporation"],
    ["TME", "Tencent Music Entertainment"],
    ["BABA", "Alibaba Group"],
    ["JD", "JD.com, Inc."],
    ["PDD", "Pinduoduo Inc."],
    ["TCEHY", "Tencent Holdings"],
    ["NIO", "NIO Inc."],
    ["XPEV", "XPeng Inc."],
    ["LI", "Li Auto Inc."],
    ["SONY", "Sony Group Corp"],
    ["TM", "Toyota Motor Corporation"],
    ["HMC", "Honda Motor Co."],
    ["NSANY", "Nissan Motor Co."],
    ["LULU", "Lululemon Athletica Inc."],
    ["ADDYY", "Adidas AG"],
    ["PINS", "Pinterest, Inc."],
    ["MTCH", "Match Group, Inc."],
    ["ETSY", "Etsy, Inc."],
    ["WISH", "ContextLogic Inc."],
    ["COIN", "Coinbase Global, Inc."],
    ["HOOD", "Robinhood Markets, Inc."],
    ["RIOT", "Riot Platforms, Inc."],
    ["MARA", "Marathon Digital Holdings"],
    ["WDC", "Western Digital Corporation"],
    ["STX", "Seagate Technology"],
    ["CSX", "CSX Corporation"],
    ["UNP", "Union Pacific Corporation"],
    ["NSC", "Norfolk Southern Corporation"],
    ["DAL", "Delta Air Lines, Inc."],
    ["AAL", "American Airlines Group Inc."],
    ["UAL", "United Airlines Holdings, Inc."],
    ["LUV", "Southwest Airlines Co."],
    ["AER", "AerCap Holdings"],
    ["RCL", "Royal Caribbean Cruises"],
    ["CCL", "Carnival Corporation"],
    ["NCLH", "Norwegian Cruise Line"],
    ["HLT", "Hilton Worldwide"],
    ["MAR", "Marriott International"],
    ["EXPE", "Expedia Group, Inc."],
    ["BKNG", "Booking Holdings Inc."],
    ["CHTR", "Charter Communications"],
    ["CMCSA", "Comcast Corporation"],
    ["VOD", "Vodafone Group"],
    ["TMUS", "T-Mobile US, Inc."],
    ["SIRI", "Sirius XM Holdings"],
    ["BEN", "Franklin Resources"],
    ["BLK", "BlackRock, Inc."],
    ["BK", "Bank of New York Mellon"],
    ["SCHW", "Charles Schwab Corporation"],
    ["UBS", "UBS Group AG"],
    ["HSBC", "HSBC Holdings"],
    ["ING", "ING Groep"],
    ["CS", "Credit Suisse"],
    ["RY", "Royal Bank of Canada"],
    ["TD", "Toronto-Dominion Bank"],
    ["BNS", "Bank of Nova Scotia"],
    ["ENB", "Enbridge Inc."],
    ["SU", "Suncor Energy, Inc."],
    ["CNQ", "Canadian Natural Resources"],
    ["BP", "BP plc"],
    ["SHEL", "Shell plc"],
    ["TOT", "TotalEnergies SE"],
    ["EQNR", "Equinor ASA"],
    ["RIO", "Rio Tinto Group"],
    ["BHP", "BHP Group"],
    ["VALE", "Vale S.A."],
    ["FCX", "Freeport-McMoRan Inc."],
    ["GLNCY", "Glencore plc"],
    ["NEM", "Newmont Corporation"],
    ["GOLD", "Barrick Gold Corporation"],
    ["AZN", "AstraZeneca plc"],
    ["GSK", "GSK plc"],
    ["SNY", "Sanofi"],
    ["RHHBY", "Roche Holding AG"],
    ["NVS", "Novartis AG"],
    ["BUD", "Anheuser-Busch InBev"],
    ["DEO", "Diageo plc"],
    ["UL", "Unilever plc"],
    ["NESN", "Nestlé S.A."],
    ["SAP", "SAP SE"],
    ["ASML", "ASML Holding N.V."],
    ["ADYEY", "Adyen N.V."],
    ["IFNNY", "Infineon Technologies"],
    ["PHG", "Philips NV"],
    ["ERIC", "Ericsson"],
    ["NOK", "Nokia"],
    ["TSM", "Taiwan Semiconductor Manufacturing"],
    ["HMC", "Honda Motor Co."],
    ["INFY", "Infosys Ltd"],
    ["TCS", "Tata Consultancy Services"],
    ["WIT", "Wipro Limited"],
    ["RELIANCE.NS", "Reliance Industries"],
    ["HDFCBANK.NS", "HDFC Bank"],
    ["ICICIBANK.NS", "ICICI Bank"],
    ["SBIN.NS", "State Bank of India"],
    ["TATASTEEL.NS", "Tata Steel"],
    ["TATAMOTORS.NS", "Tata Motors"],
    ["ASIANPAINT.NS", "Asian Paints"],
    ["ADANIENT.NS", "Adani Enterprises"],
    ["ADANIPORTS.NS", "Adani Ports"],
    ["BHARTIARTL.NS", "Bharti Airtel"],
    ["ONGC.NS", "Oil & Natural Gas Corp"],
    ["COALINDIA.NS", "Coal India"],
    ["MARUTI.NS", "Maruti Suzuki"],
    ["ITC.NS", "ITC Limited"],
    ["HINDUNILVR.NS", "Hindustan Unilever"],
    ["ULTRACEMCO.NS", "UltraTech Cement"]
]

## Single Stock Analysis Functions

def get_stock_list():
    return stocks;

def get_stock_data(ticker, start_date, end_date):
    # Download data
    data = yf.download(ticker, start=start_date, end=end_date, progress=False,threads=True)
    data.reset_index(inplace=True)
    
    # Flatten MultiIndex columns if any
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    data['Date'] = pd.to_datetime(data['Date'])

    return data

def download_stock_data(data):
    csv_buffer = StringIO()
    data.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def plot_trend_using_close_price(df):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['Date'], df["Close"], label="Close Price", color="blue")
    ax.set_title("Closing Price Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate() 
    
    ax.grid(True)
    ax.legend()
    return fig

def plot_trend_using_moving_averages(df):
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['Date'], df["Close"], label="Close Price", color="blue", alpha=0.5)
    ax.plot(df['Date'], df['MA50'], label="MA50", color="orange")
    ax.plot(df['Date'], df['MA200'], label="MA200", color="red")
    
    ax.set_title("Moving Averages (MA50 & MA200)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate() 
    
    ax.grid(True)
    ax.legend()
    return fig

def plot_volume_trend(df):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df['Date'], df['Volume'], color='green', alpha=0.6)
    ax.set_title("Volume Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()

    ax.grid(True)
    return fig

def plot_macd(df):
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['Date'], df['MACD'], label='MACD', color='blue')
    ax.plot(df['Date'], df['Signal Line'], label='Signal Line', color='red')
    ax.set_title("MACD Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("MACD")

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()

    ax.grid(True)
    ax.legend()
    return fig

## Multiple Stock Analysis Functions

def get_multiple_stock_data(tickers, start_date, end_date):
    all_data = {}
    for ticker in tickers:
        data = get_stock_data(ticker, start_date, end_date)
        all_data[ticker] = data
    return all_data

def plot_multiple_stocks(all_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    for ticker, data in all_data.items():
        data_norm = data["Close"] / data["Close"].iloc[0]
        ax.plot(data['Date'], data_norm, label=ticker)
    ax.set_title("Multiple Stocks Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()
    ax.grid(True)
    ax.legend()
    return fig

def plot_multiple_volumes(all_data):
    fig, ax = plt.subplots(figsize=(10, 6))
    for ticker, data in all_data.items():
        ax.bar(data['Date'], data['Volume'], label=ticker, alpha=0.6)
    ax.set_title("Multiple Stocks Volume Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate()
    ax.grid(True)
    ax.legend()
    return fig