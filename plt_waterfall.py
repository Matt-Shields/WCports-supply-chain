import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from plot_routines import initFigAxis, myformat, mysave

df = pd.read_excel('waterfall chart calculations_test.xlsx', sheet_name = 'domestic_content')

def plot_waterfall_domestic_content(df, fname):
    fig, ax = initFigAxis(figx=20, figy=10)

    # scenario = df['scenario'].to_list() 
    # value = df['value'].to_list() 

    # bottom = [0] * 8
    # for i in range (1,5):
        # bottom[i] = bottom[i-1] + value[i-1]
    # bottom[6] = value[5]

    # c=['#3498DB']*8
    # for i in [1,2,3,4,6]:
        # if value[i]>0: 
            # c[i]='#F1C40F'
        # else:
            # c[i]='#27AE60'

    # scenario = scenario[:5] + scenario[6:]
    # value = value[:5] + value[6:]
    # bottom = bottom[:5] + bottom[6:]
    # c = c[:5] + c[6:]
    
    scenarios = {
        'se_asia': {
            'Labor Costs': 378,
            'Material Costs': 1114,
            'Transportation Costs': 709,
        },
        'us (no IRA Domestic Content Bonus Credits)': {
            'Labor Costs': 756,
            'Material Costs': 1352,
            'Transportation Costs': 48,
            'New Factory Amortization': 105,
            # 'IRA Domestic Content Bonus Credits': 226
        },
        'us (IRA Domestic Content Bonus Credits)': {
            'Labor Costs': 756,
            'Material Costs': 1352 - 226,
            'Transportation Costs': 48,
            'New Factory Amortization': 105,
            # 'IRA Domestic Content Bonus Credits': 226
        },
        'us_steel':  {
            'Labor Costs': 756,
            'Material Costs': 1352,
            'Transportation Costs': 48,
            'New Factory Amortization': 105,
            'Section 232 Steel Tariffs': 203,
        },
        # 'us_steel':  {
            # 'Labor Costs': 756,
            # 'Material Costs': 1352,
            # 'Transportation Costs': 48,
            # 'New Factory Amortization': 105,
            # 'Section 232 Steel Tariffs': 203,
        # }
       
        
    }
   
        
    color_list = {
        'Labor Costs': '#069af3',
        'Material Costs': '#8169b7',
        'Transportation Costs': '#8a3f6d',
        'New Factory Amortization': '#6b282f',
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
            
    

    # bars = ax.bar(scenario,value,bottom=bottom,color=c, width=0.7)
    ax.set_title('Components Manufactured on the West Coast Could be Cost Competitive \nWith Imports From Southeast Asia Because of Reduced Transportation Costs \nand Benefits From the Inflation Reduction Act')

# Cost Comparison of US West Coast and Southeast Asia Supply Chains: \nAnalysing the Impact of Domestic Content Benefits and Reduced Transportation Costs
# A West Coast scenario could be cost competitive to the South East Asia supply chain \nconsidering Domestic Content Benefits and Reduced Transportation Costs
    ax.set_ylim(0, 3500)
    ax.set_ylabel('Total Landed Component Cost for a \nAnalysing1 GW Floating Wind Project ($/kW)')

    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # ax.set_xticklabels(scenarios, rotation=45)

    # for i, bar in enumerate(bars): 
        # if value[i] > 0:
            # ax.text(bar.get_x() + bar.get_width()/2, bottom[i] + value[i]*1.01, int(value[i]), ha='center', va='bottom', color='black')
        # else:
            # ax.text(bar.get_x() + bar.get_width()/2, bottom[i]+value[i]*1.1, int(value[i]), ha='center', va='top', color='black')

    # plt.show()
    if fname is not None:
        myformat(ax)
        mysave(fig, fname)

# def plot_waterfall_steel(df, fname):
#     fig, ax = initFigAxis(figx=20, figy=10)

#     scenario = df['scenario'].to_list() 
#     value = df['value'].to_list() 

#     value[4], value[6] = value[6], value[4]
#     value[5] = sum(value[:5])

#     bottom = [0] * 8
#     for i in range (1,5):
#         bottom[i] = bottom[i-1] + value[i-1]
#     bottom[6] = value[5]

#     c=['#3498DB']*8
#     for i in [1,2,3,4,6]:
#         if value[i]>0: 
#             c[i]='#F1C40F'
#         else:
#             c[i]='#27AE60'

#     scenario = scenario[:5] + scenario[6:]
#     value = value[:5] + value[6:]
#     bottom = bottom[:5] + bottom[6:]
#     c = c[:5] + c[6:]

#     bars = ax.bar(scenario,value,bottom=bottom,color=c, width=0.7)
#     ax.set_title('US will need sufficient domestic steel production to qualify for tariffs to avoid higher project costs')

#     ax.set_ylim(0, 3500)
#     ax.set_ylabel('Manufacturing Cost ($/kW)')

#     ax.get_yaxis().set_major_formatter(
#     mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

#     ax.set_xticks(range(len(scenario)))
#     ax.set_xticklabels(scenario, rotation=45)

#     for i, bar in enumerate(bars): 
#         if value[i] > 0:
#             ax.text(bar.get_x() + bar.get_width()/2, bottom[i] + value[i]*1.01, int(value[i]), ha='center', va='bottom', color='black')
#         else:
#             ax.text(bar.get_x() + bar.get_width()/2, bottom[i]+value[i]*1.1, int(value[i]), ha='center', va='top', color='black')

#     if fname is not None:
#         myformat(ax)
#         mysave(fig, fname)

# plot_waterfall_steel(df, 'plt_waterfall.png')

if __name__ == "__main__":  
    print('hi')
    plot_waterfall_domestic_content(df,'plt_waterfall.png')