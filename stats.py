import scipy.stats as stats

def one_way_anova(df):
    mentions_diff = df['Mentions-Diff-(-1,1)']
    change_HL = df['Change-HL-(-1,1)']
    Anova_vals = df['Anova_Vals']

    return stats.f_oneway(mentions_diff, change_HL)