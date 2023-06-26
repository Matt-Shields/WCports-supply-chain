import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from plot_routines import initFigAxis, myformat, mysave

df = pd.read_excel('waterfall chart calculations_test.xlsx', sheet_name = 'domestic_content')

def plot_waterfall_domestic_content(df, fname):
    fig, ax = initFigAxis(figx=20, figy=10)
    
    scenarios = {
        'se_asia': {
            'Labor Costs': 685,
            'Material Costs': 1747,
            'Transportation Costs': 708,
        },
        'us (no IRA Domestic Content Bonus Credits)': {
            'Labor Costs': 1370,
            'Material Costs': 2159,
            'Transportation Costs': 48,
            'New Factory Amortization': 164,
            # 'IRA Domestic Content Bonus Credits': 226
        },
        'us (IRA Domestic Content Bonus Credits)': {
            'Labor Costs': 1370,
            'Material Costs': 2159 - 370,
            'Transportation Costs': 48,
            'New Factory Amortization': 164,
            # 'IRA Domestic Content Bonus Credits': 226
        },
        'us_steel':  {
            'Labor Costs': 1370,
            'Material Costs': 2159,
            'Transportation Costs': 48,
            'New Factory Amortization': 164,
            'Section 232 Steel Tariffs': 354,
        },            
    }
   
        
    color_list = {
        'Labor Costs': '#069af3',
        'Material Costs': '#8169b7',
        'Transportation Costs': '#8a3f6d',
        'New Factory Amortization': '#ffa500',
        # 'IRA Domestic Content Bonus Credits': '#ff6e54',
        'Section 232 Steel Tariffs': '#3d1c02',        
    }
    
    scenario_names = {
        'se_asia': 'Southeast Asia',
        'us (no IRA Domestic Content Bonus Credits)' : 'West Coast',
        'us (IRA Domestic Content Bonus Credits)': 'West Coast \n(With Domestic Content Bonus from \n Inflation Reduction Act)',
        'us_steel': 'West Coast Using \nImported Raw Steel'
    }

    legend = []
    
    for n, s in scenarios.items():
        bottom = 0
        for k,v in s.items():
            if k == 'IRA Domestic Content Bonus Credits':
                alpha=0.4
                linestyle = '--'
                edgecolor='k'
            else:
                alpha=1
                alpha=1
                linestyle = '-'
                edgecolor='w'
                
            if k in legend:
                pass
                ax.bar(scenario_names[n], v, width=0.5, bottom=bottom, color=color_list[k], alpha=alpha, linewidth=2, linestyle= linestyle, edgecolor=edgecolor)
            else:
                legend.append(k)
                ax.bar(scenario_names[n], v, width=0.5, bottom=bottom, color=color_list[k], label=k, alpha=alpha, linewidth=2, linestyle= linestyle, edgecolor=edgecolor)

            bottom += v
    
    ax.legend()
    handles,labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left')
    
    ax.set_xlabel('Component Manufacturing Location')
            
    ax.set_title('Components Manufactured on the West Coast Could be Cost Competitive \nWith Imports From Southeast Asia Because of Reduced Transportation Costs \nand Benefits From the Inflation Reduction Act')

    ax.set_ylim(0, 4500)
    ax.set_ylabel('Total Landed Component Cost for a \nAnalysing1 GW Floating Wind Project ($/kW)')

    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if fname is not None:
        myformat(ax)
        mysave(fig, fname)

if __name__ == "__main__": 
    plot_waterfall_domestic_content(df,'plt_waterfall.png')