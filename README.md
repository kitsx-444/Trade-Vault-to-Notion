# Trade-Vault-to-Notion
### What is this program:
This program connects a small Python trade journal directly to a live Notion database. Instead of manually typing trade details into Notion every time, you enter them once in the terminal, and the program creates a new row in your Notion table automatically, pair, entry date, result, and direction, all filled in.

### Why this program matters:
Manually logging every trade into Notion was repetitive and easy to put off. This closes that gap, trades get logged the moment they're entered, straight into the same table used for tracking performance, with no copy-pasting between apps.

### What is included in this program:
1. Object-oriented design: `Trade`, `Account`, and `Trader` classes working together (composition)
2. `datetime` for automatic trade timestamps
3. Environment variables (`.env` + `python-dotenv`) to keep API credentials out of the code
4. The `requests` library for real API calls
5. Notion's REST API: creating pages inside a database with typed properties (title, date, number, select)

### What did I learn:
1. How classes can hold and call into other classes (composition), a `Trader` owns an `Account`, which stores a list of `Trade` objects, and methods reach across all three.
2. How to structure a real external API request: headers, authentication, and matching each field to the exact data shape an API expects.
3. Why credentials should never be hardcoded, using `.env` files and `.gitignore` to keep secrets out of version control.

### Setup before running this yourself:

**1. Get a Notion integration token**
- Go to [notion.so/profile/integrations](https://www.notion.so/profile/integrations)
- Create a new integration, give it a name, and copy the token it gives you (starts with `ntn_` or `secret_`)

**2. Create a Notion database to send trades to**
- In Notion, create a new full-page table with these columns:
  - `Pair` — Title (default first column)
  - `Entry Date` — Date
  - `Result` — Number
  - `Direction` — Select (add options: Long, Short)

**3. Share the database with your integration**
- Open the database, click the **`...`** menu → **Add connections** → select your integration
- This step is easy to miss — without it, the API can't see your database at all

**4. Get your database ID**
- Open the database and look at the URL — the long ID right before `?v=` is your database ID

**5. Create a `.env` file in the project folder**
```
NOTION_TOKEN=your_token_here
NOTION_DATABASE_ID=your_database_id_here
NOTION_SUMMARY_PAGE_ID=<your_database_id_here>
NOTION_EQUITY_ID=<your_page_id_here>

```

**6. Install dependencies**
```
pip install python-dotenv requests
altgraph==0.17.5
certifi==2026.7.22
charset-normalizer==3.4.9
contourpy==1.3.3
cycler==0.12.1
fonttools==4.64.0
idna==3.18
kiwisolver==1.5.1
matplotlib==3.11.1
numpy==2.5.3
packaging==26.3
pefile==2024.8.26
pillow==12.3.0
pyinstaller==6.22.1
pyinstaller-hooks-contrib==2026.6
pyparsing==3.3.2
python-dateutil==2.9.0.post0
python-dotenv==1.2.2
pywin32-ctypes==0.2.3
requests==2.34.2
setuptools==84.0.0
six==1.17.0
urllib3==2.7.0

```

**7. Run it**
```
python main.py
```

### Output example:
```
Type 1 to add trades, type 2 to upload historical trades from CSV, type 3 to view your performance, type 4 to view your equity curve, type 5 to quit: 
```

*(Corresponding rows also appear live in the connected Notion database.)*
