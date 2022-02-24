#!/usr/bin/env python3

from json import dump as dump_json,load as load_json
# import json to save the settings

from yfinance import Ticker
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pandas import set_option as set_pandas_option
from click import argument,echo,group,launch,option,Path,secho
# import Ticker class from yfinance to get the data about tickers
# import plotting from matplotlib and params to custom the plot
# import set_option from pandas to set the number of rows to infinite
# import everything from click is needed to make this app

#define the cli and mark it as a group of commands
@group()
def cli():
  """"""

# create command for custom the options of the app
@cli.command()
@argument("option",required=False)
@argument("new_value",required=False)
def custom(option=None,new_value=None):

  """"""

  if option is None:
    for key,value in settings.items(): echo(f"""Setting "{key}" have the value of "{value}".""")
    # if no argument is given loop the settings and print the setting and value of it
  elif new_value is None: echo(f"""Setting "{option}" "{settings[option]}".""")
  # if a setting is given print the value of the given setting
  else:
    settings[option]=new_value
    # if a new value is given change the value of the option

    with open("settings.json","w") as f: dump_json(settings,f,indent=4)
    # update the settings

    echo(f"""Setting "{option} was changed to "{new_value}".""")
    # announce that the value was changed

# create command for getting the earnings of a ticker
@cli.command()
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def earnings(ticker,no_print,save_plot,plot,csv,excel):

  """"""

  # verify if earnings exists
  if not ((ticker_earnings:=Ticker(ticker).earnings).empty):
    if not no_print: echo(f"{ticker.upper()} Earnings\n{ticker_earnings}")
    # print the earnings if the user didn't disabled the printing

    if plot or save_plot: ticker_earnings.plot(title=f"{ticker.upper()} Earnings",kind="bar",logy=True,rot=0)
    # if the user wants plotting, load the plot

    if plot: plt.show()
    # if the user wants, show the plot

    if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)

    if csv: ticker_earnings.to_csv(csv,settings["csv_separator"])
    # save into a csv earnings if the user want this

    if excel: ticker_earnings.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel earnings if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have earnings!""",fg="red")
  # otherwise show an error that earnings didn't exists

# create command for getting the history of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def history(ticker,crypto,no_print,save_plot,plot,csv,excel):

  """"""

  ticker_object=Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)

  # verify if history exists
  if not ((ticker_history:=ticker_object.history()).empty):
    if not no_print: echo(f"{ticker.upper()} History\n{ticker_history}")
    # print the history if the user didn't disabled the printing

    if plot or save_plot:
      ticker_history.index=[str(i)[:10] for i in ticker_history.index]

      ticker_history.Volume.plot(title=f"{ticker.upper()} Stock Volume",kind="bar",logy=True)
  
    if plot: plt.show()
    # if the user wants, show the plot

    if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)

    if csv: ticker_history.to_csv(csv,settings["csv_separator"])
    # save into a csv history if the user want this

    if excel: ticker_history.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel history if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have history!""",fg="red")
  # otherwise show an error that history didn't exists

# create command for getting the market cap of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def mcap(ticker,crypto):

  """"""

  ticker_info=(Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)).info
  # save the info about the ticker in a dictionary

  try: mcap_value=f"""{ticker_info["marketCap"]:,}""".replace(",",settings["number_separator"])
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")
  else: echo(f"""Market cap of {ticker.upper()} is {mcap_value}$""")
  # try to acces the market cap and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

# create command for getting the news of a ticker
@cli.command()
@argument("ticker")
@option("-o","--open","_open",is_flag=True)
def news(ticker,_open):

  """"""

  for i,item in enumerate(Ticker(ticker).news,1):
    echo(f"""News {i}:\n\tTitle: {item["title"]}\n\tPublisher: {item["publisher"]}\n\tLink: {item["link"]}\n""")
    # loop the list with news and print each news

    if _open: launch(item["link"])
    # if user want open the news in the browser

# create command for getting the stock/price of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def stock(ticker,crypto):

  """"""

  ticker_info=(Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)).info
  # save the info about the ticker in a dictionary

  try: price=ticker_info["regularMarketPrice"] if crypto else ticker_info["currentPrice"]
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")
  else: echo(f"""{"Value" if crypto else "Stock"} of {ticker.upper()} is {price}$""")
  # try to acces the price and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

