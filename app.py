# groq_client = Groq(api_key="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") college id api

from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)
CORS(app)  

TWILIO_ACCOUNT_SID = "AC47847977938f28f40eb6ae8c06eea688"
TWILIO_AUTH_TOKEN = "aa197eac3527727899e70e95c5992043"
TWILIO_PHONE_NUMBER = "+12318881481"  

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

groq_client = Groq(api_key="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")

@app.route('/ai_response', methods=['POST'])
def ai_response():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"response": "Please provide a query."}), 400

    try:
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": query}],
            temperature=1,
            max_tokens=50,
            top_p=1,
            stop=None,
        )
        ai_response = completion.choices[0].message.content
        print(f"AI Response: {ai_response}")
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return jsonify({"response": "Sorry, I couldn't process your request. Please try again later."}), 500


@app.route('/make_call', methods=['POST'])
def make_call():
    data = request.json
    to_phone = data.get("to_phone")
    print(to_phone)
    message = data.get("message", "Hello! This is Sia, your virtual assistant.")

    if not to_phone:
        return jsonify({"error": "Phone number is required"}), 400

    try:
        call = twilio_client.calls.create(
            to=to_phone,
            from_=TWILIO_PHONE_NUMBER,
            url=f"http://your-public-server.com/voice_response?message={message}"  
        )
        return jsonify({"status": "Call initiated", "call_sid": call.sid}), 200
    except Exception as e:
        print(f"Error making call: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/voice_response', methods=['GET', 'POST'])
def voice_response():
    message = request.args.get("message", "Hello! This is your AI assistant.")
    response = VoiceResponse()
    response.say(message, voice="alice")
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
