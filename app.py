import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from groq import Groq
import urllib.parse
import smtplib

app = Flask(__name__)
CORS(app)  
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")
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

def generate_ai_response(query):
    try:
        completion = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": query}],
            temperature=1,
            max_tokens=50,
            top_p=1,
            stop=None,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "Sorry, I couldn't process your request."

@app.route('/voice_response', methods=['GET', 'POST'])
def voice_response():
    message = request.args.get("message", "Hello! This is Sia, your virtual assistant.")
    response = VoiceResponse()
    response.say(message, voice="aditi")
    response.gather(
        num_digits=1,  
        action='/process_input',
        timeout=10  
    )
    response.say("No input received. The call will now end.")
    response.hangup()
    return str(response)

@app.route('/process_input', methods=['POST'])
def process_input():
    pressed_key = request.form.get('Digits')  
    speech_input = request.form.get('SpeechResult')
    response = VoiceResponse()
    if pressed_key:
        response.say(f"Thank you! You pressed {pressed_key}.", voice="alice")
        response.say("Please ask your question after the beep.")
        response.record(timeout=10, transcribe=True, action='/process_query')
    elif speech_input:
        print(f"User spoke: {speech_input}")  
        ai_response = generate_ai_response(speech_input) 
        response.say(ai_response, voice="aditi")
    else:
        response.say("No input detected. The call will now end.", voice="alice")
        response.hangup()
    return str(response)

@app.route('/process_query', methods=['POST'])
def process_query():
    recording_url = request.form.get('RecordingUrl')
    transcription = request.form.get('TranscriptionText') 
    response = VoiceResponse()
    if recording_url:
        print(f"Recording URL: {recording_url}")
        if transcription:
            print(f"Transcription: {transcription}")
            try:
                completion = groq_client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[{"role": "user", "content": transcription}],
                    temperature=1,
                    max_tokens=40,
                    top_p=1,
                    stop=None,
                )
                ai_response = completion.choices[0].message.content.strip()
                response.say(ai_response, voice="aditi")
            except Exception as e:
                print(f"Error generating AI response: {e}")
                response.say("Sorry, I couldn't process your input. Please try again later.", voice="aditi")
        else:
            response.say("Thank you for your input. We are processing your query.", voice="aditi")
        response.hangup()
    else:
        response.say("Sorry, we could not capture your input. Please try again later.", voice="aditi")
        response.hangup()
    return str(response)

verified_numbers = {}

@app.route('/request_verification', methods=['POST'])
def request_verification():
    data = request.json
    phone = data.get("phone")
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400
    send_email_to_admin(phone)
    verified_numbers[phone] = False 
    return jsonify({"message": "Verification requested."}), 200

@app.route('/otp_verification', methods=['POST'])
def otp_verification():
    data = request.json
    otp = data.get("otp")
    if not otp:
        return jsonify({"error": "Phone number is required"}), 400
    send_email_to_admin(otp) 
    return jsonify({"message": "Verification requested."}), 200

def send_email_to_admin(phone):
    try:
        subject = "Verification Request"
        body = f"Please verify the following phone number / OTP in Twilio: {phone}"
        email_message = f"Subject: {subject}\n\n{body}"
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, email_message)
            print(f"Verification email sent for {phone}.")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    app.run(debug=True)
