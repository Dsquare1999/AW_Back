from asgiref.sync import sync_to_async
import openai

class Generator: 

    def __init__(self, user):
        self.user = user

    @sync_to_async
    def generated_answer(self, message):
        system_message = self.system_message()

        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ]
        )
        return completion.choices[0].message.content
    

    def system_message(self):

        system = """
                Où sommes-nous ? Nous somme sur la plateforme de ALGOWAY SARL, une entreprise spécialisée dans la finance digitale, 
                dans l'information financière et constitue le meilleur espace pour un Assets Liability Manager (ALM) Banque.
                
                Qui suis-je ? Je m'appelle {first_name} {last_name}, mon email c'est {email} et je suis un utilisateur de la plateforme AlgoWay. 
                Je suis un acteur des marchés financiers africains. 
                Sur cette plateforme, j'ai la possibilité de charger des titres obligataires OAT ou BAT avec leurs caractéristiques, de pouvoir faire des analyses sur mes titres et de pouvoir faire des simulations de portefeuille.

                Qui es-tu ? Tu es mon ami sur la plateforme. Tu es un expert en finance, capable de répondre à toutes les questions sur les marchés financiers.
                Tu m'assistes dans mes réflexions et tu m'aides à faire des simulations afin de prendre des décisions avisées.

                """.format(first_name=self.user['first_name'], last_name=self.user['last_name'], email=self.user['email'])

        
        return system