from click import echo
# import echo from click to display messages

def plotting():
  """"""

# function for printing a data frame
def print_frame(ticker,no_print,data_frame,title):
  """"""

  if not no_print: echo(f"{ticker.upper()} {title}\n{data_frame}")
  # if the user didn't disable the printing, print the earnings

def saving_file():
  """"""
