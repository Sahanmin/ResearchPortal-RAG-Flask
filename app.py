from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from flask import Flask, render_template, request, jsonify

from src.load_and_extract_text import extract_text_from_pdf, extract_pdf_sections
from src.detect_and_split_sections import refine_sections, split_sections_with_content
from src.get_summary import generate_detailed_summary
from src.create_vector_db import create_vector_db
from src.RAG_retrival_chain import get_qa_chain


from dotenv import load_dotenv
import os, json

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

groq_api_key = os.getenv("GROQ_API_KEY")
llm_model = os.getenv("LLM_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")

# Global variable
full_text = ''
Research_paper_topics = None
vector_db = None


llm  = ChatGroq(groq_api_key = groq_api_key, model_name = llm_model)

# Initialize embeddings using the Hugging Face model
embedder = HuggingFaceEmbeddings(model_name=embedding_model)

# print(llm.invoke("why diwali celebrate ?").content)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global full_text
    global Research_paper_topics
    
    try:
        file = request.files.get('file')
        
        if not file:
            return jsonify({"error": "No file uploaded"}), 400
        
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # print(filename)
        file.save(filename)
        
        # Get all topics name from research paper
        extracted_text = extract_text_from_pdf(filename)
        full_text = extracted_text
        extracted_sections = extract_pdf_sections(full_text=extracted_text)
        # print(extracted_sections)
        refined_sections = refine_sections(extracted_sections, llm)
        # print(refined_sections)
        section_with_content = split_sections_with_content(extracted_text, refined_sections)
        
        Research_paper_topics = section_with_content
        
        return jsonify({"topics": list(Research_paper_topics.keys())})
    except Exception as e:
        print(f"Error in upload_pdf: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



@app.route('/summary', methods=['POST'])
def get_summary():
    global Research_paper_topics
    
    try:
        topic = request.json.get('topic')
        # print(topic)
        
        if not Research_paper_topics:
            return jsonify({"error": "No paper uploaded yet"}), 400
        
        topic_content = Research_paper_topics.get(topic, "No summary available.")
        
        if topic_content == "No summary available.":
            return jsonify({"error": f"Topic '{topic}' not found"}), 404
        
        summary = generate_detailed_summary(topic_content, llm)
        
        return jsonify({"summary": summary})
    except Exception as e:
        print(f"Error in get_summary: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    

@app.route('/chat', methods=['POST'])
def chat():
    global full_text
    global vector_db
    
    try:
        user_message = request.json.get('message')
        print(f"User question: {user_message}")
        
        if not full_text:
            return jsonify({"error": "No paper uploaded yet"}), 400
        
        if not vector_db:
            print("Creating vector database...")
            vectordb = create_vector_db(text=full_text, embedder=embedder)
            vector_db = vectordb
            print("Vector database created successfully")
            
        chain = get_qa_chain(vectordb=vector_db, llm=llm)
        
        # Use 'query' as the input key (as defined in RAG_retrival_chain.py)
        result = chain.invoke({"query": user_message})
        ai_response = result['result']
        print(f"AI response: {ai_response}")
        
        return jsonify({"response": ai_response})
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

        
    
    
    

if __name__ == "__main__":
    app.run(debug=True)
    
    # extracted_text = extract_text_from_pdf("paper.pdf")
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
    
    
    


