import gspread
import os
from google import genai
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

SHEET_NAME = "Power Generation"
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

base_path = os.path.dirname(os.path.abspath(__file__))
path_to_json = os.path.join(base_path, "service-account.json")

def analyze_energy_data():
    try:
        creds = Credentials.from_service_account_file(path_to_json, scopes=scope)
        client_sheets = gspread.authorize(creds)
        sheet = client_sheets.open(SHEET_NAME).sheet1
        
        all_data = sheet.get_all_records()
        if not all_data:
            return

        recent_entries = all_data[-10:]
        data_string = "\n".join([str(entry) for entry in recent_entries])

        if not GEMINI_KEY:
            print("Configuration Error: Check .env file")
            return

        client_gemini = genai.Client(api_key=GEMINI_KEY)

        prompt = f"""
        Latest Sensor Data:
        {data_string}

        Perform a technical audit:
        1. Calculate Average Voltage.
        2. Estimate Total Steps.
        3. Provide one engineering suggestion for efficiency.
        """

        response = client_gemini.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )

        print("\n" + "="*45)
        print("SMART GRID INSIGHTS")
        print("="*45)
        print(response.text.strip())
        print("="*45)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_energy_data()