"""
This file is a Streamlit page.
It is run via a call to `streamlit run` automatically due to its location in the /pages directory.
"""
import datetime
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
    section = Visualize.ExhibitSection.SLEEP
    st.title(_k('Sleep'))

    gxhs = filter(lambda x: x.section == section, Exhibit.loadData(path))

    # Section introduction
    st.markdown(_k(
        f'Sleep is one of the most basic features in the dataset, and one which spans the full '
        f'collection period with little change in collection behavior.\n\n'
        f'**Data Collection Changelog**\n\n'
        f'*2023-04*: Added rough tracking of sleep quality. Long periods lying awake or otherwise '
        f'not sleeping are now roughly tracked as tasks with descriptions under '
        f'`Project.{Global.Project.DORMIR.alias()}`. '
        f'These tasks no longer count toward measurements of sleep time duration. '
        f'Change reduces the upward bias of sleep durations.'
    ))
    st.divider()

    # Graphics

    # Avg Sleep Duration by Weekday and Life Phase
    next(gxhs).exhibitStreamlit()
    st.markdown(_k(
        "While not as interesting as I had hoped for, this plot does exhibit the general consistency "
        "of sleep over time. "
        "Notably, average sleep during grad school, the busiest life phase in the dataset, "
        "isn't that significantly lower than other more relaxed intervals. "
        "Sleep is one of the last things I compromise on for productivity's sake. "
        "The amount of sleep during the `{0}` life phase was lower than I expected; "
        "I had estimated an average of 9 hours from subjective memory. "
        "Subjectively, this phase had the best-quality sleep I've experienced, but there's not much "
        "other analysis that I can think of to support that claim. "
        "\n\n**Future work**\n\n"
        "- Add error bars\n"
        "- Add an overall average for each life phase"
        .format(Global.EpochScheme.MP_COARSE_ATOMIC.labelDT(datetime.datetime(2022, 4, 1, 1)))))


if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))