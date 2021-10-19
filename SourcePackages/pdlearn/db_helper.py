import sqlite3


def search_answer(title):
    answers = []
    if title:
        db = sqlite3.connect('./QuestionBank.db')
        res = db.cursor().execute(
            'select question,answer,datetime from tiku where question like "%' + title + '%" LIMIT 5 ')
        for answer in res:
            print("找到题目：{}\n 答案：{}\n".format(answer[0], answer[1]))
            answers.append(answer[1])
        db.close()
    return answers
