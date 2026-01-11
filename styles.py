"""
Saka Delivery KDS - Styles
Módulo de estilos CSS para o Streamlit
"""

def get_css():
    return """
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
"""
