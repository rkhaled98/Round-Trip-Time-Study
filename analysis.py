import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from scipy import stats
import collections

import os

def main():
    #clean_csv(site = "www.google.com")
    #create_plot_cdf(site = "aggregate", showfig = True)
    #vals = get_values()
    #create_plot_all(savefig = True)
    create_plot_all(showfig = True)
    #create_plot_cdf(showfig = True, day = "2018-02-11 Sunday")
    #create_plot_violin(site = "aggregate")
    #create_plot_violin()
    #create_plot_cdf(showfig = True, savefig = True)
    #create_plot_cdf(showfig = True, day = "2018-02-13 Tuesday")
    #create_plot_cdf(site = "www.google.com", showfig = True)
    #create_plot_cdf(site = "www.google.com", showfig = True)

def clean_csv(site = "aggregate"):
# get the important variables into the dataFrame. For specific site or aggregate
    df = pd.read_csv("aggregate.txt")
    df = df.loc[:, ['tstamp', 'sitename', 'RTT', 'RTTtwo', 'RTTthree', 'pingRTT']]
    df = df[df.sitename.str.match('^' + site + '$')] if site != "aggregate" else df #regex for getting the exact site if specified
    df = df[~df.pingRTT.str.match("None")]
    df.pingRTT.apply(lambda val: float(val))
    df.pingRTT = df.pingRTT.astype('float64')
    f = open('dataframe_out', 'w')
    f.write(df.to_csv())
    #for col in df.columns:
    #    print(df[col])
    return df

def makeFiles(file = "aggregate.txt"):
#the purpose of this function is to create
#a separate log file for each website in the
#directory folder logs.
    wd = os.getcwd() # this is where to get the files
    data = clean_csv() # get the values from the aggregate
    sites = data.sitename.unique() # get the unique sitenames
    print(sites)
    for site in sites: # for each site
        f = open(wd + '/logs/' + site, 'w') # create new file with sitename in logs
        f.write(data[data.sitename.str.match('^' + site + '$')].to_csv()) # and write site specific data

def create_plot_all(savefig = False, showfig = False):
    wd = os.getcwd() + '/logs/' # this is where to get the files
    sites = os.listdir(wd) # the list of sites in the directory
    create_plot_cdf(site = "aggregate", showfig = showfig, savefig = savefig)
    for site in sites:
        f = open(wd + site) # open individual site
        create_plot_cdf(site, showfig, savefig)


def create_plot_cdf(site, showfig = False, savefig = False):
    data = clean_csv(site)
    data = data.loc[:, ['RTT', 'RTTtwo', 'RTTthree', 'pingRTT']] # only want the relevant columns in dataframe
    y = np.arange(1, len(data.RTT)+1) / len(data.RTT)
    for col in data.columns:
        _ = plt.plot(np.sort(data[col]), np.linspace(0, 1, len(data[col]), endpoint=False))
    _ = plt.ylabel('ECDF')
    _ = plt.legend([ 'ping RTT', 'TTFB - PRET', 'TTFB - PRET 2ND LOAD', 'TTFB - PRET 3RD LOAD'])
    ax1 = plt.subplot(111)
    total = [data[x] for x in data]
    xlim_max = np.percentile(total, 97.5)
    ax1.set_xlim([0, xlim_max])
    plt.savefig('graphs/CDF-of-' + site.replace('www.','') + '.png') if savefig else {}
    plt.show() if showfig else {plt.close()}

def create_plot_violin(site = "aggregate", day = ""):
    vals = clean_csv(site)
    sns.set_style("whitegrid")

    vals = vals.loc[:, ['RTT', 'RTTtwo', 'RTTthree', 'pingRTT']]
    #tips = sns.load_dataset(vals)
    ax = plt.subplot(111)
    ax = sns.violinplot(data=vals)
    #total =
    ax.set_ylim([0, 1000])
    plt.show()
    '''
    vals = get_values(site, day)

    RTTv3 = sort_and_cast(vals[0])
    RTT = sort_and_cast(vals[1])
    RTTv2 = sort_and_cast(vals[2])
    pR = sort_and_cast(vals[3])

    sns.set_style("whitegrid")
    #tips = sns.load_dataset(RTTv3)



    ax = plt.subplot(111)

    total = [x for x in RTTv3] #+ [x for x in RTT] + [x for x in RTTv2] + [x for x in pR]
    perc = np.percentile(total, 95)

    ax.set_xlim([0, perc])


    ax = sns.violinplot(x=RTTv3)
    plt.show()

    return ax
    '''

makeFiles()
main()
