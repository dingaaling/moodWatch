from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACae0aefd9f937a87b5b17318b1a7f6bf7'
auth_token = '4929acf3a7714007a3e7225ef16aa8c8'
client = Client(account_sid, auth_token)

def sendText():

    message = client.messages.create(
                                  body="Hey there - it's mood watch. Jane could use your support right now. Reach out to her and make sure she knows that you are there for her.!",
                                  from_='+18176970873',
                                  to='+12143357064'
                              )

    print("Text Message SID:", message.sid)
