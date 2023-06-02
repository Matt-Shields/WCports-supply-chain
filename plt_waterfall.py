import pandas as pd
import matplotlib as mpl
from plot_routines import initFigAxis, myformat, mysave

df = pd.read_excel('waterfall chart calculations_test.xlsx', sheet_name = 'domestic_content')

def plot_waterfall_domestic_content(df, fname):
    fig, ax = initFigAxis(figx=20, figy=10)

    scenario = df['scenario'].to_list() 
    value = df['value'].to_list() 

    bottom = [0] * 8
    for i in range (1,5):
        bottom[i] = bottom[i-1] + value[i-1]
    bottom[6] = value[5]

    c=['#3498DB']*8
    for i in [1,2,3,4,6]:
        if value[i]>0: 
            c[i]='#F1C40F'
        else:
            c[i]='#27AE60'

    scenario = scenario[:5] + scenario[6:]
    value = value[:5] + value[6:]
    bottom = bottom[:5] + bottom[6:]
    c = c[:5] + c[6:]

    bars = ax.bar(scenario,value,bottom=bottom,color=c, width=0.7)
    ax.set_title('A West Coast scenario could be cost competitive to the South East Asia supply chain \nconsidering Domestic Content Benefits and Reduced Transportation Costs')

# Cost Comparison of US West Coast and Southeast Asia Supply Chains: \nAnalysing the Impact of Domestic Content Benefits and Reduced Transportation Costs
# A West Coast scenario could be cost competitive to the South East Asia supply chain \nconsidering Domestic Content Benefits and Reduced Transportation Costs
    ax.set_ylim(0, 3500)
    ax.set_ylabel('Manufacturing Cost ($/kW)')

    ax.get_yaxis().set_major_formatter(
        mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    ax.set_xticklabels(scenario, rotation=45)

    for i, bar in enumerate(bars): 
        if value[i] > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bottom[i] + value[i]*1.01, int(value[i]), ha='center', va='bottom', color='black')
        else:
            ax.text(bar.get_x() + bar.get_width()/2, bottom[i]+value[i]*1.1, int(value[i]), ha='center', va='top', color='black')

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

if '__name__' == '__main__':
    plot_waterfall_domestic_content(df,'plt_waterfall.png')