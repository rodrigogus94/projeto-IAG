"""
Estilos CSS customizados para a aplicação Streamlit
"""
CUSTOM_CSS = """
    <style>
    /* Ajustes gerais de dimensões - FORÇAR RESPONSIVIDADE */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        transition: max-width 0.3s ease, padding 0.3s ease, width 0.3s ease;
        width: 100%;
        box-sizing: border-box;
    }
    
    /* Quando sidebar está visível */
    [data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
        max-width: calc(1400px - 420px);
        width: calc(100% - 420px);
    }
    
    /* Quando sidebar está escondida, usar TODA a largura disponível */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container,
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .block-container * {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        box-sizing: border-box !important;
    }
    
    /* Forçar ajuste quando sidebar escondida - TODOS os elementos */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main {
        margin-left: 0 !important;
        margin-right: 0 !important;
        width: 100vw !important;
        max-width: 100vw !important;
        left: 0 !important;
        right: 0 !important;
    }
    
    /* Ajustar elementos dentro da área principal */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main [data-testid="stVerticalBlock"],
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main [data-testid="stVerticalBlock"] > div {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    
    [data-testid="stSidebar"] {
        min-width: 380px;
        max-width: 420px;
        transition: transform 0.3s ease, visibility 0.3s ease;
    }
    
    /* Garantir que a área principal se ajuste */
    .main {
        transition: margin-left 0.3s ease, width 0.3s ease, max-width 0.3s ease;
        box-sizing: border-box;
    }
    
    /* Quando sidebar escondida, área principal ocupa toda largura */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main {
        margin-left: 0 !important;
        width: 100vw !important;
        max-width: 100vw !important;
    }
    
    /* Forçar ajuste de todos os containers quando sidebar escondida */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .element-container,
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main [class*="container"],
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main [class*="block"] {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
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
        width: 100%;
        transition: width 0.3s ease;
    }
    
    /* Ajustar área vazia quando sidebar escondida */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .empty-dashboard {
        width: 100%;
        max-width: 100%;
    }
    
    /* Ajustar gráficos e visualizações quando sidebar escondida */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main [data-testid="stPlotlyChart"] {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ajustar containers de resposta quando sidebar escondida */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main .element-container {
        width: 100% !important;
        max-width: 100% !important;
    }
    
    /* Ajustar colunas quando sidebar escondida */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main [data-testid="column"] {
        width: 100% !important;
    }
    
    /* Garantir que chat messages se ajustem */
    [data-testid="stSidebar"][aria-expanded="false"] ~ .main [data-testid="stChatMessage"] {
        width: 100% !important;
        max-width: 100% !important;
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
    
    /* ============================================================================
       MEDIA QUERIES - RESPONSIVIDADE
       ============================================================================ */
    
    /* Tablets e telas médias (768px - 1024px) */
    @media screen and (max-width: 1024px) {
        .main .block-container {
            max-width: 100% !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
        
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 350px !important;
        }
        
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
            max-width: calc(100% - 350px) !important;
            width: calc(100% - 350px) !important;
        }
        
        .sidebar-header {
            padding: 1.2rem 1rem !important;
        }
        
        .sidebar-title {
            font-size: 1.3rem !important;
        }
        
        .empty-dashboard {
            padding: 2rem 1rem !important;
        }
        
        .dashboard-icon {
            width: 180px !important;
            height: 135px !important;
        }
    }
    
    /* Tablets pequenos e mobile landscape (600px - 768px) */
    @media screen and (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
        }
        
        [data-testid="stSidebar"] {
            min-width: 280px !important;
            max-width: 320px !important;
        }
        
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main .block-container {
            max-width: calc(100% - 320px) !important;
            width: calc(100% - 320px) !important;
        }
        
        .sidebar-header {
            padding: 1rem 0.8rem !important;
        }
        
        .sidebar-title {
            font-size: 1.2rem !important;
        }
        
        .sidebar-subtitle {
            font-size: 0.85rem !important;
        }
        
        .welcome-message {
            padding: 1.2rem !important;
            font-size: 0.9rem !important;
        }
        
        .empty-dashboard {
            height: 60vh !important;
            min-height: 400px !important;
            padding: 1.5rem 1rem !important;
        }
        
        .empty-text {
            font-size: 1.2rem !important;
        }
        
        .empty-text-secondary {
            font-size: 1rem !important;
        }
        
        .dashboard-icon {
            width: 150px !important;
            height: 112px !important;
        }
        
        .chat-message {
            padding: 0.8rem !important;
            font-size: 0.85rem !important;
        }
        
        .status-container {
            padding: 1rem !important;
        }
        
        .status-item {
            padding: 0.5rem 0 !important;
        }
        
        .status-label,
        .status-value {
            font-size: 0.85rem !important;
        }
    }
    
    /* Mobile (até 600px) */
    @media screen and (max-width: 600px) {
        /* Forçar sidebar a ser overlay em mobile */
        [data-testid="stSidebar"] {
            position: fixed !important;
            z-index: 1000 !important;
            height: 100vh !important;
            min-width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Quando sidebar está aberta em mobile, esconder main */
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main {
            opacity: 0.3 !important;
            pointer-events: none !important;
        }
        
        /* Main sempre ocupa 100% em mobile quando sidebar fechada */
        [data-testid="stSidebar"][aria-expanded="false"] ~ .main,
        .main {
            width: 100% !important;
            max-width: 100% !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }
        
        .main .block-container {
            max-width: 100% !important;
            width: 100% !important;
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
        
        .sidebar-header {
            padding: 1rem 0.8rem !important;
        }
        
        .sidebar-title {
            font-size: 1.1rem !important;
        }
        
        .sidebar-subtitle {
            font-size: 0.8rem !important;
        }
        
        .welcome-message {
            padding: 1rem !important;
            font-size: 0.85rem !important;
            margin: 0.8rem 0 !important;
        }
        
        .empty-dashboard {
            height: 50vh !important;
            min-height: 300px !important;
            padding: 1rem 0.5rem !important;
        }
        
        .empty-text {
            font-size: 1rem !important;
            margin: 0.8rem 0 !important;
        }
        
        .empty-text-secondary {
            font-size: 0.9rem !important;
            margin-top: 0.5rem !important;
        }
        
        .dashboard-icon {
            width: 120px !important;
            height: 90px !important;
            margin: 1.5rem auto !important;
        }
        
        .chat-message {
            padding: 0.6rem !important;
            font-size: 0.8rem !important;
            margin: 0.4rem 0 !important;
        }
        
        .status-container {
            padding: 0.8rem !important;
        }
        
        .status-item {
            padding: 0.4rem 0 !important;
            flex-direction: column !important;
            align-items: flex-start !important;
        }
        
        .status-label,
        .status-value {
            font-size: 0.8rem !important;
        }
        
        /* Ajustar botões em mobile */
        .stButton > button {
            padding: 0.5rem 1rem !important;
            font-size: 0.85rem !important;
        }
        
        /* Ajustar inputs em mobile */
        .stTextInput > div > div > input {
            padding: 0.6rem 0.8rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Ajustar chat input em mobile */
        [data-testid="stChatInput"] {
            width: 100% !important;
            padding: 0.5rem !important;
        }
        
        /* Ajustar gráficos em mobile */
        [data-testid="stPlotlyChart"] {
            width: 100% !important;
            overflow-x: auto !important;
        }
        
        /* Ajustar colunas em mobile - empilhar verticalmente */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    
    /* Mobile muito pequeno (até 400px) */
    @media screen and (max-width: 400px) {
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        .sidebar-header {
            padding: 0.8rem 0.6rem !important;
        }
        
        .sidebar-title {
            font-size: 1rem !important;
        }
        
        .empty-dashboard {
            padding: 0.8rem 0.3rem !important;
        }
        
        .empty-text {
            font-size: 0.9rem !important;
        }
        
        .empty-text-secondary {
            font-size: 0.85rem !important;
        }
        
        .dashboard-icon {
            width: 100px !important;
            height: 75px !important;
        }
    }
    
    /* Garantir que elementos se ajustem em todas as telas */
    * {
        box-sizing: border-box;
    }
    
    /* Prevenir overflow horizontal */
    body, html {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    
    /* Garantir que imagens sejam responsivas */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
    
    /* Garantir que tabelas sejam responsivas */
    table {
        width: 100% !important;
        display: block !important;
        overflow-x: auto !important;
    }
     </style>
     """

