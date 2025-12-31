"""
Saka Delivery KDS - Módulo de Banco de Dados
Gerencia persistência de pedidos usando SQLite3
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

# Caminho do banco de dados
DB_PATH = Path(__file__).parent / "saka_delivery.db"

# Status possíveis para os pedidos
STATUS_NOVO = "novo"
STATUS_PREPARANDO = "preparando"
STATUS_PRONTO = "pronto"
STATUS_SAIU = "saiu"
STATUS_CANCELADO = "cancelado"

# Mapeamento de fontes
FONTE_IFOOD = "ifood"
FONTE_99FOOD = "99food"
FONTE_WHATSAPP = "whatsapp"


def get_connection() -> sqlite3.Connection:
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
    return conn


def init_db() -> None:
    """Inicializa o banco de dados e cria as tabelas necessárias."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            client_name TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'novo',
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL
        )
    """)
    
    # Índice para otimizar busca por status
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)
    """)
    
    conn.commit()
    conn.close()


def create_order(source: str, client_name: str, description: str) -> int:
    """
    Cria um novo pedido no banco de dados.
    
    Args:
        source: Origem do pedido (ifood, 99food, whatsapp)
        client_name: Nome do cliente
        description: Descrição do pedido
        
    Returns:
        ID do pedido criado
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute("""
        INSERT INTO orders (source, client_name, description, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (source, client_name, description, STATUS_NOVO, now, now))
    
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return order_id


def get_all_orders(include_finished: bool = False) -> list[dict]:
    """
    Retorna todos os pedidos ativos.
    
    Args:
        include_finished: Se True, inclui pedidos finalizados (saiu, cancelado)
        
    Returns:
        Lista de dicionários com os dados dos pedidos
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if include_finished:
        cursor.execute("""
            SELECT * FROM orders 
            ORDER BY 
                CASE status 
                    WHEN 'novo' THEN 1 
                    WHEN 'preparando' THEN 2 
                    WHEN 'pronto' THEN 3 
                    WHEN 'saiu' THEN 4 
                    WHEN 'cancelado' THEN 5 
                END,
                created_at ASC
        """)
    else:
        cursor.execute("""
            SELECT * FROM orders 
            WHERE status NOT IN ('saiu', 'cancelado')
            ORDER BY 
                CASE status 
                    WHEN 'novo' THEN 1 
                    WHEN 'preparando' THEN 2 
                    WHEN 'pronto' THEN 3 
                END,
                created_at ASC
        """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_order_by_id(order_id: int) -> Optional[dict]:
    """
    Busca um pedido específico pelo ID.
    
    Args:
        order_id: ID do pedido
        
    Returns:
        Dicionário com dados do pedido ou None se não encontrado
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def update_order_status(order_id: int, new_status: str) -> bool:
    """
    Atualiza o status de um pedido.
    
    Args:
        order_id: ID do pedido
        new_status: Novo status (novo, preparando, pronto, saiu, cancelado)
        
    Returns:
        True se a atualização foi bem sucedida, False caso contrário
    """
    valid_statuses = [STATUS_NOVO, STATUS_PREPARANDO, STATUS_PRONTO, STATUS_SAIU, STATUS_CANCELADO]
    
    if new_status not in valid_statuses:
        return False
    
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    cursor.execute("""
        UPDATE orders 
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (new_status, now, order_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success


def delete_order(order_id: int) -> bool:
    """
    Remove um pedido do banco de dados.
    
    Args:
        order_id: ID do pedido a ser removido
        
    Returns:
        True se o pedido foi removido, False caso contrário
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    return success


def get_orders_count_by_status() -> dict[str, int]:
    """
    Retorna a contagem de pedidos por status.
    
    Returns:
        Dicionário com status como chave e contagem como valor
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM orders 
        WHERE status NOT IN ('saiu', 'cancelado')
        GROUP BY status
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    counts = {
        STATUS_NOVO: 0,
        STATUS_PREPARANDO: 0,
        STATUS_PRONTO: 0
    }
    
    for row in rows:
        counts[row['status']] = row['count']
    
    return counts


def clear_old_orders(hours: int = 24) -> int:
    """
    Remove pedidos finalizados mais antigos que o número de horas especificado.
    
    Args:
        hours: Número de horas para manter pedidos finalizados
        
    Returns:
        Número de pedidos removidos
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM orders 
        WHERE status IN ('saiu', 'cancelado')
        AND datetime(updated_at) < datetime('now', ? || ' hours')
    """, (f"-{hours}",))
    
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    
    return deleted


# Inicializa o banco de dados ao importar o módulo
init_db()
