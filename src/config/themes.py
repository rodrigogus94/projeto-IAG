"""
Módulo de temas para a aplicação
Gerencia os temas claro e escuro com cores consistentes e transições suaves
"""

# ============================================================================
# PALETAS DE CORES
# ============================================================================

# Tema Escuro
DARK_THEME = {
    # Cores principais
    "bg_primary": "#1e1e1e",  # Fundo principal
    "bg_secondary": "#2d2d2d",  # Fundo secundário (sidebar)
    "bg_tertiary": "#3d3d3d",  # Fundo terciário (cards, inputs)
    "bg_hover": "#4d4d4d",  # Hover states
    # Cores de texto
    "text_primary": "#e0e0e0",  # Texto principal
    "text_secondary": "#b0b0b0",  # Texto secundário
    "text_tertiary": "#888888",  # Texto terciário (placeholder)
    # Cores de borda
    "border": "#555555",
    "border_light": "#444444",
    # Cores de destaque
    "accent": "#667eea",  # Cor de destaque principal
    "accent_hover": "#764ba2",  # Cor de destaque hover
    "accent_light": "#a0b4ff",  # Cor de destaque clara
    # Cores de mensagens
    "user_message_bg": "#3d3d3d",
    "assistant_message_bg": "#2d4a5e",
    "message_text": "#e0e0e0",
    # Cores de alertas
    "info_bg": "#2d4a5e",
    "success_bg": "#1e4d2e",
    "warning_bg": "#4d3d1e",
    "error_bg": "#4d1e1e",
    # Cores de código
    "code_bg": "#2d2d2d",
    "code_text": "#a0ffa0",
    # Scrollbar
    "scrollbar_track": "#2d2d2d",
    "scrollbar_thumb": "#555555",
    "scrollbar_thumb_hover": "#666666",
}

# Tema Claro
LIGHT_THEME = {
    # Cores principais
    "bg_primary": "#ffffff",  # Fundo principal
    "bg_secondary": "#f8f9fa",  # Fundo secundário (sidebar)
    "bg_tertiary": "#ffffff",  # Fundo terciário (cards, inputs)
    "bg_hover": "#e9ecef",  # Hover states
    # Cores de texto
    "text_primary": "#212529",  # Texto principal
    "text_secondary": "#495057",  # Texto secundário
    "text_tertiary": "#6c757d",  # Texto terciário (placeholder)
    # Cores de borda
    "border": "#dee2e6",
    "border_light": "#e9ecef",
    # Cores de destaque
    "accent": "#667eea",  # Cor de destaque principal
    "accent_hover": "#764ba2",  # Cor de destaque hover
    "accent_light": "#a0b4ff",  # Cor de destaque clara
    # Cores de mensagens
    "user_message_bg": "#f0f0f0",
    "assistant_message_bg": "#e8f4f8",
    "message_text": "#333333",
    # Cores de alertas
    "info_bg": "#d1ecf1",
    "success_bg": "#d4edda",
    "warning_bg": "#fff3cd",
    "error_bg": "#f8d7da",
    # Cores de código
    "code_bg": "#f8f9fa",
    "code_text": "#e83e8c",
    # Scrollbar
    "scrollbar_track": "#f1f1f1",
    "scrollbar_thumb": "#c1c1c1",
    "scrollbar_thumb_hover": "#a8a8a8",
}


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================


def get_theme_colors(theme: str) -> dict:
    """
    Retorna as cores do tema especificado.

    Args:
        theme: "escuro" ou "claro"

    Returns:
        Dicionário com as cores do tema
    """
    if theme == "escuro":
        return DARK_THEME
    else:
        return LIGHT_THEME


def generate_theme_css(theme: str) -> str:
    """
    Gera o CSS completo para o tema especificado.

    Args:
        theme: "escuro" ou "claro"

    Returns:
        String com o CSS completo do tema
    """
    colors = get_theme_colors(theme)

    if theme == "escuro":
        return _generate_dark_theme_css(colors)
    else:
        return _generate_light_theme_css(colors)


