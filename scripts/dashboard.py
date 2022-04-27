#!/usr/bin/env python
import os

import requests
import streamlit as st
import pandas as pd


st.title("Differences between spaCy 2 & spaCy 3")


text = st.text_area("Text to annoate:", "To be or not to be. That is the question")
data = {"text": text}


spacy2_host = os.environ.get("SPACY2_URL", "http://localhost:1985")
spacy3_host = os.environ.get("SPACY3_URL", "http://localhost:1986")

spacy2 = requests.post(f"{spacy2_host}/syntax", params=data).json()
spacy3 = requests.post(f"{spacy3_host}/syntax", params=data).json()


def alert_differences(column_entry):
    """styles a column entry based on matching entries
    Assumes that entries ending with *_spaCy2 pair with *_spaCy3 and
    compares them

    """

    styles = []
    for idx, value in column_entry.items():
        # for each item, check equality to its pair

        if idx.endswith("_spaCy2"):
            pair_idx = idx.replace("_spaCy2", "_spaCy3")
        else:
            pair_idx = idx.replace("_spaCy3", "_spaCy2")

        if column_entry.loc[pair_idx] == value:
            styles.append("")
        else:
            styles.append("color: #fa8926;")

    return styles


_merged = (
    pd.merge(pd.DataFrame(spacy2["syntax_tokens"]), pd.DataFrame(spacy3["syntax_tokens"]),
         how="outer", left_index=True, right_index=True,
         suffixes=("_spaCy2", "_spaCy3"))
    .T.sort_index()
)

_styled = (
    _merged.style.apply(alert_differences)
)

st.write(_styled.to_html(), unsafe_allow_html=True)
