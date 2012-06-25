import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import os


def makePlot(score, allRules=False, filepath='temporary_rule_plot', viewResults=True):
    H = .8
    plottitle = ('All rules that match score \'' + score.title +
                    '\'\nfrom ruleset ' + str(score.ruleset))
    fig = plt.figure()
    ax = fig.add_subplot(111, title=plottitle)
    #plt.ion()

    def makeline(startIndex, ruleIndex, ruleLength, chosen=False):
        barcolor = 'blue'
        if chosen:
            barcolor = 'green'
        ax.barh(ruleIndex, ruleLength, x=startIndex, \
            height=H, alpha=.5, align='center', color=barcolor)
        ax.hlines(ruleIndex, startIndex, startIndex + ruleLength, \
            linewidth=3, color='r')
        ax.vlines(startIndex, ruleIndex - H / 2, ruleIndex + H / 2, \
            color='red', linewidth=4)
        ax.vlines(startIndex + ruleLength, ruleIndex - H / 2, \
            ruleIndex + H / 2, linewidth=2, color='red')

    #What rules are we plotting here?
    these_rules = []
    if allRules:
        these_rules = score._allrules
    else:
        temp_rules = []
        for i in range(len(score.possible_rules)):
            if score.possible_rules[i]:
                for r in score.possible_rules[i]:
                    temp_rules.append(r)
        these_rules = [x for x in score._allrules if x in temp_rules]

    #Plot each rule possible
    for i in range(len(score.possible_rules)):
        if score.possible_rules[i]:
            for r in score.possible_rules[i]:
                applied = False
                if r in score.chosen_rules[i]:
                    applied = True
                makeline(i, these_rules.index(r), r.size, applied)

    #Time to format plot!
    majorLocator = MultipleLocator(8)
    minorLocator = MultipleLocator(1)

    #Deal with y-axis
    yticks = [a.__class__.__name__ for a in these_rules]
    ax.set_ylim(-1, len(yticks))
    ax.set_ylabel('Rule')
    ax.set_yticks(range(len(yticks)))
    ax.set_yticklabels(yticks)

    #Deal with x-axis
    ax.set_xlabel('Note indecies')
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    ax.grid(True, which='minor')
    ax.grid(True)

    #Save it!
    filepath = filepath + '.eps'
    fig.savefig(filepath)

    #Open it?
    if viewResults:
        os.system("open " + filepath)
