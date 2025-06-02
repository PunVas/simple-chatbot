from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

GROQ_API_KEY = "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"

groq_client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    if not GROQ_API_KEY:
        return jsonify({"error": "Groq API key not configured"}), 500
    
    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        bot_response = chat_completion.choices[0].message.content
        return jsonify({"response": bot_response})
        
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
