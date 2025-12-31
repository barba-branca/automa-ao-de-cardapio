# Saka Delivery KDS

🍨 **Kitchen Display System para Loja de Açaí**

Sistema de gerenciamento de pedidos centralizado para cozinha, exibindo pedidos de múltiplas plataformas (iFood, 99Food, WhatsApp) em uma única interface otimizada para TV.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-red.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-green.svg)

## 📸 Screenshot

*Interface dark mode otimizada para TV com alto contraste*

## ✨ Funcionalidades

- 🌙 **Tema Dark** - Otimizado para TV com fontes grandes e alto contraste
- 🎨 **Status Visual** - Cores diferenciadas por status (Novo/Preparando/Pronto/Saiu)
- 📱 **Multi-plataforma** - Centraliza pedidos de iFood, 99Food e WhatsApp
- ⏱️ **Tempo Real** - Mostra tempo decorrido desde cada pedido
- 🔄 **Auto-refresh** - Atualiza automaticamente a cada 30 segundos
- 💾 **Persistência** - Armazena pedidos localmente com SQLite

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9+
- pip

### Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/saka-delivery-kds.git
cd saka-delivery-kds

# Instale as dependências
pip install streamlit

# Execute a aplicação
streamlit run app.py
```

### Acesso

Abra o navegador em: **http://localhost:8501**

## 🎮 Modo Debug

Use a barra lateral para simular pedidos de diferentes plataformas:

- 🔴 Simular Pedido iFood
- 🟡 Simular Pedido 99Food
- 🟢 Simular WhatsApp (IA)

## 📊 Cores por Status

| Status | Cor | Significado |
|--------|-----|-------------|
| 🔔 Novo | Vermelho | Aguardando confirmação |
| 👨‍🍳 Preparando | Laranja | Em preparo na cozinha |
| ✅ Pronto | Verde | Aguardando entrega |
| 🚀 Saiu | Azul | Saiu para entrega |

## 📁 Estrutura

```
saka-delivery-kds/
├── app.py           # Interface Streamlit
├── database.py      # Módulo SQLite (CRUD)
├── README.md        # Documentação
└── .gitignore       # Arquivos ignorados
```

## 🛠️ Tecnologias

- **Frontend/Backend**: Python + Streamlit
- **Banco de Dados**: SQLite3
- **Estilo**: CSS customizado (dark theme)

## 📄 Licença

MIT License - Uso livre para fins comerciais e pessoais.

---

Desenvolvido com 💜 para **SAKA DELIVERY**
