# 💬 Chat Assistente com IA

Aplicação web de chat interativo com IA usando Streamlit e OpenAI API. Interface moderna e intuitiva para conversar com modelos de linguagem da OpenAI.

## 🚀 Características

- **Interface Moderna**: Interface web responsiva construída com Streamlit
- **Múltiplos Modelos**: Suporte para GPT-3.5-turbo, GPT-4, GPT-4o e outros
- **Histórico Completo**: Mantém contexto completo da conversa
- **Configuração Flexível**: Suporte para variáveis de ambiente (.env) ou entrada manual
- **Validações**: Validação automática de API Key e modelos
- **Arquitetura Modular**: Código organizado e separado por responsabilidades

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta na OpenAI com API Key válida
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone ou baixe o projeto**

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure a API Key:**

   Crie um arquivo `.env` na raiz do projeto:
   ```env
   OPENAI_API_KEY=sk-sua-chave-api-aqui
   ```
   
   Ou use o arquivo `.env.example` como referência:
   ```bash
   cp .env.example .env
   # Edite o .env e adicione sua chave
   ```

## 🎯 Como Usar

1. **Inicie a aplicação:**
```bash
streamlit run app.py
```

2. **Configure a API Key:**
   - Na sidebar, marque "Usar variáveis de ambiente (.env)" se você configurou o `.env`
   - Ou desmarque e insira a chave manualmente
   - Clique em "🔄 Inicializar"

3. **Comece a conversar:**
   - Digite sua mensagem no campo de input
   - A IA responderá mantendo o contexto da conversa
   - Use "🗑️ Limpar Chat" para reiniciar a conversa

## ⚙️ Configurações

### Modelos Disponíveis
- `gpt-3.5-turbo` - Rápido e econômico
- `gpt-4` - Mais poderoso e preciso
- `gpt-4-turbo-preview` - Versão preview do GPT-4
- `gpt-4o` - Modelo mais recente e otimizado
- `gpt-4o-mini` - Versão compacta do GPT-4o

### Parâmetros
- **Temperature**: Controla a criatividade (0.0 = determinístico, 2.0 = muito criativo)
- **Max Tokens**: Limite de tokens na resposta (configurável no código)

## 📁 Estrutura do Projeto

```
projeto-sdk-mk00/
├── app.py              # Interface Streamlit principal
├── llm_handler.py      # Handler modular para LLM
├── requirements.txt     # Dependências do projeto
├── .env                # Variáveis de ambiente (criar)
├── .env.example        # Exemplo de configuração
└── README.md           # Este arquivo
```

## 🔐 Segurança

- ⚠️ **Nunca** commite o arquivo `.env` no controle de versão
- ⚠️ Mantenha sua API Key segura e privada
- ✅ O arquivo `.env` está no `.gitignore` por padrão
- ✅ A API Key é ocultada na interface (tipo password)

## 🛠️ Desenvolvimento

### Arquitetura

O projeto segue uma arquitetura modular:

- **`app.py`**: Gerencia a interface do usuário, estado da aplicação e interações
- **`llm_handler.py`**: Encapsula toda a lógica de comunicação com a API da OpenAI

### Melhorias Futuras

- [ ] Suporte para streaming de respostas
- [ ] Exportação de conversas
- [ ] Temas personalizáveis
- [ ] Suporte para múltiplos provedores de LLM
- [ ] Histórico persistente em banco de dados

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional e pessoal.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique se a API Key está configurada corretamente
2. Confirme que todas as dependências estão instaladas
3. Verifique os logs de erro na interface

## 🙏 Agradecimentos

- [Streamlit](https://streamlit.io/) pela excelente framework
- [OpenAI](https://openai.com/) pela API de linguagem

---

Desenvolvido com ❤️ usando Streamlit e OpenAI API

