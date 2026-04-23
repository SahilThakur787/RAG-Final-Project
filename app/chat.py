from .vectorstore import get_db
from .llm import ask_groq
def answer(q):
    docs=get_db().similarity_search(q,k=4)
    ctx='\n'.join([d.page_content[:800] for d in docs])
    if not docs:
        return 'Escalated to human support (no context found).'
    return ask_groq('Context:\n'+ctx+'\nQuestion:'+q)
def chat_loop():
    while True:
        q=input('You: ').strip()
        if q.lower() in {'quit','exit'}: break
        print('Bot:',answer(q))
