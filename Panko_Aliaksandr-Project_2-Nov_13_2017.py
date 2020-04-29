# Python 2.7 Windows 7

#1. Write a python program that prompts the user to choose
#   any five stock exchanges of the world
#   (whose data is available on Yahoo Finance)
#   
#2. For each such market, let the program automatically choose the relevant
#   Market Index (say S&P500 for USA, CNXNIFTY for India etc)
#   
#3. Download data for the last 10 years for each of the Indices.
#
#4. Calculate Correlation Coefficients of monthly returns between
#   each pair of indices
#   
#5. Plot the results in a suitable graphical format that represents the trends
#   in the data and their interdependence
#   
#6. Write a paragraph about your analysis of the results and
#   the inferences that can be drawn from it.


import datetime
import pandas as pd
from pandas_datareader import data as pdr
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

class WorldCorrelation:
    
    # Constructor
    def __init__(self):
        
        self.__df_hist_data = pd.DataFrame()
        self.__monthly_returns = pd.DataFrame()
        self.__corrma = self.__df_hist_data.corr()
        self.__exch_names = list()
        
    def DownloadData(self):
        
        # File contains world exchanges
        df = pd.read_csv('my data.csv')
        print(df.Exchange)
        print("\nChoose 5 exchanges from the list. Input appropriate indices...")
        
        # List of chosen exchanges
        exchange_numbers = list()
        
        # User Input
        while(len(exchange_numbers) < 5):       
                exchange_number = raw_input()
                # Index must be a digit
                if exchange_number.isdigit() == False:
                    print "Enter a digit between 0 and 17"
                    continue
                
                exchange_number = eval(exchange_number)
                
                # Between 0 and last available exchange
                if(exchange_number < 0 or exchange_number > len(df.Exchange)-1):
                    print ("Choose index between 0 and 17")
                # To provide correlation date duplicates are adverse    
                elif (exchange_number in exchange_numbers):
                    print "This stock exchange has already been selected. Choose another one"
                else:
                    exchange_numbers.append(exchange_number) 
                    
        # Find indices tickers
        df_tickers = df.loc[exchange_numbers]
        tickers = df_tickers.Symbol.values
        self.__exch_names = df_tickers.Economy.values
        print(tickers)
        
        # Download historical data from Yahoo Finance
        # Determine the first and the last days of the period
        # Cat first and last months because they contain biased data
        end_date = datetime.date(2017,10,31)
        start_date = datetime.date(end_date.year-10, end_date.month , end_date.day)
        
        for i in range(len(exchange_numbers)):
            try:
                df_index = pdr.get_data_yahoo(tickers[i], start = start_date, end = end_date)
                df_index = df_index.Close
                self.__df_hist_data =  pd.concat([self.__df_hist_data,df_index], axis = 1)
            except RemoteDataError:
                # handle error
                print 'Stock symbol "{}" is not valid'.format(tickers[i])
        
        # Add colomn names. Without loss of generality exhcange names are used
        self.__df_hist_data.columns = self.__exch_names
        
        
        # Dates should be adjusted because last and current months may contain
        # less days then others
        start_date = df_index.index[0]
        end_date = df_index.index[len(df_index)-1]
        start_date_adj = start_date + relativedelta(months=1)
        start_date_adj = datetime.date(start_date.year, start_date.month, 1)
        end_date_adj = datetime.date(end_date.year, end_date.month, 1)
        
        # Cut dates
        df_index =  df_index[ df_index.index.date >= start_date_adj]
        df_index =  df_index[ df_index.index.date < end_date_adj]


    def CalculateReturnsCorr(self):
        # Required to calculate monthly returns
        def total_return_from_returns(returns):
            return (returns + 1).prod() - 1
        
        # daily returns
        day_returns = self.__df_hist_data.pct_change(1)
        # Calculate monthly returns
        self.__monthly_returns = day_returns.groupby((day_returns.index.year, day_returns.index.month))\
                                              .apply(total_return_from_returns)
                                      
        # Data contains NA
        self.__df_hist_data = self.__df_hist_data.dropna()

        # Calculate correlation matrix
        self.__corrma = self.__df_hist_data.corr()
        
    def PlotCorr(self):
        
        # Plot a Heatmap for correlation matrix
        fig = plt.figure()
        ax = fig.add_subplot(111)
        im = ax.matshow( self.__corrma, interpolation = 'nearest')
        fig.colorbar(im)
        self.__exch_names = self.__exch_names.tolist()
        ax.set_xticklabels([''] + self.__exch_names, rotation=90)
        ax.set_yticklabels([''] + self.__exch_names)
        plt.show()
         
        pd.scatter_matrix(self.__monthly_returns, alpha=0.2, figsize=(6, 6),
                          diagonal='kde')
        

    # Main function
    def Main(self):
        # User input
        self.DownloadData()
        # Process data
        self.CalculateReturnsCorr()
        # Plot results
        self.PlotCorr()
        
# ------------------ End of Class ----------------------------------------
        
# Create the instance of a class
world_correlation = WorldCorrelation()
                                         
# Call Main function of a class
world_correlation.Main()
        


