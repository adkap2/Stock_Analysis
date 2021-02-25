import scipy.stats as stats
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# def one_way_anova(df):
#     mentions_diff = df['Mentions-Diff-(-1,1)']
#     change_HL = df['Change-HL-(-1,1)']
#     Anova_vals = df['Anova_Vals']

#     return stats.f_oneway(mentions_diff, change_HL)

def one_sample_ttest(df):
    return stats.ttest_1samp(df['Anova_Vals'], 0.5)

def probability_of_res_plot(model):
    fig = plt.figure(figsize= (10, 10))
    ax = fig.add_subplot(111)
    normality_plot, stat = stats.probplot(model.resid, plot= plt, rvalue= True)
    ax.set_title("Probability plot of model residual's", fontsize= 20)
    ax.set
    plt.show()

def plot_correlation_norm(symbol, df):
    df = plot_correlation_helper(df)
    fig, ax = plt.subplots()
    ax.scatter(df['Change_Norm'], df['Mentions-Diff'])
    plt.ylabel('Normalized Mentions Difference')
    plt.xlabel('Normalized Stock Day Change')
    plt.title(f"Mentions Vs daily stock price change for {symbol} normalized\n")
    plt.show(block=False)
    plt.pause(10)
    plt.close()
    figname = f"figures/{symbol}_Mentions_vs_Day_Change_Norm"
    fig.savefig(figname)

def plot_correlation_helper(result):
    result['Mentions-Diff'] = result['Mentions-Diff'].mask(result['Mentions-Diff']\
        .sub(result['Mentions-Diff'].mean()).div(result['Mentions-Diff'].std()).abs().gt(.75))
    result['Change_Norm'] = result['Change_Norm'].mask(result['Change_Norm']\
        .sub(result['Change_Norm'].mean()).div(result['Change_Norm'].std()).abs().gt(.75))
    return result
