from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

headers = {
	"Authorization": f"Bearer {NOTION_TOKEN}",
	"Notion-Version": "2022-06-28",
	"Content-Type": "application/json"
}

url = "https://api.notion.com/v1/pages"

class Trade:
	def __init__(self, pair, result, direction):
		self.pair = pair
		self.result = result
		self.direction = direction
		self.timestamp = datetime.datetime.now()

class Account:
	def __init__(self, balance):
		self.balance = balance
		self.trade_history = []

	def log_trade(self, trade):
		self.trade_history.append(trade)
		self.balance += trade.result
		send_trade_to_notion(trade)

class Trader:
	def __init__(self, name):
		self.name = name
		self.account = Account(1000)

	def place_trade(self, pair, result, direction):
		trade = Trade(pair, result, direction)
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
				"Result": {
					"number": trade.result
				},
				"Direction": {
					"select": {
						"name": trade.direction
					}
				}
			}
	        }

	response = requests.post(url, headers=headers, json=data)

def main():
	user = Trader('insert your name')
	# user.place_trade('AUDCAD', 209.50, 'Long') This is how to execute the program
	print(f'Total Account Balance: ${user.account.balance}')
	print('Total Trades Logged In:', len(user.account.trade_history))

if __name__ == '__main__':
	main()
