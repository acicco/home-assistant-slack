import os
from home_assistant import HomeAssistant

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("app_mention")
def handle_app_mention_events(event, say):
    say(f"Hi there, <@{event['user']}>!")


@app.message("toggle")
def handle_find_message(message, say):
    if message["text"].startswith("toggle"):
        # get the device name
        device_name = message["text"].split()[1]
        # look for device
        home_assistant = HomeAssistant(
            "Home", os.environ["HA_IP"], os.environ["HA_PORT"], os.environ["HA_TOKEN"]
        )
        home_assistant.getDevices()

        device = home_assistant.toggleDevice(device_name)

        if device is False:
            say(f"I couldn't find {device_name}")
        else:
            say(f"Toggled {device['device']['name']} to {device['device']['state']}")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
