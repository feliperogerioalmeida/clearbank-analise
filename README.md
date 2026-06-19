# ClearBank — Análise Financeira com Python

Projeto final do módulo de Python para Análise de Dados. O notebook lê e
valida um arquivo CSV de transações bancárias, agrupa os dados por mês,
calcula métricas financeiras, sinaliza transações suspeitas, exibe um
relatório formatado no terminal e exporta o resultado em JSON.

## Estrutura do repositório

```
clearbank-analise/
├── desafio-final.ipynb   # notebook principal (com saídas salvas)
├── transacoes.csv        # arquivo de entrada (dados de teste)
├── relatorio.json        # saída gerada pela análise
├── analise_pandas.py     # versão alternativa com pandas (opcional - RO1)
├── grafico.png           # gráfico das movimentações mensais (opcional - RO2)
└── README.md
```

## O que o notebook faz

1. **Leitura** do `transacoes.csv` com o módulo nativo `csv`
   (`csv.DictReader`), tratando o caso de arquivo inexistente.
2. **Validação e limpeza** de cada linha — descarta silenciosamente
   registros com `id` vazio/não numérico, `cliente_id` vazio, `data` em
   formato inválido, `tipo` diferente de `credito`/`debito` ou `valor`
   não numérico/menor ou igual a zero. Ao final exibe o resumo da limpeza.
3. **Datas** com `datetime` (`strptime`/`strftime`): extrai o mês de cada
   transação e calcula os dias entre a transação mais antiga e a mais
   recente.
4. **Agrupamento mensal e métricas**: por mês calcula quantidade, total de
   crédito, total de débito, saldo, valor médio, maior e menor valor.
5. **Transações suspeitas**: marca qualquer valor acima de
   `LIMITE_SUSPEITO = 10000.00`.
6. **Relatório no terminal** com separadores visuais e valores no padrão
   monetário brasileiro (`R$ 1.234,56`).
7. **Exportação** do resultado em `relatorio.json`
   (`json.dump(..., ensure_ascii=False, indent=2)`).

O código está organizado em funções com responsabilidades separadas
(`ler_transacoes`, `validar_data`, `validar_valor`, `validar_transacao`,
`processar_transacoes`, `gerar_relatorio`, `salvar_json`,
`exibir_relatorio`) e usa `try/except` em três situações distintas:
abertura do CSV, conversão do `valor` para `float` e conversão da `data`
para `datetime`.

## Como executar

### Google Colab
1. Faça upload de `desafio-final.ipynb` e de `transacoes.csv`.
2. Menu **Ambiente de execução → Executar tudo**.

### Jupyter local
```bash
pip install pandas matplotlib   # necessário apenas para os opcionais
jupyter notebook desafio-final.ipynb
```
Depois rode todas as células em ordem (**Cell → Run All**).

> O `transacoes.csv` precisa estar na mesma pasta do notebook.

## Saídas geradas

- **`relatorio.json`** — relatório completo da análise.
- **Saída no terminal** — resumo da limpeza, relatório mensal e lista de
  transações suspeitas.
- **`grafico.png`** (opcional) — gráfico de crédito/débito e saldo por mês.

## Requisitos opcionais

- **RO1 — pandas:** `analise_pandas.py` refaz a leitura e o agrupamento com
  `pd.read_csv` e `groupby`. O notebook compara os resultados e confirma que
  são idênticos aos da solução nativa.
- **RO2 — matplotlib:** geração de `grafico.png` com título, rótulos nos
  eixos e legenda.