# create command for getting the quarterly earnings of a ticker
@cli.command()
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def qearnings(ticker,no_print,save_plot,plot,csv,excel):

  """"""

  # verify if quarterly earnings exists
  if not ((ticker_qearnings:=Ticker(ticker).quarterly_earnings).empty):
    if not no_print: echo(f"{ticker.upper()} Quarterly Earnings\n{ticker_qearnings}")
    # print the quarterly earnings if the user didn't disabled the printing

    if plot or save_plot: ticker_qearnings.plot(title=f"{ticker.upper()} Quarterly Earnings",kind="bar",logy=True,rot=0)
    # if the user wants plotting, load the plot

    if plot: plt.show()
    # if the user wants, show the plot

    if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)

    if csv: ticker_qearnings.to_csv(csv,settings["csv_separator"])
    # save into a csv quarterly earnings if the user want this

    if excel: ticker_qearnings.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel quarterly earnings if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have quarterly earnings!""",fg="red")
  # otherwise show an error that quarterly earnings didn't exists

# create command for getting the recommendations maded for a ticker
@cli.command()
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def recommendations(ticker,no_print,csv,excel):

  """"""

  # verify if recommendations exists
  if (ticker_recommendations:=Ticker(ticker).recommendations) is not None:
    if not no_print: echo(f"{ticker.upper()} Recommendations\n{ticker_recommendations}")
    # print the recommendations if the user didn't disabled the printing

    if csv: ticker_recommendations.to_csv(csv,settings["csv_separator"])
    # save into a csv recommendations if the user want this

    if excel: ticker_recommendations.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel recommendations if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have recommendations!""",fg="red")
  # otherwise show an error that recommendations didn't exists

# create command for getting the name of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def whois(ticker,crypto):

  """"""

  try: ticker_name=Ticker(f"{ticker}-usd").info["name"] if crypto else Ticker(ticker).info["shortName"]
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")
  else: echo(f"""Ticker: {ticker.upper()} is for {ticker_name}""")
  # try to acces the name of the ticker and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

if __name__=="__main__":
  set_pandas_option("display.max_rows",None)

  rcParams.update({"figure.autolayout": True})

  with open("settings.json","r") as f: settings=load_json(f)

  cli()#!/usr/bin/env python3

from json import dump as dump_json,load as load_json
# import json to save the settings

from yfinance import Ticker
import matplotlib.pyplot as plt
from matplotlib import rcParams
from pandas import set_option as set_pandas_option
from click import argument,echo,group,launch,option,Path,secho
# import Ticker class from yfinance to get the data about tickers
# import plotting from matplotlib and params to custom the plot
# import set_option from pandas to set the number of rows to infinite
# import everything from click is needed to make this app

#define the cli and mark it as a group of commands
@group()
def cli():
  """"""

# create command for custom the options of the app
@cli.command()
@argument("option",required=False)
@argument("new_value",required=False)
def custom(option=None,new_value=None):

  """"""

  if option is None:
    for key,value in settings.items(): echo(f"""Setting "{key}" have the value of "{value}".""")
    # if no argument is given loop the settings and print the setting and value of it
  elif new_value is None: echo(f"""Setting "{option}" "{settings[option]}".""")
  # if a setting is given print the value of the given setting
  else:
    settings[option]=new_value
    # if a new value is given change the value of the option

    with open("settings.json","w") as f: dump_json(settings,f,indent=4)
    # update the settings

    echo(f"""Setting "{option} was changed to "{new_value}".""")
    # announce that the value was changed

# create command for getting the earnings of a ticker
@cli.command()
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def earnings(ticker,no_print,save_plot,plot,csv,excel):

  """"""

  # verify if earnings exists
  if not ((ticker_earnings:=Ticker(ticker).earnings).empty):
    if not no_print: echo(f"{ticker.upper()} Earnings\n{ticker_earnings}")
    # print the earnings if the user didn't disabled the printing

    if plot or save_plot: ticker_earnings.plot(title=f"{ticker.upper()} Earnings",kind="bar",logy=True,rot=0)
    # if the user wants plotting, load the plot

    if plot: plt.show()
    # if the user wants, show the plot

    if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)

    if csv: ticker_earnings.to_csv(csv,settings["csv_separator"])
    # save into a csv earnings if the user want this

    if excel: ticker_earnings.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel earnings if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have earnings!""",fg="red")
  # otherwise show an error that earnings didn't exists

# create command for getting the history of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def history(ticker,crypto,no_print,save_plot,plot,csv,excel):

  """"""

  ticker_object=Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)

  # verify if history exists
  if not ((ticker_history:=ticker_object.history()).empty):
    if not no_print: echo(f"{ticker.upper()} History\n{ticker_history}")
    # print the history if the user didn't disabled the printing

    if plot or save_plot:
      ticker_history.index=[str(i)[:10] for i in ticker_history.index]

      ticker_history.Volume.plot(title=f"{ticker.upper()} Stock Volume",kind="bar",logy=True)
  
    if plot: plt.show()
    # if the user wants, show the plot

    if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)

    if csv: ticker_history.to_csv(csv,settings["csv_separator"])
    # save into a csv history if the user want this

    if excel: ticker_history.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel history if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have history!""",fg="red")
  # otherwise show an error that history didn't exists

