from src.services.faiss_interface import load_kb, retrieve_info
from src.services.aws_bedrock import createEmbedding, BedrockModel, llmInference

kb = load_kb()

def get_relevant_keywords(query : str):

    prompt = f"""The user is looking to find a student event with their input. Your job is to extract a few keywords that describe the qualities of the type of event they are looking for. 

Be concise and keep your response short, as in under 20 keywords.

Do not output anything else other than the keywords in a comma-separated list.

DO NOT OUTPUT CODE."""
    
    response = llmInference(BedrockModel.LLAMA_70B, prompt, query)
    
    return response


def get_events(tags, num_events):
    return retrieve_info(kb, tags, num_events)




