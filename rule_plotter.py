import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import NullLocator
import os
from music21 import note


def makePlot(score, allRules=False, filepath='temporary_rule_plot', viewResults=True):
    H = .8
    plottitle = ('All rules that match score \'' + score.title +
                    ',\'\nfrom rule set ' + str(score.ruleset))
    fig = plt.figure()
    ax = fig.add_subplot(111, title=plottitle)

    # Function to plot each measure as a bar
    def makemeasure(startIndex, endIndex, number):
        L = endIndex - startIndex + 1
        ax.barh(0, L, x=(startIndex - .5), height=H, align='center', \
                color='yellow', alpha=None)
        ax.text(startIndex, 0.05, str(number))

    # Function to plot each rule as a bar
    def makeline(startIndex, ruleIndex, ruleLength, chosen=False):
        barcolor = 'blue'
        if chosen:
            barcolor = 'green'
        ax.barh(1 + ruleIndex, ruleLength, x=startIndex, \
            height=H, alpha=.5, align='center', color=barcolor)
        ax.hlines(1 + ruleIndex, startIndex, startIndex + ruleLength, \
            linewidth=3, color='r')
        ax.vlines(startIndex, 1 + ruleIndex - H / 2, 1 + ruleIndex + H / 2, \
            color='red', linewidth=4)
        ax.vlines(startIndex + ruleLength, 1 + ruleIndex - H / 2, \
            1 + ruleIndex + H / 2, linewidth=2, color='red')

    # Plot all the measures across the bottom
    start_index = 0
    start_measure = score.output_fb_score.flat.getElementsByClass(note.Note)[0].measureNumber
    for i in range(len(score.output_fb_score.flat.getElementsByClass(note.Note))):
        n = score.output_fb_score.flat.getElementsByClass(note.Note)[i]
        if n.measureNumber == start_measure:
            pass
        else:
            makemeasure(start_index, i, start_measure)
            start_index = i
            start_measure = n.measureNumber
    makemeasure(start_index, len(score.output_fb_score.flat.getElementsByClass(note.Note)) - 1, start_measure)

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
    minorLocator = MultipleLocator(1)

    #Deal with y-axis
    yticks = [a.__class__.__name__ for a in these_rules]
    yticks.insert(0, 'Measures:\n')
    ax.set_ylim(0, len(yticks))
    ax.set_ylabel('Rule')
    ax.set_yticks(range(len(yticks)))
    ax.set_yticklabels(yticks)

    #Deal with x-axis
    ax.set_xlabel('Note indecies \n(each vertical line represents a single note in the bass line)')
    ax.set_xlim(0, len(score.possible_rules) - 1)
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.xaxis.set_minor_locator(minorLocator)
    ax.grid(True, which='minor')
    ax.grid(True, linestyle='-')

    #Save it!
    filepath = filepath + '.eps'
    fig.savefig(filepath)

    #Open it?
    if viewResults:
        os.system("open " + filepath)
