# Trade-Vault-to-Notion
### What is this program:
This program connects a Python trade journal directly to a live Notion database. Instead of manually typing trade details into Notion every time, you enter them once in the terminal, and the program creates a new row in your Notion table automatically, pair, entry date, result, and direction, all filled in. 

With new upgrades to the versions, the program calculates expectancy and the win rate automatically. To view the overall performance of equity, the program compiles all the closing balances and creates a line graph to display overall performance and inserts it into a Notion page of choice.

### Why this program matters:
Manually logging every trade into Notion was repetitive and easy to put off, this closes that gap. Trades get logged the moment they're entered, straight into the same table used for tracking performance, with no copy-pasting between apps.

### What is included in this program:
1. Object-oriented design: `Trade`, `Account`, and `Trader` classes working together (composition)
2. `datetime` for automatic trade timestamps
3. Environment variables (`.env` + `python-dotenv`) to keep API credentials out of the code
4. The `requests` library for real API calls
5. Notion's REST API: creating pages inside a database with typed properties (title, date, number, select)
6. CSV importing: allowing previous trading data to be easily inserted into Notion by file name and location.
7. Statistics: the calculation of win rate, average wins, losses and risk per trade.
8. File uploading into Notion.
9. Matplotlib image creation.
10. Trade logging.
11. Error handling.

### What did I learn and the challenges I faced:
1. How classes can hold and call into other classes (composition), a `Trader` owns an `Account`, which stores a list of `Trade` objects, and methods reach across all three.
2. How to structure a real external API request: headers, authentication, and matching each field to the exact data shape an API expects.
3. Why credentials should never be hardcoded, using `.env` files and `.gitignore` to keep secrets out of version control.
4. Familiarizing myself with Notion API syntax format was a challenge. In that process alone:
   a.) I received an error that Notion's servers could not understand the file I had. With research I had to learn how to set the file I am uploading without requiring the server to mistake it for another. This line: `files = {'file': ('equity_graph.svg', open('equity_graph.svg', 'rb'), 'image/svg+xml')}`
   b.) I received `error 400` because of how I wrapped the file attaching block incorrectly. I researched again and learned that the payload must be wrapped in a list as the value of `children` key. 

### Setup before running this yourself:

**1. Get a Notion integration token**
- Go to [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
- Create a new integration, give it a name, and copy the token it gives you (starts with `ntn_` or `secret_`)


**2. You must create 2 databases and 1 page.**

a.) Create a Notion database to send trades to your Trade Vault Database.
In Notion, create a new full-page database with these columns:
  - `Pair` — Title (default first column)
  - `Entry Date` — Date
  - `Result` — Number
  - `Direction` — Select (add options: Long, Short)
  - `Risk Amount` — Number
  - `Session` — Select
  - `Closing Balance`- Number
  - `Opening Balance`- Number

  b.) **Create your database for your performance summary**
  In Notion, create a new database with these columns:
  - `Name` - Leave empty
  - `Win Rate` - Number
  - `Expectancy` - Number
  - `Last Updated` - Date

c.) **Create a normal page for your equity graph** 
  - That is all here.
  
**3. Add connections on all three including the equity graph page.**
- Open the database, click the **`...`** menu → **Add connections** → select your integration
- This step is easy to miss — without it, the API can't see your database at all

**4. Get your IDs**
- **Page ID** (for `NOTION_EQUITY_ID`): open the page and copy the URL. The ID is the 32-character string of letters and numbers at the end, before any `?`.

- **Database ID** (for `NOTION_DATABASE_ID` and `NOTION_SUMMARY_DATABASE_ID`): open the database as a full page, then copy the URL. The ID is the 32-character string right before `?v=`.

