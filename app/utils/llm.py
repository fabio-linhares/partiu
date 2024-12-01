from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import wikipediaapi
from geopy.geocoders import Nominatim

# # Escolha um modelo T5 para pergunta e resposta
# model_name = "t5-small"

# # Carregue o tokenizer e o modelo T5
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# # Configure o pipeline para geração de texto
# text_generation_pipeline = pipeline(
#     "text2text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_length=128,
#     do_sample=True,
#     temperature=0.7,
#     top_p=0.95,
# )

text_generation_pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=128,
    num_beams=4,  # Melhora a qualidade das respostas
    early_stopping=True,
    temperature=0.7,
    top_p=0.95,
)


llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

# Configuração dos embeddings
embeddings = HuggingFaceEmbeddings()


def get_location_info(location_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(location_name)
    if location:
        return location.address, location.latitude, location.longitude
    else:
        return "Informação não disponível."


def get_wikipedia_summary(location):
    wiki_wiki = wikipediaapi.Wikipedia('pt')
    page = wiki_wiki.page(location)
    if page.exists():
        return page.summary
    else:
        return "Informação não disponível."


def prepare_travel_data(pacotes):
    texts = []
    metadatas = []

    # Introdução ao texto
    introducao = "Atualmente, dispomos das seguintes opções de pacotes de viagem:"
    texts.append(introducao)
    metadatas.append({})  # Adiciona um metadata vazio correspondente à introdução

    # Enumerar as opções de pacotes
    for i, pacote in enumerate(pacotes, start=1):
        text = (
            f"Opção {i}: {pacote['titulo']} - "
            f"Preço Atual: R$ {pacote['preco_atual']}, "
            f"Duração: {pacote['duracao']}, "
            f"Datas Disponíveis: {pacote['datas']}."
        )
        texts.append(text)
        metadatas.append(pacote)
    
    return texts, metadatas

def create_knowledge_base(texts, metadatas):
    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)

def setup_retrieval_qa(knowledge_base):
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}

    Question: {question}
    Answer:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=knowledge_base.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )

    return qa