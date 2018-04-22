import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from scipy import stats
import collections

import os
import re # reg ex

def main():
    #makeFiles()
    #clean_csv('www.google.com', day=['2018-03-25', '2018-03-24'])
    #clean_csv(show_hours = True)
    create_plot_temporal_v(site = "aggregate", show_hours = True)
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

def clean_csv(site = "aggregate", day = ['all'], show_hours = False):
# get the important variables into the dataFrame. For specific site or aggregate,
# and also return only specific days in the dataframe if specified other than 'all'
    df = pd.read_csv("aggregate.txt")
    df = df.loc[:, ['tstamp', 'sitename', 'RTT', 'RTTtwo', 'RTTthree', 'pingRTT']]
    df = df if site == "aggregate" else df[df.sitename.str.match('^' + site + '$')] #regex for getting the exact site if specified
    #df = df if day == ['all'] else df[df.tstamp.str.contains('|'.join([x for x in day])) if len(day) > 1 else df.tstamp.str.contains(day[0])] #this line isolates specific days as specified by the array day otherwise it shows all the days if default value of ['all'] is used for days
    df = df[~df.pingRTT.str.match("None")]
    df.pingRTT.apply(lambda val: float(val))
    df.pingRTT = df.pingRTT.astype('float64')
    if show_hours:
        df.tstamp = df.tstamp.apply(lambda val: convert_tstamp_to_hour(val))
        print(df)
        '''
        d = []
        #df = df.loc[:, ['tstamp', 'RTTtwo']]
        for x in range(0, 25, 1):
            hour = "0" + str(x) if x < 10 else str(x)
            d[hour] = df[df.tstamp.str.contains('.*\s' + hour)]
        return d
        '''


    '''
    df_hours = pd.DataFrame(columns=[str(x) for x in range(0,25,1)])
    print(df_hours)
    for i in range(0, 25, 1):
        hour = "0" + str(i) if i < 10 else str(i)
        print(hour)
        df_hours[str(i)] = df[df.tstamp.str.contains('.*\s' + hour)] # + ':\d\d:\d*$')
        print(df_hours["0"])
        '''
    #f = open('dataframe_out', 'w')
    #f.write(df.to_csv())
    return df
#t
def convert_tstamp_to_hour(tstamp):
    p = re.compile('(2018-03-\d\d) ((\d\d).*)') # group 3 contains the hour
    m = p.match(tstamp)
    hour = m.group(3)
    return hour


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

def create_plot_all(savefig = False, showfig = False, day = ['all']):
    wd = os.getcwd() + '/logs/' # this is where to get the files
    sites = os.listdir(wd) # the list of sites in the directory
    create_plot_cdf(site = "aggregate", showfig = showfig, savefig = savefig)
    for site in sites:
        f = open(wd + site) # open individual site
        create_plot_cdf(site, showfig, savefig)

def create_plot_cdf(site, showfig = False, savefig = False, day = ['all'], show_hours = False):
    data = clean_csv(site, show_hours)
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

def create_plot_temporal(site, showfig = True, savefig = False, day = ['all'], show_hours = True):
    data = clean_csv(site, show_hours = True)
    #data = dict(data)
    #print(data)
    for key, value in data.iteritems():
        df = data[key]
        _ = plt.plot(np.sort(df['RTTtwo']), np.linspace(0, 1, len(df['RTTtwo']), endpoint=False))
    _ = plt.ylabel('ECDF')
    _ = plt.legend([key for key, value in data.iteritems()])
    ax1 = plt.subplot(111)
    ax1.set_xlim([0, 1000])
    plt.show() if showfig else {plt.close()}

def create_plot_temporal_v(site = "aggregate", day = ['all'], show_hours = True):
    dataf = clean_csv(site, show_hours = True)
    sns.set_style("whitegrid")
    ax1 = plt.subplot(111)
    #x_i = [key for key, value in data.iteritems()]
    #y_i = [data[key] for key, value in data.iteritems()]
    ax1 = sns.violinplot(x = 'tstamp', y = 'RTTtwo', data = dataf)
    plt.show()

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
