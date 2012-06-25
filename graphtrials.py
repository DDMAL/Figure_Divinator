import matplotlib.pyplot as plt


def makeGraph(self, score):

    # bar stacked
    # barchart2_demo
    # barh_demo
    # boxplot_demo (maybe)
    # broken_barh
    # hline_demo **

    """
    Make a "broken" horizontal bar plot, ie one with gaps
    """
    score.output_fb_score.show()

    H = .8

    fig = plt.figure()
    ax = fig.add_subplot(111)

    #datapoints = []
    ruleNames = ['rule1', 'rule2', 'rule3']

    def makeline(startIndex, ruleIndex, ruleLength):
        ax.barh(ruleIndex, ruleLength, x=startIndex, \
            height=H, alpha=.5, align='center')
        ax.hlines(ruleIndex, startIndex, startIndex + ruleLength, \
            linewidth=3, color='r')  # ruleIndex,xmin=startIndex, xmax=3, color='red')
        ax.vlines(startIndex, ruleIndex - H / 2, ruleIndex + H / 2, \
            color='red', linewidth=4)
        ax.vlines(startIndex + ruleLength, ruleIndex - H / 2, \
            ruleIndex + H / 2, linewidth=2, color='red')

    makeline(1, 1, 4)
    makeline(1, 2, 8)
    makeline(3, 1, 4)
    makeline(2, 3, 2)

    #ax.set_ylim(0,4)
    #ax.set_xlim(0,100)
    ax.set_xlabel('note index')
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(ruleNames)
    ax.grid(True)
    #ax.annotate('race interrupted', (61, 25),
                # xytext=(0.8, 0.9), textcoords='axes fraction',
                # arrowprops=dict(facecolor='black', shrink=0.05),
                # fontsize=16,
                # horizontalalignment='right', verticalalignment='top')

    plt.show()

