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
from scripts import Visualize, Exhibit


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
        f"- Decompose remaining groups logged as `Gender.{sg.Gender.NOTAPPLICABLE.alias()}` "
        f"into their constituent individuals"
    ))

    st.subheader(_k('Primary Relation'))
    st.markdown(_k(
        f"Primary relations are another high-level lens through which to characterize my social time. "
        f"Analyzing primary relation can distinguish when I'm having fun with my friends vs "
        f"meeting with work colleagues or hanging out with family. "
        f"The types of primary relation are :\n"
        f"1. `{sg.Family().alias()}`\n"
        f"1. `{sg.Friend().alias()}`\n"
        f"1. `{sg.Colleague().alias()}`\n"
        f"1. `{sg.Acquaintance().alias()}`\n\n"
        f"Every `Person` has a `{sg.Relation().alias()}`, and some people have multiple. "
        f"In those instances, the primary relation follows the order of precedence in the above list. "
        f"So when I'm with a `{sg.Colleague().alias()}` "
        f"who's grown close enough to be considered a `{sg.Friend().alias()}`, "
        f"that would be considered time with a `{sg.Friend().alias()}` in this analysis. "
    ))
    # with st.expander(Visualize.STR_BACKEND + f': `{sg.Relation().alias()}` and the `{sg.SocialGroup().alias()}` Graph'):
    #     st.markdown(_k(
    #         f"Each `Person` has a `relationships` property containing at least one `{sg.Relation().alias()}`. "
    #         # f"in that set must correspond to one of the "
    #         # f"{len(sg.Relation.__subclasses__())} primary relations above. "
    #         f"But not every `Person` has one of the {len(sg.Relation.__subclasses__())} primary relations above "
    #         f"explicitly listed in their `relationships`. "
    #         f"So how do you figure out what their primary relation is? "
    #         f"Primary relations are just part of "
    #         f"a more complex, hierarchical `{sg.SocialGroup().alias()}` classification system. "
    #         f"I'm not talking about a social group hierarchy of nobles and peasants, "
    #         f"but rather a hierarchy which relates the different groups of people you spend time with, "
    #         f"like your climbing friends, the widget testing team at work, or your secret religious cult. "
    #         f"`{sg.SocialGroup().alias()}` is the root of collection of categories structured in a "
    #         f"distributed acyclic graph (DAG) "
    #         f"which encodes the inheritance of `{sg.SocialGroup().alias()}` membership. "
    #         f"Here is a subgraph of the full hierarchy showing the descendants of the `{sg.Relation().alias()}` node. "
    #     ))
    #
    #     import pygraphviz as pgv
    #     import re
    #
    #     def newline_before_caps(s: str):
    #         return re.sub(r"([a-z])([A-Z])", r"\1\n\2", s)
    #
    #     def draw_descendants(cls: Type[kiwilib.Aliasable], g: pgv.AGraph):
    #         """Plots descendant DAG of `cls`. To be refactored and relocated."""
    #         for ch in cls.__subclasses__():
    #             g.add_edge(newline_before_caps(cls().alias()), newline_before_caps(ch().alias()))
    #             draw_descendants(ch, g)
    #     Sg = sg.Relation
    #     G = pgv.AGraph(directed=True)
    #     G.graph_attr['nodesep'] = 0.1
    #     G.node_attr["shape"] = "box"
    #     G.node_attr["margin"] = 0.02
    #     G.node_attr["width"] = 0.02
    #     G.edge_attr["color"] = "blue"
    #     G.add_node(newline_before_caps(Sg.__name__))
    #     draw_descendants(Sg, G)
    #     st.graphviz_chart(G.string(), use_container_width=True)
    #
    #     st.markdown(_k(
    #         f"The primary relations are the immediate children of `{sg.Relation().alias()}`. "
    #         f"If one's `relationships` property doesn't contain a primary relation, "
    #         f"then it must contain one of the other child nodes in the tree above, "
    #         f"and her primary relation is resolved by tracing the inheritance. "
    #         f"For example, if someone with `{sg.ColleagueBall().alias()}` doesn't also have "
    #         f"any higher precedence `{sg.Relation().alias()}` or any of their children, "
    #         f"then their primary relation is `{sg.Colleague().alias()}`.\n\n"
    #         f"I'll explore the rest of the `{sg.SocialGroup().alias()}` "
    #         f"structure comprehensively in another {Visualize.STR_BACKEND}."
    #     ))
    next(gxhs).exhibitStreamlit()
    st.markdown(_k(
        f"The total profile of this plot matches that of the *Person-Hours by Gender* plot in the previous section; "
        f"it's only the division of the total profile among the categories which differs. "
        f"Some hypotheses presented in that subsection are confirmed here. "
        f"I don't spend that much time overall with family, "
        f"and the time I do is concentrated in spikes when I visit my dad's family and around holidays. "
        f"It appears that most of the dip in 2021-02 comes from "
        f"a sharp reduction in time with {sg.Colleague().alias()}s, "
        f"but I don't recall what happened at work which would have caused that reduction.\n\n"
        f"In 2022, the scant social time contained almost no time with "
        f"`{sg.Family().alias()}` or `{sg.Colleague().alias()}`s. "
        f"It's also when I have the most time with `{sg.Acquaintance().alias()}`s logged. "
        f"But I hesitate to conclude much from that observation, because in 2022 I was more consistent in logging "
        f"time spent with `{sg.Acquaintance().alias()}`s than in other periods due to the overall low social time. "
        f"\n\n**Future work**\n\n"
        f"- Analyze other demographics, including age and shared activities\n"
    ))

if __name__ == '__main__':
    main(os.path.join(Global.rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))