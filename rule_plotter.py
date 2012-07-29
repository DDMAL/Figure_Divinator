import matplotlib.pyplot as plt
import matplotlib.ticker as mpltick
import os
import music21 as m21
import rules

_colors = ['yellow', 'green', 'red', 'grey', '#66ff99']  # unknown, coexist, conflict, never, self


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


def makerulebox(axes_handle, startIndex, ruleIndex, ruleLength, alpha=0.7,
            chosen='maybe', H=.8, barcolor=_colors[0], stickcolor='purple'):
    """
    Function to plot each rule as a bar
    """
    if chosen == 'yes':
        barcolor = _colors[1]
    elif chosen == 'no':
        barcolor = _colors[2]

    #Only draw bounding lines if stickcolor has been set
    if stickcolor:
        axes_handle.barh(ruleIndex, ruleLength, x=startIndex, \
            height=H, alpha=alpha, align='center', color=barcolor, lw=3)
        axes_handle.hlines(ruleIndex, startIndex, startIndex + ruleLength, \
            linewidth=3, color=stickcolor)
        axes_handle.vlines(startIndex, ruleIndex - H / 2, ruleIndex + H / 2, \
            color=stickcolor, linewidth=4)
        axes_handle.vlines(startIndex + ruleLength, ruleIndex - H / 2, \
            ruleIndex + H / 2, linewidth=2, color=stickcolor)
    else:
        axes_handle.hlines(ruleIndex, startIndex, startIndex + ruleLength, \
            linewidth=10, color=barcolor)


def makeruleline(axes_handle, startIndex, ruleIndex, ruleLength, alpha=1,
            existance='unknown', H=.8, barcolor=_colors[0], choice=0,
            marker='o', markersize=8, lw=5):
    """
    Function to plot each rule as a line
    """
    if existance == 'coexist':
        barcolor = _colors[2]
    elif existance == 'conflict':
        barcolor = _colors[2]
    elif existance == 'self':
        barcolor = _colors[4]
    elif existance == 'never':
        barcolor = _colors[3]

    x = range(startIndex, startIndex + ruleLength)
    y = [ruleIndex for i in x]

    # #Only draw bounding lines if stickcolor has been set
    # if choice == 1:
    #     lw = 3
    # else:
    #     lw = 10

    axes_handle.plot(x, y, c=barcolor, lw=lw, ls='-',
                    marker=marker, alpha=alpha)


def makerule(axes_handle, startIndex, ruleLength, H=.8, barcolor=_colors[1]):
    """
    Function to plot each rule as a column
    """
    axes_handle.barh(-1, ruleLength - 1, left=startIndex, \
        height=H, alpha=.2, align='center', color=barcolor)


def makerulelegend(axes_handle, type='score', allRules='True'):
    if type == 'score':
        plotlabels = ['Rule matches score', 'Rule applied']
    elif type == 'ruleset' and allRules == True:
        plotlabels = ['Conflict', 'Coexist', 'Self', 'Never overlap']
    else:
        plotlabels = ['Conflict', 'Coexist', 'Self']

    #make fake plot to get legend info
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)

    if type == 'ruleset':
        b1 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[2])
        b2 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[1])
        b3 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[4])
        b4 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[3])
        plots = [b1, b2, b3, b4]
        if allRules == False:
            plots = plots[:2]

        lgd = axes_handle.legend(plots, plotlabels, bbox_to_anchor=(1, 0.5),
            loc='center left')
    else:
        b1 = ax2.bar([0, 1, 2], [0.2, 0.3, 0.1], color=_colors[0])
        b2 = ax2.bar([0, 1, 2], [0.2, 0.3, 0.1], color=_colors[1])
        plots = [b1, b2]
        lgd = axes_handle.legend(plots, plotlabels, bbox_to_anchor=(1, 0.5),
            loc='center left')
    return lgd


def makePlotFromScore(extraction_work, allRules=False, filepath='results/temporary_rule_plot', viewResults=True, saveResults=False):
    """
    Given an ExtractionWork object, show all rules and the chosen rules.
    """
    if __name__ == '__main__':
        calledFromInterpreter = True
    else:
        calledFromInterpreter = False

    if filepath != 'results/temporary_rule_plot':
        saveResults = True

    plottitle = (unicode('All rules that match score \'') + extraction_work.title.decode('utf-8') +
                    unicode(',\'\nfrom ') + unicode(str(extraction_work.ruleset)))
    fig = plt.figure()
    ax = fig.add_subplot(111, title=plottitle)
    ax.set_axisbelow(True)

    #What rules are we plotting here?
    these_rules = []
    if allRules:
        these_rules = extraction_work._allrules
    else:
        temp_rules = []
        for i in range(len(extraction_work.possible_rules)):
            if extraction_work.possible_rules[i]:
                for r in extraction_work.possible_rules[i]:
                    temp_rules.append(r)
        these_rules = [x for x in extraction_work._allrules if x in temp_rules]
    yticks = [a.__class__.__name__ for a in these_rules]
    yticks.insert(0, 'Measures:\n')

    # Plot all the measures across the bottom
    start_index = 0
    start_measure = extraction_work._bassline.flat.getElementsByClass(m21.note.Note)[0].measureNumber
    for i in range(len(extraction_work._bassline.flat.getElementsByClass(m21.note.Note))):
        n = extraction_work._bassline.flat.getElementsByClass(m21.note.Note)[i]
        if n.measureNumber == start_measure:
            pass
        else:
            makemeasure(ax, start_index, i, start_measure, len(yticks))
            start_index = i
            start_measure = n.measureNumber
    makemeasure(ax, start_index,
        len(extraction_work._bassline.flat.getElementsByClass(m21.note.Note)) - 1,
        start_measure, len(yticks))

    #Plot each rule possible
    for i in range(len(extraction_work.possible_rules)):
        if extraction_work.possible_rules[i]:
            for r in extraction_work.possible_rules[i]:
                applied = 'maybe'
                if r in extraction_work.chosen_rules[i]:
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
    ax.set_xlim(0, len(extraction_work.possible_rules) - 1)
    ax.xaxis.set_major_locator(mpltick.NullLocator())
    ax.xaxis.set_minor_locator(mpltick.MultipleLocator(1))
    ax.grid(True, which='minor')
    ax.grid(True, linestyle='-')

    #Add legend
    lgd = makerulelegend(ax)

    #Deal with output
    #Show it?
    if viewResults == True and calledFromInterpreter == True:
        fig.show()

    #Save it?
    if saveResults == True:
        filepath = filepath + '.png'
        fig.savefig(filepath, dpi=800, bbox_extra_artists=(lgd,), bbox_inches='tight')

        #Open saved version?
        if viewResults:
            os.system("open " + filepath)


