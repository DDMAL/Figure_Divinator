# Copyright (C) 2012 by Hannah Robertson
"""
Creates visualisations of rules matching a score and internal rule set relationships.

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mpltick
import os
import music21 as m21
import rules

_colors = ['yellow', 'green', 'red', 'grey', '#66ff99']  # unknown, coexist, conflict, never, self


def _makemeasure(axes_handle, startIndex, endIndex, number, H=.8):
    """
    Plots a measure as a bar in the axis given by ``axes_handle``.

    **Args**:
        **startIndex**: Index of measure's first note.

        **endIndex**: Index of measure's last note.

        **number**: Measure number; used for text label.

    **kwargs**:
        **H**: (Optional) Height of bar drawn. Default .8.

    """
    L = endIndex - startIndex
    if H != .8:
        H = 2 * H
    axes_handle.barh(0, L, x=(startIndex - .5), height=H, align='center', \
            color='none', alpha=None)
    axes_handle.text(startIndex, 0.05, str(number))


def _makerulebox(axes_handle, startIndex, ruleIndex, ruleLength, alpha=0.7,
            chosen='maybe', H=.8, barcolor=_colors[0], stickcolor='purple'):
    """
    Plots a rule as a bar.

    **Args**:
        **axes_handle**: Handle of axis to plot in.

        **startIndex**: Index of rule's first note.

        **ruleIndex**: y-value that rule will be plotted at.

        **ruleLength**: Number of note indecies rule covers.

    **kwargs**:
        **alpha**: (Optional) Transparency of bar. Default .7.

        **chosen**: (Optional) TODO. Default 'maybe'.

        **barcolor**: (Optional) Color of bar. Defaults to 'maybe' color.

        **stickcolor**: (Optional) Color of horizontal line through bar.
        Default 'purple'.

        **H**: (Optional) Height of bar drawn. Default .8.

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


def _makeruleline(axes_handle, startIndex, ruleIndex, ruleLength, alpha=1,
            existance='unknown', H=.8, barcolor=_colors[0],
            marker='o', markersize=8, lw=5):
    """
    Plots a rule as a line.

    **Args**:
        **axes_handle**: Handle of axis to plot in.

        **startIndex**: Index of rule's first note.

        **ruleIndex**: y-value that rule will be plotted at.

        **ruleLength**: Number of note indecies rule covers.

    **kwargs**:
        **alpha**: (Optional) Transparency of line. Default .7.

        **existance**: (Optional) Determine's color; choices are 'coexist',
        'conflict', 'self', and 'never'. Default 'unknown'.

        **barcolor**: (Optional) Default color of bar if existance is 'unknown'.
        Defaults to 'yellow'.

        **lw**: (Optional) Line width. Default 5.

        **markersize**: (Optional) Default 8.

        **marker**: (Optional) Shape of marker on each index. Default 'o'.

    """
    if existance == 'coexist':
        barcolor = _colors[1]
    elif existance == 'conflict':
        barcolor = _colors[2]
    elif existance == 'self':
        barcolor = _colors[4]
    elif existance == 'never':
        barcolor = _colors[3]

    x = range(startIndex, startIndex + ruleLength)
    y = [ruleIndex for i in x]

    axes_handle.plot(x, y, c=barcolor, lw=lw, ls='-',
                    marker=marker, alpha=alpha)


def _makerule(axes_handle, startIndex, ruleLength, H=.8, barcolor=_colors[1]):
    """
    Plots a rule as a column.

    **Args**:
        **axes_handle**: Handle of axis to plot in.

        **startIndex**: Index of rule's first note.

        **ruleLength**: Number of note indecies rule covers.

    **kargs**:

        **H**: (Optional) Height of bar drawn. Default .8.

        **barcolor**: (Optional) Color of bar. Defaults to 'green'.

    """
    axes_handle.barh(-1, ruleLength - 1, left=startIndex, \
        height=H, alpha=.2, align='center', color=barcolor)