# create command for getting the market cap of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def mcap(ticker,crypto):

  """"""

  ticker_info=(Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)).info
  # save the info about the ticker in a dictionary

  try: mcap_value=f"""{ticker_info["marketCap"]:,}""".replace(",",settings["number_separator"])
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")
  else: echo(f"""Market cap of {ticker.upper()} is {mcap_value}$""")
  # try to acces the market cap and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

# create command for getting the news of a ticker
@cli.command()
@argument("ticker")
@option("-o","--open","_open",is_flag=True)
def news(ticker,_open):

  """"""

  for i,item in enumerate(Ticker(ticker).news,1):
    echo(f"""News {i}:\n\tTitle: {item["title"]}\n\tPublisher: {item["publisher"]}\n\tLink: {item["link"]}\n""")
    # loop the list with news and print each news

    if _open: launch(item["link"])
    # if user want open the news in the browser

# create command for getting the stock/price of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def stock(ticker,crypto):

  """"""

  ticker_info=(Ticker(f"{ticker}-usd") if crypto else Ticker(ticker)).info
  # save the info about the ticker in a dictionary

  try: price=ticker_info["regularMarketPrice"] if crypto else ticker_info["currentPrice"]
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")
  else: echo(f"""{"Value" if crypto else "Stock"} of {ticker.upper()} is {price}$""")
  # try to acces the price and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

# create command for getting the quarterly earnings of a ticker
@cli.command()
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-p","--plot","plot",is_flag=True)
@option("-s","--saveplot","save_plot",type=Path())
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def qearnings(ticker,no_print,save_plot,plot,csv,excel):

  """"""

  # verify if quarterly earnings exists
  if not ((ticker_qearnings:=Ticker(ticker).quarterly_earnings).empty):
    if not no_print: echo(f"{ticker.upper()} Quarterly Earnings\n{ticker_qearnings}")
    # print the quarterly earnings if the user didn't disabled the printing

    if plot or save_plot: ticker_qearnings.plot(title=f"{ticker.upper()} Quarterly Earnings",kind="bar",logy=True,rot=0)
    # if the user wants plotting, load the plot

    if plot: plt.show()
    # if the user wants, show the plot

    if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)

    if csv: ticker_qearnings.to_csv(csv,settings["csv_separator"])
    # save into a csv quarterly earnings if the user want this

    if excel: ticker_qearnings.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel quarterly earnings if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have quarterly earnings!""",fg="red")
  # otherwise show an error that quarterly earnings didn't exists

# create command for getting the recommendations maded for a ticker
@cli.command()
@argument("ticker")
@option("-n","--noprint","no_print",is_flag=True)
@option("-c","--csv","csv",type=Path())
@option("-x","--excel","excel",type=Path())
def recommendations(ticker,no_print,csv,excel):

  """"""

  # verify if recommendations exists
  if (ticker_recommendations:=Ticker(ticker).recommendations) is not None:
    if not no_print: echo(f"{ticker.upper()} Recommendations\n{ticker_recommendations}")
    # print the recommendations if the user didn't disabled the printing

    if csv: ticker_recommendations.to_csv(csv,settings["csv_separator"])
    # save into a csv recommendations if the user want this

    if excel: ticker_recommendations.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
    # save into a excel recommendations if the user want this
  else: secho(f"""Ticker: "{ticker.upper()}" doesn't exists or doesn't have recommendations!""",fg="red")
  # otherwise show an error that recommendations didn't exists

# create command for getting the name of a ticker
@cli.command()
@argument("ticker")
@option("-y","--crypto","crypto",is_flag=True)
def whois(ticker,crypto):

  """"""

  try: ticker_name=Ticker(f"{ticker}-usd").info["name"] if crypto else Ticker(ticker).info["shortName"]
  except KeyError: secho(f"""Ticker: "{ticker.upper()}" doesn't exists!""",fg="red")
  else: echo(f"""Ticker: {ticker.upper()} is for {ticker_name}""")
  # try to acces the name of the ticker and print the value
  # if a error is occurred, announce the user that the ticker doesn't exists

if __name__=="__main__":
  set_pandas_option("display.max_rows",None)

  rcParams.update({"figure.autolayout": True})

  with open("settings.json","r") as f: settings=load_json(f)

  cli()
