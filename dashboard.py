
import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 1. CONFIGURAZIONE DELLA PAGINA
# --------------------------------------------------

# Imposta il titolo della pagina nel browser
# e utilizza tutta la larghezza disponibile.
st.set_page_config(
    page_title="Dashboard Superstore",
    layout="wide"
)


# --------------------------------------------------
# 2. TITOLO E DESCRIZIONE DELLA DASHBOARD
# --------------------------------------------------

st.title("Dashboard vendite e profittabilità")

st.write("Analisi delle vendite e dei profitti del Superstore.")


# --------------------------------------------------
# 3. CARICAMENTO E PULIZIA DEI DATI
# --------------------------------------------------

# Carichiamo il dataset CSV in un DataFrame.
df = pd.read_csv("Sample_Superstore.csv")


# Convertiamo le colonne delle date da stringhe
# a formato datetime.
df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="%d/%m/%y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], format="%d/%m/%y"
)


# Creiamo una nuova colonna Year estraendo
# l'anno dalla data dell'ordine.
df["Year"] = df["Order Date"].dt.year


# --------------------------------------------------
# 4. CONTROLLO DEI DATI MANCANTI E DUPLICATI
# --------------------------------------------------

# Contiamo tutti i valori mancanti presenti nel DataFrame.
# Il primo sum() conta i valori per ogni colonna,
# il secondo somma i risultati di tutte le colonne.
valori_mancanti = int(df.isnull().sum().sum())


# Contiamo le righe duplicate dell'intero DataFrame.
duplicati = int(df.duplicated().sum())


# Mostriamo i controlli in una sezione espandibile.
with st.expander("Controlli qualità del dataset"):

    st.write(f"Valori mancanti: {valori_mancanti}")

    st.write(f"Righe duplicate: {duplicati}")


# --------------------------------------------------
# 5. FILTRO INTERATTIVO PER ANNO
# --------------------------------------------------

# Creiamo una sezione laterale dedicata ai filtri.
st.sidebar.header("Filtri")


# Recuperiamo gli anni presenti nel dataset,
# eliminando i duplicati e ordinandoli.
anni = sorted(df["Year"].unique().tolist())


# Permettiamo all'utente di selezionare uno
# o più anni dalla barra laterale.
anni_selezionati = st.sidebar.multiselect(
    "Seleziona gli anni",
    options=anni,
    default=anni
)


# Se non viene selezionato nessun anno,
# mostriamo un avviso e interrompiamo l'esecuzione.
if not anni_selezionati:

    st.warning("Seleziona almeno un anno.")

    st.stop()


# Creiamo un nuovo DataFrame contenente
# solamente i dati degli anni selezionati.
dati = df[df["Year"].isin(anni_selezionati)]


# --------------------------------------------------
# 6. INDICATORI PRINCIPALI
# --------------------------------------------------

# Creiamo tre colonne per visualizzare
# le informazioni principali della dashboard.
col1, col2, col3 = st.columns(3)


# Sommiamo le vendite totali.
col1.metric(
    "Vendite totali",
    f"${dati['Sales'].sum():,.2f}"
)


# Sommiamo i profitti totali.
col2.metric(
    "Profitti totali",
    f"${dati['Profit'].sum():,.2f}"
)


# Contiamo gli ordini distinti.
col3.metric(
    "Ordini totali",
    f"{dati['Order ID'].nunique():,}"
)


# Inseriamo una linea divisoria.
st.divider()


# --------------------------------------------------
# 7. VENDITE E PROFITTI TOTALI PER ANNO
# --------------------------------------------------

# Raggruppiamo i dati per anno e calcoliamo
# la somma delle vendite e dei profitti.
totali_annuali = (
    dati.groupby("Year")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)


# Dividiamo la dashboard in due colonne
# per visualizzare i due grafici affiancati.
grafico1, grafico2 = st.columns(2)


# Grafico delle vendite annuali.
with grafico1:

    fig_sales = px.bar(
        totali_annuali,
        x="Year",
        y="Sales",
        title="Vendite totali per anno",
        labels={"Sales": "Vendite ($)", "Year": "Anno"}
    )

    st.plotly_chart(fig_sales, use_container_width=True)


# Grafico dei profitti annuali.
with grafico2:

    fig_profit = px.bar(
        totali_annuali,
        x="Year",
        y="Profit",
        title="Profitti totali per anno",
        labels={"Profit": "Profitti ($)", "Year": "Anno"}
    )

    st.plotly_chart(fig_profit, use_container_width=True)


st.divider()


# --------------------------------------------------
# 8. TOP 5 SOTTOCATEGORIE PIÙ VENDUTE
# --------------------------------------------------

# Raggruppiamo i dati per sottocategoria.
# Sommiamo Quantity per ottenere il numero
# complessivo di prodotti venduti.
#
# Ordiniamo dal valore maggiore al minore,
# selezionando solamente le prime cinque.
piu_venduti = (
    dati.groupby("Sub-Category")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)


# Creiamo un grafico a barre della Top 5.
fig_top5 = px.bar(
    piu_venduti,
    x="Sub-Category",
    y="Quantity",
    title="Top 5 sottocategorie più vendute",
    labels={
        "Sub-Category": "Sottocategoria",
        "Quantity": "Quantità venduta"
    }
)


# Mostriamo il grafico nella dashboard.
st.plotly_chart(fig_top5, use_container_width=True)


st.divider()


# --------------------------------------------------
# 9. MAPPA INTERATTIVA DELLE VENDITE PER STATO
# --------------------------------------------------

# Raggruppiamo i dati per Stato
# e calcoliamo le vendite totali.
vendite_per_stato = (
    dati.groupby("State")["Sales"]
    .sum()
    .reset_index()
)


# Creiamo una mappa geografica interattiva.
# Ogni Stato viene colorato in base al totale
# delle vendite registrate.
fig_mappa = px.choropleth(
    data_frame=vendite_per_stato,
    locations="State",
    locationmode="USA-states",
    color="Sales",
    scope="usa",
    title="Distribuzione delle vendite per Stato"
)


# Mostriamo la mappa nella dashboard.
st.plotly_chart(fig_mappa, use_container_width=True)


# --------------------------------------------------
# 10. TABELLA DEI DATI
# --------------------------------------------------

# Creiamo una sezione espandibile per consentire
# la consultazione del dataset filtrato.
with st.expander("Visualizza i dati del dataset"):

    st.dataframe(dati, use_container_width=True)
