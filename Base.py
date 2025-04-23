import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

filename = "teste-457522-8ebf140dff6b.json"
scopes = [ 
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    filename=filename,
    scopes=scopes
)

client = gspread.authorize(creds)
print(client)


planilha= client.open(title="Teste", 
                      folder_id="1KHbn5BGdsov73OO32NIbWFVViwt8_PR9")