### MkBot is an easy way to crate inline Telegram bots and you can get json file from the user answers

### usage example

```python
import telebot
import mkBot
from telebot.types import InlineKeyboardButton

# bot
bot = telebot.TeleBot("Bot_token")

# functions
def all(msg):
    main.save(msg, msg.text)
    main.check("send", msg) 

def question(msg):
    all(msg)
    main.gen_json("output.json")

# the questions list
questions = [
    {
        "id" : 1,
        "text" : "Do you want to start ?",
        "buttons" : [
                [InlineKeyboardButton("start", callback_data="yes")]
        ]
    },
    {
        "id" : 2,
        "text" : "How old are you",
        "json_name" : "age",
        "function": question
        
    },
    {
        "id" : 3,
        "text" :  "the answers has been send",
        "buttons" : [
            [InlineKeyboardButton("again ?", callback_data="new")],
        ]
    },
]

# define the main class
main = mkBot.Main(queslist = questions, bot = bot)

@bot.message_handler(func = lambda message:True)
def message(msg):
    if msg.text == "/start":
        main.send_frist(msg)


# the callback handler that gets all inline buttons when has been clicked
@bot.callback_query_handler(func=lambda chosen_inline_result:True)
def inline(call):
    main.save(call.message, call.data)

    if main.index < len(questions) - 1:
        main.check("edit", call.message)
    else:
        main.send_frist(call.message)

bot.polling()
```
### for more informations see the source code 