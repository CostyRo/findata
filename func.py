from click import echo
import matplotlib.pyplot as plt
# import echo from click to display messages

# function for showing and saving the plot
def plotting(plot,save_plot):
  """"""

  if plot: plt.show()
  # if the user wants, show the plot

  if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)
  # if the user wants, save the plot as a svg file

# function for printing a data frame
def print_frame(ticker,no_print,data_frame,title):
  """"""

  if not no_print: echo(f"{ticker.upper()} {title}\n{data_frame}")
  # if the user didn't disable the printing, print the earnings

def save_frame():
  """"""
