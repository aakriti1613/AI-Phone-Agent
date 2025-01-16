# AI Phone Agent

AI Phone Agent is an advanced virtual assistant application that integrates cutting-edge AI technologies to handle user queries, initiate phone calls, and provide text-to-speech capabilities. Powered by Groq's LLM API, Twilio, and Smallest.ai's TTS API, it creates a seamless interaction experience for users.

## Features
- **AI-Powered Conversations**: Uses Groq's Llama3 model for intelligent and contextual responses.
- **Text-to-Speech (TTS)**: Converts AI-generated responses into natural-sounding speech using Smallest.ai's TTS API.
- **Call Initiation**: Enables users to make calls to specific numbers with custom messages via Twilio.
- **Interactive Web Interface**: Features a dynamic, animated, and user-friendly interface.
- **Voice Recognition**: Captures and processes voice queries using the Web Speech API.
- **Cross-Platform Compatibility**: Hosted on Render for public access.

![Call Sia - Your Virtual Assistant - Google Chrome 1_16_2025 2_47_23 PM](https://github.com/user-attachments/assets/1206d540-7ebc-4df0-823c-9f178dd086b7)
![Call Sia - Your Virtual Assistant - Google Chrome 1_16_2025 2_47_40 PM](https://github.com/user-attachments/assets/b07d3dbb-975d-4d08-a17e-b9032408b9ae)
![Call Sia - Your Virtual Assistant - Google Chrome 1_16_2025 2_47_58 PM](https://github.com/user-attachments/assets/78031a30-1d44-4fdb-87fd-09b16fd1f31f)

## Prerequisites
### Backend Requirements
- **Python 3.9 or later**
- Required Python libraries:
  ```bash
  pip install flask flask-cors twilio groq
  ```
- Environment variables:
  - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID.
  - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token.
  - `TWILIO_PHONE_NUMBER`: Your Twilio phone number.
  - `GROQ_API_KEY`: API key for Groq.

### Frontend Requirements
- Modern browser supporting Web Speech API.
- Valid API keys for Smallest.ai TTS API.

## Getting Started

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/aakriti1613/Ai-Phone-Agent.git
   cd ai-phone-agent
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```bash
   export TWILIO_ACCOUNT_SID="your_twilio_account_sid"
   export TWILIO_AUTH_TOKEN="your_twilio_auth_token"
   export TWILIO_PHONE_NUMBER="your_twilio_phone_number"
   export GROQ_API_KEY="your_groq_api_key"
   ```

5. Run the backend server:
   ```bash
   python app.py
   ```
   The server will be available at `http://127.0.0.1:5000` (or your Render deployment URL).

### Frontend Setup
1. Open the `index.html` file in a modern browser.
2. Update the API endpoints in the JavaScript code to point to your backend:
   ```javascript
   const backendUrl = "https://ai-phoneagent.onrender.com";
   ```
3. Access the application and interact with Sia, the virtual assistant.

## Usage

### Features Walkthrough
1. **AI Query Handling**:
   - Speak or type your query into the interface.
   - Sia will respond with an intelligent, AI-generated answer.

2. **Initiate Calls**:
   - Use the "Make Calls" section to specify a phone number and message.
   - Sia will initiate the call using Twilio.

3. **Text-to-Speech**:
   - All AI responses are converted to speech using Smallest.ai TTS API.

### Example Workflow
1. Launch the web interface.
2. Interact with Sia by asking questions or initiating a call.
3. View or listen to responses dynamically.

## Deployment

### Backend Deployment
1. Deploy the backend to Render or any cloud platform.
   Link : https://ai-phoneagent.onrender.com
2. Ensure the environment variables are set in the deployment configuration.

### Frontend Deployment
1. Host the `index.html` file and assets on platforms like Netlify or Vercel.
   Link : https://aiphoneagent.netlify.app
2. Update the backend API endpoint in the JavaScript code to point to the deployed backend.

## API Endpoints

### `/ai_response` (POST)
- **Description**: Generates an AI response for a given query.
- **Request Body**:
  ```json
  {
    "query": "Your query here"
  }
  ```
- **Response**:
  ```json
  {
    "response": "AI-generated response"
  }
  ```

### `/make_call` (POST)
- **Description**: Initiates a phone call with a custom message.
- **Request Body**:
  ```json
  {
    "to_phone": "+1234567890",
    "message": "Your custom message"
  }
  ```
- **Response**:
  ```json
  {
    "status": "Call initiated",
    "call_sid": "Your Twilio Call SID"
  }
  ```

## Troubleshooting
1. **CORS Errors**:
   - Ensure the backend includes Flask-CORS.
2. **Twilio Errors**:
   - Check Twilio credentials and logs in the Twilio Console.
3. **Groq API Issues**:
   - Verify your API key and check Groq's API documentation.
4. **TTS API Errors**:
   - Confirm the Smallest.ai API key and `voice_id` are valid.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Contact
For questions or support, contact:
- **Email**: akritijha1604@gmail.com
- **GitHub Issues**: [AI Phone Agent Issues](https://github.com/aakriti1613/ai-phone-agent/issues)