def _generate_dark_theme_css(colors: dict) -> str:
    """Gera CSS para tema escuro"""
    return f"""
    <style>
    /* ============================================================
       TEMA ESCURO - Estilos Modernos e Consistentes
       ============================================================ */
    
    /* Transições suaves para mudanças de tema */
    * {{
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
    }}
    
    /* Base - HTML e Body */
    html, body {{
        background-color: {colors['bg_primary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Aplicação principal */
    .stApp {{
        background-color: {colors['bg_primary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Container principal */
    .main .block-container {{
        background-color: {colors['bg_primary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Sidebar completa */
    [data-testid="stSidebar"] {{
        background-color: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    [data-testid="stSidebar"] > div {{
        background-color: {colors['bg_secondary']} !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        background-color: {colors['bg_secondary']} !important;
    }}
    
    /* Texto geral */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .stApp div, .stApp span, .stApp label,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Inputs de texto */
    .stTextInput > div > div > input {{
        background-color: {colors['bg_tertiary']} !important;
        color: {colors['text_primary']} !important;
        border-color: {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {colors['accent']} !important;
        box-shadow: 0 0 0 2px {colors['accent']}33 !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {colors['text_tertiary']} !important;
    }}
    
    /* Selectbox */
    .stSelectbox > div > div {{
        background-color: {colors['bg_tertiary']} !important;
        color: {colors['text_primary']} !important;
        border-color: {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    .stSelectbox > div > div:hover {{
        background-color: {colors['bg_hover']} !important;
    }}
    
    /* Slider */
    .stSlider > div > div {{
        color: {colors['text_primary']} !important;
    }}
    
    .stSlider label {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Mensagens de chat */
    .chat-message {{
        padding: 1rem;
        border-radius: 12px;
        margin: 0.6rem 0;
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .chat-message:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }}
    
    .chat-message.user-message {{
        background-color: {colors['user_message_bg']} !important;
        color: {colors['message_text']} !important;
        border-left: 4px solid {colors['accent']} !important;
    }}
    
    .chat-message.assistant-message {{
        background-color: {colors['assistant_message_bg']} !important;
        color: {colors['message_text']} !important;
        border-left: 4px solid {colors['accent_light']} !important;
    }}
    
    .empty-chat-message {{
        text-align: center;
        color: {colors['text_tertiary']} !important;
        padding: 2.5rem 1rem;
        font-size: 0.95rem;
    }}
    
    /* Mensagem de boas-vindas */
    .welcome-message {{
        background: linear-gradient(135deg, {colors['bg_tertiary']} 0%, {colors['bg_secondary']} 100%) !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid {colors['accent']} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }}
    
    /* Sidebar header */
    .sidebar-header {{
        background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_hover']} 100%) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }}
    
    /* Status container */
    .status-container {{
        background-color: {colors['bg_tertiary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }}
    
    .status-item {{
        border-bottom: 1px solid {colors['border']} !important;
        padding: 0.75rem 0 !important;
        transition: background-color 0.2s ease !important;
    }}
    
    .status-item:hover {{
        background-color: {colors['bg_hover']} !important;
    }}
    
    .status-label {{
        color: {colors['text_secondary']} !important;
        font-weight: 500 !important;
    }}
    
    .status-value {{
        color: {colors['text_primary']} !important;
        font-weight: 600 !important;
    }}
    
    /* Expander */
    [data-testid="stExpander"] {{
        background-color: {colors['bg_secondary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    .streamlit-expanderHeader {{
        background-color: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {colors['bg_hover']} !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Chat messages do Streamlit */
    [data-testid="stChatMessage"] {{
        background-color: transparent !important;
    }}
    
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Área vazia do dashboard */
    .empty-text {{
        color: {colors['text_secondary']} !important;
    }}
    
    .empty-text-secondary {{
        color: {colors['text_tertiary']} !important;
    }}
    
    /* Info boxes */
    .stInfo {{
        background-color: {colors['info_bg']} !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid {colors['accent']} !important;
        border-radius: 8px !important;
    }}
    
    .stInfo > div {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Success boxes */
    .stSuccess {{
        background-color: {colors['success_bg']} !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid #28a745 !important;
        border-radius: 8px !important;
    }}
    
    .stSuccess > div {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Warning boxes */
    .stWarning {{
        background-color: {colors['warning_bg']} !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid #ffc107 !important;
        border-radius: 8px !important;
    }}
    
    .stWarning > div {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Error boxes */
    .stError {{
        background-color: {colors['error_bg']} !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid #dc3545 !important;
        border-radius: 8px !important;
    }}
    
    .stError > div {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Markdown */
    .stMarkdown {{
        color: {colors['text_primary']} !important;
    }}
    
    .stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Indicador de pensando */
    .thinking-above-prompt {{
        background: linear-gradient(90deg, {colors['accent']}33 0%, {colors['accent_hover']}33 100%) !important;
        color: {colors['accent_light']} !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        animation: pulse 2s ease-in-out infinite !important;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    
    /* Chat input */
    [data-testid="stChatInput"] textarea {{
        background-color: {colors['bg_tertiary']} !important;
        color: {colors['text_primary']} !important;
        border-color: {colors['border']} !important;
        border-radius: 12px !important;
    }}
    
    [data-testid="stChatInput"] textarea:focus {{
        border-color: {colors['accent']} !important;
        box-shadow: 0 0 0 2px {colors['accent']}33 !important;
    }}
    
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {colors['text_tertiary']} !important;
    }}
    
    /* Botões */
    .stButton > button {{
        background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_hover']} 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px {colors['accent']}66 !important;
    }}
    
    /* Checkbox */
    .stCheckbox label {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Divider */
    hr {{
        border-color: {colors['border']} !important;
    }}
    
    /* Code blocks */
    code {{
        background-color: {colors['code_bg']} !important;
        color: {colors['code_text']} !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
    }}
    
    pre {{
        background-color: {colors['code_bg']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }}
    
    /* Links */
    a {{
        color: {colors['accent_light']} !important;
        text-decoration: none !important;
        transition: color 0.2s ease !important;
    }}
    
    a:hover {{
        color: {colors['accent']} !important;
        text-decoration: underline !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['scrollbar_track']} !important;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['scrollbar_thumb']} !important;
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['scrollbar_thumb_hover']} !important;
    }}
    
    /* Área principal completa */
    .main {{
        background-color: {colors['bg_primary']} !important;
    }}
    
    .main > div {{
        background-color: {colors['bg_primary']} !important;
    }}
    
    [data-testid="stAppViewContainer"] {{
        background-color: {colors['bg_primary']} !important;
    }}
    
    [data-testid="stAppViewContainer"] > div {{
        background-color: {colors['bg_primary']} !important;
    }}
    
    /* Elementos de texto universais */
    .main *,
    [data-testid="stSidebar"] * {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Exceções para elementos específicos */
    .sidebar-header,
    .sidebar-header * {{
        color: white !important;
    }}
    
    /* Área vazia do dashboard */
    .empty-dashboard {{
        background-color: transparent !important;
    }}
    
    .empty-dashboard * {{
        color: {colors['text_secondary']} !important;
    }}
    
    /* Selectbox dropdown */
    .stSelectbox [data-baseweb="select"] {{
        background-color: {colors['bg_tertiary']} !important;
    }}
    
    .stSelectbox [data-baseweb="popover"] {{
        background-color: {colors['bg_tertiary']} !important;
        border-color: {colors['border']} !important;
    }}
    
    /* Slider completo */
    .stSlider [data-baseweb="slider"] {{
        color: {colors['accent']} !important;
    }}
    
    /* Todos os elementos de formulário */
    input, textarea, select {{
        background-color: {colors['bg_tertiary']} !important;
        color: {colors['text_primary']} !important;
        border-color: {colors['border']} !important;
    }}
    
    /* Sobrescrever cores inline */
    div[style*="background: white"],
    div[style*="background-color: white"],
    div[style*="background: #fff"],
    div[style*="background-color: #fff"],
    div[style*="background: #ffffff"],
    div[style*="background-color: #ffffff"] {{
        background-color: {colors['bg_tertiary']} !important;
    }}
    
    div[style*="background: #f8f9fa"],
    div[style*="background-color: #f8f9fa"] {{
        background-color: {colors['bg_tertiary']} !important;
    }}
    
    div[style*="color: #666"],
    span[style*="color: #666"],
    p[style*="color: #666"] {{
        color: {colors['text_secondary']} !important;
    }}
    
    div[style*="color: #999"],
    span[style*="color: #999"],
    p[style*="color: #999"] {{
        color: {colors['text_tertiary']} !important;
    }}
    
    /* Elementos de lista */
    ul, ol, li {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Strong e em */
    strong, b, em, i {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Headers dentro de markdown */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
        color: {colors['text_primary']} !important;
    }}
    </style>
    """


