from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store game state
class ImposterGame:
    def __init__(self):
        self.name = ""
        self.score = 0
        self.current_step = "intro"
        self.choices = {}
    
    def process_input(self, user_input, step=None):
        if step:
            self.current_step = step
            
        if self.current_step == "intro":
            self.name = user_input
            self.current_step = "one"
            return f"{self.name}! You are a very brave knight in the middle ages. You have fought hundreds of battles, protecting your city from raiders and wild animal attacks." 
        elif self.current_step == "one":
                self.current_step = "two"
                return ("As you grow older you begin to feel like you have done so little for the long life you have lived. In the 80 years you have fought and the hundreds of people you have saved you feel bad. You feel like you have not achieved enough. You go to a wizard to get help, he suggests making a list of all of your accomplishments. Do you make a list or ignore him?")
        elif self.current_step == "two":
            self.choices["list1"] = user_input.lower()
            if "ignore" in user_input.lower():
                self.current_step = "two"
                return "This feeling of not having done enough is not very healthy. You need to know you have done so much. Saving so many people in such a lifetime is what some can only dream of doing. Please reload, and consider your answer again."
            elif "list" in user_input.lower() or "make" in user_input.lower():
                self.current_step = "three"
                return ("You are a very brave knight. Listening to the words of the helpful wizard will help you to realize how much you have done and how much you have accomplished. As you look at these lists of battles, you realize you fought one with an army of 100 men when fighting off a neighboring empire. In most of the other battles, it was only you and no more than one close friend. You feel like this huge win for you is much less important because you needed help. Do you stop comparing yourself or just try to become content with this feeling?")
            else:
                return "I didn't understand that. Please choose to make a list or do nothing."
        elif self.current_step == "three":
            self.choices["list2"] = user_input.lower()
            if "compare" in user_input.lower():
                self.current_step = "four"
                return ("Exactly! You are so accomplished and no matter how much help you took, you made an effort. Without you the project would have never been as successful as it was, so there is no reason to feel unaccomplished.The next day you try to take a walk in the village. The strange looks that villagers give you remind you of the eye you lost in one of your worst battles. Very few knights ever lost anything, let alone an eye. You know you have a battle coming up, do you prepare hard or recognize the accomplishment of having survived that battle.")
            elif "content" in user_input.lower() or "feeling" in user_input.lower():
                self.current_step = "three"
                return ("In the long term this will not be as helpful as removing the feeling. A feeling of avoiding help might make you seem closed off. Please reload, and consider your answer again.")
            else:
                return "Please choose to either stop comparing or be content"
        elif self.current_step == "four":
            self.choices["list3"] = user_input.lower()
            if "prepare" in user_input.lower():
                return ("Yes and no. Working harder is a very good goal to have to make your outcome better. This might help in the short term, but in a much longer span you will always be working way too hard and might possibly burn out. Please reload, and consider your answer again.")
            elif "recognize" in user_input.lower():
                self.current_step = "five"
                return "You are an amazing and brave knight fighting many battles, and saving your country numerous times. This is the best thing to do. All of this questioning makes you feel way too unsure in yourself. You begin to feel as if you don't understand these simple questions, what do you do? You feel not naturally intelligent. Do you make a list of what you know or do you work hard to learn more?"
            else:
                return "Please choose to either prepare or recognize your accomplishment"
        elif self.current_step == "four":
            self.choices["list3"] = user_input.lower()
            if "work" in user_input.lower():
                return ("Yes and no. Working harder is a very good goal to have to make your outcome better. This might help in the short term, but in a much longer span you will always be working way too hard and might possibly burn out. Please reload, and consider your answer again.")
            elif "recognize" in user_input.lower():
                self.current_step = "five"
                return "Yes, this will help you realize how much you know. You know so very much, there is no need to question your abilities, after all you have saved so many people from the evil of others. The day of battle arrives. You mount your noble steed with new knowledge on how to defeat the attackers. You have trained, and are as ready as possible. You fight a mighty last battle protecting the townspeople you have known for all your life, but age has got to you. You did not fight perfectly and feel like you did nothing at all. Do you take pride in what you have achieved or keep fighting till you get a perfect win?"
            else:
                return "Please choose to either make a list or work hard"
        elif self.current_step == "five":
            self.choices["list4"] = user_input.lower()
            if "pride" in user_input.lower():
                self.current_step = "six"
                return ("Yes, you have done so much in not just today’s battle but in all the time you have been fighting. You can do this, you are successful. Take pride, for you deserve to take pride.")
            elif "fight" in user_input.lower():
                return "Perfection is impossible, however you have perfected yourself. Fighting and staying alive for so long and so well is such a huge achievement and you must acknowledge that. Please reload, and consider your answer again."
            else:
                return "Please choose to either take pride or acknowledge"
        elif self.current_step == "six":
            return "Congratulations, {self.name} you now understand your accomplishments, and the worth that comes along with them regardless of what others tell you or what you think of yourself."
game = ImposterGame()
@app.route('/game', methods=['POST'])
def process_input():
    data = request.json
    user_input = data.get('text', '')
    step = data.get('step', None)
    
    response = game.process_input(user_input, step)
    
    return jsonify({
        'response': response,
        'current_step': game.current_step,
        'choices': game.choices
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


if __name__ == '__main__':
    app.run(debug=True)
