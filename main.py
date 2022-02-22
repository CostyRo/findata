#!/usr/bin/env python3

from yfinance import Ticker
from pandas import set_option
from click import argument,command,echo,group,launch,option,secho

@group()
def cli():
  """"""

@cli.command()
@argument("ticker")
@option("-c","--crypto","crypto",is_flag=True)
@option("-f","--format","_format",is_flag=True)
def mcap(ticker,crypto,_format):
  ticker_object=Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)
  ticker_info=ticker_object.info
  try:
    market_cap=f"""{ticker_info["marketCap"]:,}""".replace(","," ") if _format else ticker_info["marketCap"]
    echo(f"""Market cap of {ticker.upper()} is {market_cap}$""")
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")

@cli.command()
@argument("ticker")
@option("-o","--open","_open",is_flag=True)
def news(ticker,_open):
  for i,item in enumerate(Ticker(ticker).news):
    echo(f"""News {i+1}:\n\tTitle: {item["title"]}\n\tPublisher: {item["publisher"]}\n\tLink: {item["link"]}\n""")
    if _open: launch(item["link"])

@cli.command()
@argument("ticker")
@option("-c","--crypto","crypto",is_flag=True)
def stock(ticker,crypto):
  ticker_object=Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)
  ticker_info=ticker_object.info
  try:
    price=ticker_info["regularMarketPrice"] if crypto else ticker_info["currentPrice"]
    echo(f"""{"Value" if crypto else "Stock"} of {ticker.upper()} is {price}$""")
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")

if __name__=="__main__":
  pd.set_option("display.max_rows",None)
  cli()
