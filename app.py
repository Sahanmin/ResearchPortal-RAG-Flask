from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from src.load_and_extract_text import extract_text_from_pdf, extract_pdf_sections
from src.detect_and_split_sections import refine_sections, split_sections_with_content
# from src.get_summary import generate_detailed_summary
from src.create_vector_db import create_vector_db


from dotenv import load_dotenv
import os, json

load_dotenv()


groq_api_key = os.getenv("GROQ_API_KEY")
llm_model = os.getenv("LLM_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")


llm  = ChatGroq(groq_api_key = groq_api_key, model_name = llm_model)

# Initialize embeddings using the Hugging Face model
embedder = HuggingFaceEmbeddings(model_name=embedding_model)

# print(llm.invoke("why diwali celebrate ?").content)


if __name__ == "__main__":
    extracted_text = extract_text_from_pdf("paper.pdf")
    # print(extracted_text)
    # extracted_sections = extract_pdf_sections(full_text = extracted_text)
    # # with open("extracted_sections.json", "w") as f:
    # #     json.dump(extracted_sections, f, indent=4)
    
    # refined_sections = refine_sections(extracted_sections, llm)
    # # with open("refined_sections.json", "w") as f:
    # #     json.dump(refined_sections, f, indent=4)
    
    # section_with_content = split_sections_with_content(extracted_text, refined_sections)
    # with open("section_with_content.json", "w") as f:
    #     json.dump(section_with_content, f, indent=4)
    
    summary = create_vector_db(extracted_text, embedder)
    
    


