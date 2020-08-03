from plotnine import *
from pythonUtils.VariableLoader import *
import pandas as pd
import os
import sys

# baseFolder ='singleSizeExperiment/'
# config ='c0'
# configFolder =baseFolder + config + '/'
# plotFolder =baseFolder + "plots/"
#
# configDF =pd.read_pickle(configFolder + 'configData.pickle')
# summary =pd.read_pickle(configFolder + "summary.pickle");
# summaryNormalized =pd.read_pickle(configFolder + "summaryNormalized.pickle")
#
# configDF.loc[configDF.location==-1, 'location'] ='gmean'
# summary.loc[configDF.location==-1, 'location'] ='gmean'
# summaryNormalized.loc[configDF.location==-1, 'location'] ='gmean'
#
# configDF['location'] =configDF.location.astype(str)
# summary['location'] =summary.location.astype(str)
# summaryNormalized['location'] =summaryNormalized.location.astype(str)
#
# p =ggplot(configDF, aes(x='episode')) #
# #p =p + facet_wrap('location')
# p =p + geom_point(aes(y='normalized'), data=configDF)
# p =p + geom_line(aes(x='episode', y='50%'), data=summaryNormalized)
# #p =p + geom_line(aes(y=summaryNormalized['50%'] , colour='red'))
# #p =p + geom_line(aes(x='episode' , y='25%' , colour='blue'))
# #p =p + geom_line(aes(x='episode' , y='75%' , colour='blue'))
# #p =p + stat_smooth()
# #p =p + stat_smooth()
# #p =p + stat_smooth()
# p =p + ylim(0 , 10)
# p.save(plotFolder + "-stepMetrics-lim10-" + config +".png")


def plot_config(base_folder, config):
    base_folder = os.path.join(base_folder, '')
    config_folder = base_folder + config + '/'
    plot_folder = base_folder + "plots/"

    config_df = pd.read_pickle(config_folder + 'configData.pickle')
    summary = pd.read_pickle(config_folder + "summary.pickle")
    summary_normalized = pd.read_pickle(config_folder + "summaryNormalized.pickle")

    config_df.loc[config_df.location == -1, 'location'] = 'gmean'
    summary.loc[summary.location == -1, 'location'] = 'gmean'
    summary_normalized.loc[summary_normalized.location == -1, 'location'] = 'gmean'

    config_df['location'] = config_df.location.astype(str)
    summary['location'] = summary.location.astype(str)
    summary_normalized['location'] = summary_normalized.location.astype(str)

    p = ggplot()  #
    p = p + facet_wrap('location')
    p = p + geom_point(aes('episode', 'normalized'), data=config_df, alpha=0.5, shape=".")
    p = p + geom_line(aes('episode', '50%'), data=summary_normalized, color='red')
    p = p + geom_line(aes('episode', '75%'), data=summary_normalized, color='blue')
    p = p + geom_line(aes('episode', '25%'), data=summary_normalized, color='blue')
    # p =p + stat_smooth()

    filename = plot_folder + "stepMetrics-limFull-" + config + ".png"
    ggsave(plot=p, filename=filename, dpi=100)

    p = p + coord_cartesian(ylim=(1, 40))
    filename = plot_folder + "stepMetrics-lim40-" + config + ".png"
    ggsave(plot=p, filename=filename, dpi=100)

    p = p + coord_cartesian(ylim=(1, 10))
    filename = plot_folder + "stepMetrics-lim10-" + config + ".png"
    ggsave(plot=p, filename=filename, dpi=100)

    p = p + coord_cartesian(ylim=(1, 5))
    filename = plot_folder + "stepMetrics-lim5-" + config + ".png"
    ggsave(plot=p, filename=filename, dpi=100)


def plot_all_configs(base_folder):
    config_folders = get_list_of_configs(base_folder)
    for config in config_folders:
        print("plotting: ", config)
        plot_config(base_folder, config)


if __name__ == '__main__':
    # base_folder = argv[1]
    # config = argv[2]
    if len(sys.argv) > 2:
        plot_config(sys.argv[1], sys.argv[2])
    else:
        plot_all_configs(sys.argv[1])
