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
import catalogs.SocialGroups as sg
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
        f"*2018-02*: Started regularly collecting data on time spent with individual people."
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
            "What would others' plots look like if they had collected a lifelog dataset? "
            "I imagine that everyone's version of this plot would "
            "have positive log plot curvature in at least the rightmost region. "
            "This is assuming an ideal scenario where data collection is comprehensive, "
            "down to the 30 seconds spent chatting with Tina the grocery clerk, "
            "and maybe even brief moments of eye contact with strangers. "
            "It depends on where you draw the line for what constitutes a social interaction. "
            "In the ideal case where all this data is collected, "
            "the dataset would include thousands of people in a long tail of very little time spent together, "
            "and I suspect that this tail would generally show positive log plot curvature in everyone's plot.\n\n"
            "So hypothesizing that the right side of the distribution looks about the same for most people, "
            "I'm curious how the shape of the left side of the distribution would compare. "
            "I can imagine social behavior patterns which might produce negative curvature at the left side. "
            "How common is this compared to positive curvature? "
            "\n\n**Future work**\n\n"
            "- Create a scalar metric of breadth/tightness of social activities related to "
            "the curvature of the semilog plot. "
            "Evaluate this metric over different time domains.\n"
            "- Compare versions of this plot over life phases and other time intervals."
            ))

    st.header(_k('Demographics'))

    st.subheader(_k('Gender'))

    # Total Time Spent with Individual People, Sorted
    st.markdown(_k(
        "The plot below shows the gender distribution of my social time. "
        "Specifically, this plot is in units of person-hours/day, "
        "meaning that an hour spent with two friends counts for twice as much as an hour spent with one. "
        "This seems like a reasonable way to answer the question "
        "'How much time do I spend with people of different genders?'\n\n"
        "But this measure does not reflect how much of my time I spend socializing in general. "
        "I expect there to be quite a difference between a plot of 'Hours per Day of Social Interaction' "
        "and the total profile of person-hours per day in the plot below. "
        "Person-hours is a measure more susceptible to data collection errors than a simple measure of hours. "
        "There's plenty of social time where I didn't record the identities of the people involved, "
        "and all of that data is filtered out during any analysis of person-hours. "
        "Also, large gatherings contribute heavily to person-hours due to the quantity of people, "
        "but the limitations of data collection frequently lead to misleading results. "
        "For example, if I go to a party with 3 friends, but there are 12 other people whose names I don't know, "
        "that party will be logged as time spent with 3 people, not 15. "
        "And maybe that incomplete data is actually a more honest representation of the time than "
        "if I did log all 15 people. "
        "Should it really count as 15 people if you don't really know 12 of them and you only even talked to 6? "
        "It depends on your semantics of 'social interaction'. "
        "It's good to keep this in mind when interpreting this plot and others showing units of 'person-hours'."
    ))
    st.markdown(_k(
        f"Gender is classified into the mutually-exclusive categories {['`'+g.alias()+'`' for g in list(sg.Gender)]}. "
        f"`{sg.Gender.NOTAPPLICABLE.alias()}` "
        f"is used for entries in the `Person` catalog which don't correspond to individual people. "
        f"For example, there are several `Person` instances which actually correspond to teams and other groups, "
        f"all of which use `{sg.Gender.NOTAPPLICABLE.alias()}` unless the group is single-gendered. "
    ))
    next(gxhs).exhibitStreamlit()
    st.markdown(_k(
        f"The `{sg.Gender.MALE.alias()}` prevalence is obvious. "
        f"The right subplot shows the overall proportion of time by gender, "
        f"with `{sg.Gender.MALE.alias()}` occupying around 75% of the total. "
        f"Grad school in the first half of 2018 was clearly `{sg.Gender.MALE.alias()}`-dominated. "
        f"That eased up in 2019, when, I hypothesize, "
        f"my job became more collaborative within a gender-balanced team."
        f"Spikes around July, November, or December make sense, "
        f"since that's when I usually visit my dad's family.\n\n"
        f"The pandemic didn't have much of an effect in this plot apart from "
        f"maybe being responsible for the dip in 2020-03 through 2020-04. "
        f"But this apparent lack of effect may just be a coincidence. "
        f"A roommate moved in in 2020-04, and we spent lots of time cooped up together for the next 12 months. "
        f"Perhaps the social time with colleagues was merely approximately supplanted by social time with my roommate. "
        f"Looking at other demographics will tell.\n\n"
        f"The only month in which I spent more time with women was 2022-03. "
        f"This month was an anomaly within an anomaly. "
        f"The outer anomaly was the lonely cycle tour spanning 2022, "
        f"and the inner anomaly was the two weeks in 2022-03 when I toured along with two girls Suzie and Veronika, "
        f"during which we spent nearly every hour together. "
        f"The other 2022 anomaly was 2022-09, when I spent a week in Germany with several friends from back home.\n\n"
        f"There are plenty of questions this plot raises to be investigated further. "
        f"I'm not sure what caused the spike in 2022-10 through 2022-11, nor the dip in 2021-02. "
        f"\n\n**Future work**\n\n"
        f"- Analyze other demographics, including relation, age, and shared activities\n"
        f"- Decompose remaining groups logged as `Gender.{sg.Gender.NOTAPPLICABLE.alias()}` "
        f"into their constituent individuals"
    ))

    st.subheader(_k('Primary Relation'))
    st.markdown(_k(
        f"The primary relations are {['`'+g().alias()+'`' for g in list(sg.Relation.__subclasses__())]}. "
        f"Similarly to `{sg.Gender().alias()}`, every person is assigned to a primary relation. "
        f"But primary relations are just part of "
        f"a more complex, hierarchical classification system of `{sg.SocialGroup().alias()}`s. "
        f"`{sg.SocialGroup().alias()}` is the root of collection of categories structured in a "
        f"distributed acyclic graph (DAG). "
        f"For example, `{sg.Colleague().alias()}` is the parent of the subcategories "
        f"{['`'+g().alias()+'`' for g in list(sg.Colleague.__subclasses__())]}. "
        f"All members of `{sg.ColleagueWork().alias()}` are also members of `{sg.Colleague().alias()}`. "
        f"Each person in the catalog may belong to several `{sg.SocialGroup().alias()}`s. "
        f"I'll explore the `{sg.SocialGroup().alias()}` structure more fully"
    ))
    next(gxhs).exhibitStreamlit()
    st.markdown(_k(
        f"The total profile of this plot matches that of the *Person-Hours by Gender* plot in the previous section; "
        f"it's only the division of the total which differs. "
        f"Some hypotheses presented in that subsection are confirmed here. "
        f"I don't spend that much time overall with family, "
        f"and the time I do is concentrated in spikes when I visit my dad's family and around holidays. "
        f"It appears that most of the dip in 2021-02 comes from "
        f"a sharp reduction in time with {sg.Colleague.alias()}s. "
        f"But I don't recall why that reduction took place. "
        f"\n\n**Future work**\n\n"
        f"- Analyze other demographics, including relation, age, and shared activities\n"
    ))

if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))