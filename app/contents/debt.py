"""Main module for the streamlit app"""
import os.path as op
import sys

import streamlit as st
import plotly.express as px

sys.path.append(op.abspath(op.join(op.dirname(__file__), "..")))

from app.contents import household_debt_workbook

sheet_name = "Page 3 Data"
title = "Total Debt Balance and Its Composition"
x_axis = "Year:Quarter"
y_axis = "Trillions of $"
source = "Source: New York Fed Consumer Credit Panel/Equifax"
columns = ["Mortgage", "HE", "Revolving", "Auto Loan", "Credit Card", "Student Loan", "Other", "Total"]

def total_debt_guarterly():
    total_debt = household_debt_workbook.parse(sheet_name, header=3).set_index("Unnamed: 0").iloc[:,:-1]
    total_debt.index.names = [x_axis]

    return total_debt

def run():
    total_debt = total_debt_guarterly().iloc[:,:-1]

    fig = px.bar(total_debt, x=total_debt.index, y=total_debt.columns, labels={"variable": "Debt Type"})
    fig.update_xaxes(tickvals=total_debt.index[::4], tickangle=45, tickfont=dict(size=12))
    fig.update_yaxes(title=y_axis, tickfont=dict(size=12), tickprefix="$", showgrid=False)

    st.plotly_chart(fig)