def _makerulelegend(axes_handle, type='score', allRules='True'):
    """
    Creates, returns legend for plot.

    Args:

        **type**: (Optional) Choices: 'score' or 'ruleset'. Default is 'score'.

        **allRules**: (Optional) Boolean. If legend type is for a 'ruleset'
        plot, sets whether to include all rule types or only ones without
        conflict. Default is True.

    """
    #make fake plot to get legend info
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    b1 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[2])
    b2 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[1])
    b3 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[4])
    b4 = ax2.bar([0.2, 0.3, 0.1], [0.2, 0.3, 0.1], linewidth=0, color=_colors[3])

    if type == 'ruleset' and allRules == True:
        plots = [b1, b2, b3, b4]
        plotlabels = ['Conflict', 'Coexist', 'Self', 'Never overlap']
    elif type == 'ruleset' and allRules == False:
        plots = [b1, b2, b3]
        plotlabels = ['Conflict', 'Coexist', 'Self']
    else:
        b1 = ax2.bar([0, 1, 2], [0.2, 0.3, 0.1], color=_colors[0])
        b2 = ax2.bar([0, 1, 2], [0.2, 0.3, 0.1], color=_colors[1])
        plots = [b1, b2]
        plotlabels = ['Rule matches score', 'Rule applied']

    lgd = axes_handle.legend(plots, plotlabels, bbox_to_anchor=(1, 0.5),
            loc='center left')
    return lgd


def makePlotFromScore(extraction_work, allRules=False,
                        filepath='results/temporary_rule_plot',
                        viewResults=True, saveResults=False,
                        direction='unknown'):
    """
    Plots a score's possible and applied rules.

    **Args**:
        **extraction_work**: :class:`ExtractionWork` object that contains the
        score and rule set.

    **kwargs**:
        **allRules**: (Optional) If true, show all possible rules on y-axis,
        even if rules never match score. Default False.

        **filepath**: (Optional) Path/name at which to save the plot. Default
        ``results/temporary_rule_plot``.

        **viewResults**: (Optional) If true, displays plot immediately after
        creation. Default True.

        **saveResults**: (Optional) If true, saves plot. Default False.

        **direction**: (Optional) Direction in which rules were applied,
        used only to correctly title plot. Default 'unknown'.

    """
    if __name__ == '__main__':
        calledFromInterpreter = True
    else:
        calledFromInterpreter = False

    if filepath != 'results/temporary_rule_plot':
        saveResults = True

    plottitle = (unicode('All rules that match score \'') + extraction_work.title.decode('utf-8') + \
                    unicode(',\'\nfrom ') + unicode(str(extraction_work.ruleset))) + \
                    unicode(',\' applied in ') + unicode(str(direction)) + unicode(' direction.')
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
            _makemeasure(ax, start_index, i, start_measure, len(yticks))
            start_index = i
            start_measure = n.measureNumber
    _makemeasure(ax, start_index,
        len(extraction_work._bassline.flat.getElementsByClass(m21.note.Note)) - 1,
        start_measure, len(yticks))

    #Plot each rule possible
    for i in range(len(extraction_work.possible_rules)):
        if extraction_work.possible_rules[i]:
            for r in extraction_work.possible_rules[i]:
                applied = 'maybe'
                applied_rules = [x.__class__.__name__ for x in extraction_work.chosen_rules[i]]
                if r.__class__.__name__ in applied_rules:
                    applied = 'yes'
                _makerulebox(ax, i, 1 + these_rules.index(r), r.size, chosen=applied)

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
    lgd = _makerulelegend(ax)

    #Deal with output
    #Save it?
    if saveResults == True:
        filepath = filepath + '-' + direction + '.png'
        fig.savefig(filepath, dpi=800, bbox_extra_artists=(lgd,), bbox_inches='tight')

        #Open saved version?
        if viewResults:
            os.system("open " + filepath)

    #Show it?
    if viewResults == True and calledFromInterpreter == True:
        fig.show()


