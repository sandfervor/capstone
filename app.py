from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
import numpy as np

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped text-sm text-lg-normal'})

#scraping data of "Date"
table.find_all('th', attrs={'class':'font-semibold text-center'})[:5]
table.find_all('th', attrs={'class':'font-semibold text-center'})[0].text
row = table.find_all('th', attrs={'class':'font-semibold text-center'})

#fingding row_length of "Date"
row_length = len(row)
row_length

#scraping data of marketcap, volume, open and close
table.find_all('td', attrs={'class':'text-center'})[0:5]
stock = table.find_all('td', attrs={'class':'text-center'})

#check stock_length
stock_length = len(stock)
stock_length


temp = [] #init
for i in range(0, row_length):
    
    #get date 
    date = row[i].text
 
    #get market_cap
    x0 = i * 4
    market_cap = stock[x0].text.strip()
        
    #get volume
    x1 = (i * 4)+1
    volume = stock[x1].text.strip() 
        
    #get open
    x2 = (i * 4)+2
    open_info = stock[x2].text.strip()
    
    #get close
    x3 = (i * 4)+3
    close_info = stock[x3].text.strip()

    temp.append((date,market_cap,volume,open_info,close_info))

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','market_cap','volume','open','close'))

#insert data wrangling here
eth = df.copy()
eth.dtypes

eth['date'] = eth['date'].astype('datetime64')

eth['market_cap'] = eth['market_cap'].str.replace("$","")
eth['market_cap'] = eth['market_cap'].str.replace(",","")
eth['market_cap'] = eth['market_cap'].astype("float64")

eth['volume'] = eth['volume'].str.replace("$","")
eth['volume'] = eth['volume'].str.replace(",","")
eth['volume'] = eth['volume'].astype("float64")

eth['open'] = eth['open'].str.replace("$","")
eth['open'] = eth['open'].str.replace(",","")
eth['open'] = eth['open'].astype("float64")

eth['close'] = eth['close'].str.replace("$","")
eth['close'] = eth['close'].str.replace(",","")
eth['close']= eth['close'].replace('N/A',np.NaN) # to handle "N/A" by change as missing value
eth['close'] = eth['close'].astype("float64")

eth = eth.set_index('date')




#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'${eth["volume"].mean().round(0):,.0f}' #be careful with the " and ' 

	# generate plot
	ax = eth[['volume']].plot(figsize = (20,9)) 
		
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)