# app.py - Layout moderno com sidebar de chat
import streamlit as st
import os
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Adicionar diretório raiz do projeto ao Python path
# Isso permite que os imports de src.core e src.config funcionem
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar logging
try:
    from src.config.logging_config import setup_logging, get_logger

    setup_logging(level=os.getenv("LOG_LEVEL", "INFO"), log_to_console=False)
    logger = get_logger(__name__)
    logger.info("Aplicação iniciada")
except ImportError:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# Imports dos módulos customizados
try:
    from src.core.llm_handler import create_llm_handler
    from src.core.openai_handler import create_openai_handler
    from src.core.audio_transcriber import transcribe_audio
    from src.config.styles import CUSTOM_CSS
    from src.config.themes import generate_theme_css
    from src.core.input_validator import validate_user_input, sanitize_input
    from src.core.history_manager import (
        save_history,
        load_history,
        list_history_sessions,
        auto_save_history,
    )
    from src.core.data_loader import load_csv_data, get_data_info, get_data_summary
    from src.core.chart_generator import (
        generate_chart_from_request,
        display_chart,
        PLOTLY_AVAILABLE,
    )

    LLM_AVAILABLE = True
    OPENAI_AVAILABLE = True
    AUDIO_AVAILABLE = True
    VALIDATION_AVAILABLE = True
    HISTORY_AVAILABLE = True
    DATA_AVAILABLE = True
    CHARTS_AVAILABLE = PLOTLY_AVAILABLE
except ImportError as e:
    LLM_AVAILABLE = False
    OPENAI_AVAILABLE = False
    AUDIO_AVAILABLE = False
    VALIDATION_AVAILABLE = False
    HISTORY_AVAILABLE = False
    DATA_AVAILABLE = False
    CHARTS_AVAILABLE = False
    CUSTOM_CSS = ""
    logger.warning(f"Alguns módulos não foram encontrados: {str(e)}")
    st.warning(f"⚠️ Alguns módulos não foram encontrados: {str(e)}")

    # Fallbacks para módulos de dados
    def load_csv_data(filepath=None):
        return None

    def get_data_summary(df):
        return "Dados não disponíveis."

    def generate_chart_from_request(df, chart_type, **kwargs):
        return None

    def display_chart(chart):
        st.warning("Bibliotecas de gráficos não disponíveis")

    # Fallbacks
    def create_llm_handler(base_url=None):
        return None

    def create_openai_handler(api_key=None):
        return None

    def validate_user_input(text, **kwargs):
        return (True, None)

    def sanitize_input(text):
        return text

    def auto_save_history(messages, session_id="current"):
        pass

    def generate_theme_css(theme):
        return ""


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


# Importar módulo de temas
try:
    from src.config.themes import generate_theme_css
except ImportError:
    # Fallback caso o módulo não esteja disponível
    def generate_theme_css(theme):
        return ""


# CSS dinâmico para tema escuro/claro (mantido para compatibilidade)
def get_theme_css(theme):
    """Retorna CSS baseado no tema selecionado - DEPRECATED: use generate_theme_css do módulo themes"""
    return generate_theme_css(theme)


# Inicializar tema antes de usar
if "theme" not in st.session_state:
    st.session_state.theme = "escuro"  # "claro" ou "escuro" - padrão: escuro

# Aplicar CSS do tema usando o novo módulo
st.markdown(generate_theme_css(st.session_state.theme), unsafe_allow_html=True)

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

# Importar configurações do modelo
try:
    from src.config.model_config import DEFAULT_MODEL, DEFAULT_TEMPERATURE
except ImportError:
    DEFAULT_MODEL = "llama2:latest"
    DEFAULT_TEMPERATURE = 0.7

if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL

if "temperature" not in st.session_state:
    st.session_state.temperature = DEFAULT_TEMPERATURE

if "prompt_in_center" not in st.session_state:
    st.session_state.prompt_in_center = True  # Padrão: prompt no centro

if "audio_transcribed" not in st.session_state:
    st.session_state.audio_transcribed = None

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

if "ollama_url" not in st.session_state:
    st.session_state.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

if "llm_provider" not in st.session_state:
    st.session_state.llm_provider = "ollama"  # "ollama" ou "openai"

if "transcription_method" not in st.session_state:
    st.session_state.transcription_method = os.getenv("TRANSCRIPTION_METHOD", "whisper")

# Carregar dados de veículos
if "veiculos_df" not in st.session_state:
    if DATA_AVAILABLE:
        try:
            st.session_state.veiculos_df = load_csv_data()
            if st.session_state.veiculos_df is not None:
                logger.info(f"Dados de veículos carregados: {len(st.session_state.veiculos_df)} registros")
        except Exception as e:
            logger.warning(f"Erro ao carregar dados: {e}")
            st.session_state.veiculos_df = None
    else:
        st.session_state.veiculos_df = None

