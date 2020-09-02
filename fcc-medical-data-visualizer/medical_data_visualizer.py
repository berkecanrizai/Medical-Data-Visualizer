import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")


df["overweight"] = (df["weight"] / (df["height"] / 100)**2).apply(lambda v:0 if v<25
else 1)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["cholesterol"] = df["cholesterol"].apply(lambda v:0 if v==1 else 1)
#if else doesnt work for some reason ////
#if df["gluc"]==1:
 # df["gluc"]=0
#else:
 # df["gluc"]=1

df["gluc"] = df["gluc"].apply(lambda v:0 if v==1 else 1) 
# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=["cholesterol", "gluc","smoke","alco","active","overweight"])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature.
    df_cat["total"]=1
    df_cat=df_cat.groupby(["variable","cardio","value"],as_index=False).count()

    # Draw the catplot with 'sns.catplot()'
    dr=sns.catplot(x="variable", y="total", hue="value", data=df_cat,col="cardio",kind = 'bar')

    fig=dr.fig

    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df["ap_lo"]<=df["ap_hi"])&(df["height"]>=df["height"].quantile(0.025))&(df["height"]<=df["height"].quantile(0.975))&(df["weight"]>=df["weight"].quantile(0.025))&(df["weight"]<=df["weight"].quantile(0.975))]

    # Calculate the correlation matrix
    corr =df_heat.corr()

    # Generate a mask for the upper triangle
    # mask = np.triu(np.ones_like(corr, dtype=np.bool))
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True


    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))
    # Draw the heatmap with 'sns.heatmap()'

    ax=sns.heatmap(corr, mask=mask, vmax=.25,fmt=".1f", center=0,square=True, linewidths=.5, cbar_kws={"shrink": .45,"format":"%.2f"},vmin=-0.1,annot=True)


    fig.savefig("heatmap.png")
    return fig
