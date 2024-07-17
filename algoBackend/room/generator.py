from asgiref.sync import sync_to_async
import openai
import re
import json
from spreads.models import SpreadOperation as Spread
from spreads.serializers import SpreadOperationSerializer

class Generator: 

    def __init__(self, user):
        self.user = user
        # self.client = openai.OpenAI()

    def is_function_call(self, response):
        print("Is function call: ", response)
        return re.match(r"^<\d+>\|", response) is not None
    
    async def handle_function_call(self, message, response):
        parts = response.split("|")
        print("Parameters Parts : ", parts)
        function_number = int(parts[0].strip("<>"))

        corrected_json = parts[1].replace("'", "\"")
        parameters = json.loads(corrected_json)

        print("Function Parameters : ", parameters)
        if function_number == 1:
            result = await sync_to_async(self.get_spread_by_id)(**parameters)
        elif function_number == 2:
            result = await sync_to_async(self.filter_spread_by_bid_ask)(**parameters)
        else:
            result = "Unknown function number."

        print("Function call result: ", result)
        formated_message = self.format_result_message(function_number, message, result)
        return await sync_to_async(self.generated_answer_with_result)(formated_message)
    
    
    async def generated_answer(self, message):
        system_message = await sync_to_async(self.system_message)()

        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": message}
            ]
        )
        response = completion.choices[0].message.content

        if self.is_function_call(response):
            print("Function call detected")
            return await self.handle_function_call(message, response)
        else:
            return response
    
    def generated_answer_with_result(self, result):
        system_message = self.system_message()

        client = openai.OpenAI()
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": result}
            ]
        )
        print("Generated answer with result: ", completion.choices[0].message.content)
        return completion.choices[0].message.content
    

    def system_message(self):
        # Fetch spread data from database
        spread_data = Spread.objects.filter(user=self.user['id'])
        spreads = SpreadOperationSerializer(spread_data, many=True).data

        user_info = {
            "first_name": self.user['first_name'],
            "last_name": self.user['last_name'],
            "email": self.user['email']
        }

        functions_info = {
            1: "get_spread_by_id(id)",
            2: "filter_spread_by_bid_ask(bid, ask)"
        }

        system_message = {
            "platform_description": "Nous sommes sur la plateforme de ALGOWAY SARL, une entreprise spécialisée dans la finance digitale et l'information financière.",
            "user_description": f"Je m'appelle {user_info['first_name']} {user_info['last_name']}, mon email c'est {user_info['email']}, et je suis un utilisateur de la plateforme AlgoWay. Je suis un acteur des marchés financiers africains.",
            "assistant_description": "Tu es un expert en finance, capable de répondre à toutes les questions sur les marchés financiers. Tu m'assistes dans mes réflexions et m'aides à faire des simulations pour prendre des décisions avisées.",
            "spread_information": {
                "description": "Sur AlgoWay, les spreads représentent des offres d'achat ou de vente d'un titre obligataire sur le marché secondaire proposées par moi ou d'autres utilisateurs.",
                "example": "Un spread a un ISIN, une option de Buy ou de Sell, un bid, un ask, une quantité, une validité (en jours), et un type d'ordre (MinVol, VolAvail, AllNone, Complex).",
                "spreads": spreads
            },
            "response_instructions": {
                "general_questions": "Pour les questions générales, donne ta réponse directement.",
                "specific_questions": "Pour les questions nécessitant plus d'informations, utilise les fonctions backend suivantes pour récupérer les informations nécessaires, et retourne uniquement le numéro de la fonction avec les paramètres nécessaires, sans explications supplémentaires. Et ne mentionne surtout pas les fonctions ni leur utilisation dans ta réponse.",
                "available_functions": functions_info,
                "example_response": "Exemple de réponse pour appeler une fonction : <number>|{\"param1\": value1, \"param2\": value2}. Exemple pratique: <2>|{'bid': 500, 'ask': 650}"
            }
        }

        return json.dumps(system_message, ensure_ascii=False, indent=4)
    

    def get_spread_by_id(self, id):
        # Dummy implementation, replace with actual database call
        spread = Spread.objects.get(id=id)
        return SpreadOperationSerializer(spread).data

    def filter_spread_by_bid_ask(self, bid, ask):
        # Dummy implementation, replace with actual database call
        spreads = Spread.objects.filter(bid=bid, ask=ask)
        if not spreads.exists():
            return "Aucun spread trouvé."
        
        serialized_spreads = SpreadOperationSerializer(spreads, many=True).data
        return serialized_spreads
    
    def format_result_message(self, function_number, message, result):
        # Dummy implementation, replace with actual response generation
        return f"Afin de répondre à ce message: {message}, tu as demandé l'exécution de la fonction {function_number}. Elle a retourné comme résultat:{result}. Formule une bonne réponse à partir de ces informations."