# Carregar dados de veículos
if "veiculos_df" not in st.session_state:
    if DATA_AVAILABLE:
        try:
            st.session_state.veiculos_df = load_csv_data()
            if st.session_state.veiculos_df is not None:
                logger.info(f"Dados de veículos carregados: {len(st.session_state.veiculos_df)} registros")
        except Exception as e:
            logger.warning(f"Erro ao carregar dados: {e}")
            st.session_state.veiculos_df = None
    else:
        st.session_state.veiculos_df = None

# Configurar timeout (pode ser definido via variável de ambiente ou model_config)
try:
    from src.config.model_config import MODEL_RULES

    DEFAULT_TIMEOUT = MODEL_RULES.get("timeout_seconds", 120)
except ImportError:
    DEFAULT_TIMEOUT = 120

OLLAMA_TIMEOUT = int(
    os.getenv("OLLAMA_TIMEOUT", str(DEFAULT_TIMEOUT))
)  # Padrão vem de model_config.py ou 120 segundos

# Auto-inicialização do handler baseado no provedor
if st.session_state.llm_handler is None:
    try:
        if st.session_state.llm_provider == "openai":
            if OPENAI_AVAILABLE:
                st.session_state.llm_handler = create_openai_handler(timeout=OLLAMA_TIMEOUT)
        else:  # ollama
            if LLM_AVAILABLE:
                st.session_state.llm_handler = create_llm_handler(
                    st.session_state.ollama_url, timeout=OLLAMA_TIMEOUT
                )
        # Verificar conexão silenciosamente na inicialização
        if st.session_state.llm_handler:
            st.session_state.llm_handler.is_configured()
    except Exception as e:
        st.session_state.llm_handler = None
        # Log do erro (pode ser útil para debug)
        if "connection_debug" not in st.session_state:
            st.session_state.connection_debug = str(e)

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
        # Seleção de provedor LLM
        st.markdown("### 🤖 Provedor de IA")
        llm_provider = st.selectbox(
            "Escolha o provedor de IA",
            ["ollama", "openai"],
            index=0 if st.session_state.llm_provider == "ollama" else 1,
            help="Ollama: modelos locais. OpenAI: modelos da OpenAI (requer API key)",
        )

        if llm_provider != st.session_state.llm_provider:
            st.session_state.llm_provider = llm_provider
            st.session_state.llm_handler = None
            st.rerun()

        # Configuração baseada no provedor selecionado
        if st.session_state.llm_provider == "openai":
            st.markdown("### 🔧 Configuração da OpenAI")
            
            # Verificar se a API key está configurada
            openai_key = os.getenv("OPENAI_API_KEY", "")
            if not openai_key:
                st.warning(
                    "⚠️ OPENAI_API_KEY não encontrada no arquivo .env. "
                    "Configure a chave no arquivo .env para usar modelos OpenAI."
                )
                st.info(
                    "💡 Para configurar: Edite o arquivo `.env` e adicione:\n"
                    "`OPENAI_API_KEY=sk-sua-chave-aqui`"
                )

            if st.button("🔄 Conectar à OpenAI", use_container_width=True):
                try:
                    if OPENAI_AVAILABLE:
                        # Usar API key do .env (não da interface)
                        st.session_state.llm_handler = create_openai_handler(
                            api_key=None, timeout=OLLAMA_TIMEOUT
                        )
                        if (
                            st.session_state.llm_handler
                            and st.session_state.llm_handler.is_configured()
                        ):
                            st.success("✅ Conectado à OpenAI!")
                            st.rerun()
                        else:
                            st.warning("⚠️ OpenAI não está disponível. Verifique a API key.")
                    else:
                        st.error("❌ Módulo OpenAI não disponível")
                except Exception as e:
                    st.error(f"❌ Erro ao conectar: {str(e)}")
                    st.session_state.llm_handler = None

        else:  # ollama
            st.markdown("### 🔧 Configuração do Ollama")
            ollama_url = st.text_input(
                "URL do servidor Ollama",
                value=st.session_state.ollama_url,
                help="URL padrão: http://localhost:11434",
            )

            if ollama_url != st.session_state.ollama_url:
                st.session_state.ollama_url = ollama_url
                try:
                    if LLM_AVAILABLE:
                        st.session_state.llm_handler = create_llm_handler(
                            ollama_url, timeout=OLLAMA_TIMEOUT
                        )
                        if (
                            st.session_state.llm_handler
                            and st.session_state.llm_handler.is_configured()
                        ):
                            st.success("✅ Conectado ao Ollama!")
                        else:
                            st.warning("⚠️ Ollama não está disponível nesta URL")
                    else:
                        st.error("❌ Módulo Ollama não disponível")
                except Exception as e:
                    st.error(f"❌ Erro ao conectar: {str(e)}")
                    st.session_state.llm_handler = None

        # Status detalhado da conexão
        if st.session_state.llm_handler:
            status = st.session_state.llm_handler.get_connection_status()
            if status["connected"]:
                st.success(status["message"])
                if st.session_state.llm_provider == "ollama":
                    st.info(
                        f"📡 URL: {status.get('url', 'N/A')} | 📦 Modelos: {status.get('model_count', 0)}"
                    )
                else:  # openai
                    st.info(
                        f"📦 Modelos disponíveis: {status.get('model_count', 0)}"
                    )
                if status.get("models"):
                    st.caption(f"Modelos: {', '.join(status['models'])}")
            else:
                st.error(status["message"])
                if status.get("error"):
                    st.caption(f"Erro: {status['error']}")
                if status.get("suggestion"):
                    st.info(f"💡 {status['suggestion']}")
        else:
            st.warning("⚠️ Handler não inicializado")

        # Botão para reconectar
        provider_name = "Ollama" if st.session_state.llm_provider == "ollama" else "OpenAI"
        if st.button(f"🔄 Reconectar ao {provider_name}", use_container_width=True):
            try:
                if st.session_state.llm_provider == "openai":
                    if OPENAI_AVAILABLE:
                        # Usar API key do .env (não da interface)
                        st.session_state.llm_handler = create_openai_handler(
                            api_key=None, timeout=OLLAMA_TIMEOUT
                        )
                    else:
                        st.error("❌ Módulo OpenAI não disponível")
                else:  # ollama
                    if LLM_AVAILABLE:
                        st.session_state.llm_handler = create_llm_handler(
                            st.session_state.ollama_url, timeout=OLLAMA_TIMEOUT
                        )
                    else:
                        st.error("❌ Módulo Ollama não disponível")

                if st.session_state.llm_handler:
                    status = st.session_state.llm_handler.get_connection_status()
                    if status["connected"]:
                        st.success("✅ Conectado com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"❌ {status['message']}")
                        if status.get("error"):
                            st.caption(f"Detalhes: {status['error']}")
                        if status.get("suggestion"):
                            st.info(f"💡 {status['suggestion']}")
                else:
                    st.error("❌ Não foi possível criar o handler")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
                import traceback

                with st.expander("🔍 Detalhes do erro"):
                    st.code(traceback.format_exc())

        # Seleção de modelo - buscar dinamicamente do provedor selecionado
        st.markdown("### 📦 Seleção de Modelo")
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
                    model_label = f"Modelo {provider_name}"
                    st.session_state.selected_model = st.selectbox(
                        model_label, available_models, index=current_index
                    )
                else:
                    if st.session_state.llm_provider == "ollama":
                        st.warning(
                            "⚠️ Nenhum modelo encontrado. Baixe modelos usando: ollama pull <nome_do_modelo>"
                        )
                    else:
                        st.warning("⚠️ Nenhum modelo disponível")
                    st.session_state.selected_model = st.text_input(
                        "Digite o nome do modelo", value=st.session_state.selected_model
                    )
            else:
                st.warning(f"⚠️ Conecte ao {provider_name} primeiro")
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

        # Informação sobre posição do prompt
        st.markdown("**📍 Posição do Prompt**")
        st.info(
            "💡 O prompt e o gravador de voz estão fixos no centro inferior da tela para melhor acessibilidade."
        )

        st.markdown("---")

        # Configuração de tema
        st.markdown("### 🎨 Aparência")
        theme = st.selectbox(
            "Tema da página",
            ["escuro", "claro"],  # Escuro primeiro (padrão)
            index=0 if st.session_state.theme == "escuro" else 1,
            help="Escolha entre tema escuro ou claro",
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
        logger.warning("Tentativa de enviar mensagem sem Ollama configurado")
    else:
        # Validar input do usuário
        if VALIDATION_AVAILABLE:
            user_input = sanitize_input(user_input)
            is_valid, error = validate_user_input(user_input)
            if not is_valid:
                st.error(f"❌ {error}")
                logger.warning(f"Input do usuário rejeitado: {error}")
                st.stop()

        logger.info(f"Mensagem do usuário recebida: {len(user_input)} caracteres")

        # Adicionar mensagem do usuário no histórico
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Exibir imediatamente a mensagem do usuário
        with st.chat_message("user"):
            st.markdown(user_input)

        # Gerar resposta
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            try:
                # Gerar resposta (streaming será implementado futuramente)
                response = st.session_state.llm_handler.generate_response(
                    messages=st.session_state.messages,
                    model=st.session_state.selected_model,
                    temperature=st.session_state.temperature,
                    stream=False,  # Streaming pode ser ativado aqui
                )

                placeholder.markdown(response)
                full_response = response
                logger.info(f"Resposta gerada: {len(full_response)} caracteres")
            except Exception as e:
                error_msg = f"Erro ao gerar resposta: {str(e)}"
                placeholder.error(error_msg)
                logger.error(error_msg, exc_info=True)
                full_response = error_msg

        # Salvar no histórico
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

        # Salvar histórico automaticamente
        if HISTORY_AVAILABLE:
            try:
                auto_save_history(st.session_state.messages, "current")
            except Exception as e:
                logger.warning(f"Erro ao salvar histórico: {e}")

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

                # Tentar gerar gráfico se o usuário solicitou
                if DATA_AVAILABLE and CHARTS_AVAILABLE and st.session_state.veiculos_df is not None:
                    try:
                        from src.core.chart_analyzer import create_smart_chart, detect_chart_request
                        
                        # Verificar última mensagem do usuário
                        if len(st.session_state.messages) >= 2:
                            last_user_message = st.session_state.messages[-2].get("content", "")
                            
                            # Detectar se é solicitação de gráfico
                            chart_request = detect_chart_request(last_user_message)
                            if chart_request:
                                st.markdown("---")
                                st.markdown("### 📈 Visualização Gerada")
                                
                                # Criar gráfico inteligente
                                chart = create_smart_chart(st.session_state.veiculos_df, last_user_message)
                                if chart:
                                    display_chart(chart)
                                else:
                                    # Tentar gráfico padrão
                                    from src.core.chart_generator import create_bar_chart
                                    df = st.session_state.veiculos_df
                                    if "cidade" in df.columns and "km_mes" in df.columns:
                                        # Agrupar por cidade
                                        df_grouped = df.groupby("cidade")["km_mes"].sum().reset_index()
                                        chart = create_bar_chart(df_grouped, x="cidade", y="km_mes", 
                                                                title="Quilometragem Total por Cidade")
                                        if chart:
                                            display_chart(chart)
                    except Exception as e:
                        logger.warning(f"Erro ao gerar gráfico: {e}")

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

    # Prompt e gravador sempre no centro, abaixo da tela
    st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço antes do prompt

    # Mostrar indicador de pensando acima do prompt se estiver pensando
    if st.session_state.is_thinking:
        st.markdown(
            '<div class="thinking-above-prompt">💭 <em>Pensando...</em></div>',
            unsafe_allow_html=True,
        )

    # Input de mensagem usando chat_input no centro
    center_user_input = st.chat_input(
        "Digite sua mensagem...", key="center_chat_input"
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
                "⚠️ Provedor de IA não está disponível. Verifique a conexão nas configurações."
            )
            logger.warning("Tentativa de enviar mensagem sem handler configurado")
        else:
            # Validar input do usuário
            if VALIDATION_AVAILABLE:
                center_user_input = sanitize_input(center_user_input)
                is_valid, error = validate_user_input(center_user_input)
                if not is_valid:
                    st.error(f"❌ {error}")
                    logger.warning(f"Input do usuário rejeitado: {error}")
                    st.stop()

            logger.info(
                f"Mensagem do usuário recebida (centro): {len(center_user_input)} caracteres"
            )

            # Adicionar mensagem do usuário no histórico
            st.session_state.messages.append(
                {"role": "user", "content": center_user_input}
            )

            # Exibir imediatamente a mensagem do usuário
            with st.chat_message("user"):
                st.markdown(center_user_input)

            # Gerar resposta
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_response = ""

                try:
                    # Gerar resposta
                    response = st.session_state.llm_handler.generate_response(
                        messages=st.session_state.messages,
                        model=st.session_state.selected_model,
                        temperature=st.session_state.temperature,
                        stream=False,
                    )

                    placeholder.markdown(response)
                    full_response = response
                    logger.info(f"Resposta gerada: {len(full_response)} caracteres")
                except Exception as e:
                    error_msg = f"Erro ao gerar resposta: {str(e)}"
                    placeholder.error(error_msg)
                    logger.error(error_msg, exc_info=True)
                    full_response = error_msg

            # Salvar no histórico
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

            # Salvar histórico automaticamente
            if HISTORY_AVAILABLE:
                try:
                    auto_save_history(st.session_state.messages, "current")
                except Exception as e:
                    logger.warning(f"Erro ao salvar histórico: {e}")

            # Recarregar para atualizar a interface
            st.rerun()