**5. Create a `.env` file in the project folder**
```
NOTION_TOKEN=<your_token_here>
NOTION_DATABASE_ID=<your_trade_journal_database_id_here>
NOTION_SUMMARY_DATABASE_ID=<your_performance_summary_id_here>
NOTION_EQUITY_ID=<your_page_id_here_for_your_graph> 

```
**If you are importing CSV**
Your CSV must include:  `Pair`, `Entry Date`, `Result`, `Direction`, `Risk Amount`, `Session`, `Opening Balance`, `Closing Balance` and their values in the same order.

**6. Install the libraries**
This installs everything the program needs. The libraries are listed further down the README.
```
pip install -r requirements.txt
```
If `pip` isn't recognised, use `py -m pip install -r requirements.txt`

**7. Run it**
```
python main.py
```

### Terminal example:
```
Type 1 to add trades, type 2 to upload historical trades from CSV, type 3 to view your performance, type 4 to view your equity curve, type 5 to quit: <choose_your_desired_task>
```

### Usage examples of each option:
```
Option 1:
Type 1 to add trades, type 2 to upload historical trades from CSV, type 3 to view your performance, type 4 to view your equity curve, type 5 to quit: 1
Pair name: EURUSD
PnL Result: 200
Direction: Long
Risk Amount: 444
Trading Session: London

Option 2:
Type 1 to add trades, type 2 to upload historical trades from CSV, type 3 to view your performance, type 4 to view your equity curve, type 5 to quit: 2
Successfully uploaded NAS100 trade from 2026-08-17
Successfully uploaded NAS100 trade from 2026-07-23

Option 3:
Type 1 to add trades, type 2 to upload historical trades from CSV, type 3 to view your performance, type 4 to view your equity curve, type 5 to quit: 3
You have a positive expectancy.
Your win rate: 32.32%
$0.2 return per $1.00 risked.

Option 4:
Your performance equity line graph will be displayed to you and will be uploaded into your Notion equity graph page.

Option 5:
Type 1 to add trades, type 2 to upload historical trades from CSV, type 3 to view your performance, type 4 to view your equity curve, type 5 to quit: 5
Trade Journal Closed.
```
### Demo

### Trades logged straight into Notion
<img width="1516" height="305" alt="Trade_Vault" src="https://github.com/user-attachments/assets/8f0fe758-6160-4208-bebb-979e80685af2" />


### Equity curve embedded in Notion
<img width="1459" height="650" alt="equity-graph" src="https://github.com/user-attachments/assets/face3a8b-652a-4cb7-8b70-9c89989827bb" />

### Libraries

**Built into Python (nothing to install)**
- `os` - reads your credentials from the environment
- `csv` - parses your CSV file of historical trades
- `datetime` - timestamps trades and converts string dates into date objects

**Installed with pip (included in `requirements.txt`)**
- `requests` - sends the API calls to Notion
- `python-dotenv` - loads your `.env` file so credentials stay out of the code
- `matplotlib` - draws the equity curve graph

### Changelog:
**Version 01**
* Notion integration
* Manually logging trades
* Option to close the program

**Version 02**
* Addition of further trade details: `Risk amount`, `Session`
* Addition of error handling.

**Version 03**
* Receiving trade data from Notion
* Inserting performance metric calculations
* Using the received data to extract their performance metrics.
* Sending back the performance metrics to a dedicated database.

**Version 04**
* Insertion of Parse CSV trades.
* Insertion of Upload CSV trades. A function that automatically uploads a CSV file containing trade data into Notion's database.
* Addition of 3rd option: Uploading CSV file into Notion. (At the time.)

**Version 05**
* Indentation fixes
* <0 and >3 inputs with if/elif statements
* Fixed parse csv trades to use the file_path
* Moved receive notion and update performance to give them their own options.

**Version 06** 
* Adding `self.balance_history` to track closing balances.
* Using matplotlib to create an equity graph of closed balances.
* Adding an option to view the equity curve.

**Version 07**
* Adding the blocks to attach the equity curve into Notion.

### Author
Richard Jr Ocaya, kitsx-444,
LinkedIn: https://www.linkedin.com/in/richard-ocaya-59350a3a0/ 
