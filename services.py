import random
import database as db

def simulate_ifood_order():
    """Simula um pedido do iFood."""
    items = [
        "1x Açaí 500ml Tradicional + Granola + Leite Condensado + Banana",
        "2x Açaí 300ml + Morango + Leite em Pó",
        "1x Açaí 700ml Premium + Frutas Variadas + Mel + Paçoca",
        "1x Açaí 500ml + Nutella + Morango + Granola",
        "2x Açaí 400ml Fitness + Whey + Banana + Aveia"
    ]
    clients = ["Maria Silva", "João Santos", "Ana Oliveira", "Pedro Costa", "Julia Lima"]

    db.create_order(
        source=db.FONTE_IFOOD,
        client_name=random.choice(clients),
        description=random.choice(items)
    )

def simulate_99food_order():
    """Simula um pedido do 99Food."""
    items = [
        "1x Açaí 600ml + Frutas da Estação + Granola + Mel",
        "1x Açaí Bowl Grande + Banana + Morango + Kiwi",
        "2x Açaí 350ml Tradicional + Leite Condensado",
        "1x Açaí 500ml + Nutella + Amendoim + Leite em Pó",
        "1x Combo Família (3x Açaí 400ml) + Coberturas Variadas"
    ]
    clients = ["Carlos Mendes", "Fernanda Souza", "Ricardo Lima", "Patrícia Santos", "Bruno Alves"]

    db.create_order(
        source=db.FONTE_99FOOD,
        client_name=random.choice(clients),
        description=random.choice(items)
    )

def simulate_whatsapp_order():
    """Simula um pedido do WhatsApp (processado pela IA)."""
    # Simula JSON processado pela IA
    orders = [
        {"client": "Thiago Ferreira", "items": "2x Açaí 500ml + 1x Suco Natural Laranja 500ml"},
        {"client": "Amanda Costa", "items": "1x Açaí 700ml com tudo + 1x Água de Coco"},
        {"client": "Rafael Martins", "items": "3x Açaí 300ml Kids + Confete + Granola"},
        {"client": "Camila Rocha", "items": "1x Açaí 1L para viagem + Potes extras de cobertura"},
        {"client": "Lucas Pereira", "items": "2x Açaí Fitness 500ml + Whey + Banana + Sem açúcar"}
    ]

    order = random.choice(orders)
    db.create_order(
        source=db.FONTE_WHATSAPP,
        client_name=order["client"],
        description=order["items"]
    )
