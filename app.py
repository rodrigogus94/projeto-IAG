# app.py - Layout moderno com sidebar de chat
import streamlit as st
import os
from typing import Tuple
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Tenta importar, se falhar cria um handler mock
try:
    from llm_handler import create_llm_handler

    LLM_AVAILABLE = True
except ImportError as e:
    LLM_AVAILABLE = False

    # Cria uma classe mock para teste
    class MockLLMHandler:
        def __init__(self, api_key=None):
            self.api_key = api_key

        def generate_response(
            self, messages=None, user_input=None, model="gpt-3.5-turbo", temperature=0.7
        ):
            input_text = user_input or (
                messages[-1]["content"] if messages else "sem entrada"
            )
            return f"[MOCK] Resposta para: {input_text}\n\nAPI Key configurada: {bool(self.api_key)}"

        def is_configured(self):
            return bool(self.api_key)

    def create_llm_handler(api_key=None):
        return MockLLMHandler(api_key)


# Configuração da página com layout wide
st.set_page_config(
    page_title="Omnilink AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado para estilo similar à imagem
st.markdown(
    """
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
     """,
    unsafe_allow_html=True,
)

# Inicialização do session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_handler" not in st.session_state:
    st.session_state.llm_handler = None

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-3.5-turbo"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "input_key_counter" not in st.session_state:
    st.session_state.input_key_counter = 0

if "prompt_in_center" not in st.session_state:
    st.session_state.prompt_in_center = False

if "audio_transcribed" not in st.session_state:
    st.session_state.audio_transcribed = None

if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False

# Auto-inicialização se API Key do .env estiver disponível e válida
if st.session_state.llm_handler is None:
    env_api_key = os.getenv("OPENAI_API_KEY", "")
    if env_api_key:
        if env_api_key.startswith("sk-") and len(env_api_key) >= 20:
            st.session_state.llm_handler = create_llm_handler(env_api_key)

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

    # Entrada por microfone (acima do prompt)
    audio_file = st.audio_input("🎙️ Grave uma mensagem de voz (opcional)")

    # Processar áudio se fornecido
    if audio_file:
        st.audio(audio_file, format="audio/wav")
        with st.spinner("Transcrevendo áudio..."):
            # TODO: Aqui você chamaria a função de transcrição
            # user_text_from_audio = transcrever_audio_para_texto(audio_file)
            # Por enquanto, vamos simular
            st.session_state.audio_transcribed = (
                "Mensagem transcrita do áudio (implementar transcrição)"
            )
        if st.session_state.audio_transcribed:
            st.info(
                f"📝 Transcrição do áudio: **{st.session_state.audio_transcribed}**"
            )

    # Mostrar indicador de pensando acima do prompt se estiver pensando
    if st.session_state.is_thinking:
        st.markdown(
            '<div class="thinking-above-prompt">💭 <em>Pensando...</em></div>',
            unsafe_allow_html=True,
        )

    # Input de mensagem usando chat_input (como no código de exemplo)
    # Apenas se não estiver no centro
    if not st.session_state.prompt_in_center:
        # Usar texto transcrito do áudio se disponível
        user_input = st.chat_input("Digite sua mensagem (ou use o microfone acima)")

        # Se houver transcrição e não houver input do usuário, usar a transcrição
        if audio_file and not user_input and st.session_state.audio_transcribed:
            user_input = st.session_state.audio_transcribed
            st.session_state.audio_transcribed = None  # Limpar após usar
    else:
        # Placeholder para manter estrutura
        user_input = None

    # Processar mensagem quando enviada (texto ou áudio transcrito)
    if user_input:
        if st.session_state.llm_handler is None:
            st.error("⚠️ Configure a API Key primeiro nas configurações")
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

                # Simulação de streaming (opcional - pode ser removido se não quiser)
                # for chunk in response.split():
                #     full_response += chunk + " "
                #     placeholder.markdown(full_response + "▌")

                placeholder.markdown(response)
                full_response = response

            # Salvar no histórico
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

            # Recarregar para atualizar a interface
            st.rerun()

    st.markdown("---")

    # Configurações (colapsável)
    with st.expander("⚙️ Configurações"):
        # Opção para usar .env ou input manual
        use_env = st.checkbox("Usar variáveis de ambiente (.env)", value=True)

        # Carrega API Key do .env se disponível
        env_api_key = os.getenv("OPENAI_API_KEY", "")

        if use_env:
            if env_api_key:
                st.success("✅ API Key carregada do .env")
                manual_key = st.text_input(
                    "Ou insira manualmente (sobrescreve .env):",
                    type="password",
                    value="",
                    placeholder="Deixe em branco para usar .env",
                )
                api_key = manual_key if manual_key else env_api_key
            else:
                st.warning("⚠️ OPENAI_API_KEY não encontrada no .env")
                api_key = st.text_input(
                    "OpenAI API Key",
                    type="password",
                    placeholder="sk-...",
                )
        else:
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-...",
            )

        # Validação de API Key
        def validate_api_key(key: str) -> Tuple[bool, str]:
            """Valida o formato da API Key"""
            if not key:
                return False, "API Key não pode estar vazia"
            if not key.startswith("sk-"):
                return False, "API Key deve começar com 'sk-'"
            if len(key) < 20:
                return False, "API Key muito curta (mínimo 20 caracteres)"
            return True, "✅ API Key válida"

        # Botão para inicializar
        if st.button("🔄 Inicializar", type="primary", use_container_width=True):
            if api_key:
                is_valid, message = validate_api_key(api_key)
                if is_valid:
                    st.session_state.llm_handler = create_llm_handler(api_key)
                    st.success("Handler inicializado!")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("Por favor, insira uma API Key")

        # Seleção de modelo
        model_options = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-4o",
            "gpt-4o-mini",
        ]
        st.session_state.selected_model = st.selectbox("Modelo", model_options, index=0)

        # Controle de temperatura
        st.session_state.temperature = st.slider(
            "Criatividade (temperature)",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
        )

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

        api_configured = (
            "✅ Sim"
            if (
                st.session_state.llm_handler
                and st.session_state.llm_handler.is_configured()
            )
            else "❌ Não"
        )
        api_configured_color = (
            "#28a745"
            if (
                st.session_state.llm_handler
                and st.session_state.llm_handler.is_configured()
            )
            else "#dc3545"
        )

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
                    <span class="status-label">API Key Configurada</span>
                    <span class="status-value" style="color: {api_configured_color};">
                        {api_configured}
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

                # Estilo para botões de ação - apenas ícones com tooltips
                st.markdown(
                    """
                    <style>
                    /* Container dos botões de ação */
                    div[data-testid="column"]:has(button[key="btn_regenerar"]),
                    div[data-testid="column"]:has(button[key="btn_copiar"]),
                    div[data-testid="column"]:has(button[key="btn_limpar"]) {
                        display: flex;
                        justify-content: center;
                    }
                    
                    /* Estilizar botões de ação - apenas ícones */
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
                        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
                    }
                    
                    button[key="btn_regenerar"]:hover,
                    button[key="btn_copiar"]:hover,
                    button[key="btn_limpar"]:hover {
                        transform: translateY(-3px) !important;
                        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.5) !important;
                    }
                    
                    /* Ocultar qualquer texto dentro dos botões */
                    button[key="btn_regenerar"] > div > p,
                    button[key="btn_copiar"] > div > p,
                    button[key="btn_limpar"] > div > p {
                        display: none !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

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

                # JavaScript para adicionar tooltips funcionais
                st.markdown(
                    """
                    <script>
                    (function() {
                        function addTooltips() {
                            const tooltips = {
                                'btn_regenerar': 'Regenerar',
                                'btn_copiar': 'Copiar',
                                'btn_limpar': 'Limpar'
                            };
                            
                            Object.keys(tooltips).forEach(key => {
                                const button = document.querySelector(`button[key="${key}"]`);
                                if (button && !button.hasAttribute('data-tooltip-added')) {
                                    button.setAttribute('data-tooltip-added', 'true');
                                    button.setAttribute('title', tooltips[key]);
                                    
                                    // Criar tooltip customizado
                                    const tooltip = document.createElement('div');
                                    tooltip.className = 'custom-tooltip';
                                    tooltip.textContent = tooltips[key];
                                    tooltip.style.cssText = `
                                        position: absolute;
                                        bottom: calc(100% + 10px);
                                        left: 50%;
                                        transform: translateX(-50%);
                                        background: rgba(0, 0, 0, 0.9);
                                        color: white;
                                        padding: 0.5rem 1rem;
                                        border-radius: 6px;
                                        font-size: 0.85rem;
                                        white-space: nowrap;
                                        z-index: 10000;
                                        pointer-events: none;
                                        opacity: 0;
                                        transition: opacity 0.2s ease;
                                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                                    `;
                                    
                                    // Seta do tooltip
                                    const arrow = document.createElement('div');
                                    arrow.style.cssText = `
                                        position: absolute;
                                        top: 100%;
                                        left: 50%;
                                        transform: translateX(-50%);
                                        border: 5px solid transparent;
                                        border-top-color: rgba(0, 0, 0, 0.9);
                                    `;
                                    tooltip.appendChild(arrow);
                                    button.appendChild(tooltip);
                                    
                                    // Mostrar tooltip no hover
                                    button.addEventListener('mouseenter', function() {
                                        tooltip.style.opacity = '1';
                                    });
                                    
                                    button.addEventListener('mouseleave', function() {
                                        tooltip.style.opacity = '0';
                                    });
                                }
                            });
                        }
                        
                        // Executar quando o DOM estiver pronto
                        if (document.readyState === 'loading') {
                            document.addEventListener('DOMContentLoaded', addTooltips);
                        } else {
                            addTooltips();
                        }
                        
                        // Executar após delays
                        setTimeout(addTooltips, 100);
                        setTimeout(addTooltips, 500);
                        setTimeout(addTooltips, 1000);
                        
                        // Observar mudanças no DOM
                        const observer = new MutationObserver(function() {
                            setTimeout(addTooltips, 50);
                        });
                        observer.observe(document.body, { 
                            childList: true, 
                            subtree: true 
                        });
                    })();
                    </script>
                    """,
                    unsafe_allow_html=True,
                )

        # Histórico completo (colapsável)
        if len(st.session_state.messages) > 2:
            with st.expander("📜 Histórico Completo da Conversa"):
                for i, message in enumerate(st.session_state.messages):
                    role_icon = "👤" if message["role"] == "user" else "🤖"
                    st.markdown(f"**{role_icon} {message['role'].title()}:**")
                    st.markdown(message["content"])
                    if i < len(st.session_state.messages) - 1:
                        st.markdown("---")

    # Prompt no centro (se configurado ou quando sidebar está escondida)
    # Verificar se deve mostrar prompt no centro
    show_center_prompt = st.session_state.prompt_in_center

    if show_center_prompt:
        st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço antes do prompt

        # Entrada por microfone no centro (acima do prompt)
        center_audio_file = st.audio_input(
            "🎙️ Grave uma mensagem de voz (opcional)", key="audio_input_center"
        )

        # Processar áudio se fornecido
        if center_audio_file:
            st.audio(center_audio_file, format="audio/wav")
            with st.spinner("Transcrevendo áudio..."):
                # TODO: Aqui você chamaria a função de transcrição
                # user_text_from_audio = transcrever_audio_para_texto(center_audio_file)
                # Por enquanto, vamos simular
                st.session_state.audio_transcribed = (
                    "Mensagem transcrita do áudio (implementar transcrição)"
                )
            if st.session_state.audio_transcribed:
                st.info(
                    f"📝 Transcrição do áudio: **{st.session_state.audio_transcribed}**"
                )

        # Mostrar indicador de pensando acima do prompt se estiver pensando
        if st.session_state.is_thinking:
            st.markdown(
                '<div class="thinking-above-prompt">💭 <em>Pensando...</em></div>',
                unsafe_allow_html=True,
            )

        # Input de mensagem usando chat_input (como no código de exemplo)
        center_user_input = st.chat_input(
            "Digite sua mensagem (ou use o microfone acima)"
        )

        # Se houver transcrição e não houver input do usuário, usar a transcrição
        if (
            center_audio_file
            and not center_user_input
            and st.session_state.audio_transcribed
        ):
            center_user_input = st.session_state.audio_transcribed
            st.session_state.audio_transcribed = None  # Limpar após usar

        # Processar mensagem quando enviada do centro
        if center_user_input:
            if st.session_state.llm_handler is None:
                st.error("⚠️ Configure a API Key primeiro nas configurações")
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

                    # Simulação de streaming (opcional - pode ser removido se não quiser)
                    # for chunk in response.split():
                    #     full_response += chunk + " "
                    #     placeholder.markdown(full_response + "▌")

                    placeholder.markdown(response)
                    full_response = response

                # Salvar no histórico
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

                # Recarregar para atualizar a interface
                st.rerun()

# JavaScript para mostrar indicador de "pensando" acima do prompt
st.markdown(
    """
    <script>
    (function() {
        function showThinkingAbovePrompt() {
            // Encontrar o chat_input
            const chatInputs = document.querySelectorAll('[data-testid="stChatInput"]');
            
            chatInputs.forEach(chatInput => {
                // Verificar se já existe um indicador
                const existingIndicator = chatInput.parentElement.querySelector('.thinking-above-prompt');
                
                // Verificar se há uma mensagem do assistente sendo gerada
                const assistantMessages = document.querySelectorAll('[data-testid="stChatMessage"]');
                let isGenerating = false;
                
                assistantMessages.forEach(msg => {
                    const isAssistant = msg.getAttribute('data-testid') && 
                                       msg.getAttribute('data-testid').includes('assistant');
                    if (isAssistant) {
                        // Verificar se a mensagem está vazia ou tem apenas placeholder
                        const markdownContainers = msg.querySelectorAll('[data-testid="stMarkdownContainer"]');
                        const hasContent = Array.from(markdownContainers).some(c => {
                            const text = c.textContent.trim();
                            return text.length > 0 && !text.includes('▌');
                        });
                        
                        // Se não tem conteúdo ainda, está gerando
                        if (!hasContent) {
                            isGenerating = true;
                        }
                    }
                });
                
                // Se está gerando e não tem indicador, criar um
                if (isGenerating && !existingIndicator) {
                    const indicator = document.createElement('div');
                    indicator.className = 'thinking-above-prompt';
                    indicator.innerHTML = '💭 <em>Pensando...</em>';
                    
                    // Inserir antes do chat_input
                    const parent = chatInput.parentElement;
                    if (parent) {
                        parent.insertBefore(indicator, chatInput);
                    }
                }
                
                // Se não está gerando e tem indicador, remover
                if (!isGenerating && existingIndicator) {
                    existingIndicator.remove();
                }
            });
        }
        
        // Executar quando o DOM estiver pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', showThinkingAbovePrompt);
        } else {
            showThinkingAbovePrompt();
        }
        
        // Executar frequentemente para capturar mudanças
        setInterval(showThinkingAbovePrompt, 100);
        
        // Observar mudanças no DOM
        const observer = new MutationObserver(function() {
            setTimeout(showThinkingAbovePrompt, 50);
        });
        observer.observe(document.body, { 
            childList: true, 
            subtree: true 
        });
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

# JavaScript para detectar quando sidebar está escondida e mover prompt automaticamente
if not st.session_state.prompt_in_center:
    st.markdown(
        """
        <script>
        (function() {
            let lastSidebarState = null;
            
            function checkSidebarState() {
                const sidebar = document.querySelector('[data-testid="stSidebar"]');
                if (!sidebar) return;
                
                const isVisible = sidebar.offsetParent !== null;
                
                // Se sidebar mudou de estado (de visível para escondida)
                if (lastSidebarState === true && isVisible === false) {
                    // Notificar que sidebar foi escondida
                    console.log('Sidebar escondida - prompt deve ir para o centro');
                    // Aqui poderia fazer um callback para Streamlit, mas por enquanto
                    // apenas mostra uma mensagem visual
                }
                
                lastSidebarState = isVisible;
            }
            
            // Verificar quando a página carrega
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', checkSidebarState);
            } else {
                checkSidebarState();
            }
            
            // Verificar quando há mudanças no DOM
            const observer = new MutationObserver(checkSidebarState);
            observer.observe(document.body, { 
                childList: true, 
                subtree: true,
                attributes: true,
                attributeFilter: ['style', 'class']
            });
            
            // Verificar periodicamente (fallback)
            setInterval(checkSidebarState, 1000);
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
