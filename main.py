import gspread
import parse
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
    ]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1GWqdskR-ibtKkxWZ981BOiePkOS4kKHAN4-p6QWp3NU"
work_book = client.open_by_key(sheet_id)
sheet = work_book.worksheets()[0]

sheet.batch_clear(["A1:C10"])
data = parse.get_data()

sheet.format("A1:D1", {
    "textFormat": {"bold": True,
            "foregroundColor": {  
            "red": 1.0,
            "green": 1.0,
            "blue": 1.0
            }
            },
    "backgroundColor": {
        "red": 42/255,
        "green": 76/255,
        "blue": 68/255
        },
    "horizontalAlignment": "CENTER"
})

sheet.format(f"A2:D8", {
    "wrapStrategy": "WRAP",
    "verticalAlignment": "TOP",
    "textFormat": {"foregroundColor": {  
            "red": 42/255,
            "green": 76/255,
            "blue": 68/255
            }
        },
    "horizontalAlignment": "CENTER"
})

# Prepare header and data rows
headers = ["Organizations", "General Information", "Published Eligibility Requirements"]
rows = [headers]

for i in range(len(data["Organizations"])):
    # Combine name and website in the same cell with line break
    rows.append([
        data["Organizations"][i],
        data["General Information"][i],
        data["Published Eligibility Requirements"][i]
    ])


# Write all data to the sheet
sheet.update(values=rows, range_name='A1')

for i in range(len(data['Organizations'])):
    row_index = i + 2  # +2 for header row
    url = data['Website'][i]
    display_text = f"{data['Organizations'][i]}"
    
    # Create HYPERLINK formula
    formula = f'=HYPERLINK("{url}", "{display_text}")'
    
    # Update the cell with the formula
    sheet.update_cell(row_index, 1, formula)

# Set the current date in the last cell
sheet.merge_cells("C8:D8")
sheet.format("C8", {
    "horizontalAlignment": "RIGHT"
})
california_date = datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M %Z')
sheet.update_cell(8,3, "Last updated: " + str(california_date))

