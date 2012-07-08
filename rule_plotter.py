import matplotlib.pyplot as plt
import matplotlib.ticker as mpltick
import os
import music21 as m21
import rules

_colors = ['yellow', 'green', 'red']  # maybe, yes, no
DEBUG = 1


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


def makerulebox(axes_handle, startIndex, ruleIndex, ruleLength,
            chosen='maybe', H=.8, barcolor=_colors[0], stickcolor='purple'):
    """
    Function to plot each rule as a bar
    """
    if chosen == 'yes':
        barcolor = _colors[1]
    elif chosen == 'no':
        barcolor = _colors[2]

    axes_handle.barh(ruleIndex, ruleLength, x=startIndex, \
        height=H, alpha=.7, align='center', color=barcolor)
    axes_handle.hlines(ruleIndex, startIndex, startIndex + ruleLength, \
        linewidth=3, color=stickcolor)
    axes_handle.vlines(startIndex, ruleIndex - H / 2, ruleIndex + H / 2, \
        color=stickcolor, linewidth=4)
    axes_handle.vlines(startIndex + ruleLength, ruleIndex - H / 2, \
        ruleIndex + H / 2, linewidth=2, color=stickcolor)


def makerulelegend(axes_handle, type='score'):
    if type == 'score':
        plotlabels = ['Rule matches score', 'Rule applied']
    elif type == 'ruleset':
        plotlabels = ['Can coexist', 'Self', 'Mutually exclusive']
        # plotlabels = ['Can coexist', 'Can coexist (trumps)', 'Mutually exclusive']

    #make fake plot to get legend info
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    b1 = ax2.bar([0, 1, 2], [0.2, 0.3, 0.1], color=_colors[0])
    b2 = ax2.bar([0, 1, 2], [0.2, 0.3, 0.1], color=_colors[1])
    if type == 'ruleset':
        b3 = ax2.bar([0, 1, 2], [0.2, 0.3, 0.1], color=_colors[2])
        plots = [b1, b2, b3]
    else:
        plots = [b1, b2]
    lgd = axes_handle.legend(plots, plotlabels, bbox_to_anchor=(1, 0.5),
         loc='center left')
    return lgd


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
                makerulebox(ax, i, 1 + these_rules.index(r), r.size, chosen=applied)

    #Time to format plot!
    #Deal with y-axis
    ax.set_ylim(0, len(yticks))
    ax.set_ylabel('Rule')
    ax.set_yticks(range(len(yticks)))
    ax.set_yticklabels(yticks)

    #Deal with x-axis
    ax.set_xlabel('Note indicies: \nEach vertical dotted ' + \
                    'line represents a single note in the score\'s bass line.')
    ax.set_xlim(0, len(score.possible_rules) - 1)
    ax.xaxis.set_major_locator(mpltick.NullLocator())
    ax.xaxis.set_minor_locator(mpltick.MultipleLocator(1))
    ax.grid(True, which='minor')
    ax.grid(True, linestyle='-', linewidth=10)

    #Add legend
    lgd = makerulelegend(ax)

    #Save it!
    filepath = filepath + '.png'
    fig.savefig(filepath, dpi=800, bbox_extra_artists=(lgd,), bbox_inches='tight')

    #Open it?
    if viewResults:
        os.system("open " + filepath)


def makePlotFromRuleset(ruleset, ruleOffset=False, filepath='results/temporary_ruleset_plot', viewResults=True):
    """
    Given a ruleset, show all rules and the chosen rules.
    """
    plottitle = (unicode('Rule interactions from rule set "') + unicode(str(ruleset.name)) + unicode('"'))
    fig = plt.figure()
    ax = fig.add_subplot(111, title=plottitle)
    ax.set_axisbelow(True)

    #What rules are we plotting here?
    these_rules = ruleset.rulelist
    yticks = [a.__class__.__name__ for a in these_rules]
    #yticks.insert(0, 'Measures:\n')

    # Plot all the measures across the bottom
    # start_index = 0
    # start_measure = score._bassline.flat.getElementsByClass(m21.note.Note)[0].measureNumber
    # for i in range(len(score._bassline.flat.getElementsByClass(m21.note.Note))):
    #     n = score._bassline.flat.getElementsByClass(m21.note.Note)[i]
    #     if n.measureNumber == start_measure:
    #         pass
    #     else:
    #         makemeasure(ax, start_index, i, start_measure, len(yticks))
    #         start_index = i
    #         start_measure = n.measureNumber
    # makemeasure(ax, start_index,
    #     len(score._bassline.flat.getElementsByClass(m21.note.Note)) - 1,
    #     start_measure, len(yticks))

    # Starting x value
    current_x = 0
    max_rule_length, min_rule_length = rules.rule_max_min(these_rules)

    # For each rule in the ruleset...
    for i in range(len(these_rules)):
        ruleA = these_rules[i]

        # ...matched against every other rule in the ruleset
        for j in range(len(these_rules)):
            ruleB = these_rules[j]
            applied = 'no'

            if ruleB in ruleset.coexistence_array[ruleA]:
                applied = 'maybe'

            if ruleB == ruleA:
                applied = 'yes'

            makerulebox(ax, current_x, these_rules.index(ruleB), ruleB.size, chosen=applied)

        current_x = current_x + max_rule_length + 1

    #Time to format plot!
    #Deal with y-axis
    ax.set_ylim(0, len(yticks))
    ax.set_ylabel('Rule')
    ax.set_yticks(range(len(yticks)))
    ax.set_yticklabels(yticks)

    #Deal with x-axis
    ax.set_xlabel('Note indicies: \nEach vertical dotted ' + \
                    'line represents a single note in the score\'s bass line)')
    #ax.set_xlim(0, len(score.possible_rules) - 1)
    ax.xaxis.set_major_locator(mpltick.MultipleLocator(max_rule_length + 1))
    ax.xaxis.set_minor_locator(mpltick.MultipleLocator(1))
    ax.set_xticklabels(yticks)
    #ax.grid(True, which='minor')
    #ax.grid(True, linestyle='-')

    #Add legend
    lgd = makerulelegend(ax, type='ruleset')

#########

    if DEBUG == 1:
        fig.show()
    else:
        #Save it!
        filepath = filepath + '.png'
        fig.savefig(filepath, dpi=800, bbox_extra_artists=(lgd,), bbox_inches='tight')

        #Open it?
        if viewResults:
            os.system("open " + filepath)