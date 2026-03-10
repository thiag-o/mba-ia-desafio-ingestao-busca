from search import search_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.runnables import RunnableLambda


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=1.0, 
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def main():
   
    chain = RunnableLambda(search_prompt) | llm
    
    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return

    print("*"*50)
    print("Pergunte algo sobre o contexto")
    print("*"*50)
  
    while True:
        question: str = input()
        if not question: 
            continue
        if question.lower() in ("sair", "exit", "quit"):
            print("Encerrando o chat. Até mais!")
            break
        result = chain.invoke(question)
        
        print(f"\n{result.content}\n")
        print("Você tem outra pergunta?\n")
    pass

if __name__ == "__main__":
    main()