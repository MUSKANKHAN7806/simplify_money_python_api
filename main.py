from fastapi import FastAPI, HTTPException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
import yfinance as yf
import os

# Load API Keys
GEMINI_API_KEY = "AIzaSyC0pobVS-Jdx6cX1HfETGFgPi_qT8zmykw"

# Initialize FastAPI app
app = FastAPI()

# Initialize LLM (Gemini via LangChain)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY)

# Stock Price Fetching Function
def fetch_stock_data(ticker: str) -> str:
    """Fetches stock details including price, volume, and valuation metrics using Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        latest_price = info.get("currentPrice", "N/A")
        previous_close = info.get("previousClose", "N/A")
        day_high = info.get("dayHigh", "N/A")
        day_low = info.get("dayLow", "N/A")
        year_high = info.get("fiftyTwoWeekHigh", "N/A")
        year_low = info.get("fiftyTwoWeekLow", "N/A")
        volume = info.get("volume", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        
        stock_summary = f"""
        Ticker: {ticker.upper()}
        Current Price: ${latest_price}
        Previous Close: ${previous_close}
        Day High: ${day_high}, Day Low: ${day_low}
        52-Week High: ${year_high}, 52-Week Low: ${year_low}
        Volume: {volume}
        Market Cap: {market_cap}
        P/E Ratio: {pe_ratio}
        """

        return stock_summary.strip()
    
    except Exception as e:
        return f"Error fetching stock data: {str(e)}"

stock_tool = Tool(
    name="Stock Data Fetcher",
    func=fetch_stock_data,
    description="Fetch latest stock price, volume, valuation metrics, and performance indicators using Yahoo Finance. Useful for making buy/sell/hold decisions."
)

# Initialize Agent
agent = initialize_agent(
    tools=[stock_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# ticker = "TSLA"
# query = f"""
# Analyze the stock {ticker} based on the provided financial data.
# Consider its historical trends, valuation, and market conditions.
# Give a well-justified Buy, Sell, or Hold recommendation.
# """
# response = agent.run(query)
# print({"ticker": ticker, "advice": response})

@app.get("/")
def home():
    return "Server started"

@app.get("/stock/{ticker}")
def get_stock_price(ticker: str):
    try:
        query = f"latest stock data of {ticker}"
        response = agent.run(query)
        return {"ticker": ticker, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/advice/{ticker}")
def get_stock_advice(ticker: str):
    try:
        query = f"""
        Analyze the stock {ticker} based on the provided financial data.
        Consider its historical trends, valuation, and market conditions.
        Give a well-justified Buy, Sell, or Hold recommendation.
        """
        response = agent.run(query)
        return {"ticker": ticker, "advice": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
