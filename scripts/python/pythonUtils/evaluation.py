import pandas as pd
from scipy import stats
from plotnine import *
import scikit_posthocs as sp
"""
    this file will provide code for comparing run times, including:
        * calculation of mean / median metrics
        * calculation of convergence time
        * calculation of performance metric : example mean of last 10 episodes
        * calculation of kruskal wallis
        * calculation of anova
        
    parametric tests:
        anova one way
    non-parametric tests:
        kruskal wallis one way
        Dunn's test
        pairwise mann-whitney without bonferroni correction
        Conover-Iman
    normality tests:
        
"""


def prepare_data_frame(df: pd.DataFrame, group_variables, variable):
    df = df.reset_index()
    res = pd.DataFrame()
    res['groups'] = df[group_variables[0]].astype(str)
    for i in range(1,len(group_variables)):
        res['groups'] = res['groups'] + '_' + df[group_variables[i]].astype(str)
    res['values'] = df[variable]
    return res


def plot_test_results(results):
    heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True,
                    'cbar_ax_bbox': [0.80, 0.35, 0.04, 0.3]}
    return sp.sign_plot(results, **heatmap_args)


def kruskal_wallis(df: pd.DataFrame, group_variables, variable):
    """
    kruskal wallis one way analysis of variance:
            Non-parametric method that tests whether samples originate from same distribution.
            Does not assume normal distribution.
    :param df: data frame
    :param group_variables: variables used for grouping
    :param variable: variable to which the test is applied
    :return: result of the kruskal wallis test
    """
    return stats.kruskal(*[group[variable].values for name, group in df.groupby(group_variables)])


def dunn(df: pd.DataFrame, group_variables, variable):
    df = prepare_data_frame(df, group_variables, variable)
    return sp.posthoc_dunn(df, val_col='values', group_col='groups', p_adjust='holm')


def anova_one_way(df: pd.DataFrame, group_variables, variable):
    """
    Anova one way test:
            Parametric test that tests whether samples originate from same distribution.
            Assumes normal distribution.
    :param df: data frame
    :param group_variables: variables used for grouping
    :param variable: variable to which the test is applied
    :return: result of the one way anova test
    """
    return stats.f_oneway(*[group[variable].values for name, group in df.groupby(group_variables)])


def statistic_to_color_mapper(stat):
    if stat <0:
        return 'above'
    # if stat <= 0.001:
    #     return '<0.001'
    # if stat <= 0.01:
    #     return '<0.01'
    if stat < 0.03:
        return '<0.03'
    if stat < 0.05:
        return '<0.05'
    if stat < 0.07:
        return '<0.07'
    return 'above'


stat_colors = {'above': '#ef3b2c',
               '<0.07': '#a1d99b',
               '<0.05': '#238b45',
               '<0.03': '#005a32'
               }


if __name__ == '__main__':
    # test file:
    tdf = pd.DataFrame({'g1': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c'],
                        'g2': ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c', 'c'],
                        'v': [1, 2, 3, 5, 1, 12, 31, 54, 62, 12, 10, 12, 6, 74, 11]
                        })
    pc1 = dunn(tdf, ['g1', 'g2'], 'v')
    pc = pc1.reset_index().melt(id_vars='index', value_vars=pc1.columns)
    # pc.loc[0, 'value'] = 0.0
    # pc.loc[1, 'value'] = 0.01
    # pc.loc[2, 'value'] = 0.031
    # pc.loc[3, 'value'] = 0.051
    # pc.loc[4, 'value'] = 0.071
    pc['stat'] = pc.value.map(statistic_to_color_mapper)

    p = ggplot(pc, aes('index', 'variable', fill='factor(stat)'))
    p = p + geom_tile(aes(width=0.95, height=0.95))
    p = p + scale_fill_manual(values=stat_colors, drop=False)
    p = p

    print(p)

    # print(pc1)
    # res = plot_test_results(pc1)
    # print(res)
