# 📊 Como Gerar Gráficos com os Dados de Veículos

## 📋 Visão Geral

O projeto agora suporta geração automática de gráficos a partir do arquivo `dados_veiculos_300.csv`. Você pode pedir gráficos em linguagem natural e o sistema irá gerá-los automaticamente.

## 📁 Dados Disponíveis

O arquivo `dados/dados_veiculos_300.csv` contém informações sobre 300 veículos com as seguintes colunas:

- **id_veiculo**: Identificador único
- **marca**: Marca do veículo (Chevrolet, Ford, Toyota, etc.)
- **modelo**: Modelo do veículo
- **ano**: Ano de fabricação
- **status**: Status (ativo, inativo, manutencao)
- **cidade**: Cidade onde o veículo está localizado
- **km_mes**: Quilometragem mensal
- **velocidade_media**: Velocidade média
- **alertas**: Número de alertas
- **consumo_combustivel**: Consumo de combustível
- **dias_operacionais**: Dias operacionais no mês
- **custo_manutencao**: Custo de manutenção

## 🎯 Como Usar

### 1. Pedir um Gráfico em Linguagem Natural

Simplesmente digite o que você quer ver. Exemplos:

```
"Mostre um gráfico de quilometragem por cidade"
"Crie um gráfico de barras com veículos por marca"
"Exiba a distribuição de status dos veículos"
"Gere um gráfico de pizza com veículos por cidade"
"Mostre um histograma de consumo de combustível"
```

### 2. Tipos de Gráficos Disponíveis

#### Gráfico de Barras
```
"Gráfico de barras de km_mes por cidade"
"Barras de veículos por marca"
"Mostre um gráfico de barras"
```

#### Gráfico de Pizza
```
"Gráfico de pizza de status"
"Distribuição de veículos por cidade"
"Pizza de marcas"
```

#### Histograma
```
"Histograma de consumo de combustível"
"Distribuição de velocidade média"
"Histograma de km_mes"
```

#### Gráfico de Dispersão
```
"Gráfico de dispersão de km_mes vs consumo"
"Correlação entre velocidade e consumo"
```

#### Box Plot
```
"Box plot de consumo por marca"
"Box plot de km_mes por status"
```

#### Heatmap (Mapa de Calor)
```
"Mapa de calor de correlação"
"Heatmap das variáveis numéricas"
```

## 🔍 Exemplos Práticos

### Exemplo 1: Gráfico por Cidade
**Solicitação**: "Mostre um gráfico de quilometragem total por cidade"

**Resultado**: Gráfico de barras mostrando a soma de `km_mes` agrupado por `cidade`

### Exemplo 2: Distribuição por Status
**Solicitação**: "Exiba a distribuição de veículos por status"

**Resultado**: Gráfico de pizza mostrando quantos veículos estão ativos, inativos ou em manutenção

### Exemplo 3: Análise por Marca
**Solicitação**: "Crie um gráfico de barras com quantidade de veículos por marca"

**Resultado**: Gráfico de barras mostrando o número de veículos de cada marca

### Exemplo 4: Análise de Consumo
**Solicitação**: "Mostre um histograma de consumo de combustível"

**Resultado**: Histograma mostrando a distribuição dos valores de consumo

## 🛠️ Funcionalidades Técnicas

### Detecção Automática

O sistema detecta automaticamente quando você está pedindo um gráfico através de palavras-chave:
- "gráfico", "grafico", "chart", "visualização"
- "mostre", "exiba", "crie", "gere"
- "dashboard", "análise", "estatística"

### Geração Inteligente

O sistema analisa sua solicitação e:
1. Detecta o tipo de gráfico desejado
2. Identifica as colunas mencionadas
3. Escolhe o gráfico mais apropriado
4. Gera automaticamente

### Tipos de Gráficos Suportados

- ✅ **Barras** (bar) - Comparação entre categorias
- ✅ **Pizza** (pie) - Distribuição proporcional
- ✅ **Linha** (line) - Tendências ao longo do tempo
- ✅ **Dispersão** (scatter) - Correlação entre variáveis
- ✅ **Histograma** (histogram) - Distribuição de valores
- ✅ **Box Plot** (box) - Distribuição estatística
- ✅ **Heatmap** (heatmap) - Matriz de correlação

## 📊 Colunas Disponíveis para Análise

### Colunas Numéricas
- `km_mes` - Quilometragem mensal
- `velocidade_media` - Velocidade média
- `alertas` - Número de alertas
- `consumo_combustivel` - Consumo de combustível
- `dias_operacionais` - Dias operacionais
- `custo_manutencao` - Custo de manutenção
- `ano` - Ano de fabricação

### Colunas Categóricas
- `marca` - Marca do veículo
- `modelo` - Modelo do veículo
- `status` - Status (ativo, inativo, manutencao)
- `cidade` - Cidade

## 💡 Dicas de Uso

1. **Seja Específico**: Mencione as colunas que deseja visualizar
   - ✅ "Gráfico de km_mes por cidade"
   - ❌ "Mostre um gráfico" (muito genérico)

2. **Mencione o Tipo**: Especifique o tipo de gráfico se tiver preferência
   - ✅ "Gráfico de pizza de status"
   - ✅ "Histograma de consumo"

3. **Use Agregações**: O sistema agrupa automaticamente quando necessário
   - "Total de km por cidade" → Soma de km_mes agrupado por cidade
   - "Média de consumo por marca" → Média de consumo agrupado por marca

4. **Combine Variáveis**: Você pode pedir correlações
   - "Correlação entre velocidade e consumo"
   - "Gráfico de dispersão de km_mes vs consumo"

## 🔧 Instalação de Dependências

Para usar os gráficos, instale as dependências:

```bash
pip install pandas plotly
```

Ou instale todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

## 📝 Exemplos de Solicitações

### Análise por Cidade
- "Mostre um gráfico de veículos por cidade"
- "Exiba a quilometragem total por cidade"
- "Gráfico de barras de custo de manutenção por cidade"

### Análise por Marca
- "Quantidade de veículos por marca"
- "Gráfico de pizza de marcas"
- "Consumo médio por marca"

### Análise por Status
- "Distribuição de status dos veículos"
- "Gráfico de pizza de status"
- "Quantidade de veículos ativos, inativos e em manutenção"

### Análise Numérica
- "Histograma de consumo de combustível"
- "Distribuição de velocidade média"
- "Box plot de km_mes por status"

### Análise de Correlação
- "Mapa de calor de correlação"
- "Correlação entre variáveis numéricas"
- "Gráfico de dispersão de km_mes vs consumo"

## 🚀 Próximos Passos

1. **Instale as dependências**: `pip install pandas plotly`
2. **Execute o projeto**: `streamlit run src/app.py`
3. **Peça um gráfico**: Digite algo como "Mostre um gráfico de veículos por cidade"
4. **Explore os dados**: Experimente diferentes tipos de gráficos

---

**Criado para o Projeto IAG - Chat Assistente com IA**

