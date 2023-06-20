from util.const_util import OPENAI_API_KEY
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

llm = OpenAI(model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY, temperature=0.9)

prompt = PromptTemplate.from_template(
    "you are an artist,  a writer, a photographer. I will give you some word, they are: {subjects}, you have to combine them and imagine to describe me a creative picture or a photo. Your sentence should be simple, succinct, detail, max in 30 words, use collective nouns, visual description only. You have to give me 10 creative sentence, write results in 1 line separated by vertical bar")
