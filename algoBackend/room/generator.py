from asgiref.sync import sync_to_async
import openai

class Generator: 

    @sync_to_async
    def generated_answer(self, message):
        client = openai.OpenAI()  

        completion = client.Completion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message