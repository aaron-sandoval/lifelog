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
from utils import Visualize
from utils import Exhibit


def main(path: str = os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl')):
    # Section parameters
    section = Visualize.ExhibitSection.PEOPLE
    st.title(_k('People'))

    gxhs = filter(lambda x: x.section == section, Exhibit.loadData(path))

    # Section introduction
    st.markdown(_k(
        f"This is probably the data feature which has the most potential for interesting analysis. "
        f"Due to signal-to-noise ratio, data on time spent with people is particularly susceptible to "
        f"collection errors for people with whom I've spent little time. "
        f"I usually decide whether to add a new person to the dataset if I've interacted with them "
        f"meaningfully for >15 minutes or expect to in the future. "
        f"But I make frequent errors in both directions relative to "
        f"this rule of thumb, adding noise to the data most visible in the long tail of people with whom "
        f"I've spent little time. "
        f"\n\n"
        f"**Data Collection Changelog**\n\n"
        f"*2017-12*: Started regularly collecting data on time spent with individual people."
    ))
    st.divider()

    # Graphics

    # Total Time Spent with Individual People, Sorted
    next(gxhs).exhibitStreamlit()
    st.markdown(_k(
            "Excluding people with whom I've spent <3 hours with in total, where the data is noisy, "
            "the distribution of time spent is even more skewed than a power law distribution. "
            "That is to say, the curve has distinctly positive curvature "
            "in a log plot, not a linear relationship. "
            "I'm curious how the shape of this distribution compares to other peoples' "
            "and how the distribution has looked in different phases of my life. "
            "\n\n**Future work**\n\n"
            "- Create a scalar metric of breadth/tightness of social activities related to "
            "the curvature of the semilog plot. "
            "Evaluate this metric over different time domains.\n"
            "- Compare versions of this plot over various life phases and other time intervals."
            ))


if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))