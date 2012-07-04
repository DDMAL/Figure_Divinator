import matplotlib.pyplot as plt
import matplotlib.ticker as mpltick
import os
import music21 as m21


def makemeasure(axes_handle, startIndex, endIndex, number, H=.8):
    """
    Function to plot each measure as a bar
    """
    L = endIndex - startIndex
    if H != .8:
        H = 2 * H
    axes_handle.barh(0, L, x=(startIndex - .5), height=H, align='center', \
            color='none', alpha=None)
    axes_handle.text(startIndex, 0.05, str(number))


def makeline(axes_handle, startIndex, ruleIndex, ruleLength,
            chosen='maybe', H=.8, barcolor='yellow', stickcolor='purple'):
    """
    Function to plot each rule as a bar
    """
    if chosen == 'yes':
        barcolor = 'green'
    elif chosen == 'no':
        barcolor = 'red'
    axes_handle.barh(1 + ruleIndex, ruleLength, x=startIndex, \
        height=H, alpha=.7, align='center', color=barcolor)
    axes_handle.hlines(1 + ruleIndex, startIndex, startIndex + ruleLength, \
        linewidth=3, color=stickcolor)
    axes_handle.vlines(startIndex, 1 + ruleIndex - H / 2, 1 + ruleIndex + H / 2, \
        color=stickcolor, linewidth=4)
    axes_handle.vlines(startIndex + ruleLength, 1 + ruleIndex - H / 2, \
        1 + ruleIndex + H / 2, linewidth=2, color=stickcolor)


def makePlotFromScore(score, allRules=False, filepath='results/temporary_rule_plot', viewResults=True):
    """
    Given a score (including extraction), show all rules and the chosen rules.
    """
    plottitle = (unicode('All rules that match score \'') + score.title.decode('utf-8') +
                    unicode(',\'\nfrom rule set ') + unicode(str(score.ruleset)))
    fig = plt.figure()
    ax = fig.add_subplot(111, title=plottitle)
    ax.set_axisbelow(True)

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
    yticks = [a.__class__.__name__ for a in these_rules]
    yticks.insert(0, 'Measures:\n')

    # Plot all the measures across the bottom
    start_index = 0
    start_measure = score._bassline.flat.getElementsByClass(m21.note.Note)[0].measureNumber
    for i in range(len(score._bassline.flat.getElementsByClass(m21.note.Note))):
        n = score._bassline.flat.getElementsByClass(m21.note.Note)[i]
        if n.measureNumber == start_measure:
            pass
        else:
            makemeasure(ax, start_index, i, start_measure, len(yticks))
            start_index = i
            start_measure = n.measureNumber
    makemeasure(ax, start_index,
        len(score._bassline.flat.getElementsByClass(m21.note.Note)) - 1,
        start_measure, len(yticks))

    #Plot each rule possible
    for i in range(len(score.possible_rules)):
        if score.possible_rules[i]:
            for r in score.possible_rules[i]:
                applied = 'maybe'
                if r in score.chosen_rules[i]:
                    applied = 'yes'
                makeline(ax, i, these_rules.index(r), r.size, applied)

    #Time to format plot!
    #Deal with y-axis
    ax.set_ylim(0, len(yticks))
    ax.set_ylabel('Rule')
    ax.set_yticks(range(len(yticks)))
    ax.set_yticklabels(yticks)

    #Deal with x-axis
    ax.set_xlabel('Note indicies: \nEach vertical dotted ' + \
                    'line represents a single note in the score\'s bass line)')
    ax.set_xlim(0, len(score.possible_rules) - 1)
    ax.xaxis.set_major_locator(mpltick.NullLocator())
    ax.xaxis.set_minor_locator(mpltick.MultipleLocator(1))
    ax.grid(True, which='minor')
    ax.grid(True, linestyle='-')

    #Save it!
    filepath = filepath + '.png'
    fig.savefig(filepath, dpi=800)

    #Open it?
    if viewResults:
        os.system("open " + filepath)
