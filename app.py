"""
🍨 SAKA DELIVERY - Kitchen Display System (KDS)
Sistema de gerenciamento de pedidos para loja de Açaí
Otimizado para TV com tema escuro e fontes grandes
"""

import streamlit as st
from datetime import datetime
from time import sleep

# Importa funções do banco de dados e serviços
import database as db
import styles
import services

# Initialize database
db.init_db()

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

st.markdown(styles.get_css(), unsafe_allow_html=True)

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


# ============================================================================
# SIDEBAR - PAINEL DEBUG
# ============================================================================

with st.sidebar:
    st.markdown("## 🔧 Painel Debug")
    st.markdown("---")
    st.markdown("### Simular Pedidos")
    
    if st.button("🔴 Simular Pedido iFood", use_container_width=True):
        services.simulate_ifood_order()
        st.toast("✅ Pedido iFood simulado!", icon="🔴")
        sleep(0.3)
        st.rerun()
    
    if st.button("🟡 Simular Pedido 99Food", use_container_width=True):
        services.simulate_99food_order()
        st.toast("✅ Pedido 99Food simulado!", icon="🟡")
        sleep(0.3)
        st.rerun()
    
    if st.button("🟢 Simular WhatsApp (IA)", use_container_width=True):
        services.simulate_whatsapp_order()
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
