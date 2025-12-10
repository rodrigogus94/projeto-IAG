"""
Estilos CSS customizados para a aplicação Streamlit
"""
CUSTOM_CSS = """
    <style>
    /* Ajustes gerais de dimensões */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    [data-testid="stSidebar"] {
        min-width: 380px;
        max-width: 420px;
    }
    
    /* Estilo para o header da sidebar */
    .sidebar-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.8rem 1.5rem;
        border-radius: 0;
        margin: -1rem -1rem 1.5rem -1rem;
        color: white;
    }
    
    .sidebar-title {
        font-size: 1.6rem;
        font-weight: bold;
        color: white;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    
    .sidebar-subtitle {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.6rem;
    }
    
    /* Estilo para mensagem de boas-vindas */
    .welcome-message {
        background: white;
        padding: 1.6rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1.2rem 0;
        border-left: 4px solid #667eea;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Estilo para área principal vazia */
    .empty-dashboard {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 75vh;
        min-height: 500px;
        text-align: center;
        padding: 3rem 2rem;
    }
    
    .dashboard-icon {
        width: 240px;
        height: 180px;
        margin: 2.5rem auto;
        opacity: 0.35;
    }
    
    .dashboard-icon svg {
        width: 100%;
        height: 100%;
    }
    
    .empty-text {
        color: #666;
        font-size: 1.4rem;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .empty-text-secondary {
        color: #999;
        font-size: 1.1rem;
        margin-top: 0.8rem;
    }
    
    /* Estilo para mensagens do chat */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.6rem 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Status do sistema na sidebar */
    .status-container {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 10px;
        margin-top: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    .status-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0;
        border-bottom: 1px solid #e8e8e8;
    }
    
    .status-item:last-child {
        border-bottom: none;
    }
    
    .status-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    .status-value {
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Botão roxo customizado */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        transform: translateY(-1px);
    }
    
     /* Input customizado */
     .stTextInput > div > div > input {
         border-radius: 10px;
         border: 2px solid #e0e0e0;
         padding: 0.7rem 1rem;
         font-size: 0.95rem;
         transition: border-color 0.3s ease;
     }
     
     .stTextInput > div > div > input:focus {
         border-color: #667eea;
         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
     }
     
     /* Estilo do prompt moderno (escuro) */
     .modern-prompt-wrapper {
         position: relative;
         display: flex;
         align-items: center;
         background: #2d2d2d;
         border-radius: 50px;
         padding: 0.5rem 1rem;
         box-shadow: 0 4px 12px rgba(0,0,0,0.2);
         width: 100%;
         max-width: 900px;
         margin: 0 auto;
         gap: 0.5rem;
     }
     
     /* Estilizar o input do Streamlit dentro do wrapper */
     .modern-prompt-wrapper [data-testid="stTextInput"] > div > div > input {
         background: transparent !important;
         border: none !important;
         color: #e0e0e0 !important;
         font-size: 1rem;
         padding: 0.8rem 0.5rem !important;
         box-shadow: none !important;
     }
     
     .modern-prompt-wrapper [data-testid="stTextInput"] > div > div > input::placeholder {
         color: #999 !important;
     }
     
     .modern-prompt-wrapper [data-testid="stTextInput"] > div > div > input:focus {
         border: none !important;
         box-shadow: none !important;
         outline: none !important;
     }
     
     /* Botão de enviar integrado */
     .modern-prompt-wrapper [data-testid="stButton"] > button {
         background: transparent !important;
         border: none !important;
         color: #999 !important;
         padding: 0.5rem 0.8rem !important;
         min-width: auto !important;
         width: auto !important;
         box-shadow: none !important;
         font-size: 1.3rem;
         border-radius: 50% !important;
     }
     
     .modern-prompt-wrapper [data-testid="stButton"] > button:hover {
         color: #667eea !important;
         background: rgba(102, 126, 234, 0.1) !important;
         transform: scale(1.1);
     }
     
     /* Ajustar colunas dentro do wrapper */
     .modern-prompt-wrapper [data-testid="column"] {
         padding: 0 !important;
     }
    
    /* Ajustes de espaçamento na sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.8rem;
    }
    
    /* Melhorar espaçamento dos elementos */
    .element-container {
        margin-bottom: 1rem;
    }
    
     /* Prompt no centro da tela */
     .center-prompt-container {
         position: fixed;
         bottom: 0;
         left: 0;
         right: 0;
         background: rgba(0,0,0,0.9);
         padding: 1.5rem 2rem;
         z-index: 999;
         display: flex;
         justify-content: center;
         align-items: center;
         backdrop-filter: blur(10px);
     }
    
    /* Quando sidebar está escondida, mostrar prompt no centro automaticamente */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .sidebar-prompt {
        display: none !important;
    }
    
    /* Ajustar padding do main quando prompt está no centro */
    .main .block-container {
        transition: padding-bottom 0.3s ease;
    }
    
    /* Ocultar prompt da sidebar quando está no centro */
    .sidebar-prompt {
        display: block;
    }
    
     /* Estilizar botões de ação com gradiente - apenas ícones */
     button[key="btn_regenerar"],
     button[key="btn_copiar"],
     button[key="btn_limpar"] {
         background: linear-gradient(90deg, #1e3a8a 0%, #7c3aed 100%) !important;
         border: none !important;
         border-radius: 10px !important;
         color: white !important;
         font-size: 1.2rem !important;
         padding: 0.5rem 0.8rem !important;
         min-width: 45px !important;
         width: 45px !important;
         height: 45px !important;
         transition: all 0.3s ease !important;
         display: flex !important;
         align-items: center !important;
         justify-content: center !important;
         position: relative !important;
         cursor: pointer !important;
     }
     
     button[key="btn_regenerar"]:hover,
     button[key="btn_copiar"]:hover,
     button[key="btn_limpar"]:hover {
         transform: translateY(-2px) !important;
         box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4) !important;
     }
     
     /* Estilo para o indicador de pensando */
     .thinking-indicator {
         order: -1000 !important;
         margin-bottom: 0.5rem !important;
         opacity: 0.8 !important;
         font-style: italic !important;
         display: block !important;
     }
     
     /* Reorganizar mensagens do assistente para mostrar "Pensando..." acima */
     [data-testid="stChatMessage"] {
         display: flex !important;
         flex-direction: column !important;
     }
     
     /* Container do chat message do assistente */
     [data-testid="stChatMessage"] [data-testid="stVerticalBlock"],
     [data-testid="stChatMessage"] > div {
         display: flex !important;
         flex-direction: column !important;
     }
     
     /* Garantir que elementos possam ser reordenados */
     [data-testid="stChatMessage"] [data-testid="stVerticalBlock"] > div,
     [data-testid="stChatMessage"] > div > div {
         position: relative;
     }
     
     /* Indicador de pensando acima do prompt */
     .thinking-above-prompt {
         background: rgba(102, 126, 234, 0.1);
         border-left: 3px solid #667eea;
         padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        border-radius: 8px;
        color: #667eea;
        font-style: italic;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Ocultar elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
     </style>
     """

