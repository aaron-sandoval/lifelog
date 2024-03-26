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
        f'Change reduces the upward bias of sleep durations.\n\n'
        f'*2023-12-13*: Began explicitly logging all sleep tasks instead of assuming untracked intervals are sleep. '
        f'Change disambiguates naps from occasional erroneously unlogged intervals.'
    ))
    st.divider()

    # Graphics

    # Distributions of Time of Falling Asleep and Waking Up by Life Phase
    next(gxhs).exhibitStreamlit()
    epsc = Global.EpochScheme.MP_COARSE_ATOMIC
    st.markdown(_k(
        f"This plot shows an overview of my sleep behavior related to time of day over different phases of life."
        f"The most obvious feature is the distributional shift between `{epsc.sortedEpochGroupNames()[0]}` and "
        f"`{epsc.sortedEpochGroupNames()[1]}`, when median sleep behavior shifted earlier by 2+ hours. "
        f"The shift in modes is even greater, shifting by about 3 hours. "
        f"I recall this transition from moderate night owl to early bird feeling pretty easy. "
        f"I've never been a caffeine drinker, and waking early has never been a problem.\n\n"
        f"It's interesting to compare the shapes of the `Fall asleep` and `Wake up` distributions for each phase. "
        f"Ignoring the long tails, there's clearly a rough correspondence in shape for each pair. "
        f"The bimodal distributions of `{epsc.sortedEpochGroupNames()[1]}` likely correspond to weekdays and weekends. "
        f"I'd estimate that the bimodality is clearer for `Wake up` "
        f"just because waking time is controlled by an alarm clock.\n\n"
        f"The variance of the `Wake up` distributions also appears to be decreasing over time, "
        f"visible in the diminishing interquartile range. "
        f"Certainly, my schedule during `{epsc.sortedEpochGroupNames()[0]}` was comparatively irregular. "
        f"From subjective memory, during `{epsc.sortedEpochGroupNames()[2]}` and `{epsc.sortedEpochGroupNames()[3]}`, "
        f"my sleep schedule on weekdays and weekends has has little distinction, "
        f"but that's a claim that can be backed by data at some point."
        "\n\n**Future work**\n\n"
        "- Compare weekday and weekend distributions\n"
        "- Scatterplot of `Wake up` vs `Fall asleep` to examine correlation"
    ))

    st.divider()

    # Avg Sleep Duration by Weekday and Life Phase
    # next(gxhs).exhibitStreamlit()
    # st.markdown(_k(
    #     "While not as interesting as I had hoped for, this plot does exhibit the general consistency "
    #     "of sleep over time. "
    #     "Notably, average sleep during grad school, the busiest life phase in the dataset, "
    #     "isn't that significantly lower than other more relaxed intervals. "
    #     "Sleep is one of the last things I compromise on for productivity's sake. "
    #     "The amount of sleep during `{0}` was lower than I expected; "
    #     "I had estimated an average of 9 hours from subjective memory. "
    #     "Subjectively, this phase had the best-quality sleep I've experienced, but there's not much "
    #     "other analysis that I can think of to support that claim. "
    #     "\n\n**Future work**\n\n"
    #     "- Add error bars\n"
    #     "- Add an overall average for each life phase"
    #     .format(Global.EpochScheme.MP_COARSE_ATOMIC.sortedEpochGroupNames()[2])))


if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))