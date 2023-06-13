import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.text as txt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch
import os
import datetime as dt
import pandas as pd
import numpy as np



def mysave(fig, froot, mode='png'):
    assert mode in ['png', 'eps', 'pdf', 'all']
    fileName, fileExtension = os.path.splitext(froot)
    padding = 0.1
    dpiVal = 200
    legs = []
    for a in fig.get_axes():
        addLeg = a.get_legend()
        if not addLeg is None: legs.append(a.get_legend())
    ext = []
    if mode == 'png' or mode == 'all':
        ext.append('png')
    if mode == 'eps':  # or mode == 'all':
        ext.append('eps')
    if mode == 'pdf' or mode == 'all':
        ext.append('pdf')

    for sfx in ext:
        fig.savefig(fileName + '.' + sfx, format=sfx, pad_inches=padding, bbox_inches='tight',
                    dpi=dpiVal, bbox_extra_artists=legs)


titleSize = 24  # 40 #38
axLabelSize = 20  # 38 #36
tickLabelSize = 18  # 30 #28
ganttTick = 18
legendSize = tickLabelSize + 2
textSize = legendSize - 2
deltaShow = 4
linewidth = 3


def myformat(ax, linewidth=linewidth, xticklabel=tickLabelSize, yticklabel=tickLabelSize, mode='save'):
    assert type(mode) == type('')
    assert mode.lower() in ['save', 'show'], 'Unknown mode'

    def myformat(myax, linewidth=linewidth, xticklabel=xticklabel, yticklabel=yticklabel):
        if mode.lower() == 'show':
            for i in myax.get_children():  # Gets EVERYTHING!
                if isinstance(i, txt.Text):
                    i.set_size(textSize + 3 * deltaShow)

            for i in myax.get_lines():
                if i.get_marker() == 'D': continue  # Don't modify baseline diamond
                i.set_linewidth(linewidth)
                # i.set_markeredgewidth(4)
                i.set_markersize(10)

            leg = myax.get_legend()
            if not leg is None:
                for t in leg.get_texts(): t.set_fontsize(legendSize + deltaShow + 6)
                th = leg.get_title()
                if not th is None:
                    th.set_fontsize(legendSize + deltaShow + 6)

            myax.set_title(myax.get_title(), size=titleSize + deltaShow, weight='bold', pad=20)
            myax.set_xlabel(myax.get_xlabel(), size=axLabelSize + deltaShow, weight='bold')
            myax.set_ylabel(myax.get_ylabel(), size=axLabelSize + deltaShow, weight='bold')
            myax.tick_params(labelsize=tickLabelSize + deltaShow)
            myax.patch.set_linewidth(3)
            for i in myax.get_xticklabels():
                i.set_size(tickLabelSize + deltaShow)
            for i in myax.get_xticklines():
                i.set_linewidth(3)
            for i in myax.get_yticklabels():
                i.set_size(yticklabel + deltaShow)
            for i in myax.get_yticklines():
                i.set_linewidth(3)

        elif mode.lower() == 'save':
            for i in myax.get_children():  # Gets EVERYTHING!
                if isinstance(i, txt.Text):
                    i.set_size(textSize)

            for i in myax.get_lines():
                if i.get_marker() == 'D': continue  # Don't modify baseline diamond
                i.set_linewidth(linewidth)
                # i.set_markeredgewidth(4)
                i.set_markersize(10)

            leg = myax.get_legend()
            if not leg is None:
                for t in leg.get_texts(): t.set_fontsize(legendSize)
                th = leg.get_title()
                if not th is None:
                    th.set_fontsize(legendSize)

            myax.set_title(myax.get_title(), size=titleSize, weight='bold', pad=20)
            myax.set_xlabel(myax.get_xlabel(), size=axLabelSize, weight='bold')
            myax.set_ylabel(myax.get_ylabel(), size=axLabelSize, weight='bold')
            myax.tick_params(labelsize=tickLabelSize)
            myax.patch.set_linewidth(3)
            for i in myax.get_xticklabels():
                i.set_size(xticklabel)
            for i in myax.get_xticklines():
                i.set_linewidth(3)
            for i in myax.get_yticklabels():
                i.set_size(yticklabel)
            for i in myax.get_yticklines():
                i.set_linewidth(3)

    if type(ax) == type([]):
        for i in ax: myformat(i)
    else:
        myformat(ax)

def initFigAxis(figx=28, figy=21):
    fig = plt.figure(figsize=(figx, figy))
    ax = fig.add_subplot(111)
    return fig, ax

