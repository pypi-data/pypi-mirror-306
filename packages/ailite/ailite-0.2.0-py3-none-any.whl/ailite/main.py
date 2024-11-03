from parselite import parse
from searchlite import google
from wordllama import WordLlama

llm = None
def vision(query,k=1,max_urls=5,animation=False):
    global llm
    if llm is None:
        llm = WordLlama.load()
    res = llm.topk(query, llm.split("".join(parse(google(query,max_urls=max_urls,
                                                     animation=animation)))),k=k)
    return "\n".join(res)
