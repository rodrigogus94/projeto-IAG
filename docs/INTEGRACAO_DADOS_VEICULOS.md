# 🚗 Integração de Dados de Veículos - Guia Completo

## 📋 Resumo

Foi implementada uma solução completa para carregar dados do arquivo `dados_veiculos_300.csv` e gerar gráficos automaticamente através de comandos em linguagem natural.

## ✨ Funcionalidades Implementadas

### 1. Carregamento Automático de Dados
- ✅ Carrega automaticamente o arquivo CSV na inicialização
- ✅ Armazena dados no `session_state` para acesso rápido
- ✅ Validação e tratamento de erros

### 2. Geração Inteligente de Gráficos
- ✅ Detecta automaticamente solicitações de gráficos
- ✅ Analisa a intenção do usuário
- ✅ Gera o gráfico mais apropriado
- ✅ Suporta múltiplos tipos de gráficos

### 3. Tipos de Gráficos Suportados
- ✅ Gráfico de Barras
- ✅ Gráfico de Pizza
- ✅ Histograma
- ✅ Gráfico de Dispersão
- ✅ Box Plot
- ✅ Heatmap (Mapa de Calor)
- ✅ Gráfico de Linha

## 📁 Arquivos Criados

### 1. `src/core/data_loader.py`
**Função**: Carregar e processar dados CSV

**Principais Funções**:
- `load_csv_data()` - Carrega arquivo CSV
- `get_data_info()` - Retorna informações sobre os dados
- `filter_data()` - Filtra dados por critérios
- `get_data_summary()` - Resumo textual dos dados

### 2. `src/core/chart_generator.py`
**Função**: Gerar gráficos usando Plotly

**Principais Funções**:
- `create_bar_chart()` - Gráfico de barras
- `create_pie_chart()` - Gráfico de pizza
- `create_histogram()` - Histograma
- `create_scatter_chart()` - Gráfico de dispersão
- `create_box_plot()` - Box plot
- `create_heatmap()` - Mapa de calor
- `display_chart()` - Exibir gráfico no Streamlit

### 3. `src/core/chart_analyzer.py`
**Função**: Analisar solicitações e gerar gráficos automaticamente

**Principais Funções**:
- `detect_chart_request()` - Detecta se é solicitação de gráfico
- `extract_columns()` - Extrai colunas mencionadas
- `suggest_chart_for_data()` - Sugere gráfico apropriado
- `create_smart_chart()` - Cria gráfico inteligente

## 🎯 Como Usar

### Exemplo 1: Gráfico Simples
**Digite**: "Mostre um gráfico de veículos por cidade"

**Resultado**: Gráfico de barras com quantidade de veículos por cidade

### Exemplo 2: Gráfico de Distribuição
**Digite**: "Exiba a distribuição de status dos veículos"

**Resultado**: Gráfico de pizza mostrando ativos, inativos e em manutenção

### Exemplo 3: Análise por Marca
**Digite**: "Gráfico de barras de veículos por marca"

**Resultado**: Gráfico de barras com quantidade de veículos de cada marca

### Exemplo 4: Histograma
**Digite**: "Histograma de consumo de combustível"

**Resultado**: Histograma mostrando distribuição de consumo

## 📊 Estrutura dos Dados

O arquivo CSV contém 300 registros com as seguintes colunas:

### Colunas Numéricas
- `km_mes` - Quilometragem mensal
- `velocidade_media` - Velocidade média (km/h)
- `alertas` - Número de alertas
- `consumo_combustivel` - Consumo de combustível
- `dias_operacionais` - Dias operacionais no mês
- `custo_manutencao` - Custo de manutenção (R$)
- `ano` - Ano de fabricação

### Colunas Categóricas
- `marca` - Marca do veículo
- `modelo` - Modelo do veículo
- `status` - Status (ativo, inativo, manutencao)
- `cidade` - Cidade onde está localizado

## 🔧 Integração no App

O sistema está integrado ao `app.py` e funciona automaticamente:

1. **Carregamento**: Dados são carregados na inicialização
2. **Detecção**: Sistema detecta quando você pede um gráfico
3. **Geração**: Gráfico é gerado automaticamente
4. **Exibição**: Gráfico aparece abaixo da resposta do assistente

## 💡 Palavras-Chave Reconhecidas

O sistema reconhece estas palavras para detectar solicitações de gráficos:

- **Gráfico**: "gráfico", "grafico", "chart", "visualização"
- **Ações**: "mostre", "exiba", "crie", "gere", "criar"
- **Análise**: "dashboard", "análise", "estatística", "visualização"

## 🎨 Tipos de Gráficos e Quando Usar

### Gráfico de Barras
**Quando usar**: Comparar valores entre categorias
**Exemplo**: "Gráfico de barras de km_mes por cidade"

### Gráfico de Pizza
**Quando usar**: Mostrar proporções
**Exemplo**: "Distribuição de veículos por status"

### Histograma
**Quando usar**: Ver distribuição de valores numéricos
**Exemplo**: "Histograma de consumo de combustível"

### Gráfico de Dispersão
**Quando usar**: Ver correlação entre duas variáveis
**Exemplo**: "Correlação entre km_mes e consumo"

### Box Plot
**Quando usar**: Ver distribuição estatística
**Exemplo**: "Box plot de consumo por marca"

### Heatmap
**Quando usar**: Ver correlações entre múltiplas variáveis
**Exemplo**: "Mapa de calor de correlação"

## 🚀 Próximos Passos

1. **Instale as dependências** (já instalado):
   ```bash
   pip install pandas plotly
   ```

2. **Execute o projeto**:
   ```bash
   streamlit run src/app.py
   ```

3. **Teste os gráficos**:
   - "Mostre um gráfico de veículos por cidade"
   - "Exiba a distribuição de status"
   - "Gráfico de barras de marcas"

## 📝 Notas Técnicas

- Os dados são carregados uma vez na inicialização
- Gráficos são gerados usando Plotly (interativos)
- Sistema detecta automaticamente o tipo de gráfico mais apropriado
- Suporta agregações automáticas (soma, média, contagem)

## 🔍 Exemplos Avançados

### Análise por Múltiplas Dimensões
```
"Gráfico de consumo médio por marca e cidade"
"Box plot de velocidade por status"
```

### Análise de Correlação
```
"Mapa de calor de correlação entre variáveis numéricas"
"Gráfico de dispersão de km_mes vs consumo"
```

### Análise Temporal
```
"Gráfico de linha de consumo ao longo dos anos"
"Tendência de custo de manutenção"
```

---

**Implementado para o Projeto IAG - Chat Assistente com IA**

