#!/usr/bin/env python3

from yfinance import Ticker
from click import argument,command,echo,group,option,secho

@group()
def cli():
    """"""

@cli.command()
@argument("ticker")
def mcap(ticker):
  ticker_object=Ticker(ticker)
  ticker_info=ticker_object.info
  if ticker_info["longName"] is not None: echo(f"""Market cap of {ticker_info["longName"]}({ticker_object.ticker}) is {ticker_info["marketCap"]}$""")
  else: secho(f"""Ticker: "{ticker}" doesn't exists!""",fg="red")

if __name__=="__main__": cli()
