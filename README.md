# 💈 BarberAI — Inteligência Preditiva & Retenção Automática para Barbearias

> Transformando históricos brutos de agendamentos em receita recorrente através de **Ciência de Dados**, **Machine Learning** e **IA Generativa**.

---

## 📌 O Problema de Negócio

A maioria das barbearias modernas já utiliza sistemas básicos para organizar a agenda e o caixa. No entanto, esses sistemas funcionam apenas como **repositórios passivos**: eles registram quando o cliente corta o cabelo, mas não agem quando ele para de frequentar o estabelecimento.

Na prática, quando a barbearia percebe que um cliente habitual sumiu, ele já migrou para a concorrência.

## 💡 A Solução

O **BarberAI** atua como uma **camada de inteligência e automação** que opera em paralelo ao sistema de gestão que a barbearia já utiliza. O sistema analisa o histórico de visitas, descobre o ritmo individual de cada cliente, prevê o risco de abandono (*churn*) antes que ele aconteça e aciona uma comunicação personalizada via WhatsApp para trazê-lo de volta.

---

## 🧠 Como a Inteligência Artificial Funciona (Dados & Modelos)

O projeto divide a atuação da IA em duas frentes complementares: **IA Preditiva** (para identificar o momento exato de agir) e **IA Assistiva** (para humanizar o contato).

### 1. Engenharia de Recursos (*Feature Engineering*) e Descoberta de Padrões
Sistemas reais de barbearia raramente possuem um campo dizendo *"este cliente corta o cabelo a cada X dias"*. O pipeline de dados em Python (`pandas` / `numpy`) ingere os logs brutos de atendimento (`id_cliente`, `data_atendimento`, `barbeiro`, `servico`, `valor_pago`) e constrói dinamicamente o perfil comportamental (**RFM adaptado**) de cada cliente:

* **`recencia_dias`**: Dias decorridos desde o último atendimento até a data atual.
* **`frequencia_media_dias`**: Intervalo médio histórico (calculado via diferença temporal entre visitas consecutivas) que aquele cliente específico leva para retornar.
* **`razao_atraso`**: Índice relativo de atraso dado por $\frac{\text{recencia\_dias}}{\text{frequencia\_media\_dias}}$. *(Ex.: Um cliente com ciclo habitual de 20 dias que está há 26 dias sem agendar apresenta razão `1.30`, indicando 30% de atraso em relação ao seu próprio padrão).*
* **`total_visitas` & `ticket_medio`**: Métricas de fidelidade e valor monetário para priorização de receita em risco.

### 2. Modelo Preditivo de *Churn* (Machine Learning)
Com as variáveis comportamentais estruturadas, algoritmos baseados em árvores de decisão (**Random Forest Classifier** / **XGBoost** via `scikit-learn`) classificam a probabilidade de abandono (`predict_proba`) de cada cliente. Clientes que ultrapassam o limiar crítico de atraso (`razao_atraso >= 1.15`) e apresentam queda na probabilidade de retorno são isolados na fila de retenção.

### 3. IA Generativa para Hiperpersonalização (LLM)
Para evitar mensagens robóticas de disparo em massa, os metadados dos clientes em risco (nome, dias desde o último corte, serviço habitual e barbeiro de preferência) são enviados via API para um Modelo de Linguagem (**Google Gemini API**), que redige um convite curto, natural e contextualizado para envio no WhatsApp.

---

## 🏗️ Arquitetura do Sistema

A arquitetura foi desenhada com foco em **Ciência de Dados e agilidade (Low-Code)**, concentrando o desenvolvimento no pipeline analítico em Python e delegando infraestrutura e mensageria para ferramentas gerenciadas:

```text
[Sistema Atual da Barbearia (CSV / Logs)]
                  │
                  ▼
[Pipeline Python: Limpeza + Cálculo RFM + Modelo ML]
                  │
                  ▼
[Armazenamento em Nuvem (Supabase / Airtable)] ──► [Dashboard Interativo (Streamlit)]
                  │
                  ▼
[Orquestrador de Fluxo (n8n / Make)]
                  │
                  ├──► [Google Gemini API] (Geração de mensagem personalizada)
                  └──► [API WhatsApp] (Disparo automático para o cliente)
