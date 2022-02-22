#!/usr/bin/env python3

from yfinance import Ticker
from pandas import set_option
import matplotlib.pyplot as plt
from click import argument,command,echo,group,launch,option,Path,secho

@group()
def cli():
  """"""

@cli.command()
@argument("ticker")
@option("-n","-noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def earnings(ticker,no_print,save_plot,plot,csv,excel):
  ticker_earnings=Ticker(ticker).earnings
  if not ticker_earnings.empty:
    if not no_print:
        echo(f"{ticker.upper()} Earnings")
        echo(ticker_earnings)
    if plot or save_plot: ticker_earnings.plot(title=f"{ticker.upper()} Earnings",kind="bar")
    if plot: plt.show()
    if save_plot: plt.savefig(save_plot)
    if csv: ticker_earnings.to_csv(csv)
    if excel: ticker_earnings.to_excel(excel)
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have earnings!""",fg="red")

@cli.command()
@argument("ticker")
@option("-n","-noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def history(ticker,no_print,save_plot,plot,csv,excel):
  ticker_history=Ticker(ticker).history()
  if not ticker_history.empty:
    if not no_print:
        echo(f"{ticker.upper()} History")
        echo(ticker_history)
    if plot or save_plot: ticker_history.Volume.plot(title=f"{ticker.upper()} Stock Volume",kind="bar")
    if plot: plt.show()
    if save_plot: plt.savefig(save_plot)
    if csv: ticker_history.to_csv(csv)
    if excel: ticker_history.to_excel(excel)
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have history!""",fg="red")

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

@cli.command()
@argument("ticker")
@option("-n","-noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def qearnings(ticker,no_print,save_plot,plot,csv,excel):
  ticker_qearnings=Ticker(ticker).quarterly_earnings
  if not ticker_qearnings.empty:
    if not no_print:
        echo(f"{ticker.upper()} Quarterly Earnings")
        echo(ticker_qearnings)
    if plot or save_plot: ticker_qearnings.plot(title=f"{ticker.upper()} Quarterly Earnings",kind="bar")
    if plot: plt.show()
    if save_plot: plt.savefig(save_plot)
    if csv: ticker_qearnings.to_csv(csv)
    if excel: ticker_qearnings.to_excel(excel)
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have quarterly earnings!""",fg="red")

if __name__=="__main__":
  set_option("display.max_rows",None)
  plt.ticklabel_format(style="plain")
  cli()
