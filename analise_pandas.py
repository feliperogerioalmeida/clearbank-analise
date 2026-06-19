"""Versao alternativa da analise usando pandas (Requisito Opcional 1).

Carrega o transacoes.csv com pd.read_csv, aplica a mesma validacao da
solucao nativa, agrupa por mes com groupby e calcula as metricas.
Os valores devem ser identicos aos da solucao nativa do notebook.

Execucao:
    pip install pandas
    python analise_pandas.py
"""

import pandas as pd

ARQUIVO_CSV = "transacoes.csv"
LIMITE_SUSPEITO = 10000.00


def formatar_moeda(valor):
    """Formata um numero no padrao monetario brasileiro: R$ 1.234,56."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def carregar_dados(caminho):
    """Le o CSV e devolve apenas as linhas validas como DataFrame limpo."""
    try:
        df = pd.read_csv(caminho, dtype=str)
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' nao encontrado.")
        return pd.DataFrame()

    # id precisa ser inteiro
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    # valor precisa ser numerico e maior que zero
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    # data precisa estar no formato AAAA-MM-DD
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    # cliente_id e tipo normalizados
    df["cliente_id"] = df["cliente_id"].fillna("").str.strip()
    df["tipo"] = df["tipo"].fillna("").str.strip().str.lower()

    filtro_valido = (
        df["id"].notna()
        & (df["cliente_id"] != "")
        & df["data"].notna()
        & df["tipo"].isin(["credito", "debito"])
        & df["valor"].notna()
        & (df["valor"] > 0)
    )

    limpo = df[filtro_valido].copy()
    limpo["mes"] = limpo["data"].dt.strftime("%Y-%m")
    return limpo


def gerar_resumo_mensal(df):
    """Agrupa por mes e calcula as metricas financeiras usando groupby."""
    creditos = (
        df[df["tipo"] == "credito"].groupby("mes")["valor"].sum()
    )
    debitos = (
        df[df["tipo"] == "debito"].groupby("mes")["valor"].sum()
    )

    resumo = df.groupby("mes").agg(
        quantidade=("valor", "count"),
        valor_medio=("valor", "mean"),
        maior_valor=("valor", "max"),
        menor_valor=("valor", "min"),
    )
    resumo["total_credito"] = creditos
    resumo["total_debito"] = debitos
    resumo = resumo.fillna(0.0)
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]
    return resumo.round(2).sort_index()


def exibir(df, resumo):
    print("=" * 40)
    print("ANALISE FINANCEIRA - VERSAO PANDAS")
    print("=" * 40)
    print(f"Transacoes validas: {len(df)}")
    print(f"Periodo: {df['data'].min().date()} a {df['data'].max().date()}")
    print(f"Dias no periodo: {(df['data'].max() - df['data'].min()).days}")
    print()

    print("===== RELATORIO MENSAL =====")
    for mes, linha in resumo.iterrows():
        print()
        print(f"Mes: {mes}")
        print(f"  Transacoes: {int(linha['quantidade'])}")
        print(f"  Total credito: {formatar_moeda(linha['total_credito'])}")
        print(f"  Total debito:  {formatar_moeda(linha['total_debito'])}")
        print(f"  Saldo:         {formatar_moeda(linha['saldo'])}")
        print(f"  Media:         {formatar_moeda(linha['valor_medio'])}")
        print(f"  Maior valor:   {formatar_moeda(linha['maior_valor'])}")
        print(f"  Menor valor:   {formatar_moeda(linha['menor_valor'])}")
    print()

    print("===== TRANSACOES SUSPEITAS =====")
    suspeitas = df[df["valor"] > LIMITE_SUSPEITO].sort_values("id")
    if suspeitas.empty:
        print("Nenhuma transacao suspeita encontrada.")
    else:
        for _, s in suspeitas.iterrows():
            print(
                f"ID: {int(s['id'])} | Cliente: {s['cliente_id']} | "
                f"Data: {s['data'].date()} | Valor: {formatar_moeda(s['valor'])}"
            )


def main():
    df = carregar_dados(ARQUIVO_CSV)
    if df.empty:
        print("Sem dados validos para analisar.")
        return
    resumo = gerar_resumo_mensal(df)
    exibir(df, resumo)


if __name__ == "__main__":
    main()
