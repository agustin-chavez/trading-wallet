import yfinance as yf

from app.tickers.model import Ticker
from app import db

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "JPM", "V", "PG", "CSCO",
           "INTC", "IBM", "NFLX", "NVDA", "GS", "DIS", "C", "BA", "WMT", "T",
           "XOM", "CVX", "KO", "PEP", "JNJ", "MRK", "PFE", "ABBV", "GILD", "MMM",
           "HON", "CAT", "GE", "UNH", "VZ", "PYPL", "BAC", "MCD", "AMGN", "QCOM",
           "WFC", "CMCSA", "HD", "ORCL", "SBUX", "AMAT", "MDT", "TXN", "NKE",
           "TMO", "AVGO", "PYPL", "GSK", "BP", "AZN", "NVO", "TSM", "TM",
           "BABA", "WBA", "CRM", "FDX", "F", "GM", "EBAY", "AMD", "ADBE",
           "IBM", "AXP", "COST", "LMT", "BA", "UPS", "FDX", "GD", "COP", "MA",
           "INTU", "AMD", "PDD", "JD", "SE", "BILI", "NTES", "AMAT", "NOW", "ASML",
           "NET", "PLTR", "ZM", "SQ", "ROKU", "NIO", "SPCE", "AAPL", "TSLA"]


def init_yf_snapshot():
    if len(Ticker.query.all()) == 0:
        print('Creating Yahoo Finance snapshot...')
        for symbol in tickers:
            try:
                ticker = yf.Ticker(symbol)
                if ticker:
                    name = ticker.info.get('longName')
                    price = ticker.info.get('currentPrice')
                    stocks = ticker.info.get('volume')
                    if not name or not price or not stocks:
                        raise Exception(f'No data for ticker {symbol}', ticker.info)
                    new_ticker = Ticker(
                        symbol=symbol, name=name, price=price, stocks=stocks
                    )
                    db.session.add(new_ticker)
                    db.session.commit()
            except Exception as e:
                print(f'Unable to get ticker {symbol} from Yahoo Finance API. ', e)
