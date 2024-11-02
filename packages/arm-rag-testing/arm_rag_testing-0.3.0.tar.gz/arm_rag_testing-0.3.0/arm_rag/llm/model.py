from .gpt import Gpt
from .claude import Claude
from .opensource import Open_Source


def get_model(model_type):
    if model_type == 'gpt':
        return Gpt()
    elif model_type == 'claude':
        return Claude()
    elif model_type == 'open_source':
        return Open_Source()
    else:
        raise ValueError("Invalid model_type")