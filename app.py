# app.py - Layout moderno com sidebar de chat
import streamlit as st
import os
from typing import Optional
from dotenv import load_dotenv
import pandas as pd

@st.cache_data
def load_vehicle_data():
    return pd.read_csv("data/dados_veiculos_300.csv")

df_veiculos = load_vehicle_data()
df_text = df_veiculos.to_string()

if "llm_handler" in st.session_state and st.session_state.llm_handler:
    st.session_state.llm_handler.set_dataframe_context(df_text)



# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Imports dos módulos customizados
try:
    from llm_handler import create_llm_handler
    from audio_transcriber import transcribe_audio
    from styles import CUSTOM_CSS

    LLM_AVAILABLE = True
    AUDIO_AVAILABLE = True
except ImportError as e:
    LLM_AVAILABLE = False
    AUDIO_AVAILABLE = False
    CUSTOM_CSS = ""
    st.warning(f"⚠️ Alguns módulos não foram encontrados: {str(e)}")

    # Fallback para create_llm_handler
    def create_llm_handler(base_url=None):
        return None


# Configuração da página com layout wide
st.set_page_config(
    page_title="Omnilink AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado importado de styles.py
if CUSTOM_CSS:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# CSS dinâmico para tema escuro/claro
def get_theme_css(theme):
    """Retorna CSS baseado no tema selecionado"""
    if theme == "escuro":
        return """
        <style>
        /* Tema Escuro - Cobertura Completa */
        
        /* Base - HTML e Body */
        html, body {
            background-color: #1e1e1e !important;
            color: #e0e0e0 !important;
        }
        
        /* Aplicação principal */
        .stApp {
            background-color: #1e1e1e !important;
            color: #e0e0e0 !important;
        }
        
        /* Container principal */
        .main .block-container {
            background-color: #1e1e1e !important;
            color: #e0e0e0 !important;
        }
        
        /* Sidebar completa */
        [data-testid="stSidebar"] {
            background-color: #2d2d2d !important;
            color: #e0e0e0 !important;
        }
        
        [data-testid="stSidebar"] > div {
            background-color: #2d2d2d !important;
        }
        
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            background-color: #2d2d2d !important;
        }
        
        /* Texto geral - cobertura ampla */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp p, .stApp div, .stApp span, .stApp label,
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] div, [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #e0e0e0 !important;
        }
        
        /* Inputs de texto */
        .stTextInput > div > div > input {
            background-color: #3d3d3d !important;
            color: #e0e0e0 !important;
            border-color: #555 !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #999 !important;
        }
        
        /* Selectbox */
        .stSelectbox > div > div {
            background-color: #3d3d3d !important;
            color: #e0e0e0 !important;
        }
        
        .stSelectbox > div > div > div {
            background-color: #3d3d3d !important;
            color: #e0e0e0 !important;
        }
        
        /* Slider */
        .stSlider > div > div {
            color: #e0e0e0 !important;
        }
        
        .stSlider label {
            color: #e0e0e0 !important;
        }
        
        /* Mensagens de chat */
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin: 0.6rem 0;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .chat-message.user-message {
            background-color: #3d3d3d !important;
            color: #e0e0e0 !important;
        }
        
        .chat-message.assistant-message {
            background-color: #2d4a5e !important;
            color: #e0e0e0 !important;
        }
        
        .empty-chat-message {
            text-align: center;
            color: #888 !important;
            padding: 2.5rem 1rem;
            font-size: 0.95rem;
        }
        
        /* Mensagem de boas-vindas */
        .welcome-message {
            background-color: #3d3d3d !important;
            color: #e0e0e0 !important;
            border-left-color: #667eea !important;
        }
        
        /* Sidebar header - manter gradiente mas ajustar texto */
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        
        /* Status container */
        .status-container {
            background-color: #3d3d3d !important;
            border-color: #555 !important;
        }
        
        .status-item {
            border-bottom-color: #555 !important;
        }
        
        .status-label {
            color: #b0b0b0 !important;
        }
        
        .status-value {
            color: #e0e0e0 !important;
        }
        
        /* Expander */
        [data-testid="stExpander"] {
            background-color: #2d2d2d !important;
        }
        
        .streamlit-expanderHeader {
            background-color: #2d2d2d !important;
            color: #e0e0e0 !important;
        }
        
        .streamlit-expanderContent {
            background-color: #2d2d2d !important;
            color: #e0e0e0 !important;
        }
        
        /* Chat messages do Streamlit */
        [data-testid="stChatMessage"] {
            background-color: transparent !important;
        }
        
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            color: #e0e0e0 !important;
        }
        
        /* Área vazia do dashboard */
        .empty-text {
            color: #b0b0b0 !important;
        }
        
        .empty-text-secondary {
            color: #888 !important;
        }
        
        /* Sobrescrever cores inline na área vazia */
        div[style*="color: #999"] {
            color: #888 !important;
        }
        
        div[style*="color: #666"] {
            color: #b0b0b0 !important;
        }
        
        /* Info boxes */
        [data-testid="stAlert"] {
            background-color: #2d4a5e !important;
        }
        
        .stInfo {
            background-color: #2d4a5e !important;
            color: #e0e0e0 !important;
        }
        
        .stInfo > div {
            color: #e0e0e0 !important;
        }
        
        /* Success boxes */
        .stSuccess {
            background-color: #1e4d2e !important;
            color: #e0e0e0 !important;
        }
        
        .stSuccess > div {
            color: #e0e0e0 !important;
        }
        
        /* Warning boxes */
        .stWarning {
            background-color: #4d3d1e !important;
            color: #e0e0e0 !important;
        }
        
        .stWarning > div {
            color: #e0e0e0 !important;
        }
        
        /* Error boxes */
        .stError {
            background-color: #4d1e1e !important;
            color: #e0e0e0 !important;
        }
        
        .stError > div {
            color: #e0e0e0 !important;
        }
        
        /* Markdown */
        .stMarkdown {
            color: #e0e0e0 !important;
        }
        
        .stMarkdown p, .stMarkdown li, .stMarkdown ul, .stMarkdown ol {
            color: #e0e0e0 !important;
        }
        
        /* Indicador de pensando */
        .thinking-above-prompt {
            background-color: rgba(102, 126, 234, 0.2) !important;
            color: #a0b4ff !important;
        }
        
        /* Chat input */
        [data-testid="stChatInput"] textarea {
            background-color: #3d3d3d !important;
            color: #e0e0e0 !important;
            border-color: #555 !important;
        }
        
        [data-testid="stChatInput"] textarea::placeholder {
            color: #999 !important;
        }
        
        /* Audio input */
        [data-testid="stAudioInput"] {
            background-color: transparent !important;
        }
        
        /* Botões */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        /* Checkbox */
        .stCheckbox label {
            color: #e0e0e0 !important;
        }
        
        /* Divider */
        hr {
            border-color: #555 !important;
        }
        
        /* Code blocks */
        code {
            background-color: #2d2d2d !important;
            color: #a0ffa0 !important;
        }
        
        pre {
            background-color: #2d2d2d !important;
            color: #e0e0e0 !important;
        }
        
        /* Container e elementos gerais */
        [data-testid="stVerticalBlock"] {
            color: #e0e0e0 !important;
        }
        
        /* Elementos de coluna */
        [data-testid="column"] {
            color: #e0e0e0 !important;
        }
        
        /* Links */
        a {
            color: #a0b4ff !important;
        }
        
        a:hover {
            color: #667eea !important;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #2d2d2d !important;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #555 !important;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #666 !important;
        }
        
        /* Sobrescrever TODOS os elementos de texto - cobertura universal */
        * {
            color: inherit;
        }
        
        /* Área principal completa */
        .main {
            background-color: #1e1e1e !important;
        }
        
        .main > div {
            background-color: #1e1e1e !important;
        }
        
        /* Todos os containers e blocos */
        [data-testid="stAppViewContainer"] {
            background-color: #1e1e1e !important;
        }
        
        [data-testid="stAppViewContainer"] > div {
            background-color: #1e1e1e !important;
        }
        
        /* Elementos de texto universais */
        .main *,
        [data-testid="stSidebar"] * {
            color: #e0e0e0 !important;
        }
        
        /* Exceções para elementos específicos que devem manter suas cores */
        .sidebar-header,
        .sidebar-header * {
            color: white !important;
        }
        
        /* Sobrescrever estilos do styles.py */
        .welcome-message {
            background: #3d3d3d !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
        }
        
        .status-container {
            background: #3d3d3d !important;
            border: 1px solid #555 !important;
        }
        
        .empty-text {
            color: #b0b0b0 !important;
        }
        
        .empty-text-secondary {
            color: #888 !important;
        }
        
        /* Área vazia do dashboard */
        .empty-dashboard {
            background-color: transparent !important;
        }
        
        .empty-dashboard * {
            color: #b0b0b0 !important;
        }
        
        /* Selectbox dropdown */
        .stSelectbox [data-baseweb="select"] {
            background-color: #3d3d3d !important;
        }
        
        .stSelectbox [data-baseweb="popover"] {
            background-color: #3d3d3d !important;
        }
        
        /* Slider completo */
        .stSlider [data-baseweb="slider"] {
            color: #e0e0e0 !important;
        }
        
        /* Todos os elementos de formulário */
        input, textarea, select {
            background-color: #3d3d3d !important;
            color: #e0e0e0 !important;
            border-color: #555 !important;
        }
        
        /* Elementos específicos do Streamlit que podem estar escondidos */
        section[data-testid="stSidebar"] {
            background-color: #2d2d2d !important;
        }
        
        /* Garantir que divs inline com cores sejam sobrescritas */
        div[style*="background: white"],
        div[style*="background-color: white"],
        div[style*="background: #fff"],
        div[style*="background-color: #fff"],
        div[style*="background: #ffffff"],
        div[style*="background-color: #ffffff"] {
            background-color: #3d3d3d !important;
        }
        
        div[style*="background: #f8f9fa"],
        div[style*="background-color: #f8f9fa"] {
            background-color: #3d3d3d !important;
        }
        
        /* Sobrescrever cores de texto inline */
        div[style*="color: #666"],
        span[style*="color: #666"],
        p[style*="color: #666"] {
            color: #b0b0b0 !important;
        }
        
        div[style*="color: #999"],
        span[style*="color: #999"],
        p[style*="color: #999"] {
            color: #888 !important;
        }
        
        /* Elementos de lista */
        ul, ol, li {
            color: #e0e0e0 !important;
        }
        
        /* Strong e em */
        strong, b, em, i {
            color: #e0e0e0 !important;
        }
        
        /* Headers dentro de markdown */
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3,
        .stMarkdown h4,
        .stMarkdown h5,
        .stMarkdown h6 {
            color: #e0e0e0 !important;
        }
        </style>
        """
    else:
        return """
        <style>
        /* Tema Claro - Resetar estilos do tema escuro e restaurar padrão */
        html, body {
            background-color: #ffffff !important;
            color: inherit !important;
        }
        
        .stApp {
            background-color: #ffffff !important;
            color: inherit !important;
        }
        
        .main {
            background-color: #ffffff !important;
        }
        
        .main .block-container {
            background-color: transparent !important;
            color: inherit !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            color: inherit !important;
        }
        
        [data-testid="stSidebar"] > div {
            background-color: #ffffff !important;
        }
        
        /* Remover sobrescritas universais de texto */
        .main *,
        [data-testid="stSidebar"] * {
            color: inherit !important;
        }
        
        /* Restaurar cores padrão dos elementos customizados */
        .welcome-message {
            background: white !important;
            color: inherit !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }
        
        .status-container {
            background: #f8f9fa !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        .status-label {
            color: #666 !important;
        }
        
        .status-value {
            color: inherit !important;
        }
        
        .empty-text {
            color: #666 !important;
        }
        
        .empty-text-secondary {
            color: #999 !important;
        }
        
        /* Inputs voltam ao padrão */
        input, textarea, select {
            background-color: white !important;
            color: inherit !important;
            border-color: #e0e0e0 !important;
        }
        
        .stTextInput > div > div > input {
            background-color: white !important;
            border-color: #e0e0e0 !important;
        }
        
        .stSelectbox > div > div {
            background-color: white !important;
        }
        
        [data-testid="stChatInput"] textarea {
            background-color: white !important;
            border-color: #e0e0e0 !important;
        }
        
        /* Estilos para mensagens de chat */
        .chat-message {
            padding: 1rem;
            border-radius: 10px;
            margin: 0.6rem 0;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .chat-message.user-message {
            background-color: #f0f0f0 !important;
            color: #333 !important;
        }
        
        .chat-message.assistant-message {
            background-color: #e8f4f8 !important;
            color: #333 !important;
        }
        
        .empty-chat-message {
            text-align: center;
            color: #999 !important;
            padding: 2.5rem 1rem;
            font-size: 0.95rem;
        }
        </style>
        """


# Inicializar tema antes de usar
if "theme" not in st.session_state:
    st.session_state.theme = "claro"  # "claro" ou "escuro"

# Aplicar CSS do tema
st.markdown(get_theme_css(st.session_state.theme), unsafe_allow_html=True)

# CSS SIMPLIFICADO para alternância microfone/seta
st.markdown(
    """
<style>
/* Container para posicionar elementos */
.chat-input-wrapper {
    position: relative !important;
    width: 100% !important;
}

/* Posicionar o audio input sobre o botão de envio */
.chat-input-wrapper > div[data-testid="stAudioInput"] {
    position: absolute !important;
    right: 45px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 100 !important;
    width: auto !important;
}

/* Esconder label do audio input */
.chat-input-wrapper > div[data-testid="stAudioInput"] label {
    display: none !important;
}

/* Estilizar o botão do microfone */
.chat-input-wrapper > div[data-testid="stAudioInput"] button {
    background: transparent !important;
    border: none !important;
    padding: 8px !important;
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.3rem !important;
    color: #666 !important;
    transition: all 0.2s ease !important;
}

.chat-input-wrapper > div[data-testid="stAudioInput"] button:hover {
    background: rgba(102, 126, 234, 0.1) !important;
    color: #667eea !important;
}

/* Esconder microfone quando há texto */
.chat-input-wrapper.has-text > div[data-testid="stAudioInput"] {
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Esconder seta de envio quando não há texto */
.chat-input-wrapper:not(.has-text) button[data-testid="baseButton-secondary"] {
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Mostrar seta quando há texto */
.chat-input-wrapper.has-text button[data-testid="baseButton-secondary"] {
    opacity: 1 !important;
    pointer-events: all !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# JavaScript SIMPLIFICADO para detectar texto no input
st.markdown(
    """
<script>
// Função para configurar a detecção de texto
function setupTextDetection() {
    // Aguardar um pouco para garantir que os elementos estejam carregados
    setTimeout(() => {
        // Encontrar todos os inputs de chat
        const chatInputs = document.querySelectorAll('[data-testid="stChatInput"] input');
        
        chatInputs.forEach((input, index) => {
            // Encontrar o wrapper mais próximo
            let wrapper = input.closest('.chat-input-wrapper');
            if (!wrapper) {
                // Criar wrapper se não existir
                wrapper = document.createElement('div');
                wrapper.className = 'chat-input-wrapper';
                input.parentElement.parentElement.parentElement.insertBefore(wrapper, input.parentElement.parentElement);
                wrapper.appendChild(input.parentElement.parentElement);
                
                // Tentar encontrar o audio input correspondente e mover para o wrapper
                const audioInputs = document.querySelectorAll('[data-testid="stAudioInput"]');
                if (audioInputs[index]) {
                    wrapper.appendChild(audioInputs[index]);
                }
            }
            
            // Função para atualizar o estado
            function updateState() {
                if (input.value.trim().length > 0) {
                    wrapper.classList.add('has-text');
                } else {
                    wrapper.classList.remove('has-text');
                }
            }
            
            // Configurar listeners
            input.addEventListener('input', updateState);
            input.addEventListener('keyup', updateState);
            input.addEventListener('change', updateState);
            
            // Estado inicial
            updateState();
        });
    }, 500);
}

// Executar quando a página carrega
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupTextDetection);
} else {
    setupTextDetection();
}

