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