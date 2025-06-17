# 🌦️ Análise Meteorológica Porto Alegre (1961-2016) – Fase 2 do Projeto

Projeto em Python para análise e visualização de dados históricos meteorológicos de Porto Alegre, abrangendo informações diárias de precipitação, temperatura, umidade e vento.

---

## 📌 Descrição

Este sistema lê arquivos CSV com dados meteorológicos e oferece recursos para:

- Visualizar dados em intervalos de tempo customizados, com filtros por tipo de dado.
- Identificar o mês e ano mais chuvoso no período analisado.
- Calcular e exibir médias anuais da temperatura mínima para um mês específico entre 2006 e 2016.
- Gerar gráficos de barras para as médias anuais.
- Corrigir ou excluir registros de dados inválidos.
- Salvar dados filtrados e resultados em arquivos CSV para análise posterior.

---

## ✅ Funcionalidades principais

- Leitura e tratamento automático de dados faltantes e inválidos.
- Interface para seleção do arquivo CSV.
- Visualização em texto detalhada, segmentada por categorias (precipitação, temperatura, umidade e vento).
- Cálculo automático de estatísticas relevantes.
- Geração de gráficos interativos com `matplotlib`.
- Salvamento dos dados tratados e médias em arquivos CSV.
- Permite exclusão e correção de registros incorretos via menu interativo.

---

## 🧑‍💻 Tecnologias utilizadas

- Python 3.x  
- Biblioteca `csv` para manipulação de arquivos CSV  
- Biblioteca `datetime` para manipulação de datas  
- Biblioteca `matplotlib` para gráficos  
- Biblioteca `tkinter` para diálogo gráfico na seleção do arquivo  

---

## 📁 Estrutura do projeto

```
analisador_meteorologico/
│
├── script.py             # Script principal com todas as funções
└── README.md             # Documentação do projeto
```

---

## 🛠️ Como usar

1. Execute o script `script.py` via terminal ou IDE.
2. Selecione o arquivo CSV contendo os dados meteorológicos (formato esperado: data, precipitação, temp. máxima, temp. mínima, umidade, vento).
3. Utilize o menu interativo para:
   - Visualizar dados em diferentes formatos e períodos.
   - Calcular médias e gerar gráficos.
   - Corrigir ou excluir registros.
   - Salvar dados tratados e estatísticas em CSV.

---

## 📆 Atualizações da Fase 2

- Implementação do tratamento avançado de dados faltantes e inválidos.
- Melhoria no filtro de data, com final do mês calculado corretamente.
- Inclusão das funções de correção e exclusão de registros.
- Funções para salvar dados e médias em arquivos CSV nomeados e organizados.
- Interface de seleção de arquivo usando `tkinter`.

---

## 👨‍🎓 Autor

Ryan Lizze Broilo  
PUC-RS – Curso de Análise e Desenvolvimento de Sistemas  
Disciplina: Fundamentos de Sistemas Web – 2025  
