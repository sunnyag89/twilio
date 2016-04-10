from flask import Flask, request, redirect, session
import twilio.twiml
from yahoo_finance import Share
 
# The session object makes use of a secret key.
SECRET_KEY = 'a secret key'
app = Flask(__name__)
app.config.from_object(__name__)
 
 
@app.route("/", methods=['GET', 'POST'])
def getStockInfo():
    messageBody = request.values.get('Body')
    try:
      """Splitting the text input into action and ticker"""
      actionMessage = messageBody.split(" ")[0]
      stockTicker = messageBody.split(" ")[1].upper()
      """Using the Yahoo api to respond to user requests"""
      stock = Share(stockTicker)
      if actionMessage.upper() == "QUOTE":
        message = "Last Trading Price: "+ stock.get_price()
      elif actionMessage.upper() == "VOLUME":
        message = "Last Trading VOLUME: "+ stock.get_volume()
      elif actionMessage.upper() == "MCAP":
        message = "MarketCap: "+ stock.get_market_cap()
      elif actionMessage.upper() == "EBITDA":
        message = "EBITDA: "+ stock.get_ebitda()
    except:
      message = "Wrong input, please try again" 
    resp = twilio.twiml.Response()
    resp.sms(message)
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)