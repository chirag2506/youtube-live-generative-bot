from langchain_openai import OpenAI
from helpers.llmFunctionalities.prompts import *
from appUtils import log, configuration

#make sure to add helpers/llmFunctionalities/prompts.py file
#prompts.py, add myInfoPrompt variable which will contain context for LLM to answer

defaultLlm = OpenAI(
    model= configuration["LLM"]["OpenAI"]["Model"],
    temperature= configuration["LLM"]["OpenAI"]["Temperature"],
    max_tokens= configuration["LLM"]["OpenAI"]["MaxTokens"],
    top_p= configuration["LLM"]["OpenAI"]["TopP"]
)

def respondToFaq(query):
    response = "I just hit my head. I won't be able to answer your question🥴🥴"
    try:
        response = defaultLlm.invoke(myInfoPrompt.format(query= query))
    except Exception as e:
        log.error("Error generating LLM response: {}".format(e))
    return response
