<div style="text-align: right;">
  <a href="README.md">English</a> | <a href="README.pt.md">Português</a>
</div>

# Sistema Multi-Agente de Análise de Desempenho

Um sistema multi-agente que responde perguntas de análise de desempenho roteando-as para um agente de domínio especializado, executando cálculos determinísticos e sintetizando os resultados em uma percepção em linguagem natural.

Este é um projeto de aprendizado explorando como os LLMs podem ser orquestrados de forma confiável — usando lógica baseada em regras quando possível e raciocínio de LLM apenas quando realmente necessário.

## O problema

As perguntas de análise de desempenho abrangem domínios muito diferentes — saúde financeira, rendimento operacional, produtividade da equipe, adoção de produtos, métricas de crescimento — e cada domínio tem suas próprias fórmulas, formatos de dados e formas de ser interpretado incorretamente.

Um assistente de propósito geral único tende a misturar estes: pode aplicar intuição financeira a uma pergunta sobre produtos, ou pular a matemática real em favor de um palpite que parece plausível. O resultado são respostas que soam confiantes mas não são baseadas em cálculos reais.

Este projeto adota uma abordagem diferente: separar a *compreensão* de uma pergunta da *matemática* por trás dela, e separar a *matemática* da *interpretação* do que ela significa.

## Como funciona

Uma consulta passa por três estágios:

1. **Agente de ingestão** — lê a consulta e descobre duas coisas: em qual faixa de análise ela pertence e se algum enriquecimento opcional (como agrupamento) está sendo solicitado. Isso usa uma verificação de palavras-chave baseada em regras rápidas primeiro e apenas chama um classificador de LLM se a consulta for ambígua.
2. **Agente de faixa** — recebe a consulta roteada e os dados relevantes, e chama **funções Python pré-construídas e determinísticas** para fazer a matemática real. Nenhum LLM está envolvido no cálculo de uma margem ou uma taxa de perda — estas são funções simples com saída previsível e auditável.
3. **Agente de síntese** — pega os números brutos (e qualquer saída de enriquecimento) e os transforma em uma percepção real: não apenas "margem é 23%" mas o que esse número significa em contexto.

Um orquestrador fica entre os passos 2 e 3, despachando para o agente de faixa correto e opcionalmente chamando um utilitário de agrupamento se a consulta pediu por segmentação.

Todo o pipeline é encapsulado em um **aplicativo Streamlit** como o front-end — uma interface simples para digitar uma consulta, fornecer ou fazer upload de dados e visualizar a percepção sintetizada (além de quaisquer visualizações de cluster quando o enriquecimento é executado).

```
Consulta do usuário
    │
    ▼
Agente de ingestão  ──── filtro baseado em regras → fallback de LLM se ambíguo
    │
    ▼
Orquestrador ──── roteia para uma das 5 faixas
    │
    ▼
Agente de faixa ──── chama funções determinísticas (sem matemática de LLM)
    │
    ▼
Agente de síntese ──── interpreta números em percepção
    │
    ▼
Resposta final
```

## As cinco faixas

| Faixa | Domínio | Exemplo de pergunta |
|---|---|---|
| Desempenho Financeiro | Margens, taxa de queimadura, ROI, crescimento de receita | "Qual é a tendência de margem bruta neste trimestre?" |
| Eficiência Operacional | Rendimento, tempo de ciclo, utilização | "Onde está o gargalo em nosso pipeline?" |
| Análise de Pessoas | Contagem de pessoal, atrito, produtividade | "Existem perfis de desempenho distintos nesta equipe?" |
| Desempenho do Produto | Adoção, retenção, funis | "Como é o nosso funil de ativação?" |
| Crescimento e Aquisição | CAC, LTV, perda | "Nossa razão LTV:CAC é saudável?" |

O sistema foi construído para ser modular — adicionar uma 6ª faixa significa adicionar palavras-chave ao roteador, escrever as funções determinísticas que precisa e conectar um agente. Nenhuma outra parte do sistema muda.

## Princípios de design

- **Matemática determinística, interpretação de LLM.** Os cálculos nunca passam por um LLM. Isso mantém os números auditáveis e evita aritmética alucinada.
- **Regras primeiro, LLM como fallback.** O roteamento tenta uma correspondência de palavra-chave barata antes de gastar tokens em uma chamada de classificação. Isso mantém o sistema rápido e barato para o caso comum.
- **Enriquecimento opcional, não padrão.** Recursos como agrupamento só funcionam quando a consulta realmente pede segmentação — executá-los incondicionalmente produziria ruído em conjuntos de dados pequenos ou simples.
- **Modularidade sobre completude.** O sistema é fornecido com cinco faixas, mas foi projetado para que novas possam ser adicionadas sem tocar nos caminhos de código existentes.

## Estrutura do projeto

```
src/
  agents.py      # agente de ingestão, orquestrador, agentes de faixa, agente de síntese
  ai_model.py     # funções determinísticas + wrapper de API Anthropic + config de roteador
app.py            # Front-end Streamlit
main.py           # Ponto de entrada CLI (útil para teste rápido sem a UI)
.env              # ANTHROPIC_API_KEY
```

## Executando localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

A versão CLI (`main.py`) também está disponível para testar o pipeline diretamente sem a UI — útil ao desenvolver uma nova faixa ou depurar o roteador.

## Status

Este é um MVP em estágio inicial. Atualmente implementado: agente de ingestão, orquestrador e a faixa de Desempenho Financeiro de ponta a ponta. As quatro faixas restantes e a camada de enriquecimento de agrupamento foram projetadas mas ainda não construídas — veja a apresentação técnica do projeto para a arquitetura completa e questões em aberto.
