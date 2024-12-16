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
        """Lemme tell you about some things."""
    ))
    st.divider()

    # Graphics

    # SM word cloud
    next(gxhs).exhibitStreamlit()
    epsc = Global.EpochScheme.MP_COARSE_ATOMIC
    st.markdown(_k(
        """Those are some nice subjects."""
    ))

    st.divider()


if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))