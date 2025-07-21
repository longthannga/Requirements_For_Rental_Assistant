import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
sheet_id = "1GWqdskR-ibtKkxWZ981BOiePkOS4kKHAN4-p6QWp3NU"
work_book = client.open_by_key(sheet_id)
sheet = work_book.worksheets()[0]

