# Saka Delivery KDS

🍨 **Kitchen Display System para Loja de Açaí**

Sistema de gerenciamento de pedidos centralizado para cozinha, exibindo pedidos de múltiplas plataformas (iFood, 99Food, WhatsApp) em uma única interface otimizada para TV.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)

## 📸 Screenshot

*Interface dark mode otimizada para TV com alto contraste*

## ✨ Funcionalidades

- 🌙 **Tema Dark** - Otimizado para TV com fontes grandes e alto contraste
- 🎨 **Status Visual** - Cores diferenciadas por status (Novo/Preparando/Pronto/Saiu)
- 📱 **Multi-plataforma** - Centraliza pedidos de iFood, 99Food e WhatsApp
- ⏱️ **Tempo Real** - Mostra tempo decorrido desde cada pedido
- 🔄 **Auto-refresh** - Atualiza automaticamente a cada 30 segundos
- 💾 **Persistência** - Armazena pedidos em banco de dados PostgreSQL

## 🚀 Como Executar

### Pré-requisitos

- Python 3.9+
- pip
- Servidor PostgreSQL

### Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto com as credenciais do seu banco de dados:

```ini
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_NAME=saka_delivery
DB_PORT=5432
```

### Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/saka-delivery-kds.git
cd saka-delivery-kds

# Instale as dependências
pip install -r requirements.txt

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
├── app.py           # Interface Streamlit (View)
├── database.py      # Módulo PostgreSQL (Model)
├── services.py      # Lógica de simulação e serviços
├── styles.py        # Definições de CSS
├── tests/           # Testes automatizados
├── requirements.txt # Dependências do projeto
├── README.md        # Documentação
└── .gitignore       # Arquivos ignorados
```

## 🛠️ Tecnologias

- **Frontend**: Python + Streamlit
- **Backend**: Python
- **Banco de Dados**: PostgreSQL
- **Estilo**: CSS customizado (dark theme)

## 📝 Histórico de Alterações

**Atualização Recente (Refatoração & PostgreSQL)**

O projeto passou por uma reestruturação completa para atender a padrões de engenharia de software mais robustos:

1.  **Migração de Banco de Dados**: Substituição do SQLite pelo **PostgreSQL** para maior escalabilidade e robustez em produção.
2.  **Arquitetura Modular**:
    *   Separação de estilos em `styles.py`.
    *   Extração de lógica de negócios para `services.py`.
    *   Implementação de padrão Context Manager para conexões de banco de dados.
3.  **Testes**: Adição de suíte de testes unitários (mockados) para validação segura da lógica de banco de dados.
4.  **Configuração**: Suporte a variáveis de ambiente (.env).

## 📄 Licença

MIT License - Uso livre para fins comerciais e pessoais.

---

Desenvolvido com 💜 para **SAKA DELIVERY**
