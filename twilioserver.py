from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# ✅ NEW: Route to check if the server is running
@app.route("/", methods=["GET"])
def home():
    return "Flask Server is Running!"

@app.route("/ivr-response", methods=["POST"])
def ivr_response():
    response = VoiceResponse()
    gather = Gather(input="speech dtmf", timeout=5, action="/process_speech")
    gather.say("Please say 'customer service' or press 2 for customer support. Say 'live agent' or press 0 to speak with a representative.")
    response.append(gather)
    return str(response)

@app.route("/process_speech", methods=["POST"])
def process_speech():
    user_speech = request.form.get("SpeechResult")
    user_dtmf = request.form.get("Digits")
    response = VoiceResponse()

    print(f"IVR Speech: {user_speech}")
    print(f"IVR DTMF Input: {user_dtmf}")

    if user_dtmf == "2":
        response.say("Pressing 2 for customer service.")
        response.play(digits="2")
    elif user_dtmf == "0":
        response.say("Pressing 0 to speak with a live agent.")
        response.play(digits="0")
    elif user_speech:
        user_speech = user_speech.lower()
        if "customer service" in user_speech or "press 2" in user_speech:
            response.say("Pressing 2 for customer service.")
            response.play(digits="2")
        elif "live agent" in user_speech or "press 0" in user_speech:
            response.say("Pressing 0 to speak with a live agent.")
            response.play(digits="0")
        else:
            response.say("I didn't understand that. Transferring you to an agent.")
            response.play(digits="0")
    else:
        response.say("I didn't hear a response. Please say 'customer service' or press 2. Say 'live agent' or press 0.")
        gather = Gather(input="speech dtmf", timeout=5, action="/process_speech")
        response.append(gather)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
