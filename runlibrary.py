from fastapi import FastAPI, Request
from twilio.twiml.voice_response import VoiceResponse
import subprocess
import os

app = FastAPI()
Room_url = "https://call-object-react.netlify.app/?roomUrl=https%3A%2F%2Fdevrel.daily.co%2FyxG9b0UaURLFQAFdKngN"

@app.post("/start_bot")
async def start_bot(request: Request):
    form_data = await request.form()
    call_sid = form_data.get('CallSid')

    # Create a room and spawn bot
    room_url = Room_url  # Obtain this dynamically as needed
    token = "your_daily_token"        # Generate or retrieve as required

    subprocess.Popen(
        [
            f"python3 -m bot_twilio -u {room_url} -t {token} -i {call_sid}"
        ],
        shell=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )

    # Respond to Twilio with hold music until bot is ready
    response = VoiceResponse()
    response.play(url="http://com.twilio.sounds.music.s3.amazonaws.com/MARKOVICHAMP-Borghestral.mp3", loop=10)
    return str(response)



from pipecat.transports.services.helpers.daily_rest import DailyRoomParams, DailyRoomProperties, DailyRoomSipParams

params = DailyRoomParams(
    properties=DailyRoomProperties(
        sip=DailyRoomSipParams(
            display_name="sip-dialin",
            video=False,
            sip_mode="dial-in",
            num_endpoints=1
        )
    )
)

# Create SIP-enabled Daily room via REST
try:
    room = daily_rest_helper.create_room(params=params)
except Exception as e:
    raise Exception(f"Unable to provision room: {e}")

print(f"Daily room created: {room.url} with SIP endpoint: {room.config.sip_endpoint}")




import requests

API_KEY = "your_daily_api_key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "name": "my-ai-call-room",
    "properties": {
        "enable_sip": True,  # Allows SIP dialing for Twilio
        "enable_chat": False,
        "exp": 3600
    }
}

response = requests.post("https://api.daily.co/v1/rooms", json=data, headers=headers)
print(response.json())  # Get the room URL from response