def makePlotFromRuleset(ruleset, allRules=True,
                filepath='results/temporary_ruleset_plot', viewResults=True, saveResults=False):
    """
    Given a ruleset, show all rules and the chosen rules.
    """
    if __name__ == '__main__':
        calledFromInterpreter = True
    else:
        calledFromInterpreter = False

    if filepath != 'results/temporary_rule_plot':
        saveResults = True

    #What rules are we plotting here?
    these_rules = ruleset.rulelist
    yticks = [a.__class__.__name__ for a in these_rules]

    #Set up the plot
    plottitle = (unicode('Matrix of rule interactions from rule set "') + unicode(str(ruleset.name)) + unicode('"'))
    fig = plt.figure()
    ax = fig.add_subplot(111, title=plottitle)
    ax.set_axisbelow(True)

    # Starting x value
    current_x = 0
    max_rule_length, min_rule_length = rules.rule_max_min(these_rules)
    rule_bar_height = 2.3 / (8 + max_rule_length * 2.0)  # To keep bars from overlapping, set 1.8 to 1
    rule_jump = 3 * max_rule_length - 1

    # For each rule in the ruleset...
    for i in range(len(these_rules)):
        ruleA = these_rules[i]

        # ...draw rule column
        rule_start_x = current_x + max_rule_length
        makerule(ax, rule_start_x, ruleA.size, H=2 * len(yticks) + 2)

        # ...matched against every other rule in the ruleset
        for j in range(len(these_rules)):
            ruleB = these_rules[j]

            # ...in every possible offset possibility
            all_o = range(-1 * (ruleB.size - 1), ruleA.size)
            for o in all_o:
                keycolor = 'never'

                if (ruleB, o) in ruleset.coexistence_array[ruleA]:
                    keycolor = 'unknown'

                if ruleB == ruleA and o == 0:
                    keycolor = 'self'

                #Show all the rules, or just the ones that can coexist?
                if allRules == True:
                    this_y = these_rules.index(ruleB) + .1 * o - .5
                    makeruleline(ax, rule_start_x + o, this_y,
                                ruleB.size, H=rule_bar_height, existance=keycolor,
                                )
                elif keycolor != 'no':
                    this_y = these_rules.index(ruleB) + .1 * o - .5
                    makeruleline(ax, rule_start_x + o, this_y,
                                ruleB.size, H=rule_bar_height, existance=keycolor,
                                )

        current_x = current_x + rule_jump

    #Time to format plot!
    ylabels = yticks
    if ruleset.name == 'Saint Lambert (Full)':
        ylabels = [x.strip('SLRule_') for x in yticks]

    #Deal with y-axis
    ax.set_ylim(-1, len(yticks) - 1)
    ax.set_ylabel('Rules')

    ax.yaxis.set_major_locator(mpltick.MultipleLocator(1))
    ax.yaxis.set_minor_locator(mpltick.IndexLocator(1, .5))
    ax.yaxis.set_minor_formatter(mpltick.IndexFormatter(ylabels))
    ax.yaxis.set_major_formatter(mpltick.NullFormatter())

    #Deal with x-axis
    ax.set_xlabel('Rules \n(Each vertical dotted ' + \
                    'line represents a single bass note to be figured)')
    ax.set_xlim(0, rule_jump * len(yticks))
    ax.xaxis.set_major_locator(mpltick.MultipleLocator(rule_jump))
    ax.xaxis.set_minor_locator(mpltick.MultipleLocator(1))
    ax.set_xticklabels(ylabels, ha='left')
    ax.xaxis.grid(True, which='minor')
    ax.grid(True, ls='--')

    #Add legend
    lgd = makerulelegend(ax, type='ruleset', allRules=allRules)

    #Deal with output
    #Show it?
    if viewResults == True and calledFromInterpreter == True:
        fig.show()

    #Save it?
    if saveResults == True:
        filepath = filepath + '.png'
        fig.savefig(filepath, dpi=800, bbox_extra_artists=(lgd,), bbox_inches='tight')

        #Open saved version?
        if viewResults:
            os.system("open " + filepath)