def plot_gantt(df, manager, color_by, fname=None):
    fig, ax = initFigAxis()

    assign_colors(df, color_by)

    df["Date Finished"].plot(kind="barh", ax=ax, zorder=4, label="Project Time", color=df["install color"])
    df["Date Started"].plot(kind="barh", color=df["delay color"], ax=ax, zorder=4, label="Project Delay", hatch="////", linewidth=0.5)
    df["Date Initialized"].plot(kind='barh', ax=ax, zorder=4, label="__nolabel__", color='w')

    region_base_handles = [
    Patch(facecolor=color, label=label)
    for label, color in zip(['Central OR', 'Southern OR', 'Northern CA', 'Central CA'], ['#3498DB', '#F1C40F', '#E74C3C', '#8E44AD'])
    ]

    region_exp_handles = [
    Patch(facecolor=color, label=label)
    for label, color in zip(['Central OR', 'Southern OR', 'Northern CA', 'Central CA', 'Southern WA'], ['#3498DB', '#F1C40F', '#E74C3C', '#8E44AD', '#27AE60'])
    ]

    port_base_handles = [
    Patch(facecolor=color, label=label)
    for label, color in zip(['Humboldt', 'Coos Bay', 'Port San Luis', 'Long Beach', 'Grays Harbor'], ['#F39C12', '#16A085', '#C0392B', '#8E44AD', '#3498DB'])
    ]

    #port_exp_handles = [
    #Patch(facecolor=color, label=label)
    #for label, color in zip(['Central OR', 'Southern OR', 'Northern CA', 'Central CA', 'Southern WA'], ['#3498DB', '#F1C40F', '#E74C3C', '#8E44AD', '#27AE60'])
    #]

    if "Southern WA" in df[color_by]:
        handles = region_exp_handles
    elif color_by == "port":
        handles = port_base_handles
    else:
        handles = region_base_handles

    # Plot formatting
    ax.set_xlabel("")
    ax.set_ylabel("")
    _ = ax.set_yticklabels(df['region'])

    plt.yticks(fontsize=6)
    plt.plot((0, 0), (0, 30), scaley = False)
    ax.legend(handles=handles, loc = 'upper right')
    ax.set_xlim(manager._start - dt.timedelta(days=30), dt.date(2060, 6, 1) + dt.timedelta(days=30))
    num_proj = len(df['Date Finished'])

    ax.axvline(dt.date(2031, 1, 1), lw=0.5, ls="--", color="#2C3E50", zorder=6)
    installed_capacity_31 = get_installed_capacity_by(df, 2031)
    #ax.text(x=dt.date(2051, 1, 1), y=25, s=f"Capacity installed \nby end of 2030: \n{installed_capacity_31/1000:,.3} GW", fontsize=20, color="#2C3E50")

    ax.axvline(dt.date(2046, 1, 1), lw=0.5, ls="--", color="#2C3E50", zorder=6)
    installed_capacity_46 = get_installed_capacity_by(df, 2046)
    ax.text(x=dt.date(2048, 1, 1), y=(0.75*num_proj), s=f"Capacity installed \nby end of 2030: \n{installed_capacity_31/1000:,.3} GW. \nCapacity installed \nby end of 2045: \n{installed_capacity_46/1000:,.3} GW.", fontsize=30, color="#2C3E50")

    fig.subplots_adjust(left=0.25)


    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

## Bar chart of annual throughput of each port
def plot_throughput(throughput, fname=None):
    fig, ax = initFigAxis()

    throughput.plot.bar(ax=ax, width=0.75)

    ax.set_ylim(0, 2000)

    ax.set_ylabel("Annual Capacity Throughput (MW)")
    ax.set_xlabel("")

    plt.xticks(rotation=0, fontsize=6)
    plt.yticks(fontsize=6)

    ax.legend(fontsize=6, ncol=5)

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()
    #fname_t = 'results/throughput_'+str(s)+'.png'
    #fig.savefig(fname_t, dpi=300)

## Plot a near-term gantt chart
def plot_gantt_nt(df, manager, num_proj, color_by, fname=None):
    fig, ax = initFigAxis()

    assign_colors(df, color_by)

    df_nt = df.tail(num_proj)

    df_nt["Date Finished"].plot(kind="barh", ax=ax, zorder=4, label="Project Time", color=df_nt["install color"])
    df_nt["Date Started"].plot(kind="barh", color=df_nt["delay color"], ax=ax, zorder=4, label="Project Delay", hatch="////", linewidth=0.5)
    df_nt["Date Initialized"].plot(kind='barh', ax=ax, zorder=4, label="__nolabel__", color='w')

    # Plot formatting
    ax.set_xlabel("")
    ax.set_ylabel("")
    _ = ax.set_yticklabels(df_nt['region'])

    plt.yticks(fontsize=6)
    plt.plot((0, 0), (0, 30), scaley = False)
    ax.legend()
    ax.set_xlim(manager._start - dt.timedelta(days=30), dt.date(2040, 6, 1) + dt.timedelta(days=30))

    ax.axvline(dt.date(2031, 1, 1), lw=0.5, ls="--", color="#2C3E50", zorder=6)
    installed_capacity_31 = get_installed_capacity_by(df, 2031)
    ax.text(x=dt.date(2037, 1, 1), y=25, s=f"Capacity installed \nby end of 2030: \n{installed_capacity_31/1000:,.3} GW", fontsize=24, color="#2C3E50")

    fig.subplots_adjust(left=0.25)

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)
        plt.close()

