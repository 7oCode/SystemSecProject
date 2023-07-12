from urllib import parse

TOKEN = "MTEyNTI3MDExMDc5ODYyMjcyNg.GQ38aj.R3EzRdzvSv4cvvQJ6RTXUEQCWh_BLQVBPYB57s"
CLIENT_SECRET = "T3E4N74XKx3saGg-S4FU5nvavqfIIT8z"
REDIRECT_URI = "http://localhost:5000/oauth/callback"
OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id=1125270110798622726&redirect_uri={parse.quote(REDIRECT_URI)}&response_type=code&scope=identify"
