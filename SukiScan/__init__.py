from flask import Flask

app = Flask(__name__)
app.secret_key = "SukiScan"

from SukiScan import route
from SukiScan import forms