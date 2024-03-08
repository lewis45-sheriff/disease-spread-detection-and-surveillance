import streamlit as st
import plotly.express as px
from data import *


def drawPieChart():
    names = list(gender_confirm.head())[1:]
    values = [
        int(gender_confirm["Another sex/gender"].sum()),
        int(gender_confirm["Men"].sum()),
        int(gender_confirm["Transgender men"].sum()),
        int(gender_confirm["Transgender women"].sum()),
        int(gender_confirm["Women"].sum()),
    ]
    colors = ["#1D3354", "#D64045", "#E9FFF9", "#8ED8DB", "#467599"]
    fig = px.pie(
        gender_confirm, values=values, names=names, color_discrete_sequence=colors
    )

    st.plotly_chart(fig, use_container_width=True)


def calculateDeltas(weeks):
    pairs = [
        pd.Series(list((gender_tests.loc[weeks[0]][0], gender_tests.loc[weeks[1]][0]))),
        pd.Series(list((gender_tests.loc[weeks[0]][1], gender_tests.loc[weeks[1]][1]))),
        pd.Series(list((gender_tests.loc[weeks[0]][2], gender_tests.loc[weeks[1]][2]))),
        pd.Series(list((gender_tests.loc[weeks[0]][3], gender_tests.loc[weeks[1]][3]))),
    ]

    deltaPairs = list(map(lambda x: round(x.pct_change() * 100, 2), pairs))
    deltas = []
    for i in range(len(deltaPairs)):
        deltas.append(deltaPairs[i][1])

    return deltas


def displayMetrics(weeks, isSingle):
    labels = list(gender_tests.head())
    col1, col2, col3, col4 = st.columns(4)

    # Display only the data; no deltas
    if isSingle:
        with col1:
            st.metric(label=labels[0], value=gender_tests.loc[weeks[0]][0])
        with col2:
            st.metric(label=labels[1], value=str(gender_tests.loc[weeks[0]][1]) + "%")
        with col3:
            st.metric(label=labels[2], value=gender_tests.loc[weeks[0]][2])
        with col4:
            st.metric(label=labels[3], value=str(gender_tests.loc[weeks[0]][3]) + "%")
    else:
        deltas = calculateDeltas(weeks)
        with col1:
            st.metric(
                label=labels[0],
                value=gender_tests.loc[weeks[1]][0],
                delta=str(deltas[0]) + "%",
            )
        with col2:
            st.metric(
                label=labels[1],
                value=str(gender_tests.loc[weeks[1]][1]) + "%",
                delta=str(deltas[1]) + "%",
            )
        with col3:
            st.metric(
                label=labels[2],
                value=gender_tests.loc[weeks[1]][2],
                delta=str(deltas[2]) + "%",
            )
        with col4:
            st.metric(
                label=labels[3],
                value=str(gender_tests.loc[weeks[1]][3]) + "%",
                delta=str(deltas[3]) + "%",
            )


def weeklyDifference():
    label = "Select Two Weeks to Compare"
    options = gender_tests.index.tolist()
    firstWk = options[0]
    finalWk = options[-1]

    weeks = st.multiselect(
        label=label, options=options, max_selections=2, default=[firstWk, finalWk]
    )

    weeks.sort()

    if len(weeks) == 0:
        st.error("Must include at least one week", icon="🚨")
    elif len(weeks) == 1:
        displayMetrics(weeks=weeks, isSingle=True)
    else:
        displayMetrics(weeks=weeks, isSingle=False)


def weeklyRace():
    st.header("Weekly Percentage Difference of Race")

    options = race_percent.columns[1:]
    series = race_percent.iloc[-1][1:]
    max_value = series.max()
    default = series[series == max_value].index[0]

    races = st.multiselect(
        label="Select which races to display", options=options, default=default
    )
    st.line_chart(data=race_percent, x="MMWR Week", y=races, width=700, height=700)


def cumCases():
    st.line_chart(nation_cum, x="epi_date_V3", y="Cumulative Cases")


def dailyCases():
    st.line_chart(nation_cum, x="epi_date_V3", y="Cases")


def sevenDayAvg():
    st.bar_chart(
        nation_cum, x="epi_date_V3", y="7-Day Average", use_container_width=True
    )


def drawAgeDistro():
    pct_gc = gender_confirm.copy(deep=True)
    pct_gc.set_index("web_age_grp", inplace=True)

    sums = sum(list(pct_gc.sum(axis=1)))
    ages = pct_gc.index.values.tolist()
    genders = list(pct_gc.head())
    colors = ["#8ED8DB", "#1D3354", "#467599", "#E9FFF9", "#D64045"]

    pct_gc = pct_gc.div(sums)

    fig = px.bar(pct_gc, x=ages, y=genders, color_discrete_sequence=colors)
    st.plotly_chart(fig, use_container_width=True)