def assign_colors(df, color_by):

    delay_color = []
    install_color = []

    for index, row in df.iterrows():
        if df[color_by][index] == "Northern CA":
            delay_color.append("#F5B7B1")
            install_color.append("#E74C3C")
        elif df[color_by][index] == "Central CA":
            delay_color.append("#D2B4DE")
            install_color.append("#8E44AD")
        elif df[color_by][index] == "Central OR":
            delay_color.append("#AED6F1")
            install_color.append("#3498DB")
        elif df[color_by][index] == "Southern OR":
            delay_color.append("#F9E79F")
            install_color.append("#F1C40F")
        elif df[color_by][index] == "Southern WA":
            delay_color.append("#A9DFBF")
            install_color.append("#27AE60")
        elif df[color_by][index] == "Humboldt":
            delay_color.append("#FAD7A0")
            install_color.append("#F39C12")
        elif df[color_by][index] == "Coos Bay":
            delay_color.append("#A2D9CE")
            install_color.append("#16A085")
        elif df[color_by][index] == "Port of San Luis":
            delay_color.append("#E6B0AA")
            install_color.append("#C0392B")
        elif df[color_by][index] == "Long Beach":
            delay_color.append("#D2B4DE")
            install_color.append("#8E44AD")
        elif df[color_by][index] == "Grays Harbor":
            delay_color.append("#AED6F1")
            install_color.append("#3498DB")
        else:
            delay_color.append("#e9e9e9")
            install_color.append("#e9e9e9")

    df["delay color"] = delay_color
    df["install color"] = install_color

def plot_summary(scenarios, capacity_list, target_capacity):
    by_year = 2045

    inv_df = pd.read_excel('library/investments/scenario-investments.xlsx', sheet_name='schedule')
    inv_df = inv_df.set_index('Year')

    invest_list = []
    for s in scenarios:
        invest_list.append(inv_df[s][by_year])

    fig = plt.figure(figsize=(6, 4))
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    width = 0.25

    x_ind = np.arange(len(scenarios))

    target = [target_capacity[s.split('-')[0]] for s in scenarios]
    ax1.bar(x_ind-width, target, width, color='#28DA16')

    ax1.bar(x_ind, capacity_list, width, color='#3C2AC0')
    ax1.set_ylabel('Installed capacity by end of ' + str(by_year) + ', GW')
    ax1.set_ylim([0,60])

    perc_installed = [int(round(100*c/t,0)) for c,t in zip(capacity_list, target)]
    perc_installed_dict = {}
    for s,p in zip(scenarios, perc_installed):
        perc_installed_dict[s] = p

    ax2.bar(x_ind+width, invest_list, width, color='#FFA319')
    ax2.set_ylabel('Investment required, $M')
    ax2.set_ylim([0,8000])
    ax2.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax1.set_xticks(x_ind)
    plot_names = scenarios
    ax1.set_xticklabels(plot_names, rotation=45)

    plt.title('made with dummy investment numbers!', color = 'red')

    handles = [
        Patch(facecolor=color, label=label)
        for label, color in zip(['Target capacity','Installed capacity', 'Investment'], ['#28DA16','#3C2AC0', '#FFA319'])
    ]

    ax1.legend(handles=handles, loc='upper left');

    fig.savefig('results/summary.png', bbox_inches='tight', dpi=300)

    return perc_installed_dict

def plot_deployment():
    levels = ['Baseline', 'Moderate', 'Expanded']

    schedules = 'library/pipeline/deployment-schedules.xlsx'

    for s in levels:
        df = pd.read_excel(schedules, sheet_name = s, index_col='Year')

        if s=='Baseline':
            regions = df[['Central CA','Northern CA']].copy()
            total = regions.sum(axis=1)[2045]
        elif s=='Moderate':
            regions = df[['Central CA','Northern CA', 'Central OR', 'Southern OR']].copy()
            total = regions.sum(axis=1)[2045]
        elif s =='Expanded':
            regions = df[['Central CA','Northern CA', 'Central OR', 'Southern OR', 'Southern WA']].copy()
            total = regions.sum(axis=1)[2045]

        fig = plt.figure(figsize=(9, 6))
        ax = fig.add_subplot(111)
        ax2 = fig.add_subplot(111)

        ## Stacked area charts
        ax = regions.plot.area()
        plt.title('Deployment for the '+ s +' Scenario: ' + str(int(total/1000)) + ' GW')
        ax.set_ylabel('Cumulative installed capacity')

        area_fname = 'results/Deployment/' + s + '_stacked.png'
        plt.savefig(area_fname, bbox_inches='tight')

        ## Simple line graphs
        ax2 = regions.plot.line()
        plt.title('Deployment for the '+ s +' Scenario: ' + str(int(total/1000)) + ' GW')
        ax2.set_ylabel('Cumulative installed capacity')

        line_fname = 'results/Deployment/' + s + '_line.png'
        plt.savefig(line_fname, bbox_inches='tight')

