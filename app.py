# app.py - Layout moderno com sidebar de chat
import streamlit as st
import os
from typing import Optional
from dotenv import load_dotenv

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

# Adicionar CSS específico para alternância microfone/seta
st.markdown(
    """
<style>
/* Container principal para chat input */
.chat-input-wrapper {
    position: relative;
    width: 100%;
}

/* Esconder completamente o label do audio input */
div[data-testid="stAudioInput"] label {
    display: none !important;
}

/* Posicionar o audio input ao lado do botão de envio */
div[data-testid="stAudioInput"] {
    position: absolute !important;
    right: 45px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 1000 !important;
    width: auto !important;
}

/* Estilizar o botão do audio input */
div[data-testid="stAudioInput"] button {
    background: transparent !important;
    border: none !important;
    padding: 8px !important;
    min-width: 40px !important;
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

div[data-testid="stAudioInput"] button:hover {
    background: rgba(102, 126, 234, 0.1) !important;
    color: #667eea !important;
}

/* Ocultar microfone quando há texto */
.hide-microphone div[data-testid="stAudioInput"] {
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Mostrar microfone quando não há texto */
.show-microphone div[data-testid="stAudioInput"] {
    opacity: 1 !important;
    pointer-events: all !important;
}

/* Ocultar seta de envio quando não há texto */
.hide-send-button button[aria-label="Send"] {
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Mostrar seta de envio quando há texto */
.show-send-button button[aria-label="Send"] {
    opacity: 1 !important;
    pointer-events: all !important;
}

/* Indicador de pensando */
.thinking-indicator {
    text-align: center;
    color: #667eea;
    font-style: italic;
    margin: 10px 0;
    padding: 8px;
    background: rgba(102, 126, 234, 0.1);
    border-radius: 8px;
    font-size: 0.9rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# JavaScript para alternância microfone/seta
st.markdown(
    """
<script>
// Função para configurar a alternância
function setupMicrophoneToggle() {
    // Encontrar todos os containers de chat
    const chatInputs = document.querySelectorAll('[data-testid="stChatInput"]');
    
    chatInputs.forEach((chatInput, index) => {
        // Criar wrapper se não existir
        let wrapper = chatInput.closest('.chat-input-wrapper');
        if (!wrapper) {
            wrapper = document.createElement('div');
            wrapper.className = 'chat-input-wrapper hide-send-button show-microphone';
            chatInput.parentNode.insertBefore(wrapper, chatInput);
            wrapper.appendChild(chatInput);
        }
        
        // Encontrar elementos
        const textInput = chatInput.querySelector('input[type="text"]');
        const sendButton = chatInput.querySelector('button[aria-label="Send"]');
        
        if (!textInput || !sendButton) return;
        
        // Função para atualizar visibilidade
        function updateVisibility() {
            const hasText = textInput.value.trim().length > 0;
            
            if (hasText) {
                // Tem texto: mostrar seta, ocultar microfone
                wrapper.classList.remove('hide-send-button');
                wrapper.classList.add('show-send-button');
                wrapper.classList.add('hide-microphone');
                wrapper.classList.remove('show-microphone');
            } else {
                // Sem texto: mostrar microfone, ocultar seta
                wrapper.classList.add('hide-send-button');
                wrapper.classList.remove('show-send-button');
                wrapper.classList.remove('hide-microphone');
                wrapper.classList.add('show-microphone');
            }
        }
        
        // Configurar listeners
        textInput.addEventListener('input', updateVisibility);
        textInput.addEventListener('keyup', updateVisibility);
        
        // Atualizar inicialmente
        updateVisibility();
        
        // Verificar periodicamente (fallback)
        setInterval(updateVisibility, 500);
    });
}

// Executar quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupMicrophoneToggle);
} else {
    setTimeout(setupMicrophoneToggle, 1000);
}

// Reexecutar quando o Streamlit atualizar a página
let observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length > 0) {
            setTimeout(setupMicrophoneToggle, 500);
        }
    });
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
                    st.markdown(
                        f'<div class="chat-message" style="background: #f0f0f0;"><strong>Você:</strong> {message["content"]}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="chat-message" style="background: #e8f4f8;"><strong>Assistente:</strong> {message["content"]}</div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown(
                '<div style="text-align: center; color: #999; padding: 2.5rem 1rem; font-size: 0.95rem;">Nenhuma mensagem ainda</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Mostrar indicador de pensando acima do prompt se estiver pensando
    if st.session_state.is_thinking:
        st.markdown(
            '<div class="thinking-indicator">💭 <em>Pensando...</em></div>',
            unsafe_allow_html=True,
        )

    # Container integrado para prompt e microfone
    user_input = None
    audio_file = None

    if not st.session_state.prompt_in_center:
        # Input de mensagem usando chat_input
        user_input = st.chat_input("Digite sua mensagem...", key="sidebar_chat_input")

        # Microfone posicionado ao lado do botão de envio via CSS
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

# Processar mensagem quando enviada da sidebar (texto ou áudio transcrito)
if user_input:
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
                '<div class="thinking-indicator">💭 <em>Pensando...</em></div>',
                unsafe_allow_html=True,
            )

        # Input de mensagem no centro
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
