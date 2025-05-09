from enum import Enum
import boto3
import json
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME, AWS_SESSION_TOKEN


print(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME, AWS_SESSION_TOKEN)
boto3.setup_default_session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME,
        aws_session_token=AWS_SESSION_TOKEN
    )



bedrockRuntime = boto3.client('bedrock-runtime', region_name=AWS_REGION_NAME)

class BedrockModel(Enum):
    TITAN_EMBEDDINGS_V2 = "amazon.titan-embed-text-v2:0"
    LLAMA_3_1_8B_INSTRUCT = "meta.llama3-1-8b-instruct-v1:0"
    LLAMA_3_2_3B_INSTRUCT = "arn:aws:bedrock:us-west-2:365396090247:inference-profile/us.meta.llama3-2-3b-instruct-v1:0"
    LLAMA_3_2_11B_INSTRUCT = "arn:aws:bedrock:us-west-2:365396090247:inference-profile/us.meta.llama3-2-11b-instruct-v1:0"
    CLAUDE_3_INSTANT = "anthropic.claude-instant-v1"
    LLAMA_70B = "meta.llama3-70b-instruct-v1:0"
def createEmbedding(model : BedrockModel, text : str) -> list[float]:

    body = json.dumps({
        "inputText": text,
        "dimensions": 1024,  # Optional: You can specify 256, 512, or 1024 (default)
        "normalize": True    # Optional: Defaults to true
    })

    response = bedrockRuntime.invoke_model(
        modelId=model.value,
        body=body,
        contentType='application/json',
    )

    responseBody = json.loads(response.get('body').read())

    return responseBody.get('embedding')

def llmInference(model : BedrockModel, prompt : str, userInput : str | None = None) -> str:
    fullPrompt = f"Human: {prompt}\nUser Input:{userInput}\nAssistant:" if userInput else prompt

    body = json.dumps({
        "prompt": fullPrompt,
        "temperature": 0.7,
        "top_p": 0.9,
        # "max_tokens_to_sample": 200
    })


    response = bedrockRuntime.invoke_model(
        modelId=model.value,
        body=body,
        contentType='application/json',
        accept='application/json',
    )

    responseBody = json.loads(response.get('body').read())

    return responseBody.get('generation')   






