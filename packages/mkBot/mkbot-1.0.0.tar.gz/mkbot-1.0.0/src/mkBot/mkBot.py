from telebot.types import InlineKeyboardMarkup
import json

class Main():
    def __init__(self, queslist, bot):
        self.queslist = queslist
        self.answers = []
        self.index = 0
        self.bot = bot

    def get_user_answers(self, user_id):
        for answer in self.answers:
            if answer.get("usr_id") == user_id:
                return answer
        return None 
    
    def check(self, type, msg):
        try:
            ques = self.queslist[self.index]
            self.ques = ques

            if type == "send":
                if "buttons" in ques:
                    self.bot.send_message(msg.chat.id, ques["text"], reply_markup=InlineKeyboardMarkup(ques["buttons"]))
                    
                else:
                    self.bot.send_message(msg.chat.id, ques["text"])
                    self.bot.register_next_step_handler(msg, ques["function"])

            elif type == "edit":
                if "buttons" in ques:
                    self.bot.edit_message_text(ques["text"], msg.chat.id, message_id = msg.message_id,  reply_markup = InlineKeyboardMarkup(ques["buttons"]))
                    
                else:
                    self.bot.edit_message_text(ques["text"], msg.chat.id, message_id = msg.message_id)
                    self.bot.register_next_step_handler(msg, ques["function"])

            self.index += 1

        except Exception as e:
            print(e)
            self.send_frist(msg)

    def send_frist(self, message):
        self.index = 0

        user_id = message.chat.id
        ans = self.get_user_answers(user_id)

        if ans is None:
            ans = {"usr_id": user_id, "questions": []}
            self.answers.append(ans) 

            self.send_frist(message)
            return 

        ans["questions"].append({})

        if self.queslist[0]:
            self.check("send", message)
        else:
            self.bot.reply_to(message, "there is error")

    def save(self, msg, morc):
        usr_id = msg.chat.id
        ans = self.get_user_answers(usr_id)

        if ans is not None:
            if "json_name" in self.ques:  
                ans["questions"][-1][self.ques["json_name"]] = morc

        else:
            self.send_frist(msg)
            return
    
    def gen_json(self,name):
        with open(name, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.answers, ensure_ascii=False))
            f.close()