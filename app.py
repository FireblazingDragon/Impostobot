from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store game state
game_state = {
    "current_step": "intro",
    "user_name": "",
    "last_message": "Hello, what is your name? "
}

@app.route('/game', methods=['POST'])
def process_game():
    data = request.json
    user_text = data.get('text', '')
    step = data.get('step', 'intro')
    
    # Process game logic based on step
    response, next_step = process_game_logic(user_text, step)
    
    # Store the last message for the skip animation feature
    game_state["last_message"] = response
    game_state["current_step"] = next_step
    
    return jsonify({
        "response": response,
        "current_step": next_step
    })

@app.route('/get-last-message', methods=['GET'])
def get_last_message():
    # This endpoint allows the frontend to get the full message when skipping animation
    return jsonify({
        "message": game_state["last_message"]
    })

@app.route('/reset-game', methods=['POST'])
def reset_game():
    # Reset the game state
    game_state["current_step"] = "intro"
    game_state["user_name"] = ""
    game_state["last_message"] = "Hello, what is your name? "
    
    return jsonify({
        "status": "success"
    })

def process_game_logic(user_text, step):
    # Your existing game logic here
    if step == "intro":
        # Store the user's name
        game_state["user_name"] = user_text
        
        # Example response
        response = f"Nice to meet you, {user_text}! I'm FISH, your friendly companion to discuss imposter syndrome. Have you ever felt like you don't belong or that you're not good enough despite your achievements?"
        next_step = "first_question"
        
    elif step == "first_question":
        # Continue with your game logic
        response = "Many people experience imposter syndrome, especially in academic and professional settings. It's the feeling that you've only succeeded due to luck, and not because of your talent or qualifications.\n\nWould you like to explore this topic further?"
        next_step = "exploration"
    
    elif step == "exploration":
        # More of your game logic
        response = "Great! Let's talk about some strategies to overcome imposter syndrome. Remember that everyone feels this way sometimes, even the most accomplished professionals!\n\nWhat specific situation makes you feel like an imposter?"
        next_step = "strategies"
    
    else:
        # Default response
        response = "I'm still learning about imposter syndrome. Can you tell me more about your experience?"
        next_step = "custom"
    
    return response, next_step

if __name__ == '__main__':
    app.run(debug=True)
