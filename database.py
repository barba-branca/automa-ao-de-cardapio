"""
Saka Delivery KDS - Módulo de Banco de Dados
Gerencia persistência de pedidos usando PostgreSQL
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from datetime import datetime
from typing import Optional, Generator
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

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


@contextmanager
def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """Context manager para conexão com o banco de dados PostgreSQL."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        dbname=os.getenv("DB_NAME", "saka_delivery"),
        port=os.getenv("DB_PORT", "5432")
    )
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Inicializa o banco de dados e cria as tabelas necessárias."""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        source TEXT NOT NULL,
                        client_name TEXT NOT NULL,
                        description TEXT NOT NULL,
                        status TEXT NOT NULL DEFAULT 'novo',
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NOT NULL
                    )
                """)

                # Índice para otimizar busca por status
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)
                """)
            conn.commit()
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        # Em ambiente de desenvolvimento sem banco, pode falhar silenciosamente ou levantar erro
        # Aqui optamos por apenas logar se for importado, mas se chamado explicitamente deve falhar
        raise e


def create_order(source: str, client_name: str, description: str) -> int:
    """
    Cria um novo pedido no banco de dados.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            now = datetime.now()

            cursor.execute("""
                INSERT INTO orders (source, client_name, description, status, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (source, client_name, description, STATUS_NOVO, now, now))

            order_id = cursor.fetchone()[0]
        conn.commit()
    
    return order_id


def get_all_orders(include_finished: bool = False) -> list[dict]:
    """
    Retorna todos os pedidos ativos.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
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
            return [dict(row) for row in rows]


def get_order_by_id(order_id: int) -> Optional[dict]:
    """
    Busca um pedido específico pelo ID.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            row = cursor.fetchone()
            return dict(row) if row else None


def update_order_status(order_id: int, new_status: str) -> bool:
    """
    Atualiza o status de um pedido.
    """
    valid_statuses = [STATUS_NOVO, STATUS_PREPARANDO, STATUS_PRONTO, STATUS_SAIU, STATUS_CANCELADO]
    
    if new_status not in valid_statuses:
        return False
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            now = datetime.now()

            cursor.execute("""
                UPDATE orders
                SET status = %s, updated_at = %s
                WHERE id = %s
            """, (new_status, now, order_id))

            success = cursor.rowcount > 0
        conn.commit()
    
    return success


def delete_order(order_id: int) -> bool:
    """
    Remove um pedido do banco de dados.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
            success = cursor.rowcount > 0
        conn.commit()
    
    return success


def get_orders_count_by_status() -> dict[str, int]:
    """
    Retorna a contagem de pedidos por status.
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM orders
                WHERE status NOT IN ('saiu', 'cancelado')
                GROUP BY status
            """)

            rows = cursor.fetchall()

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
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # PostgreSQL syntax: NOW() - INTERVAL '1 hour' * param
            cursor.execute("""
                DELETE FROM orders
                WHERE status IN ('saiu', 'cancelado')
                AND updated_at < NOW() - INTERVAL '1 hour' * %s
            """, (hours,))

            deleted = cursor.rowcount
        conn.commit()
    
    return deleted
