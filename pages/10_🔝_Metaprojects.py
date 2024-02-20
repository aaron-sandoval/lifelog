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
    section = Visualize.ExhibitSection.METAPROJECT
    st.title(_k('Metaprojects'))

    gxhs = filter(lambda x: x.section == section, Exhibit.loadData(path))

    # Section introduction
    st.markdown(_k(
        f"Much of the design work in this project has been in abstracting as much as possible about daily activities"
        f" into data structures like `Project`, `Tag`, `Collectible`, etc. "
        f"At the top of the `Project` taxonomy is the `Metaproject`, "
        f"a set of 5 broad categories which together contain every `Project`. "
        f"This is a useful data feature to begin with in a top-down analysis approach, "
        f"since major shifts in lifestyle are evident while smaller details don't muddy the waters.\n\n"
        f"- `Metaproject.{Global.Metaproject.Carrera.alias()}`: Working, career planning\n"
        f"- `Metaproject.{Global.Metaproject.Academico.alias()}`: Studying, independent learning and projects\n"
        f"- `Metaproject.{Global.Metaproject.Logistica.alias()}`: Transport, researching, email, chores, "
        f"the 'everything else' bucket\n"
        f"- `Metaproject.{Global.Metaproject.Recreo.alias()}`: Fun stuff\n"
        f"- `Metaproject.{Global.Metaproject.Dormir.alias()}`: :sleeping:\n\n"
        f"Errors in `Metaproject` attribution mostly come from `Project` instances which don't cleanly fit into a "
        f"single `Metaproject`. "
        f"For example, `Project.{Global.Project.CICLISMO.alias()}` contains tasks for both rec riding and "
        f"bike maintenance, which belong to `Metaproject.{Global.Metaproject.Recreo.alias()}` and "
        f"`Metaproject.{Global.Metaproject.Logistica.alias()}`, respectively. "
        f"Some of these split attribution cases have been handled in data cleaning, but I haven't caught all of them."
    ))
    st.divider()

    # Graphics

    # Duration by Metaproject per Day, Averaged over 1 Week
    next(gxhs).exhibitStreamlit()
    st.markdown(_k(
            "I like how this plot illstrates the phases of my adult life with different `Metaproject` focus. "
            "You can easily see the shifts from grad school, to working, to long-haul cycle touring in 2022, "
            "and to independent study in 2023. "
            "\n\nThere's so much to see in the details of this plot. "
            "Like how data collection was consistently incomplete until 2018-06. "
            "This is probably because, when I started my first job, I used this same data to fill in my timesheet "
            "at work, and I got into the habit of logging data more precisely at all hours. "
            "\n\nOr the big zero-sum spike-trough pairs poking above the 24-hour total line. "
            "I'm not sure what is causing them. Most likely some unclean data. "
            "\n\nOr comparing how overworked I was in grad school vs in the busiest periods in my first job. "
            "Grad school was consistently more consuming than work, with only 2 spikes around 2021-01 coming close. "
            "\n\nOr how as my studies in Spring 2018 gradually ate up more time over the course of the semester, "
            "it was mostly `Recreation` which was sacrificed, `Sleep` only dropping a bit. "
            "\n\n**Future work**\n\n"
            "- Check out the spikes about 24 hours noted above.\n"
            "- Add labels for smaller events like the short cycle tours in 2019 and 2021.\n"
            "- Split this plot into 2 subplots looking at weekdays and weekends."
        ))


if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))