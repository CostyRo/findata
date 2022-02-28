#!/usr/bin/env python3

from json import dump as dump_json,load as load_json
# import json to save the settings

from yfinance import Ticker
from matplotlib import rcParams
from pandas import set_option as set_pandas_option
from click import argument,echo,group,launch,option,Path
# import Ticker class from yfinance to get the data about tickers
# import params from matplotlib to custom the plot
# import set_option from pandas to set the number of rows to infinite
# import everything is needed from click to make this app

from func import plotting,print_error,print_frame,save_frame
# import necessary functions from my function module

#define the cli and mark it as a group of commands
@group()
def cli():
  """
  A simple app for getting the financial data from yahoo finance
  """

# create the command for custom the options of the app
@cli.command(short_help="Custom the varibles of the app")
@argument("option",required=False)
@argument("new_value",required=False)
def custom(option=None,new_value=None):

  """
  Custom the varibles of the app

  OPTION is the option that you want to change
  NEW_VALUE is the new value for the given option

  No NEW_VALUE will print the value of the OPTION
  No OPTION will print all the option and their values
  """

  if option is None:
    for key,value in settings.items(): echo(f"""Setting "{key}" have the value of "{value}".""")
    # if no argument is given, loop the settings and print the setting and the value of it
  elif new_value is None: echo(f"""Setting "{option}" have value of "{settings[option]}".""")
  # if a setting is given, print the value of the given setting
  else:
    settings[option]=new_value
    # if a new value is given, change the value of the option

    with open("settings.json","w") as f: dump_json(settings,f,indent=4)
    # update the settings

    echo(f"""Setting "{option} was changed to "{new_value}".""")
    # announce user that the value was changed

# create the command for getting the earnings of a ticker
@cli.command(short_help="Get the earnings of a company")
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def earnings(ticker,no_print,plot,save_plot,csv,excel):

  """
  Get the earnings of a company

  TICKER is the ticker that you want to track
  NOPRINT is for disable the printing of the data
  PLOT is for plotting the data
  SAVEPLOT is for saving the plot as a svg image
  CSV is for saving the data in a csv file
  EXCEL is for saving the data in a excel file
  """

  # verify if earnings exists
  if not ((ticker_earnings:=Ticker(ticker).earnings).empty):
    print_frame(ticker,no_print,ticker_earnings,"Earnings")
    # print what is needed

    if plot or save_plot: ticker_earnings.plot(title=f"{ticker.upper()} Earnings",kind="bar",logy=True,rot=0)
    # if the user wants plotting, load the plot

    plotting(plot,save_plot)
    # handle plotting commands

    save_frame(ticker_earnings,csv,excel,settings["csv_separator"])
    # handle saving commands
  else: print_error(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have earnings!""")
  # otherwise show an error that earnings didn't exists

# create the command for getting the history of a ticker
@cli.command(short_help="Get the history of a company or a cryptocurrency")
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def history(ticker,crypto,no_print,plot,save_plot,csv,excel):

  """
  Get the history of a company or a cryptocurrency

  TICKER is the ticker that you want to track
  CRYPTO is for enable the tickers for cryptocurrencies
  NOPRINT is for disable the printing of the data
  PLOT is for plotting the data
  SAVEPLOT is for saving the plot as a svg image
  CSV is for saving the data in a csv file
  EXCEL is for saving the data in a excel file
  """

  ticker_history=(Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)).history()
  # save the history about the ticker in a dictionary

  # verify if history exists
  if not ticker_history.empty:
    print_frame(ticker,no_print,ticker_history,"History")
    # print what is needed

    # if the user wants plotting, load the plot
    if plot or save_plot:
      ticker_history.index=[str(i)[:10] for i in ticker_history.index]
      # update the index column with the shorter version of the time

      ticker_history.Volume.plot(title=f"{ticker.upper()} Stock Volume",kind="bar",logy=True)
      # load only the column with volume as a plot

    plotting(plot,save_plot)
    # handle plotting commands

    save_frame(ticker_history,csv,excel,settings["csv_separator"])
    # handle saving commands
  else: print_error(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have history!""")
  # otherwise show an error that history didn't exists

# create the command for getting the market cap of a ticker
@cli.command(short_help="Get the market cap of a company or a cryptocurrency")
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def mcap(ticker,crypto):

  """
  Get the market cap of a company or a cryptocurrency

  CRYPTO is for enable the tickers for cryptocurrencies
  """

  ticker_info=(Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)).info
  # save the info about the ticker in a dictionary

  try: mcap_value=f"""{ticker_info["marketCap"]:,}""".replace(",",settings["number_separator"])
  except KeyError: print_error(f"""Ticker: "{ticker.upper()}" doesn't exists!""")
  else: echo(f"""Market cap of {ticker.upper()} is {mcap_value}$""")
  # try to acces the market cap and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

