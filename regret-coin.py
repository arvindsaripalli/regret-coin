import requests
import json
import datetime
import sys

def get_current_rate():
	current_price = 'https://api.coindesk.com/v1/bpi/currentprice.json'
	
	response = requests.get(current_price)
	data = json.loads(response.content)
 
	# Clean returned rate of comma
	rate = data['bpi']['USD']['rate'].split(",")
	if(len(rate) > 1):
		rate = rate[0] + rate[1]
	else:
		rate = rate[0]

	return float(rate)

def get_historical_rate(year, month, day):
	time = str(year) + "-" + str(month) + "-" + str(day)
	historical_price = 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + time + '&end=' + time
	
	response = requests.get(historical_price)
	data = json.loads(response.content)

	# Historical price is returned as a float instead of string by
	# the api for some reason (inconsistent with above)
	rate = data['bpi'][time]

	return float(rate)


def main():
	while(True):
		now = datetime.datetime.now()
		now_year = now.year
		now_month = now.month
		now_day = now.day 

		year_cap = 2010
		month_cap = 07
		day_cap = 17

		invested = float(raw_input("If I had invested: \n"))
		print("USD into bitcoin on: \n")
		
		year = int(raw_input("year: "))
		month = int(raw_input("month: "))
		day = int(raw_input("day: "))

		# Check if supplied dates preceed bitcoin
		if(year < year_cap):
			print("Error. Date supplied preceeds bitcoin. \n")
			continue
		elif(year == year_cap and month < month_cap):
			print("Error. Date supplied preceeds bitcoin. \n")
			continue
		elif(year == year_cap and month == month_cap and day < day_cap):
			print("Error. Date supplied preceeds bitcoin. \n")
			continue

		# Check if supplied dates are greater than present time
		if(year > now_year):
			print("Error. Future date supplied. \n")
			continue
		elif(year == now_year and month > now_month):
			print("Error. Future date supplied. \n")
			continue
		elif(year == now_year and month == now_month and day > now_day):
			print("Error. Future date supplied. \n")
			continue

		# Check if supplied dates are valid dates
		if(day < 1):
			print("Error. Invalid date supplied. \n")
			continue
		elif(month < 1):
			print("Error. Invalid date supplied. \n")
			continue

		# Add leading 0s to supplied month and day if single digit
		if(month / 10 == 0):
			month = "0" + str(month)

		if(day / 10 == 0):
			day = "0" + str(day)

		# Get current and historical bitcoin rates
		current_rate = get_current_rate()
		historical_rate = get_historical_rate(year, month, day)

		print("\nI would currently have: \n")
		print(str(current_rate * (invested / historical_rate)) + " USD")
		sys.exit()
main()
