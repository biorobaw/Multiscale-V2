import pandas as pd
from plotnine import *


if __name__ == '__main__':

    # set trace base folder
    traces_base_folder = 'singleSizeExperiment/calib/'

    # load data
    ratGeomMeansExtended = pd.read_pickle(traces_base_folder + 'ratGeomMeansExtended.pickle')

    # plot data
    for scale in ratGeomMeansExtended.index.unique():

        print('plotting scale:', scale)

        p0 = ggplot(ratGeomMeansExtended.loc[scale], aes('episode', 'geom_mean'))
        p0 = p0 + facet_wrap('traces')
        p0 = p0 + geom_point(color='black', shape=".", alpha=0.5)
        p0 = p0 + stat_smooth(color='red')
        p0 = p0 + ggtitle('Calibration experiment - scale '+str(scale))
        filename = traces_base_folder + 'plots/scale_full-' + "{:.2f}".format(scale)+'.png'
        ggsave(plot=p0, filename=filename, dpi=100)

        filename = traces_base_folder + 'plots/scale_lim_40-' + "{:.2f}".format(scale)+'.png'
        p = p0 + coord_cartesian(ylim=(1, 40))
        ggsave(plot=p, filename=filename, dpi=100)

        filename = traces_base_folder + 'plots/scale_lim_10-' + "{:.2f}".format(scale)+'.png'
        p = p0 + coord_cartesian(ylim=(1, 10))
        ggsave(plot=p, filename=filename, dpi=100)

        filename = traces_base_folder + 'plots/scale_lim_05-' + "{:.2f}".format(scale)+'.png'
        p = p0 + coord_cartesian(ylim=(1, 5))
        ggsave(plot=p, filename=filename, dpi=100)

        filename = traces_base_folder + 'plots/scale_last10-' + str(scale)+'.png'
        p = p0 + coord_cartesian(ylim=(1, 5), xlim=(70, 79))
        p = p + ggtitle('Calibration experiment - scale ' + "{:.2f}".format(scale) + ' - last 10 episodes')
        ggsave(plot=p, filename=filename, dpi=100)
