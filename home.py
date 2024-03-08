import streamlit as st
import plotly.express as px
from data import *
from pages.gis import drawCaseMap, drawVacMap
from pages.demographics import *

## PAGE INFO
st.set_page_config(page_title="infectious diseases dashboard", page_icon="🛖", layout="wide")
st.sidebar.success("Select a page above.")
st.title("Infectious disease surveillance")




def overviewModule():
    st.header("Overview")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "All Time",
            "Last Month",
            "Last Week",
            "Weekly Difference",
            "Weekly Race Difference",
        ]
    )

    dates = [
        [nation_cum.iloc[-1], gender_tests.iloc[-1]],
        [nation_cum.iloc[-30], gender_tests.iloc[-4]],
        [nation_cum.iloc[-7], gender_tests.iloc[-2]],
    ]
    deltas = [
        (dates[0][0]["Cumulative Cases"] - dates[1][0]["Cumulative Cases"]),
        (dates[0][0]["Cumulative Cases"] - dates[2][0]["Cumulative Cases"]),
    ]
    genderDates = gender_tests.index.tolist()

    # All Time
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Total Cases")
            st.metric(
                label=f"Reporting as of {dates[0][0]['epi_date_V3']}",
                value=dates[0][0]["Cumulative Cases"],
            )
        with col2:
            st.subheader("Total Tests")
            st.metric(
                label=f"Reporting as of {genderDates[-1]}",
                value=gender_tests["Total_Tests"].sum(),
            )
    # Last Month
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cases")
            st.metric(
                label=f"Reporting as of {dates[1][0]['epi_date_V3']}", value=deltas[0]
            )
        with col2:
            st.subheader("Tests")
            st.metric(
                label=f"Reporting as of {genderDates[-4]}",
                value=dates[1][1]["Total_Tests"],
            )
    # Last Week
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cases")
            st.metric(
                label=f"Reporting as of {dates[2][0]['epi_date_V3']}", value=deltas[1]
            )
        with col2:
            st.subheader("Tests")
            st.metric(
                label=f"Reporting as of {genderDates[-2]}",
                value=dates[2][1]["Total_Tests"],
            )
    # Weekly Difference
    with tab4:
        weeklyDifference()
    # Weekly Race
    with tab5:
        weeklyRace()


def gisModule():
    st.header("GIS Map")
    col1, col2, col3 = st.columns(3)

    with col1:
        radio = st.radio(
            label="Select One of the Following", options=["Cases", "Vaccines"]
        )

    with col2:
        state = st.selectbox(label="Select a State", options=state_total["Location"])

    with col3:
        if radio == "Cases":
            st.metric(
                label=f"Cases in {state}",
                value=state_total["Cases"][state_total["Location"] == state],
            )
        else:
            st.metric(
                label=f"Vaccines Administered in {state}",
                value=int(
                    state_vac["Total"][state_vac["Reporting Jurisdictions"] == state]
                ),
            )

    if radio == "Cases":
        drawCaseMap()
    else:
        drawVacMap()


def genderModule():
    col1, col2 = st.columns(2)

    with col1:
        drawPieChart()
    with col2:
        drawAgeDistro()


def casesModule():
    col1, col2 = st.columns(2)

    with col1:
        cumCases()
    with col2:
        dailyCases()

    sevenDayAvg()


def main():
    overviewModule()
    genderModule()
    casesModule()
    gisModule()


main()
