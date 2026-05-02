# validation/producer.py
import json
from confluent_kafka import Producer

# Configuração do Producer apontando para o Kafka no Docker
conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'django-producer'
}

producer = Producer(conf)

def delivery_report(err, msg):
    """ Callback para confirmar se a mensagem foi entregue ao Kafka """
    if err is not None:
        print(f"Erro ao entregar mensagem: {err}")
    else:
        print(f"Mensagem enviada com sucesso para o tópico {msg.topic()} [{msg.partition()}]")

def send_operation_to_kafka(operation_data):
    """ Envia os dados da operação financeira para o tópico do Kafka """
    topic = 'financial-operations'
    
    # Converte os dados para JSON e depois para bytes
    payload = json.dumps(operation_data).encode('utf-8')
    
    # Dispara a mensagem de forma assíncrona
    producer.produce(topic, value=payload, callback=delivery_report)
    
    # Garante que as mensagens pendentes sejam enviadas
    producer.poll(0)
    producer.flush()