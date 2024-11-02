import os 
from openai import OpenAI
from dotenv import load_dotenv
from anthropic import Anthropic
from config import CONFIG

load_dotenv()


class Gpt:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        
        self.model = CONFIG['gpt']['model']
        self.user_prompt = CONFIG['gpt']['prompt_template'][1]['user']
        self.system_prompt = CONFIG['gpt']['prompt_template'][0]['system']
        self.max_tokens = CONFIG['gpt']['max_tokens']
        self.temperature = CONFIG['gpt']['temperature']
    
    def generate_response(self, input_text: str, context: str) -> str:
        # Format user prompt
        combined_prompt = self.user_prompt.format(
            context=context,
            question=input_text
        )
        
        completion = self.client.chat.completions.create(
                                                        model=self.model,
                                                        max_tokens=self.max_tokens,
                                                        temperature=self.temperature,
                                                        messages=[
                                                            {"role": "system", "content": self.system_prompt},
                                                            {
                                                                "role": "user",
                                                                "content": combined_prompt
                                                            }
                                                        ]
                                                    )
                
        # print(completion.choices[0].message)
        
        return completion.choices[0].message.content


#########################
#########################

# claude = Gpt()
# claude.generate_response(input_text='Ինչու է աղմկում գետը ?',
#                          context='Գետ է կոչվում, ջրային բնական հոսքը, \
#                                   որպես կանոն քաղցրահամ ջրով, որը հոսում է \
#                                   դեպի օվկիանոս, ծով, լիճ կամ այլ գետ։ \
#                                   Որոշ դեպքերում գետը կարող է անցնել հողի \
#                                   մեջ կամ չորանալ, մինչև այլ ջրային օբյեկտի հասնելը։')