def _generate_light_theme_css(colors: dict) -> str:
    """Gera CSS para tema claro"""
    return f"""
    <style>
    /* ============================================================
       TEMA CLARO - Estilos Modernos e Consistentes
       ============================================================ */
    
    /* Transições suaves para mudanças de tema */
    * {{
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
    }}
    
    /* Base - HTML e Body */
    html, body {{
        background-color: {colors['bg_primary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Aplicação principal */
    .stApp {{
        background-color: {colors['bg_primary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Container principal */
    .main .block-container {{
        background-color: transparent !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    [data-testid="stSidebar"] > div {{
        background-color: {colors['bg_secondary']} !important;
    }}
    
    /* Remover sobrescritas universais de texto */
    .main *,
    [data-testid="stSidebar"] * {{
        color: inherit !important;
    }}
    
    /* Mensagem de boas-vindas */
    .welcome-message {{
        background: linear-gradient(135deg, {colors['bg_primary']} 0%, {colors['bg_secondary']} 100%) !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid {colors['accent']} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
    }}
    
    /* Status container */
    .status-container {{
        background: {colors['bg_secondary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    
    .status-item {{
        border-bottom: 1px solid {colors['border_light']} !important;
        padding: 0.75rem 0 !important;
        transition: background-color 0.2s ease !important;
    }}
    
    .status-item:hover {{
        background-color: {colors['bg_hover']} !important;
    }}
    
    .status-label {{
        color: {colors['text_secondary']} !important;
        font-weight: 500 !important;
    }}
    
    .status-value {{
        color: {colors['text_primary']} !important;
        font-weight: 600 !important;
    }}
    
    /* Mensagens de chat */
    .chat-message {{
        padding: 1rem;
        border-radius: 12px;
        margin: 0.6rem 0;
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .chat-message:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    .chat-message.user-message {{
        background-color: {colors['user_message_bg']} !important;
        color: {colors['message_text']} !important;
        border-left: 4px solid {colors['accent']} !important;
    }}
    
    .chat-message.assistant-message {{
        background-color: {colors['assistant_message_bg']} !important;
        color: {colors['message_text']} !important;
        border-left: 4px solid {colors['accent_light']} !important;
    }}
    
    .empty-chat-message {{
        text-align: center;
        color: {colors['text_tertiary']} !important;
        padding: 2.5rem 1rem;
        font-size: 0.95rem;
    }}
    
    /* Inputs */
    input, textarea, select {{
        background-color: {colors['bg_primary']} !important;
        color: {colors['text_primary']} !important;
        border-color: {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    .stTextInput > div > div > input {{
        background-color: {colors['bg_primary']} !important;
        border-color: {colors['border']} !important;
        border-radius: 8px !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {colors['accent']} !important;
        box-shadow: 0 0 0 2px {colors['accent']}33 !important;
    }}
    
    .stSelectbox > div > div {{
        background-color: {colors['bg_primary']} !important;
        border-radius: 8px !important;
    }}
    
    .stSelectbox > div > div:hover {{
        background-color: {colors['bg_hover']} !important;
    }}
    
    [data-testid="stChatInput"] textarea {{
        background-color: {colors['bg_primary']} !important;
        border-color: {colors['border']} !important;
        border-radius: 12px !important;
    }}
    
    [data-testid="stChatInput"] textarea:focus {{
        border-color: {colors['accent']} !important;
        box-shadow: 0 0 0 2px {colors['accent']}33 !important;
    }}
    
    /* Botões */
    .stButton > button {{
        background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent_hover']} 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px {colors['accent']}66 !important;
    }}
    
    /* Indicador de pensando */
    .thinking-above-prompt {{
        background: linear-gradient(90deg, {colors['accent']}33 0%, {colors['accent_hover']}33 100%) !important;
        color: {colors['accent']} !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        animation: pulse 2s ease-in-out infinite !important;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['scrollbar_track']} !important;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['scrollbar_thumb']} !important;
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['scrollbar_thumb_hover']} !important;
    }}
    
    /* Área vazia */
    .empty-text {{
        color: {colors['text_secondary']} !important;
    }}
    
    .empty-text-secondary {{
        color: {colors['text_tertiary']} !important;
    }}
    
    /* Code blocks */
    code {{
        background-color: {colors['code_bg']} !important;
        color: {colors['code_text']} !important;
        padding: 0.2rem 0.4rem !important;
        border-radius: 4px !important;
    }}
    
    pre {{
        background-color: {colors['code_bg']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }}
    
    /* Links */
    a {{
        color: {colors['accent']} !important;
        text-decoration: none !important;
        transition: color 0.2s ease !important;
    }}
    
    a:hover {{
        color: {colors['accent_hover']} !important;
        text-decoration: underline !important;
    }}
    </style>
    """