// Executar também quando houver mudanças (Streamlit reruns)
const observer = new MutationObserver(() => {
    setTimeout(setupTextDetection, 300);
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
</script>
""",
    unsafe_allow_html=True,
)

# Inicialização do session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_handler" not in st.session_state:
    st.session_state.llm_handler = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama2:latest"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "prompt_in_center" not in st.session_state:
    st.session_state.prompt_in_center = False

if "audio_transcribed" not in st.session_state:
    st.session_state.audio_transcribed = None

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

if "ollama_url" not in st.session_state:
    st.session_state.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

if "transcription_method" not in st.session_state:
    st.session_state.transcription_method = os.getenv("TRANSCRIPTION_METHOD", "whisper")

# Auto-inicialização do Ollama
if st.session_state.llm_handler is None:
    try:
        st.session_state.llm_handler = create_llm_handler(st.session_state.ollama_url)
        if (
            st.session_state.llm_handler
            and st.session_state.llm_handler.is_configured()
        ):
            st.session_state.llm_handler = st.session_state.llm_handler
    except Exception:
        st.session_state.llm_handler = None

# ========== SIDEBAR ESQUERDA - CHAT ==========
with st.sidebar:
    # Header com gradiente roxo
    st.markdown(
        """
        <div class="sidebar-header">
            <div class="sidebar-title">
                🤖 Omnilink AI
            </div>
            <div class="sidebar-subtitle">
                Assistente de Dashboards Inteligentes
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mensagem de boas-vindas
    st.markdown(
        """
        <div class="welcome-message">
            <strong>Olá! 👋</strong><br>
            Sou seu assistente de dashboards. Peça visualizações de dados e eu gero para você em tempo real!
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Container para histórico de mensagens (scrollável)
    chat_history_container = st.container()
    with chat_history_container:
        if st.session_state.messages:
            for message in st.session_state.messages:
                if message["role"] == "user":
                    # Usar classe CSS que será estilizada pelo tema
                    st.markdown(
                        f'<div class="chat-message user-message"><strong>Você:</strong> {message["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    # Usar classe CSS que será estilizada pelo tema
                    st.markdown(
                        f'<div class="chat-message assistant-message"><strong>Assistente:</strong> {message["content"]}</div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(
                '<div class="empty-chat-message">Nenhuma mensagem ainda</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar indicador de pensando acima do prompt se estiver pensando
    if st.session_state.is_thinking:
        st.markdown(
            '<div class="thinking-above-prompt">💭 <em>Pensando...</em></div>',
            unsafe_allow_html=True,
        )

    # Container integrado para prompt e microfone - SIMPLIFICADO
    if not st.session_state.prompt_in_center:
        # Input de mensagem usando chat_input
        user_input = st.chat_input("Digite sua mensagem...", key="sidebar_chat_input")

        # Microfone posicionado via CSS
        audio_file = st.audio_input(
            "🎙️", key="sidebar_audio", help="Clique para gravar uma mensagem de voz"
        )

        # Processar áudio se fornecido
        if audio_file:
            st.audio(audio_file, format="audio/wav")
            with st.spinner("Transcrevendo áudio..."):
                try:
                    if AUDIO_AVAILABLE:
                        transcribed_text = transcribe_audio(
                            audio_file, method=st.session_state.transcription_method
                        )
                        if transcribed_text:
                            st.session_state.audio_transcribed = transcribed_text
                        else:
                            st.error(
                                "❌ Erro ao transcrever áudio. Verifique se o serviço está configurado."
                            )
                    else:
                        st.warning(
                            "⚠️ Transcrição de áudio não disponível. Instale as dependências necessárias."
                        )
                except Exception as e:
                    st.error(f"❌ Erro na transcrição: {str(e)}")

            if st.session_state.audio_transcribed:
                st.info(
                    f"📝 Transcrição do áudio: **{st.session_state.audio_transcribed}**"
                )
                # Se houver transcrição, usar como input
                if not user_input:
                    user_input = st.session_state.audio_transcribed
                    st.session_state.audio_transcribed = None  # Limpar após usar

    else:
        # Placeholder para manter estrutura quando prompt está no centro
        user_input = None

    st.markdown("---")

    # Configurações (colapsável)
    with st.expander("⚙️ Configurações"):
        # Configuração do Ollama
        st.markdown("### 🔧 Configuração do Ollama")
        ollama_url = st.text_input(
            "URL do servidor Ollama",
            value=st.session_state.ollama_url,
            help="URL padrão: http://localhost:11434",
        )

        if ollama_url != st.session_state.ollama_url:
            st.session_state.ollama_url = ollama_url
            try:
                st.session_state.llm_handler = create_llm_handler(ollama_url)
                if (
                    st.session_state.llm_handler
                    and st.session_state.llm_handler.is_configured()
                ):
                    st.success("✅ Conectado ao Ollama!")
                else:
                    st.warning("⚠️ Ollama não está disponível nesta URL")
            except Exception as e:
                st.error(f"❌ Erro ao conectar: {str(e)}")
                st.session_state.llm_handler = None

        # Botão para reconectar
        if st.button("🔄 Reconectar ao Ollama", use_container_width=True):
            try:
                st.session_state.llm_handler = create_llm_handler(
                    st.session_state.ollama_url
                )
                if (
                    st.session_state.llm_handler
                    and st.session_state.llm_handler.is_configured()
                ):
                    st.success("✅ Conectado com sucesso!")
                    st.rerun()
                else:
                    st.error(
                        "❌ Não foi possível conectar ao Ollama. Verifique se o servidor está rodando."
                    )
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")

        # Seleção de modelo - buscar dinamicamente do Ollama
        try:
            if st.session_state.llm_handler:
                available_models = st.session_state.llm_handler.list_available_models()
                if available_models:
                    # Se o modelo atual não está na lista, usar o primeiro disponível
                    if st.session_state.selected_model not in available_models:
                        st.session_state.selected_model = available_models[0]

                    current_index = (
                        available_models.index(st.session_state.selected_model)
                        if st.session_state.selected_model in available_models
                        else 0
                    )
                    st.session_state.selected_model = st.selectbox(
                        "Modelo Ollama", available_models, index=current_index
                    )
                else:
                    st.warning(
                        "⚠️ Nenhum modelo encontrado. Baixe modelos usando: ollama pull <nome_do_modelo>"
                    )
                    st.session_state.selected_model = st.text_input(
                        "Digite o nome do modelo", value=st.session_state.selected_model
                    )
            else:
                st.warning("⚠️ Conecte ao Ollama primeiro")
                st.session_state.selected_model = st.text_input(
                    "Nome do modelo", value=st.session_state.selected_model
                )
        except Exception as e:
            st.error(f"Erro ao listar modelos: {str(e)}")
            st.session_state.selected_model = st.text_input(
                "Nome do modelo", value=st.session_state.selected_model
            )

        # Controle de temperatura
        st.session_state.temperature = st.slider(
            "Criatividade (temperature)",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
        )

        st.markdown("---")

        # Configuração de transcrição de áudio
        st.markdown("### 🎙️ Transcrição de Áudio")
        transcription_method = st.selectbox(
            "Método de transcrição",
            ["whisper", "openai"],
            index=0 if st.session_state.transcription_method == "whisper" else 1,
            help="Whisper: local (requer openai-whisper). OpenAI: API (requer OPENAI_API_KEY)",
        )
        st.session_state.transcription_method = transcription_method

        if transcription_method == "openai":
            openai_key = os.getenv("OPENAI_API_KEY", "")
            if not openai_key:
                st.warning("⚠️ OPENAI_API_KEY não encontrada no .env para transcrição")

        st.markdown("---")

        # Configuração de posição do prompt
        st.markdown("**📍 Posição do Prompt**")
        prompt_in_center = st.checkbox(
            "Prompt no centro (abaixo)",
            value=st.session_state.prompt_in_center,
            help="Quando ativado, o prompt fica fixo no centro inferior da tela. Recomendado quando a sidebar está escondida.",
        )

        if prompt_in_center != st.session_state.prompt_in_center:
            st.session_state.prompt_in_center = prompt_in_center
            st.rerun()

        if prompt_in_center:
            st.info(
                "💡 O prompt está configurado para aparecer no centro inferior da tela."
            )
        else:
            st.info(
                "💡 Dica: Se esconder a sidebar, ative esta opção para mover o prompt para o centro."
            )

        st.markdown("---")

        # Configuração de tema
        st.markdown("### 🎨 Aparência")
        theme = st.selectbox(
            "Tema da página",
            ["claro", "escuro"],
            index=0 if st.session_state.theme == "claro" else 1,
            help="Escolha entre tema claro ou escuro",
        )

        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()

        # Botão limpar chat
        if st.button("🗑️ Limpar Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")

    # Status do Sistema (na sidebar)
    with st.expander("🔧 Status do Sistema", expanded=False):
        # Preparar valores do status
        handler_available = "✅ Sim" if LLM_AVAILABLE else "❌ Não"
        handler_available_color = "#28a745" if LLM_AVAILABLE else "#dc3545"

        handler_initialized = (
            "✅ Sim" if st.session_state.llm_handler is not None else "❌ Não"
        )
        handler_initialized_color = (
            "#28a745" if st.session_state.llm_handler is not None else "#dc3545"
        )

        ollama_configured = (
            "✅ Sim"
            if (
                st.session_state.llm_handler
                and st.session_state.llm_handler.is_configured()
            )
            else "❌ Não"
        )
        ollama_configured_color = (
            "#28a745"
            if (
                st.session_state.llm_handler
                and st.session_state.llm_handler.is_configured()
            )
            else "#dc3545"
        )

        audio_available = "✅ Sim" if AUDIO_AVAILABLE else "❌ Não"
        audio_available_color = "#28a745" if AUDIO_AVAILABLE else "#dc3545"

        num_messages = len(st.session_state.messages)
        current_model = st.session_state.selected_model

        st.markdown(
            f"""
            <div class="status-container">
                <div class="status-item">
                    <span class="status-label">Handler Disponível</span>
                    <span class="status-value" style="color: {handler_available_color};">
                        {handler_available}
                    </span>
                </div>
                <div class="status-item">
                    <span class="status-label">Handler Inicializado</span>
                    <span class="status-value" style="color: {handler_initialized_color};">
                        {handler_initialized}
                    </span>
                </div>
                <div class="status-item">
                    <span class="status-label">Ollama Conectado</span>
                    <span class="status-value" style="color: {ollama_configured_color};">
                        {ollama_configured}
                    </span>
                </div>
                <div class="status-item">
                    <span class="status-label">Transcrição de Áudio</span>
                    <span class="status-value" style="color: {audio_available_color};">
                        {audio_available}
                    </span>
                </div>
                <div class="status-item">
                    <span class="status-label">Mensagens no Histórico</span>
                    <span class="status-value" style="color: #667eea;">
                        {num_messages}
                    </span>
                </div>
                <div class="status-item">
                    <span class="status-label">Modelo Atual</span>
                    <span class="status-value" style="color: #667eea;">
                        {current_model}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Processar mensagem quando enviada (texto ou áudio transcrito)
if "user_input" in locals() and user_input:
    if (
        st.session_state.llm_handler is None
        or not st.session_state.llm_handler.is_configured()
    ):
        st.error("⚠️ Ollama não está disponível. Verifique se o servidor está rodando.")
    else:
        # Adicionar mensagem do usuário no histórico
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Exibir imediatamente a mensagem do usuário
        with st.chat_message("user"):
            st.markdown(user_input)

        # Gerar resposta em streaming
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            # Gerar resposta
            response = st.session_state.llm_handler.generate_response(
                messages=st.session_state.messages,
                model=st.session_state.selected_model,
                temperature=st.session_state.temperature,
            )

            placeholder.markdown(response)
            full_response = response

        # Salvar no histórico
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

        # Recarregar para atualizar a interface
        st.rerun()

# ========== ÁREA PRINCIPAL - DASHBOARD ==========
# Área principal para exibir conteúdo/dashboards
main_area = st.container()

with main_area:
    if not st.session_state.messages:
        # Estado vazio - mostrar ícone e mensagem
        st.markdown(
            """
            <div class="empty-dashboard">
                <div class="dashboard-icon">
                    <svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
                        <!-- Retângulo principal com bordas arredondadas -->
                        <rect x="10" y="10" width="180" height="130" rx="8" ry="8" 
                              fill="none" stroke="#999" stroke-width="2"/>
                        <!-- Painel superior horizontal -->
                        <rect x="20" y="20" width="160" height="30" rx="4" ry="4" 
                              fill="#e0e0e0" stroke="#ccc" stroke-width="1"/>
                        <!-- Painel esquerdo vertical -->
                        <rect x="20" y="60" width="70" height="70" rx="4" ry="4" 
                              fill="#e0e0e0" stroke="#ccc" stroke-width="1"/>
                        <!-- Painel inferior direito (quadrado) -->
                        <rect x="100" y="100" width="80" height="30" rx="4" ry="4" 
                              fill="#e0e0e0" stroke="#ccc" stroke-width="1"/>
                        <!-- Painel superior direito -->
                        <rect x="100" y="60" width="80" height="30" rx="4" ry="4" 
                              fill="#e0e0e0" stroke="#ccc" stroke-width="1"/>
                    </svg>
                </div>
                <div class="empty-text">Nenhum dashboard gerado</div>
                <div class="empty-text-secondary">Envie uma mensagem no chat para começar</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        # Exibir conteúdo das respostas
        # Se a última mensagem for do assistente, mostrar em destaque
        if (
            st.session_state.messages
            and st.session_state.messages[-1]["role"] == "assistant"
        ):
            last_response = st.session_state.messages[-1]["content"]

            # Container para resposta
            st.markdown("### 📊 Resposta do Assistente")
            st.markdown("---")

            # Exibir resposta formatada
            response_container = st.container()
            with response_container:
                st.markdown(last_response)

                # Botões de ação - apenas ícones
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("🔄", use_container_width=True, key="btn_regenerar"):
                        # Remove última resposta e regenera
                        if len(st.session_state.messages) >= 2:
                            st.session_state.messages.pop()
                            st.session_state.messages.pop()
                            st.rerun()

                with col2:
                    if st.button("📋", use_container_width=True, key="btn_copiar"):
                        st.success("Resposta copiada!")

                with col3:
                    if st.button("🗑️", use_container_width=True, key="btn_limpar"):
                        st.session_state.messages = []
                        st.rerun()

        # Histórico completo (colapsável)
        if len(st.session_state.messages) > 2:
            with st.expander("📜 Histórico Completo da Conversa"):
                for i, message in enumerate(st.session_state.messages):
                    role_icon = "👤" if message["role"] == "user" else "🤖"
                    st.markdown(f"**{role_icon} {message['role'].title()}:**")
                    st.markdown(message["content"])
                    if i < len(st.session_state.messages) - 1:
                        st.markdown("---")

    # Prompt no centro (se configurado)
    if st.session_state.prompt_in_center:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço antes do prompt

        # Mostrar indicador de pensando acima do prompt se estiver pensando
        if st.session_state.is_thinking:
            st.markdown(
                '<div class="thinking-above-prompt">💭 <em>Pensando...</em></div>',
                unsafe_allow_html=True,
            )

        # Input de mensagem usando chat_input no centro
        center_user_input = st.chat_input(
            "Digite sua mensagem no centro...", key="center_chat_input"
        )

        # Microfone no centro
        center_audio_file = st.audio_input(
            "🎙️", key="center_audio", help="Clique para gravar uma mensagem de voz"
        )

        # Processar áudio se fornecido
        if center_audio_file:
            st.audio(center_audio_file, format="audio/wav")
            with st.spinner("Transcrevendo áudio..."):
                try:
                    if AUDIO_AVAILABLE:
                        transcribed_text = transcribe_audio(
                            center_audio_file,
                            method=st.session_state.transcription_method,
                        )
                        if transcribed_text:
                            st.session_state.audio_transcribed = transcribed_text
                        else:
                            st.error(
                                "❌ Erro ao transcrever áudio. Verifique se o serviço está configurado."
                            )
                    else:
                        st.warning(
                            "⚠️ Transcrição de áudio não disponível. Instale as dependências necessárias."
                        )
                except Exception as e:
                    st.error(f"❌ Erro na transcrição: {str(e)}")

            if st.session_state.audio_transcribed:
                st.info(
                    f"📝 Transcrição do áudio: **{st.session_state.audio_transcribed}**"
                )
                # Se houver transcrição, usar como input
                if not center_user_input:
                    center_user_input = st.session_state.audio_transcribed
                    st.session_state.audio_transcribed = None  # Limpar após usar

        # Processar mensagem quando enviada do centro
        if center_user_input:
            if (
                st.session_state.llm_handler is None
                or not st.session_state.llm_handler.is_configured()
            ):
                st.error(
                    "⚠️ Ollama não está disponível. Verifique se o servidor está rodando."
                )
            else:
                # Adicionar mensagem do usuário no histórico
                st.session_state.messages.append(
                    {"role": "user", "content": center_user_input}
                )

                # Exibir imediatamente a mensagem do usuário
                with st.chat_message("user"):
                    st.markdown(center_user_input)

                # Gerar resposta em streaming
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    full_response = ""

                    # Gerar resposta
                    response = st.session_state.llm_handler.generate_response(
                        messages=st.session_state.messages,
                        model=st.session_state.selected_model,
                        temperature=st.session_state.temperature,
                    )

                    placeholder.markdown(response)
                    full_response = response

                # Salvar no histórico
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

                # Recarregar para atualizar a interface
                st.rerun()
