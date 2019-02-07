from datetime import *
from statistics import mean
import calendar
import json, requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
matplotlib.use("agg")

#text formatting colours
blue = '\033[94m'
yellow = '\u001b[33m'
green = '\033[92m'
cyan = '\u001b[36m'
red = '\u001b[31m'
bold = '\033[1m'
underline = '\033[4m'
italics = '\033[3m'
f_end = '\033[0m'

#lists stablecoin symbols and currencies
stablecoin_array = ["BAY", "BITCNY", "BITUSD", "BTS", "COR", "DAI", "DGX", "GUSD", "EURS", "HAV", "NBT", "NUSD", "PAX", "STEEM", "SUSD", "TCX", "TUSD", "USDC", "USDT"]
currency_array = ["CNY", "EUR", "USD"]


#calculates how many days of pricing to extract from cryptocompare api
d = datetime.utcnow()
unixtime = calendar.timegm(d.utctimetuple())

date_format = '%Y-%m-%d'
datetime_unix_time = datetime.utcfromtimestamp(unixtime).strftime(date_format)
stasis_genesis_unix_timestamp = 1534982400
datetime_stasis_time = datetime.utcfromtimestamp(stasis_genesis_unix_timestamp).strftime(date_format)

a = datetime.strptime(str(datetime_stasis_time), date_format)
b = datetime.strptime(str(datetime_unix_time), date_format)

delta_days = (b - a).days
currency = currency_array[2]
ticker = stablecoin_array[2]
stasis_cryptocompare_ohlcv = "https://min-api.cryptocompare.com/data/histoday?fsym=" + ticker + "&tsym=" + currency + "&limit=" + str(delta_days)

cryptocompare_req = requests.get(stasis_cryptocompare_ohlcv)
cryptocompare_jsonified = cryptocompare_req.json()
pretty_print_cryptocompare = json.dumps(cryptocompare_jsonified, indent=2)
stasis_data_list = cryptocompare_jsonified.get('Data')

stasis_legacy = []

#compares closing price, opening price, daily high, daily low, and extracts the value furthest away from peg of EUR 1.00 for each day  
for l in range(len(stasis_data_list)):
	
	date_time = stasis_data_list[l]['time'] 
	
	close_value = stasis_data_list[l]['close']
	distance_to_1_at_close = abs(float(1) - close_value) 
	
	high_value = stasis_data_list[l]['high']
	distance_to_1_from_high = abs(float(1) - high_value) 
	
	open_value = stasis_data_list[l]['open']
	distance_to_1_at_open = abs(float(1) - open_value)
	
	low_value = stasis_data_list[l]['low']
	distance_to_1_from_low = abs(float(1) - low_value)

	highest_disparity = max(distance_to_1_at_close, distance_to_1_from_high, distance_to_1_at_open, distance_to_1_from_low)

	stasis_legacy.append(highest_disparity)

#create arrays to plot [x,y] variables
x_axis = list(range(0, delta_days + 1))
y_axis = stasis_legacy

#numpy arrays with explicit datatypes
xs = np.array(x_axis, dtype=np.float64)
ys = np.array(y_axis, dtype=np.float64)

# best fit slope for traditional straight line equation y = mx + b equation, where m is the gradient and b is the y-intercept
def best_fit_slope_and_intercept(xs, ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    return m, b

m, b = best_fit_slope_and_intercept(xs,ys)

print(f'\nThe equation of the best-fit line for {ticker} is \n y = {yellow + str(m) + f_end}x {blue + str(b) + f_end}')

#plot linear best-fit regression line
regression_line = []
for x in xs:
	regression_line.append((m*x) + b)

#allows creationg of graph visuals
style.use('ggplot')

# plots regression line of scatter graph of stasis historical prices and saves output as .png
plt.scatter(xs, ys, color = '#003F72', label = 'data')
plt.plot(xs, regression_line, label='regression line')
plt.title('Stability Index')

# use regression line to predict tomorrow's stasis price and plot this additional data point
predict_x = x_axis[-1] + 1
predict_y = (m * predict_x) + b
print(f'\nThe prediction for {ticker} tomorrow as per Linear Regression is: \n {green}{currency} {str(1 + predict_y)} {f_end}')
plt.scatter(predict_x,predict_y, color = 'g', label='predicted')
plt.legend(loc=4)
plt.savefig('regression_scatter.png', bbox_inches='tight')
#plt.show()

# method returns the distance squared between each of the y coordinates plotted and the regression line
def squared_error(ys_orig, ys_line):
    return sum((ys_line - ys_orig)**2)

# method that returns a r-squared value that reflects how much better the regression line is relative to a horizontal average of all the y coordinates 
# the closer the r-squared value is to 1, the better the fit of the regression line to the actual data points)
def coefficient_of_determination(ys_orig, ys_line):
    y_mean_line = [mean(ys_orig) for y in ys_orig]
    squared_error_regr = squared_error(ys_orig, ys_line)
    squared_error_y_mean = squared_error(ys_orig, y_mean_line)
    return 1 - (squared_error_regr/squared_error_y_mean)

r_squared = coefficient_of_determination(ys, regression_line)

print(f'\nThe suitability of the Linear Regression model {yellow}(Y = mX + C) {f_end}as the {yellow}"Coefficient of Determination"{f_end} for{blue} {ticker}\'s{f_end} Best-Fit Line is: \n {blue + str(r_squared) + f_end} \n(as per {italics}"R-squared"{f_end})\n')