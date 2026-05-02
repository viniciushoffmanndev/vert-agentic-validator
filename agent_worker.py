# agent_worker.py
import os
import json
from confluent_kafka import Consumer, KafkaError
from dotenv import load_dotenv  # <-- Importamos a biblioteca que acabamos de instalar
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# Verifica se a chave foi carregada corretamente
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("ERRO: A variável OPENAI_API_KEY não foi encontrada. Verifique o seu arquivo .env")

# 2. Configuração do Consumer do Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'ai-agent-validator-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['financial-operations'])

# 3. Inicialização do modelo de IA via LangChain (ele lê a chave do .env sozinho agora)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 4. Criação do Prompt de Validação
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
    Você é um agente de validação sênior do mercado de capitais da VERT. 
    Sua função é analisar as operações financeiras e validar se os dados estão consistentes.
    
    Regras de Negócio:
    1. O código do ativo deve começar com 'CRI', 'CRA' ou 'DEB'.
    2. O emissor do título não pode estar em branco.
    3. O valor da operação deve ser maior que 0 e coerente para o mercado (normalmente acima de 100.000).

    Analise a operação e retorne uma resposta estritamente no seguinte formato JSON:
    {{
        "status": "VALIDATED" ou "REJECTED",
        "motivo": "Explicação concisa da decisão"
    }}
    """),
    ("human", "Por favor, valide esta operação financeira: {operation_json}")
])

chain = prompt_template | llm

def process_message(msg_value):
    """ Envia o dado para a IA e processa o retorno """
    try:
        operation_data = json.loads(msg_value.decode('utf-8'))
        print(f"\n[Agente] Nova operação recebida para análise: {operation_data['asset_code']}")
        
        response = chain.invoke({"operation_json": json.dumps(operation_data)})
        
        result = json.loads(response.content)
        print(f"[Agente] Decisão: {result['status']} | Motivo: {result['motivo']}")
        
    except Exception as e:
        print(f"Erro ao processar validação de IA: {e}")

print("🤖 Agente de IA ativado e escutando o Kafka. Pressione CTRL+C para sair.\n")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Erro no Kafka: {msg.error()}")
                break
        
        process_message(msg.value())

except KeyboardInterrupt:
    print("\nEncerrando o agente...")
finally:
    consumer.close()