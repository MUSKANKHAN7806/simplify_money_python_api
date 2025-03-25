# Stock Market AI Agent

## Description

This project implements an AI-powered stock market agent using FastAPI, LangChain, Gemini and Yahoo Finance (yfinance). The agent can:

* Fetch the latest stock market data for a given ticker.

* Analyze stock data and provide a Buy/Sell/Hold recommendation with a valid justification

* Expose APIs accessible via cURL, Postman, or any HTTP client.

## Technologies Used
* FastAPI: Web framework for API development.

* LangChain: Framework for integrating LLMs with external tools.

* Google Gemini API: Used as the LLM for analyzing stock data.

* Yahoo Finance (yfinance): Fetches real-time stock market data

## Workflow Summary
1. User makes an API request to `/stock/{ticker}` or `/stock/advice/{ticker}`.

2. FastAPI processes the request and extracts the stock ticker.

3. Yahoo Finance fetches stock details.

4. If `/stock/advice/{ticker}` is requested:

    * LangChain AI Agent analyzes stock data (using gemini as LLM).

    *  AI generates a Buy/Sell/Hold recommendation.

7. FastAPI returns the response as JSON.

## Deployment   

The project is deployed on Render with the following base URL.

*NOTE: Sometimes render displays 502 error because they down the webservice when it is not been used within an hour*

[https://simplify-money-python-api.onrender.com/](https://simplify-money-python-api.onrender.com/)

## API Endpoints

### 1. Home
* URL: `/`
* Method: `GET`
* Example: 
```curl
curl -X GET https://simplify-money-python-api.onrender.com/
```
* Response:
```json
{ "message": "Server started" }
```

### 2. Fetch Stock Data
* URL: `/stock/{ticker}`
* Method: GET
* Example: 
```curl
curl -X GET https://simplify-money-python-api.onrender.com/stock/MSFT
```
* Response:
```json
{
"ticker": "MSFT",
"response": "The latest stock data for MSFT is: Current Price: $393.08, Previous Close: $391.26, Day High: $395.4, Day Low: $389.81, 52-Week High: $468.35, 52-Week Low: $376.91, Volume: 20,132,071, Market Cap: $2,922,148,790,272, P/E Ratio: 31.65.  Note that these values are approximate and based on the output of the Stock Data Fetcher at the time of execution."
}
```

### 3. Stock Advice Endpoint
* URL: `/stock/advice/{ticker}`
* Method: GET
* Example: 
```curl
curl -X GET https://simplify-money-python-api.onrender.com/stock/advice/MSFT
```
* Response:
```json
{
"ticker": "MSFT",
"advice": "Hold.  The current price of MSFT is below its 52-week high but above its 52-week low.  However, the relatively high P/E ratio suggests the stock may be overvalued.  Therefore, a \"Hold\" recommendation is appropriate based on the limited data provided.  Further analysis incorporating market conditions and future earnings projections would be beneficial for a more informed decision."
}
```

## Setup & Installation
### Prerequisites
**Ensure you have Python 3.8+ installed.**

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Running the Server
Start the FastAPI server using Uvicorn:
```powershell
python -m uvicorn main:app --host localhost --port 8000
```
The server will be accessible at: `http://localhost:8000/`

### Project Structure
```curl
/stock_market_agent
│── main.py        # Main FastAPI application with LangChain integration
│── requirements.txt  # Python dependencies
│── README.md      # Documentation
```