def makePlotFromRuleset(ruleset, allRules=False,
                        filepath='results/temporary_ruleset_plot',
                        viewResults=True, saveResults=False):
    """
    Plots a rule set's similarity matrix of rule interactions and dominances.

    **Args**:
        **ruleset**: :class:`rules.Ruleset` object that contains the
        list of rules and the rule interaction arrays.

    **kwargs**:
        **allRules**: (Optional) If true, shows even interactions that never
        occur because rule definitions are mutually exclusive. 'True' gives
        the most accurate plot, but can be overwhelminly busy if the ruleset is
        large (>5 rules or so). Default False.

        **filepath**: (Optional) Path/name at which to save plot. Default
        ``results/temporary_rule_plot``.

        **viewResults**: (Optional) If true, displays plot immediately after
        creation. Default True.

        **saveResults**: (Optional) If true, save plot. Default False.

    """
    if __name__ == '__main__':
        calledFromInterpreter = True
    else:
        calledFromInterpreter = False

    if filepath != 'results/temporary_ruleset_plot':
        saveResults = True

    #What rules are we plotting here?
    #For x:
    these_rules = ruleset.rulelist
    xticks = [a.__class__.__name__ for a in these_rules]

    #For y: What are the rules with all offsets that we're plotting here
    these_rules_offset = []
    max_rule_length, min_rule_length = rules.rule_max_min(these_rules)
    for r in these_rules:
        for o in range(1 - r.size, max_rule_length):
            these_rules_offset.append((r, o))
        these_rules_offset.append(False)
    yticks = [' ' for x in range(1 + len(these_rules_offset))]
    for x in range(len(these_rules_offset)):
        if these_rules_offset[x]:
            (r, o) = these_rules_offset[x]
            yticks[x] = '%s (offset %s)' % (r.__class__.__name__, str(o))

    #Set up the plot
    plottitle = (unicode('Matrix of rule interactions from rule set "') + unicode(str(ruleset.name)) + unicode('"'))
    fig = plt.figure()
    ax = fig.add_subplot(111, title=plottitle)
    ax.set_axisbelow(True)

    # Starting x value
    current_x = 0

    rule_bar_height = 2.3 / (8 + max_rule_length * 2.0)  # To keep bars from overlapping, set 1.8 to 1
    rule_jump = 3 * max_rule_length - 1

    # For each rule in the ruleset...
    for i in range(len(these_rules)):
        ruleA = these_rules[i]

        # ...draw rule column
        rule_start_x = current_x + max_rule_length
        _makerule(ax, rule_start_x, ruleA.size, H=2 * len(yticks) + 2)

        # ...matched against every other rule in the ruleset
        for j in range(len(these_rules)):
            ruleB = these_rules[j]

            # ...in every possible offset possibility
            all_o = range(-1 * (ruleB.size - 1), ruleA.size)
            for o in all_o:
                keycolor = 'never'

                if (ruleB, o) in ruleset.coexistence_array[ruleA]:
                    keycolor = 'unknown'

                if (ruleB, o, 'coexist') in ruleset.coexistence_array[ruleA]:
                    keycolor = 'coexist'

                if (ruleB, o, 'conflict') in ruleset.coexistence_array[ruleA]:
                    keycolor = 'conflict'

                if ruleB == ruleA and o == 0:
                    keycolor = 'self'

                #Show all the rules, or just the ones that can coexist?
                if allRules == True:
                    this_y = these_rules_offset.index((ruleB, o))
                    _makeruleline(ax, rule_start_x + o, this_y,
                                ruleB.size, H=rule_bar_height, existance=keycolor,
                                )
                elif keycolor != 'never':
                    this_y = these_rules_offset.index((ruleB, o))
                    _makeruleline(ax, rule_start_x + o, this_y,
                                ruleB.size, H=rule_bar_height, existance=keycolor,
                                )

        current_x = current_x + rule_jump

    #Time to format plot!
    if ruleset.name == 'Saint Lambert (Full)':
        yticks = [y.strip('SLRule_') for y in yticks]

    #Deal with y-axis

    ax.set_ylabel('Rules')
    ax.set_ylim(0, len(yticks))
    ax.yaxis.set_major_locator(mpltick.MultipleLocator(1))
    ax.yaxis.set_minor_locator(mpltick.MultipleLocator(1))

    ax.yaxis.set_minor_formatter(mpltick.IndexFormatter(yticks))
    ax.yaxis.set_major_formatter(mpltick.NullFormatter())
    ax.set_ylim(-1, len(yticks) - 1)

    #Deal with x-axis
    ax.set_xlabel('Rules \n(Each vertical dotted ' + \
                    'line represents a single bass note to be figured)')
    ax.set_xlim(0, rule_jump * len(xticks))
    #ax.xaxis.set_major_locator(mpltick.MultipleLocator(rule_jump))
    ax.xaxis.set_major_locator(mpltick.IndexLocator(rule_jump, max_rule_length - 1))
    ax.xaxis.set_minor_locator(mpltick.MultipleLocator(1))
    ax.set_xticklabels(xticks, ha='left')
    ax.xaxis.grid(True, which='minor')
    ax.grid(True, ls='--')

    #Add legend
    lgd = _makerulelegend(ax, type='ruleset', allRules=allRules)

    #Make sure image is sized in accordance with the number of rows/columns.
    fig.set_size_inches(3 * len(xticks), .5 * len(yticks))

    #Save it?
    if saveResults == True:
        filepath = filepath + '.pdf'
        fig.savefig(filepath, dpi=fig.dpi, bbox_extra_artists=(lgd,), bbox_inches='tight')
        print 'saved at %s' % filepath

        #Open saved version?
        if viewResults:
            os.system("open " + filepath)

    #Show it?
    if viewResults == True and calledFromInterpreter == True:
        fig.show()
