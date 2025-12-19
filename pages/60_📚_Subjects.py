"""
This file is a Streamlit page.
It is run via a call to `streamlit run` automatically due to its location in the /pages directory.
"""
import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import pickle
# from typing import List
import os
import sys
sys.path.append(os.curdir)
import src.TimesheetGlobals as Global
from scripts import Visualize, Exhibit

SECTION = Visualize.ExhibitSection.SUBJECT_MATTER

def main(path: str = os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl')):
    st.title(_k('Subjects'))

    gxhs = filter(lambda x: x.section == SECTION, Exhibit.loadData(path))

    # Section introduction
    st.markdown(_k(
        """
        Since Spring 2023, I've tracked the subject matters of the media that I consume and the things I research.
        """
    ))
    st.divider()

    # Graphics

    # SM word cloud
    next(gxhs).exhibitStreamlit()
    st.markdown(_k(
        """This word cloud shows a very rough approximation of the relative amount of time that I've spent engaged with each subject. The size of each word is supposed to be proportional to the square root of the time spent on that subject, but since the distribution is heavy-tailed and is over such a wide range, I think the sizes of some of them saturated.\n\n
The color corresponds to the top-level category of the subject matter:\n\n
- 🔵 Personal Matters 
- 🔴 Hard Science and Technology
- 🟠 Philosophy
- 🟢 Social Sciences, Humanities, Culture
- 🟤 Major Problems and Solutions
- 🟣 Metadata tags about the information ("NEWS" is the only one so far)\n\n
Some of these subjects are subsets of others. I organized every subject into a directed acyclic graph to structure those relationships, but this visualization just shows the raw data without any aggregation using the graph structure.
"""
    ))
    

    st.divider()


if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))