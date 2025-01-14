import streamlit as st
import pandas as pd
import altair as alt


class PortofoliuInvestitii:
    def __init__(self):
        self.investitii = []

    def adaugare_investitie(self, nume, cantitate, pret_cumparare, pret_curent):
        self.investitii.append({
            "Nume": nume,
            "Cantitate": cantitate,
            "Pret Cumparare": pret_cumparare,
            "Pret Curent": pret_curent
        })

    def stergere_investitie(self, nume):
        for i in self.investitii:
            if i["Nume"] == nume:
                self.investitii.remove(i)


    def calcul_valoare_totala(self):
        s = 0
        for i in self.investitii:
            s += i["Pret Curent"] * i["Cantitate"]
        return s


    def calcul_profit(self):
        s = 0
        for i in self.investitii:
            s += i["Cantitate"]*(i["Pret Curent"] - i["Pret Cumparare"])
        return s

    def get_investitie(self, nume):
        for i in self.investitii:
            if i["Nume"] == nume:
                return True
        return False




if "portofoliu" not in st.session_state:
    st.session_state["portofoliu"] = PortofoliuInvestitii()

portofoliu = st.session_state["portofoliu"]

# Interfața aplicației
st.title("Aplicație pentru gestionarea portofoliului de investiții")

# Meniu lateral
meniu = ["Adaugă investiție", "Șterge investiție", "Vizualizează portofoliul", "Exportă în CSV"]
alegere = st.sidebar.selectbox("Alege o opțiune", meniu)

# Adaugă investiție
if alegere == "Adaugă investiție":
    st.header("Adaugă o nouă investiție")
    nume = st.text_input("Numele activului")
    cantitate = st.number_input("Cantitate", min_value=0.0)
    pret_cumparare = st.number_input("Preț de achiziție", min_value=0.0)
    pret_curent = st.number_input("Preț curent", min_value=0.0)

    if st.button("Adaugă"):
        portofoliu.adaugare_investitie(nume, cantitate, pret_cumparare, pret_curent)
        st.success(f"Investiția {nume} a fost adăugată!")

# Șterge investiție
elif alegere == "Șterge investiție":
    st.header("Șterge o investiție")
    nume = st.text_input("Numele activului de șters")
    verificare_existenta_investitie = portofoliu.get_investitie(nume)
    if st.button("Șterge"):
        if verificare_existenta_investitie:
            portofoliu.stergere_investitie(nume)
            st.success(f"Investiția {nume} a fost ștearsă!")
        else:
            st.error(f"Investiția {nume} nu se află in portofoliu!")


# Vizualizează portofoliul
elif alegere == "Vizualizează portofoliul":
    st.header("Portofoliu")
    if portofoliu.investitii:
        # Convertim investițiile într-un DataFrame Pandas
        df = pd.DataFrame(portofoliu.investitii)
        df['Valoare Totală'] = df['Cantitate'] * df['Pret Curent']

        # Afișăm tabelul
        st.dataframe(df.style.format({"Pret Cumparare": "{:.2f}", "Pret Curent": "{:.2f}", "Valoare Totală": "{:.2f}"}))

        # Afișăm metrici
        st.subheader("Valoarea totală a portofoliului")
        st.metric("Valoare Totală", f"{portofoliu.calcul_valoare_totala():.2f} RON")

        profit = portofoliu.calcul_profit()
        culoare_profit = "green" if profit > 0 else "red"
        st.subheader("Profit total")
        st.markdown(f"<h3 style='color:{culoare_profit};'>{profit:.2f} RON</h3>", unsafe_allow_html=True)

        # Adăugăm un grafic pentru vizualizarea distribuției investițiilor
        chart = alt.Chart(df).mark_bar().encode(
            x='Nume:N',
            y=alt.Y('Valoare Totală:Q', title='Valoare Totală'),
            color='Nume:N'
        ).properties(
            title="Distribuția valorii investițiilor"
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Portofoliul este gol.")

