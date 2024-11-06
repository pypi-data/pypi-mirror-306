import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

def plot_CFB(
        df_toplot, x_value, y_value, groupby,
        plot_type = 'mean', # median
        group_order = None, group_color = None, 
        units = None,
        linewidth_dict = None, linestyle_dict = None, marker_dict = None,
        errorbar = 'se', # 'sd', ('ci', 90)
        figsize = (8,5), ax = None, 
        showfliers = False, box_width = 0.5, general_linewidth = 0.8, 
        position_adjust = 0.27, 
        x_ticks = None, stripplot = False, title = None, 
        bbox_to_anchor = None, legend_title = None, legend_loc = None
):
    """
    Plot change from baseline figures
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    assert plot_type in ['mean','median'], "plot_type can be either 'mean' or 'median'"
    groupby_term = [x_value, groupby] if groupby is not None else x_value
    group_order = list(df_toplot[groupby].unique()) if group_order is None else group_order    
    palette = sns.color_palette("colorblind") if group_color is None else group_color
    num_hue_levels = len(group_order)
    
    if plot_type == 'mean':
        sns.lineplot(
            data = df_toplot, x = x_value, y = y_value, 
            hue = groupby, hue_order = group_order, palette = palette,
            units = units,             
            errorbar = errorbar, err_style= 'bars', 
            linewidth= 0, ax = ax
        )
        connect_dots = df_toplot.groupby(groupby_term, observed = True)[y_value].mean().reset_index()
    
    else:
        sns.boxplot(
            data = df_toplot, x = x_value, y = y_value, 
            hue = groupby, palette= palette, hue_order = group_order,
            showfliers = showfliers, showmeans = False,
            linewidth= general_linewidth, width = box_width, ax = ax
        )
        connect_dots = df_toplot.groupby(groupby_term, observed = True)[y_value].median().reset_index()

        if stripplot:
           sns.stripplot(
               data = df_toplot, x = x_value, y = y_value, 
               hue = groupby, palette= palette, dodge= True, # legend = None,
               linewidth = general_linewidth, ax = ax
        )
    
    # add lines that connect mean or median
    x_positions = {val: i for i, val in enumerate(df_toplot[x_value].unique())}
    handles = []
    labels = []

    for i, group in enumerate(group_order):
        subset = connect_dots[connect_dots[groupby] == group]
        if len(subset) > 0:
            # Calculate position for each dot
            dodge_value = (num_hue_levels - 1) / 2
            if plot_type == "mean":
                positions = subset[x_value]
            else:
                positions = [x_positions[x] + (i-dodge_value) * position_adjust for x in subset[x_value]]

            color = palette[i] if isinstance(palette, list) else palette[group]
            linestyle = linestyle_dict.get(group, '-') if linestyle_dict is not None else '-'
            marker = marker_dict.get(group, 'o') if marker_dict is not None else 'o'
            linewidth = linewidth_dict.get(group, general_linewidth) if linewidth_dict is not None else general_linewidth

            # Plot the lines - adjust 'x' to match position of boxes
            ax.plot(positions, subset[y_value], 
                color = color, linestyle = linestyle, marker = marker, linewidth = linewidth,
                markeredgewidth = general_linewidth, 
                markeredgecolor = "white"
            )

        # costom legend
        line = Line2D([0], [0], 
            color = color, linestyle = linestyle, marker = marker, linewidth = linewidth,
            markeredgewidth=general_linewidth,
            markeredgecolor="white"
        )
        handles.append(line)
        labels.append(group)
        
    ax.get_legend().remove()
    ax.legend(handles, labels, 
              title=groupby if legend_title is None else legend_title,
              bbox_to_anchor = bbox_to_anchor, loc = legend_loc,
             )
    ax.set_title(title)

    if x_ticks is not None:
        ax.set_xticks(ticks= x_ticks)

    return ax