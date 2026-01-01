import gspread
from google import genai
from google.oauth2.service_account import Credentials
import os


scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]


base_path = os.path.dirname(os.path.abspath(__file__))
path_to_json = os.path.join(base_path, "service-account.json")

try:
    creds = Credentials.from_service_account_file(path_to_json, scopes=scope)
    client_sheets = gspread.authorize(creds)
    sheet = client_sheets.open("Power Generation").sheet1
    all_data = sheet.get_all_records()
except FileNotFoundError:
    print(f"Error: Could not find {path_to_json}. Please move the JSON file to this folder.")
    exit()

recent_entries = all_data[-10:]
data_string = "\n".join([str(entry) for entry in recent_entries])

GEMINI_KEY = "AIzaSyDgF4EUsem2g87pEJZjJVpOAWjuZGeBuKU"
client_gemini = genai.Client(api_key=GEMINI_KEY)

prompt = f"""
I am developing a kinetic energy harvesting system. 
Here is the latest data from my 'Power Generation' Google Sheet:
{data_string}

Analyze this data and provide:
1. Average voltage generated.
2. An estimate of the total steps detected.
3. One technical suggestion to improve power efficiency.
"""


try:
    response = client_gemini.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=prompt
    )
    print("\n--- Gemini Energy Analysis ---")
    print(response.text)
except Exception as e:
    print(f"\nError calling Gemini: {e}")
    print("Tip: If you see a 404 again, check AI Studio to see which models are available for your key.")