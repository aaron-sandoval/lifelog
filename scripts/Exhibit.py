import streamlit as st
import pickle
from typing import List
import os
import sys
sys.path.append(os.curdir)
from src.Visualization import GraphicExhibit
from src.TimesheetGlobals import rootProjectPath, Privacy
from scripts.Visualize import babelx
from i18n_l10n.internationalization import lang_en, lang_es


def main(path: str = os.path.join(rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl')):
    def exhibitHeader():
        locale = st.selectbox(label='Language/Idioma', options=['English', 'Español'])
        locale = {'English': lang_en, 'Español': lang_es}[locale]
        babelx.setLang(locale)
        if locale is not lang_en:
            st.warning(
                _k(
                    "Spanish translations across the site are in work. Apologies for any confusion this may cause."
                ),
                icon="⚠️"
            )
        st.title(_k('Deep Lifelog Data Analysis DEMO'))
        st.markdown('[Github](https://github.com/aaron-sandoval/lifelog)')
        st.header(_k('Introduction'))
        st.markdown(_k(
            "Welcome to Deep Lifelog, my first serious data analysis project! "
            "Since I started grad school in September 2017, I've collected continuous time series tabular data "
            "on my daily activities. "
            "It started as a small productivity exercise to track my academic tasks, "
            "but as my data obsession kicked in the scope ballooned out of control :smile:. "
            "I was inspired by "
            "[r/dataisbeautiful content like this](https://www.reddit.com/r/dataisbeautiful/comments/ab4uzz/i_recorded_every_hour_of_my_2018_and_17_oc/),"
            " but I wanted to track way more detail than a single categorical variable over fixed intervals. "
            "Over the years, I've adding data features like:\n\n"
            "- Media consumed\n"
            "- People I spend time with\n"
            "- Food\n"
            "- Location\n"
            "- Subject matters researched/discussed\n\n"
            "Though all of those features are in the data, "
            "there is more feature engineering and visualization work to be done. "
            "In addition to being an exercise in data analysis and software engineering, "
            "this project is also a mode of introspection, one more objective than fallible memory. "
            "Of course, this is all going to be much more interesting to me that it is to anyone else, "
            "so I'll try to focus on relatable ideas before diving down weird rabbit holes."
        ))
        st.divider()

    exhibitHeader()
    babelx.flush()


@st.cache_data
def loadData(path: str) -> List[GraphicExhibit]:
    """
    Loads visualization data from disk.
    """
    with open(path, 'rb') as f:
        data = pickle.load(f)
    # TODO: figure out how to securely generalize for different privacies
    # assert all([g.privacy == Privacy.PUBLIC for g in data])
    return list(filter(lambda x: x.privacy == Privacy.PUBLIC, data))


if __name__ == '__main__':
    main(os.path.join(rootProjectPath(), 'VS_Persistent', 'figs_PUBL.pkl'))
