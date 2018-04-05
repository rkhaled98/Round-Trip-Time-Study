import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from scipy import stats
import collections

import os

def main():
    #makeFiles()
    #clean_csv('www.google.com', day=['2018-03-25', '2018-03-24'])
    clean_csv('www.google.com')
    #create_plot_cdf(site = "aggregate", showfig = True)
    #create_plot_all(savefig = True)
    #create_plot_all(showfig = True)
    #create_plot_cdf(showfig = True, day = "2018-02-11 Sunday")
    #create_plot_violin(site = "aggregate")
    #create_plot_violin("www.taobao.com")
    #create_plot_cdf(showfig = True, savefig = True)
    #create_plot_cdf(showfig = True, day = "2018-02-13 Tuesday")
    #create_plot_cdf(site = "www.google.com", showfig = True)
    #create_plot_cdf(site = "www.google.com", showfig = True)

def clean_csv(site = "aggregate", day = ['all']):
# get the important variables into the dataFrame. For specific site or aggregate
    df = pd.read_csv("aggregate.txt")
    df = df.loc[:, ['tstamp', 'sitename', 'RTT', 'RTTtwo', 'RTTthree', 'pingRTT']]
    df = df if site == "aggregate" else df[df.sitename.str.match('^' + site + '$')] #regex for getting the exact site if specified
    df = df if day == ['all'] else df[df.tstamp.str.contains('|'.join([x for x in day])) if len(day) > 1 else df.tstamp.str.contains(day[0])] #this line isolates specific days as specified by the array day otherwise it shows all the days if default value of ['all'] is used for days
    df = df[~df.pingRTT.str.match("None")]
    df.pingRTT.apply(lambda val: float(val))
    df.pingRTT = df.pingRTT.astype('float64')
    f = open('dataframe_out', 'w')
    f.write(df.to_csv())
    return df

def makeFiles(file = "aggregate.txt"):
#the purpose of this function is to create
#a separate log file for each website in the
#directory folder logs.
    wd = os.getcwd() # this is where to get the files
    data = clean_csv() # get the values from the aggregate
    sites = data.sitename.unique() # get the unique sitenames
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

def create_plot_cdf(site, showfig = False, savefig = False, day = ['all']):
    data = clean_csv(site)
    data = data.loc[:, ['RTT', 'RTTtwo', 'RTTthree', 'pingRTT']] # only want the relevant columns in dataframe
    y = np.arange(1, len(data.RTT)+1) / len(data.RTT)
    for col in data.columns:
        _ = plt.plot(np.sort(data[col]), np.linspace(0, 1, len(data[col]), endpoint=False))
    _ = plt.ylabel('ECDF')
    _ = plt.legend(['ping RTT', 'TTFB - PRET', 'TTFB - PRET 2ND LOAD', 'TTFB - PRET 3RD LOAD'])
    ax1 = plt.subplot(111)
    total = [data[x] for x in data]
    xlim_max = np.percentile(total, 97.5)
    ax1.set_xlim([0, xlim_max])
    plt.savefig('graphs/CDF-of-' + site.replace('www.','') + '.png') if savefig else {}
    plt.show() if showfig else {plt.close()}

def create_plot_violin(site = "aggregate", day = ""):
    data = clean_csv(site)
    data = data.loc[:, ['RTT', 'RTTtwo', 'RTTthree', 'pingRTT']]
    sns.set_style("whitegrid")
    sns.violinplot(data=data)
    ax1 = plt.subplot()
    total = [data[x] for x in data]
    ylim_max = np.percentile(total, 97.5)
    ax1.set_ylim([0, ylim_max])
    plt.show()

main()