# create the command for getting the news of a ticker
@cli.command(short_help="Get the financial news for the given word")
@argument("ticker")
@option("-o","--open","_open",is_flag=True)
def news(ticker,_open):

  """
  Get the financial news for the given word

  OPEN is for opening the news in the default browser
  """

  for i,item in enumerate(Ticker(ticker).news,1):
    echo(f"""News {i}:\n\tTitle: {item["title"]}\n\tPublisher: {item["publisher"]}\n\tLink: {item["link"]}\n""")
    # loop the list with news and print each news

    if _open: launch(item["link"])
    # if user want open the news in the browser

# create the command for getting the stock/price of a ticker
@cli.command(short_help="Get the price of a stock or the price of a cryptocurrency")
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def stock(ticker,crypto):

  """
  Get the price of a stock or the price of a cryptocurrency

  CRYPTO is for enable the tickers for cryptocurrencies
  """

  ticker_info=(Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)).info
  # save the info about the ticker in a dictionary

  try: price=ticker_info["regularMarketPrice"] if crypto else ticker_info["currentPrice"]
  except KeyError: print_error(f"""Ticker: "{ticker.upper()}" doesn't exists!""")
  else: echo(f"""{"Value" if crypto else "Stock"} of {ticker.upper()} is {price}$""")
  # try to acces the price and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

# create the command for getting the quarterly earnings of a ticker
@cli.command(short_help="Get the quarterly earnings of a company")
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def qearnings(ticker,no_print,plot,save_plot,csv,excel):

  """
  Get the quarterly earnings of a company

  TICKER is the ticker that you want to track
  NOPRINT is for disable the printing of the data
  PLOT is for plotting the data
  SAVEPLOT is for saving the plot as a svg image
  CSV is for saving the data in a csv file
  EXCEL is for saving the data in a excel file
  """

  # verify if quarterly earnings exists
  if not ((ticker_qearnings:=Ticker(ticker).quarterly_earnings).empty):
    print_frame(ticker,no_print,ticker_qearnings,"Quarterly Earnings")
    # print what is needed

    if plot or save_plot: ticker_qearnings.plot(title=f"{ticker.upper()} Quarterly Earnings",kind="bar",logy=True,rot=0)
    # if the user wants plotting, load the plot

    plotting(plot,save_plot)
    # handle plotting commands

    save_frame(ticker_qearnings,csv,excel,settings["csv_separator"])
    # handle saving commands
  else: print_error(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have quarterly earnings!""")
  # otherwise show an error that quarterly earnings didn't exists

# create the command for getting the recommendations maded for a ticker
@cli.command(short_help="Get the recommendations of a company or a cryptocurrency")
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def recommendations(ticker,no_print,csv,excel):

  """
  Get the recommendations of a company or a cryptocurrency

  TICKER is the ticker that you want to track
  NOPRINT is for disable the printing of the data
  CSV is for saving the data in a csv file
  EXCEL is for saving the data in a excel file
  """

  # verify if recommendations exists
  if (ticker_recommendations:=Ticker(ticker).recommendations) is not None:
    print_frame(ticker,no_print,ticker_recommendations,"Recommendations")
    # print what is needed

    save_frame(ticker_recommendations,csv,excel,settings["csv_separator"])
    # handle saving commands
  else: print_error(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have recommendations!""")
  # otherwise show an error that recommendations didn't exists

# create the command for getting the name of a ticker
@cli.command(short_help="Identify the company or the cyptocurrency for a ticker")
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def whois(ticker,crypto):

  """
  Identify the company or the cyptocurrency for a ticker

  CRYPTO is for enable the tickers for cryptocurrencies
  """

  try: ticker_name=Ticker(f"{ticker}-usd").info["name"] if crypto else Ticker(ticker).info["shortName"]
  except KeyError: print_error(f"""Ticker: "{ticker.upper()}" doesn't exists!""")
  else: echo(f"""Ticker: {ticker.upper()} is for {ticker_name}""")
  # try to acces the name of the ticker and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

if __name__=="__main__":
  set_pandas_option("display.max_rows",None)
  # set the displayed rows to infinite

  rcParams.update({"figure.autolayout": True})
  # set autolayout to true to display the ploy correctly

  with open("settings.json","r") as f: settings=load_json(f)
  # load the settings in a dictionary

  cli()
  # start the cli app
