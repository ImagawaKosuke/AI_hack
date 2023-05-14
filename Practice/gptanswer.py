import openai

KEY = "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"
openai.api_key = KEY

def Answer(question):
    

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": question,
        }]
    )

    response = completion.choices[0].message.content

    return response
question = '''
私は肉料理を食べたいです。
JR大阪駅周辺でおすすめのレストランを10個箇条書きで教えてください。
ただし表示は「レストラン名:説明」の感じでお願いします。
'''

answer = Answer(question)

print(answer)