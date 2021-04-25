from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot(name = 'CoronavirusBot',
                  read_only = False,
                  logic_adapters=[
                      {
                          'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                          'input_text': 'Help',
                          'output_text': 'Type a question or type Questions for a list of the questions.'
                      },
                      {
                          'import_path': 'chatterbot.logic.BestMatch',
                          'default_response': 'I am sorry, but I do not understand. I am still learning.',
                          'maximum_similarity_threshold': 0.95
                      }
                  ],
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")
#chatbot.storage.drop()
# Training with Personal Ques & Ans
#training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
#medical = open('training_data/medical.yml').read().splitlines()
#training_data_personal = open('training_data/personal_ques.txt').read().splitlines()
#training_data = training_data_quesans + training_data_personal + medical
#trainer = ListTrainer(chatbot)
#trainer.train(training_data)

#Training with training_data file contents
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('training_data')

#Training with English Corpus Data
#trainer_corpus = ChatterBotCorpusTrainer(chatbot)
#trainer_corpus.train(
#    'chatterbot.corpus.english'
#)

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    app.run()