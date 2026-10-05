from dotenv import load_dotenv
import os
import requests
import datetime
#One day, a live updated graph of performance of my trading journal. that updates per journal entry.
load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

headers = {
	"Authorization": f"Bearer {NOTION_TOKEN}",
	"Notion-Version": "2022-06-28",
	"Content-Type": "application/json"
}
# The data format is Notion specific. They require that.
# properties is the name of the dictionary.
# Pair property, for our database.
# Pair = column name
# title = What type of column it is --> value is a list --> each item is a dict with 'text'
# content = holds the string that goes into the cell.
# Notion pattern - Column name is the key, value is a dict with the type, whose inner key is the actual data.
url = "https://api.notion.com/v1/pages"

class Trade:
	def __init__(self, pair, result, direction, risk_amount, session):
		self.pair = pair
		self.result = result
		self.direction = direction
		self.risk_amount = risk_amount
		self.session = session
		self.timestamp = datetime.datetime.now()

class Account:
	def __init__(self, balance):
		self.balance = balance
		self.trade_history = []

	def log_trade(self, trade):
		self.trade_history.append(trade)
		self.balance += trade.result
		send_trade_to_notion(trade)
# self explained - log_trade is defined inside Account class. Self refers to the Account object
# that called it. Not Trader or Trade.
class Trader:
	def __init__(self, name):
		self.name = name
		self.account = Account(1000)

	def place_trade(self, pair, result, direction, risk_amount, session):
		trade = Trade(pair, result, direction, risk_amount, session)
		self.account.log_trade(trade)

def send_trade_to_notion(trade):
	data = {"parent": {"database_id": NOTION_DATABASE_ID},
	        "properties": {
				"Pair": {
					"title": [
						{
							"text": {
								"content": trade.pair
							}
						}
					]
				},
				"Entry Date": {
					"date": {
						"start": trade.timestamp.strftime('%Y-%m-%d')
					}
				},
				"PnL": {
					"number": trade.result
				},
				"Direction": {
					"select": {
						"name": trade.direction
					}
				},
				"Risk Amount": {
					"number": trade.risk_amount
				},
				"Session": {
					"select": {
						"name": trade.session
					}
				},
			}
	        }

	response = requests.post(url, headers=headers, json=data)

def main():
	user = Trader('Richard')

	while True:
		try:
			user_prompt = int(input('Type 1 to add trades, type 2 to quit: '))

			if user_prompt == 1:
				pair_input = input('Pair name: ')
				result_input = float(input('PnL Result: '))
				direction_input = input('Direction: ')
				risk_input = float(input('Risk Amount: '))
				session_input = input('Trading Session: ')

				user.place_trade(
					pair=pair_input,
					result=result_input,
					direction=direction_input,
					risk_amount=risk_input,
					session=session_input
				)
			elif user_prompt == 2:
				print('Trade Journal Closed.')
				break
		except ValueError as e:
			print(f'{e}. Please enter numbers only.')
			print('Try again!\n')

if __name__ == '__main__':
	main()
