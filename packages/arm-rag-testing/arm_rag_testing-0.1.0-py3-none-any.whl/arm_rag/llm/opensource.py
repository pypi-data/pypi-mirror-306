import os 
import torch
from dotenv import load_dotenv
from arm_rag.config import CONFIG
from transformers import AutoTokenizer, AutoModelForCausalLM

load_dotenv()


class Open_Source:
    def __init__(self):
        self.token = os.getenv('HUGGINGFACE_TOKEN')
        self.tokenizer = AutoTokenizer.from_pretrained(CONFIG['open_source']['model'])
        self.model = AutoModelForCausalLM.from_pretrained(
            CONFIG['open_source']['model'],
            device_map="auto" if torch.cuda.is_available() else None,
            torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32
        )  
              
        self.user_prompt = CONFIG['open_source']['prompt_template'][1]['user']
        self.system_prompt = CONFIG['open_source']['prompt_template'][0]['system']
        self.max_tokens = CONFIG['open_source']['max_tokens']
        self.temperature = CONFIG['open_source']['temperature']
    
    def tokenize(self, input_text):
        input_ids = self.tokenizer(input_text, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
        return input_ids
    
    def decode(self, input_ids):
        return self.tokenizer.decode(input_ids[0], skip_special_tokens=True)
    
    def generate_response(self, input_text: str, context: str) -> str:
        # Format user prompt
        combined_prompt = self.user_prompt.format(
            context=context,
            question=input_text
        )
        
        combined_prompt_ids = self.tokenize(combined_prompt) 
        
        output_ids = self.model.generate(**combined_prompt_ids, max_new_tokens=32)

        output = self.decode(output_ids)
        
        print('output: ', output)
        
        return output
    
#########################
#########################

# open_source = Open_Source()
# open_source.generate_response(input_text='Ինչու է աղմկում գետը ?',
#                          context='Գետ է կոչվում, ջրային բնական հոսքը, \
#                                   որպես կանոն քաղցրահամ ջրով, որը հոսում է \
#                                   դեպի օվկիանոս, ծով, լիճ կամ այլ գետ։ \
#                                   Որոշ դեպքերում գետը կարող է անցնել հողի \
#                                   մեջ կամ չորանալ, մինչև այլ ջրային օբյեկտի հասնելը։')

