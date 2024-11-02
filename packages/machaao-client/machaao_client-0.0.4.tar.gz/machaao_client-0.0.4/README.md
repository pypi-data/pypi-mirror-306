# Machaao - Your one stop chatbot companion
[![Gitter](https://badges.gitter.im/messengerx-io/community.svg)](https://gitter.im/messengerx-io/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)  
A module for python developers looking to rapidly build, prototype and publish personalized chatbots

### Full tutorial [below](#bot-creation) to create your first bot

## Live Web Demo ##
![figure](https://github.com/machaao/machaao-py/blob/master/images/img.png?raw=true)

[Jeanie](https://messengerx.io/jeanie) is a GPT-J powered virtual girlfriend based on the module

## Bot Creation ##

### Create a python venv (Recommended)
```bash
# For Linux/MacOS
python3 -m venv env
source ./env/bin/activate

# For Windows
python -m venv env
env\Scripts\activate
```

### Install machaao_client package
```bash
# For Linux/MacOS
pip3 install machaao_client

# For Windows
pip install machaao_client
```

### Get MessengerX.io API Key ##
* Available on the [MessengerX.io](https://portal.messengerx.io/index#!/dashboard) portal
* If you aren't registered, please create an account and login
* Set up your new bot by providing it a `Character Name` and `Description`. 
  * Select `Custom Bot` option
  * It should look something like this:
  * ![figure](https://github.com/machaao/machaao-py/raw/master/images/bot_setup.png?raw=true)
* Click on `Save`. It will redirect you to your dashboard.
* On your dashboard you can see your newly created bot
  * ![figure](https://github.com/machaao/machaao-py/raw/master/images/new_bot.png?raw=true)
* Click on `Settings` tab. It will open your bot configuration page.
  * ![figure](https://github.com/machaao/machaao-py/raw/master/images/bot_config.png?raw=true)
* On the configuration page you'd be able to see a string named `token`. That's your `Machaao API Token`


### Create a new .env file in the same directory ###
```bash
nano -w .env
```
Put these key-value pairs in your .env file
```
API_TOKEN=<Machaao API Token>
ENV=dev
```
Change ENV=prod when you want to publish your bot

### Create a python file - app.py and copy the following code
```bash
from datetime import datetime

import pytz
from flask import Flask, request
from machaao_client import MachaaoSession, QuickReply, MachaaoTextMessage

app = Flask(__name__)


@app.route('/machaao/hook', methods=['GET', 'POST'])
def receive():
    
    # Create a machaao session
    session = MachaaoSession(
        request,
        server_session_create_time=server_session_create_time
    )

    # Get user message
    text = session.user_message
    print(f"Text from user: {text}")

    # Reply to user
    reply = "Hi from Machaao!!"

    # Add Quick replies to your message
    hello_qr = QuickReply(content_type="text", title="Hello 👋", payload="Hello")
    quick_replies = [hello_qr]

    # Compose the text message
    msg = MachaaoTextMessage(text=reply, quick_replies=quick_replies, ads=True)

    # Reply back to the user
    return session.send_message(msg)


if __name__ == '__main__':
    server_session_create_time = datetime.now(
        tz=pytz.utc).replace(tzinfo=None)

    app.run(host="0.0.0.0", port=5000, debug=False)
    
```


### Run your simple chatbot on your local server
```bash
# For Linux/MacOS
python3 app.py

# For Windows
python app.py
```


### Start ngrok.io tunnel in a new terminal (local development) ###
```
ngrok http 5000
```
* You'll get a `Forwarding` URL mentioned on the console as shown below
![figure](https://github.com/machaao/machaao-py/raw/master/images/ngrok_console.png?raw=true)
* Copy the `Forwarding` URL. In this example it would be:
```
https://26ea-150-107-177-46.ngrok-free.app
```

### Update your webhook ###
Update your bot `Webhook URL` on the bot configuration page with the NGROK `Forwarding URL`<br/>
In this example your Webhook URL would be:
```
https://26ea-150-107-177-46.ngrok-free.app/machaao/hook
```
Refer to this screenshot below
![figure](https://github.com/machaao/machaao-py/raw/master/images/update_hook.png?raw=true)

### Test your bot:
Click on `Preview` to chat with your bot

#### NOTE: UNDER ACTIVE DEVELOPMENT (ACCEPTING PULL REQUESTS)
