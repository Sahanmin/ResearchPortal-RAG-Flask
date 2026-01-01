from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


def get_qa_chain(vectordb, llm):
    
    # Configure retriever with search parameters
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # Return top 4 most relevant chunks
    )
    
    # Custom prompt
    prompt_template = """
    You are an assistant. Answer the question **only using the information provided in the context below**.  
Do not use any outside knowledge.  

Context: 
{context}

Question: 
{question}

Instructions:  
- If the answer can be found in the context, provide it concisely.  
- If the answer is not present in the context, reply exactly: "I don't know."
"""   

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    return chain
    