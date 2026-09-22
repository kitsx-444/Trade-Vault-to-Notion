from dotenv import load_dotenv
import os
import requests
import datetime
import csv

load_dotenv()
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
NOTION_SUMMARY_PAGE_ID = os.getenv('NOTION_SUMMARY_PAGE_ID')

headers = {
	"Authorization": f"Bearer {NOTION_TOKEN}",
	"Notion-Version": "2022-06-28",
	"Content-Type": "application/json"
}

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
		return send_trade_to_notion(trade)


class Trader:
	def __init__(self, name):
		self.name = name
		self.account = Account(1000)

	def place_trade(self, pair, result, direction, risk_amount, session):
		trade = Trade(pair, result, direction, risk_amount, session)
		return self.account.log_trade(trade)


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
	return response.json()['id']


def receive_trades_from_notion():  # This is how to receive data from your Notion database.
	query_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
	response = requests.post(query_url, headers=headers)
	results = response.json()["results"]

	# Win rate block
	pnls = [res["properties"]["PnL"]["number"] for res in results if res["properties"]["PnL"]["number"] is not None]
	if not pnls:
		print('No trade data found in Notion yet.')
		return 0.0, 0.0

	winning_trades = [win for win in pnls if win > 0]
	win_rate = len(winning_trades) / len(pnls) * 100

	# Loss rate block
	losing_trades = [loss for loss in pnls if loss < 0]
	loss_rate = len(losing_trades) / len(pnls) * 100

	# Avg win block
	avg_win = sum(winning_trades) / len(winning_trades) if winning_trades else 0.0

	# Avg Loss block
	# abs() converts the negative number avg into the positive magnitude the formula needs.
	avg_loss = abs(sum(losing_trades) / len(losing_trades)) if losing_trades else 0.0

	# Percentage block
	win_percent = win_rate / 100
	loss_percent = loss_rate / 100

	# Avg Risk block
	risks = [result["properties"]["Risk Amount"]["number"] for result in results if
	         result["properties"]["Risk Amount"]["number"] is not None]
	avg_risk = sum(risks) / len(risks) if risks else 1.0

	# Expectancy Block
	expectancy = ((avg_win * win_percent) - (avg_loss * loss_percent)) / avg_risk
	label = "positive" if expectancy > 0 else "negative"
	print(f"You have a {label} expectancy.")
	print(f"Your win rate: {round(win_rate, 2)}%")
	print(f"${round(expectancy, 2)} return per $1.00 risked.")
	return win_rate, expectancy


def update_performance_summary(win_rate, expectancy):
	patch_url = f"https://api.notion.com/v1/pages/{NOTION_SUMMARY_PAGE_ID}"
	data = {
		"properties": {
			"Win Rate": {
				"number": round(win_rate, 2)
			},
			"Expectancy": {
				"number": round(expectancy, 2)
			},
			"Last Updated": {
				"date": {
					"start": datetime.datetime.now().strftime('%Y-%m-%d')
				}
			}
		}
	}
	response = requests.patch(patch_url, headers=headers, json=data)
	if response.status_code == 200:
		print("Performance Summary successfully updated in Notion!")
	else:
		print(f"Failed to update Summary ({response.status_code}): {response.text}")


def parse_csv_trades():
	with open('optimized_data.csv', 'r') as f:
		reader = csv.DictReader(f)
		trades = []
		for row in reader:
			raw_date = row['Entry Date']
			formatted_date = datetime.datetime.strptime(raw_date, '%B %d %Y').strftime('%Y-%m-%d')
			row['Entry Date'] = formatted_date

			session = row['Session']
			pair = row['Pair']
			direction = row.get('Direction', 'N/A')
			row['Direction'] = direction

			row['Risk Amount'] = float(row['Risk Amount'])
			row['PnL'] = float(row['PnL'])
			row['Opening Balance'] = float(row['Opening Balance'])
			row['Closing Balance'] = float(row['Closing Balance'])

			trades.append(row)
		return trades[::-1]


def upload_csv_trades(file_path):
	trades = parse_csv_trades()
	for trade in trades:
		data = {"parent": {"database_id": NOTION_DATABASE_ID},
		        "properties": {
					"Pair": {
						"title": [
							{
								"text": {
									"content": trade['Pair']
								}
							}
						]
					},
					"Entry Date": {
						"date": {
							"start": trade['Entry Date']
						}
					},
					"PnL": {
						"number": trade['PnL']
					},
					"Direction": {
						"select": {
							"name": trade['Direction']
						}
					},
					"Risk Amount": {
						"number": trade['Risk Amount']
					},
					"Session": {
						"select": {
							"name": trade['Session']
						}
					},
					"Opening Balance": {
						"number": trade['Opening Balance']
					},
					"Closing Balance": {
						"number": trade['Closing Balance']
					},
				}
		        }
		response = requests.post(url, headers=headers, json=data)
		if response.status_code == 200:
			print(f"Successfully uploaded {trade['Pair']} trade from {trade['Entry Date']}")
		else:
			print(f"Failed to upload {trade['Pair']} trade from {trade['Entry Date']}")


def main():
	user = Trader('Richard')

	while True:
		try:
			user_prompt = int(
				input('Type 1 to add trades, type 2 to upload historical trades from CSV, type 3 to quit: '))

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
				upload_csv_trades('optimized_data.csv')

			elif user_prompt == 3:
				print('Trade Journal Closed.')
				break
		except ValueError as e:
			print(f'{e}. Please enter numbers only.')
			print('Try again!\n')

	win_rate, expectancy = receive_trades_from_notion()
	update_performance_summary(win_rate, expectancy)


if __name__ == '__main__':
	main()
