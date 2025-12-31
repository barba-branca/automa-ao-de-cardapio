"""
🍨 SAKA DELIVERY - Kitchen Display System (KDS)
Sistema de gerenciamento de pedidos para loja de Açaí
Otimizado para TV com tema escuro e fontes grandes
"""

import streamlit as st
import random
from datetime import datetime
from time import sleep

# Importa funções do banco de dados
import database as db

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="SAKA DELIVERY - KDS",
    page_icon="🍨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# ESTILOS CSS - TEMA DARK OTIMIZADO PARA TV
# ============================================================================

st.markdown("""
<style>
    /* ===== RESET E BASE ===== */
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Ocultar elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== TIPOGRAFIA ===== */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
    
    /* ===== HEADER PRINCIPAL ===== */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px 40px;
        border-radius: 16px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }
    
    .main-header .subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    .clock {
        color: white;
        font-size: 2rem;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* ===== CARDS DE MÉTRICAS ===== */
    .metric-card {
        background: linear-gradient(145deg, #1e2530 0%, #252d3a 100%);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    
    .metric-card.novo {
        border-left: 4px solid #FF4B4B;
    }
    
    .metric-card.preparando {
        border-left: 4px solid #FFA500;
    }
    
    .metric-card.pronto {
        border-left: 4px solid #00D26A;
    }
    
    .metric-number {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 10px 0;
    }
    
    .metric-number.novo { color: #FF4B4B; }
    .metric-number.preparando { color: #FFA500; }
    .metric-number.pronto { color: #00D26A; }
    
    .metric-label {
        color: #8892a0;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* ===== CARDS DE PEDIDOS ===== */
    .order-card {
        background: linear-gradient(145deg, #1e2530 0%, #252d3a 100%);
        border-radius: 16px;
        padding: 20px 25px;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .order-card:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    }
    
    .order-card.status-novo {
        border-left: 5px solid #FF4B4B;
        background: linear-gradient(145deg, #2a1f1f 0%, #1e2530 100%);
    }
    
    .order-card.status-preparando {
        border-left: 5px solid #FFA500;
        background: linear-gradient(145deg, #2a2a1f 0%, #1e2530 100%);
    }
    
    .order-card.status-pronto {
        border-left: 5px solid #00D26A;
        background: linear-gradient(145deg, #1f2a1f 0%, #1e2530 100%);
    }
    
    .order-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .order-id {
        font-size: 1.8rem;
        font-weight: 800;
        color: white;
    }
    
    .order-source {
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
    }
    
    .source-ifood {
        background: linear-gradient(135deg, #EA1D2C 0%, #B71C1C 100%);
        color: white;
    }
    
    .source-99food {
        background: linear-gradient(135deg, #FFCA28 0%, #F57C00 100%);
        color: #1a1a1a;
    }
    
    .source-whatsapp {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white;
    }
    
    .order-client {
        color: #a0aec0;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    .order-description {
        color: white;
        font-size: 1.4rem;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    
    .order-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .order-time {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .time-icon {
        font-size: 1.3rem;
    }
    
    .time-value {
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .time-value.urgent {
        color: #FF4B4B;
        animation: pulse 1s infinite;
    }
    
    .time-value.warning {
        color: #FFA500;
    }
    
    .time-value.normal {
        color: #00D26A;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .status-badge {
        padding: 10px 20px;
        border-radius: 25px;
        font-weight: 700;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .badge-novo {
        background: rgba(255, 75, 75, 0.2);
        color: #FF4B4B;
        border: 2px solid #FF4B4B;
    }
    
    .badge-preparando {
        background: rgba(255, 165, 0, 0.2);
        color: #FFA500;
        border: 2px solid #FFA500;
    }
    
    .badge-pronto {
        background: rgba(0, 210, 106, 0.2);
        color: #00D26A;
        border: 2px solid #00D26A;
    }
    
    /* ===== BOTÕES DE AÇÃO ===== */
    .stButton > button {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: none;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* ===== SIDEBAR DEBUG ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 10px;
    }
    
    /* ===== SEÇÃO VAZIA ===== */
    .empty-state {
        text-align: center;
        padding: 80px 40px;
        background: linear-gradient(145deg, #1e2530 0%, #252d3a 100%);
        border-radius: 20px;
        border: 2px dashed rgba(255,255,255,0.2);
    }
    
    .empty-state .icon {
        font-size: 5rem;
        margin-bottom: 20px;
    }
    
    .empty-state h2 {
        color: #a0aec0;
        font-size: 1.8rem;
        margin-bottom: 10px;
    }
    
    .empty-state p {
        color: #6c7a89;
        font-size: 1.2rem;
    }
    
    /* ===== DIVIDER ===== */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def format_elapsed_time(created_at: str) -> tuple[str, str]:
    """
    Calcula e formata o tempo decorrido desde a criação do pedido.
    
    Returns:
        Tupla com (tempo_formatado, classe_css)
    """
    try:
        created = datetime.fromisoformat(created_at)
        elapsed = datetime.now() - created
        
        total_minutes = int(elapsed.total_seconds() / 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0:
            time_str = f"{hours}h {minutes}min"
        else:
            time_str = f"{minutes}min"
        
        # Define classe CSS baseada no tempo
        if total_minutes >= 30:
            css_class = "urgent"
        elif total_minutes >= 15:
            css_class = "warning"
        else:
            css_class = "normal"
            
        return time_str, css_class
    except:
        return "0min", "normal"


def get_source_class(source: str) -> str:
    """Retorna a classe CSS para a fonte do pedido."""
    return f"source-{source}"


def get_status_badge_class(status: str) -> str:
    """Retorna a classe CSS para o badge de status."""
    return f"badge-{status}"


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


# ============================================================================
# SIDEBAR - PAINEL DEBUG
# ============================================================================

with st.sidebar:
    st.markdown("## 🔧 Painel Debug")
    st.markdown("---")
    st.markdown("### Simular Pedidos")
    
    if st.button("🔴 Simular Pedido iFood", use_container_width=True):
        simulate_ifood_order()
        st.toast("✅ Pedido iFood simulado!", icon="🔴")
        sleep(0.3)
        st.rerun()
    
    if st.button("🟡 Simular Pedido 99Food", use_container_width=True):
        simulate_99food_order()
        st.toast("✅ Pedido 99Food simulado!", icon="🟡")
        sleep(0.3)
        st.rerun()
    
    if st.button("🟢 Simular WhatsApp (IA)", use_container_width=True):
        simulate_whatsapp_order()
        st.toast("✅ Pedido WhatsApp simulado!", icon="🟢")
        sleep(0.3)
        st.rerun()
    
    st.markdown("---")
    st.markdown("### Configurações")
    
    show_finished = st.checkbox("Mostrar finalizados", value=False)
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=True)
    
    st.markdown("---")
    st.markdown("### Manutenção")
    
    if st.button("🗑️ Limpar Finalizados", use_container_width=True):
        deleted = db.clear_old_orders(hours=0)
        st.toast(f"🗑️ {deleted} pedidos removidos", icon="✅")
        sleep(0.3)
        st.rerun()

# ============================================================================
# HEADER PRINCIPAL COM RELÓGIO AO VIVO (COMPONENT)
# ============================================================================

current_date = datetime.now().strftime("%d/%m/%Y")

# Usamos um componente HTML dedicado para garantir que o JS execute sem bloqueios
import streamlit.components.v1 as components

header_html = f"""
<div style="
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 20px 40px;
    border-radius: 16px;
    margin-bottom: 10px;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
">
    <div>
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800; letter-spacing: 2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🍨 SAKA DELIVERY</h1>
        <p style="margin: 0; font-size: 1.1rem; color: rgba(255,255,255,0.9);">Kitchen Display System - Açaí & Delivery</p>
    </div>
    <div style="text-align: right;">
        <div id="live-clock" style="font-size: 2.5rem; font-weight: 600; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">--:--:--</div>
        <div style="font-size: 1.1rem; color: rgba(255,255,255,0.9);">{current_date}</div>
    </div>
</div>

<script>
    function updateClock() {{
        const now = new Date();
        const hrs = String(now.getHours()).padStart(2, '0');
        const mins = String(now.getMinutes()).padStart(2, '0');
        const secs = String(now.getSeconds()).padStart(2, '0');
        document.getElementById('live-clock').innerText = hrs + ':' + mins + ':' + secs;
    }}
    setInterval(updateClock, 1000);
    updateClock();
</script>
"""

# Renderiza o header. Altura de 140px é suficiente para evitar rolagem interna no componente
components.html(header_html, height=150)


# ============================================================================
# MÉTRICAS - CONTADORES DE STATUS
# ============================================================================

counts = db.get_orders_count_by_status()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card novo">
        <div class="metric-label">🔔 Novos Pedidos</div>
        <div class="metric-number novo">{counts.get(db.STATUS_NOVO, 0)}</div>
        <div class="metric-label">Aguardando confirmação</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card preparando">
        <div class="metric-label">👨‍🍳 Em Preparo</div>
        <div class="metric-number preparando">{counts.get(db.STATUS_PREPARANDO, 0)}</div>
        <div class="metric-label">Na cozinha</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card pronto">
        <div class="metric-label">✅ Prontos</div>
        <div class="metric-number pronto">{counts.get(db.STATUS_PRONTO, 0)}</div>
        <div class="metric-label">Aguardando entrega</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================================
# LISTA DE PEDIDOS
# ============================================================================

orders = db.get_all_orders(include_finished=show_finished)

if not orders:
    st.markdown("""
    <div class="empty-state">
        <div class="icon">🍨</div>
        <h2>Nenhum pedido no momento</h2>
        <p>Use o painel Debug na barra lateral para simular novos pedidos</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for order in orders:
        order_id = order['id']
        source = order['source']
        client = order['client_name']
        description = order['description']
        status = order['status']
        created_at = order['created_at']
        
        elapsed_time, time_class = format_elapsed_time(created_at)
        
        # Emoji da fonte
        source_emoji = {"ifood": "🔴", "99food": "🟡", "whatsapp": "🟢"}.get(source, "⚪")
        source_label = {"ifood": "iFood", "99food": "99Food", "whatsapp": "WhatsApp"}.get(source, source)
        
        # Status labels
        status_labels = {
            "novo": "🔔 NOVO",
            "preparando": "👨‍🍳 PREPARANDO", 
            "pronto": "✅ PRONTO",
            "saiu": "🚀 SAIU",
            "cancelado": "❌ CANCELADO"
        }
        
        # Card do pedido
        st.markdown(f"""
        <div class="order-card status-{status}">
            <div class="order-header">
                <span class="order-id">#{order_id:03d}</span>
                <span class="order-source {get_source_class(source)}">{source_emoji} {source_label}</span>
            </div>
            <div class="order-client">👤 {client}</div>
            <div class="order-description">{description}</div>
            <div class="order-footer">
                <div class="order-time">
                    <span class="time-icon">⏱️</span>
                    <span class="time-value {time_class}">{elapsed_time}</span>
                </div>
                <span class="status-badge {get_status_badge_class(status)}">{status_labels.get(status, status)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Botões de ação
        if status not in ["saiu", "cancelado"]:
            cols = st.columns(4)
            
            with cols[0]:
                if status == "novo":
                    if st.button("🔄 Confirmar", key=f"confirm_{order_id}", use_container_width=True):
                        db.update_order_status(order_id, db.STATUS_PREPARANDO)
                        st.toast(f"Pedido #{order_id} confirmado!", icon="🔄")
                        sleep(0.3)
                        st.rerun()
            
            with cols[1]:
                if status == "preparando":
                    if st.button("✅ Pronto", key=f"ready_{order_id}", use_container_width=True):
                        db.update_order_status(order_id, db.STATUS_PRONTO)
                        st.toast(f"Pedido #{order_id} pronto!", icon="✅")
                        sleep(0.3)
                        st.rerun()
            
            with cols[2]:
                if status == "pronto":
                    if st.button("🚀 Saiu", key=f"out_{order_id}", use_container_width=True):
                        db.update_order_status(order_id, db.STATUS_SAIU)
                        st.toast(f"Pedido #{order_id} saiu para entrega!", icon="🚀")
                        sleep(0.3)
                        st.rerun()
            
            with cols[3]:
                if st.button("❌ Cancelar", key=f"cancel_{order_id}", use_container_width=True):
                    db.update_order_status(order_id, db.STATUS_CANCELADO)
                    st.toast(f"Pedido #{order_id} cancelado", icon="❌")
                    sleep(0.3)
                    st.rerun()
        
        st.markdown("---")

# ============================================================================
# AUTO-REFRESH
# ============================================================================

if auto_refresh:
    sleep(30)
    st.rerun()
