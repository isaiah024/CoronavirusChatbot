from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

# basic logging config
logging.basicConfig(filename="chatbot.log", level=logging.INFO, filemode="w")

# Creating ChatBot Instance
chatbot = ChatBot(name = 'CoronavirusBot',
                  read_only = True,
                  logic_adapters=[
                      {
                          'import_path': 'chatterbot.logic.BestMatch',
                          'default_response': 'I am sorry, but I do not understand. Type Questions if you need to '
                                              'view the questions.',
                          'maximum_similarity_threshold': 0.95
                      }
                  ],
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")
#Clear the chatbots storage
#Helps prevent incorrect answers from the bot
#You want to disable this when training the bot
chatbot.storage.drop()

# Training with Personal Ques & Ans using list trainer
#training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
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