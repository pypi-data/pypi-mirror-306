import os 
from anthropic import Anthropic
from dotenv import load_dotenv
from config import CONFIG

load_dotenv()

class Claude:
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic(api_key=self.api_key)
        
        self.model = CONFIG['claude']['model']
        self.user_prompt = CONFIG['claude']['prompt_template'][1]['user']
        self.system_prompt = CONFIG['claude']['prompt_template'][0]['system']
        self.max_tokens = CONFIG['claude']['max_tokens']
        self.temperature = CONFIG['claude']['temperature']
    
    def generate_response(self, input_text: str, context: str) -> str:
        # Format user prompt
        combined_prompt = self.user_prompt.format(
            context=context,
            question=input_text
        )
        
        response = self.client.messages.create(model=self.model,
                                               max_tokens=self.max_tokens,
                                               temperature=self.temperature,
                                               system=self.system_prompt,
                                               messages=[
                                                        {
                                                            "role": "user",
                                                            "content": [
                                                                {
                                                                    "type": "text",
                                                                    "text": combined_prompt
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                )
                
        # print(response.content)
        return response.content[0].text


#########################
#########################

# claude = Claude()
# claude.generate_response(input_text='Ինչու է աղմկում գետը ?',
#                          context='Գետ է կոչվում, ջրային բնական հոսքը, \
#                                   որպես կանոն քաղցրահամ ջրով, որը հոսում է \
#                                   դեպի օվկիանոս, ծով, լիճ կամ այլ գետ։ \
#                                   Որոշ դեպքերում գետը կարող է անցնել հողի \
#                                   մեջ կամ չորանալ, մինչև այլ ջրային օբյեկտի հասնելը։')

