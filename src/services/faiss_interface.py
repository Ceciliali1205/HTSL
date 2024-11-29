from langchain.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
import pandas as pd
from src.services.aws_bedrock import BedrockModel
import time


def load_csv_faq(csv_files: list[str]):
    questions = []
    metadatas = []

    for csv_file in csv_files:
        # Load CSV file from the given path
        df = pd.read_csv(csv_file)

        # Store first column in an array for all the questions
        question_list = df.iloc[:, 0].tolist()

        # Store second column in an array for all the answers
        answers_list = df.iloc[:, 1].tolist()

        len_faq = len(question_list)

        i = 0
        while i < len_faq:
            questions.append(question_list[i])
            metadatas.append({"event_id": answers_list[i]})
            i += 1

    return questions, metadatas

def create_knowledge_base(documents_list):
    embeddings = BedrockEmbeddings(model_id=BedrockModel.TITAN_EMBEDDINGS_V2.value)

    def populate_faq_db(questions, metadatas, num):
        start = time.time()
        ##print (f'Now you have {len(questions)} faq documents')

        db = FAISS.from_texts(questions, embeddings, metadatas=metadatas)
        end = time.time()

        ##print("KB Base Population Time: ", end - start)

        index_name = "faq_" + str(num)
        db.save_local(index_name)

        return index_name

    def populate_docs_db(documet, num):
        index_name = "docs_" + str(num)
        # Chunk into pieces of 500 characters with x overlap
        return index_name

    # Create main db
    ##print("Creating Main Database (1)")
    doc_type = documents_list[0]["type"]
    doc_content = documents_list[0]["content"]

    if doc_type == "FAQ":
        questions, metadatas = doc_content
        main_index_name = populate_faq_db(questions, metadatas, 0)
        main_db = FAISS.load_local(main_index_name, embeddings, allow_dangerous_deserialization=True)

    i = 1
    # Go through dbs and merge them
    num_docs = len(documents_list)
    ##print("num docs: ", num_docs)

    while i < num_docs:
        ##print("Creating Database ", i+1)
        doc = documents_list[i]
        doc_type = doc["type"]
        doc_content = doc["content"]
        ##print(f"Document Type: {doc_type}")
        ##print(f"Document Content: {doc_content}\n")

        if doc_type == "FAQ":
            questions, metadatas = doc_content
            new_db_name = populate_faq_db(questions, metadatas, i)
            new_db = FAISS.load_local(new_db_name, embeddings)
            main_db.merge_from(new_db)

        i += 1

    return main_db

def create_kb(urls):
    gdrive_urls = urls
    documents = []
    for gdrive_url in gdrive_urls:
        # Extract the file ID from the Google Drive URL
        if "/view" in gdrive_url:
            file_id = gdrive_url.split("/d/")[1].split("/view")[0]
        else:
            file_id = gdrive_url.split("/d/")[1].split("/edit")[0]
        # Construct the direct CSV download URL for Google Sheets
        download_url = (
            f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
        )
        questions, metadatas = load_csv_faq([download_url])
        #####print("faq_vectors: ", faq_vectors)

        # Any Documnets - docx, pdf, txt
        # FAQ - list of string with faq info
        documents.append({"type": "FAQ", "content": (questions, metadatas)})

    return create_knowledge_base(documents)

def retrieve_info(db: FAISS, query, k):
    start = time.time()
    similar_response = db.similarity_search(query, k=k)

    results = [{'event_id': doc.metadata['event_id'], 'content': doc.page_content} for doc in similar_response]
    end = time.time()

    ##print("Retrival Time: ", end - start)
    return results



def load_kb():
    return FAISS.load_local("faq_0", BedrockEmbeddings(model_id=BedrockModel.TITAN_EMBEDDINGS_V2.value), allow_dangerous_deserialization=True)

