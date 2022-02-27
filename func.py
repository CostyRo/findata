from click import echo,secho
import matplotlib.pyplot as plt
# import echo from click to display messages
# import plotting from matplotlib

# function for showing and saving the plot of the data frame
def plotting(plot,save_plot):
  """"""

  if plot: plt.show()
  # if the user wants, show the plot

  if save_plot: plt.savefig(f"{save_plot}.svg",format="svg",dpi=1200)
  # if the user wants, save the plot as a svg file

def print_error(text):

  """"""

  secho(text,fg="red")

# function for printing the data frame
def print_frame(ticker,no_print,data_frame,title):
  """"""

  if not no_print: echo(f"{ticker.upper()} {title}\n{data_frame}")
  # if the user didn't disable the printing, print the earnings

# function for saving the data frame in different formats
def save_frame(data_frame,csv,excel,csv_separator):
  """"""

  if csv: data_frame.to_csv(csv,csv_separator)
  # if the user wants, save earnings into a csv

  if excel: data_frame.to_excel(excel if excel.endswith(".xlsx") else excel+".xlsx")
  # if the user wants, save earnings into a excel
