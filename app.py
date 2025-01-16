import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from groq import Groq
import urllib.parse

app = Flask(__name__)
CORS(app)  
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

groq_client = Groq(api_key=GROQ_API_KEY)

@app.route('/ai_responses', methods=['POST'])
def ai_responses():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"response": "Please provide a query."}), 400

    try:
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": query}],
            temperature=1,
            max_tokens=40,
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
    message = data.get("message", "Hello! This is Sia, your virtual assistant.")
    if not to_phone or not message:
        return jsonify({"error": "Phone number and message are required"}), 400
        
    try:
        encoded_message = urllib.parse.quote(message)
        call = twilio_client.calls.create(
            to=to_phone,
            from_=TWILIO_PHONE_NUMBER,
            url=f"https://ai-phoneagent.onrender.com/voice_response?message={encoded_message}"  
        )
        return jsonify({"status": "Call initiated", "call_sid": call.sid}), 200
    except Exception as e:
        print(f"Error making call: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/voice_response', methods=['GET', 'POST'])
def voice_response():
    message = request.args.get("message", "Hello! This is Sia, your virtual assistant.")
    response = VoiceResponse()
    response.say(message, voice="alice")
    gather = response.gather(input='speech', timeout=10, action='/process_input')
    gather.say("Please ask your question after the beep.")
    return str(response)

@app.route('/process_input', methods=['POST'])
def process_input():
    user_query = request.form.get('SpeechResult', '')
    if not user_query:
        response = VoiceResponse()
        response.say("Sorry, I couldn't hear anything. Please try again.", voice="alice")
        response.redirect('/voice_response') 
        return str(response)

    ai_response =ai_responses(user_query)
    response = VoiceResponse()
    response.say(ai_response, voice="alice")
    response.hangup()  
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
