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
    #create_plot_cdf(showfig = True)
    #create_plot_cdf(showfig = True, day = "2018-02-11 Sunday")
    #create_plot_violin(site = "aggregate")
    #create_plot_violin()
    #create_plot_cdf(showfig = True, savefig = True)
    #create_plot_cdf(showfig = True, day = "2018-02-13 Tuesday")
    create_plot_cdf(site = "www.google.com", showfig = True)
    #create_plot_cdf(site = "www.google.com", showfig = True)

def clean_csv(site = "aggregate"):
# get the important variables into the dataFrame. For specific site or aggregate
    df = pd.read_csv("newtestaggregatelog.txt")
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

def makeFiles(file = "newtestaggregatelog.txt"):
    wd = os.getcwd() # this is where to get the files
    data = clean_csv()
    sites = data.sitename.unique()
    for site in sites:
        f = open(wd + '/logs/' + site, 'w')
        f.write(data[data.sitename.str.match('^' + site + '$')].to_csv())
'''
#the purpose of this function is to create
#a separate log file for each website in the
#directory folder logs.
def makeFiles():
    f = open('newtestaggregatelog.txt', 'r')
    website_logs = collections.defaultdict(list)
    for line in f.readlines():
        values = line.split(',')
        sitename = values[1].replace("https://", "").replace("/", "-")
        time = values[0]
        RTTsthree = values[-4].replace('\n','')
        RTT = values[-3].replace('\n','')
        RTTstwo = values[-2].replace('\n','')
        pRTT = values[-1].replace('\n','')

        if sitename != 'sitename':
            website_logs[sitename].append((time, RTTsthree, RTT, RTTstwo, pRTT))

    f.close()
    #will go through the sites
    for site in website_logs.keys():
        #the below gets the cwd and puts the files in
        #a folder named logs
        cwd = os.getcwd()
        f = open(cwd + '/logs/' + site, 'w')
        #will add each RTT to a log
        for RTT in website_logs[site]:
            #f.writelines(RTT[0] + ',\n' + RTT[1] + ',\n' + RTT[2])
            line = "%s,%s,%s,%s,%s\n" % (RTT[0],RTT[1],RTT[2], RTT[3], RTT[4])
            #adding time, rtts3, rtt, rttstwo, and prtt
            f.writelines(line)

    f.close()
'''
'''

def get_values(site = "newtestaggregatelog.txt", day = ""):
    #by default, if this function gets no parameters,
    #then it will do an aggregate log. But if the user
    #specifies a specific website, then it will
    #go get values for that site.
    if site != "newtestaggregatelog.txt":
        f = open(get_location(site))
    else:
        f = open("newtestaggregatelog.txt", 'r')
    RTTv3s = []
    RTTs = []
    RTTv2s = []
    pR = []
    for line in f.readlines():
        values = line.split(',')
        if day == "" :
            RTTv3s.append(values[-4].replace('\n',''))
            RTTs.append(values[-3].replace('\n',''))
            RTTv2s.append(values[-2].replace('\n',''))
            pR.append(values[-1].replace('\n',''))
        elif day[:10] in values[0]:
            RTTv3s.append(values[-4].replace('\n',''))
            RTTs.append(values[-3].replace('\n',''))
            RTTv2s.append(values[-2].replace('\n',''))
            pR.append(values[-1].replace('\n',''))


    RTTv3s = [x for x in RTTv3s if x.replace('.','',1).isdigit()]
    RTTs = [x for x in RTTs if x.replace('.','',1).isdigit()]
    RTTv2s = [x for x in RTTv2s if x.replace('.','',1).isdigit()]
    pR = [x for x in pR if x.replace('.','',1).isdigit()]

    f.close()
    return (RTTv3s, RTTs, RTTv2s, pR)

'''
def get_location(site):
    cwd = os.getcwd()
    return cwd + '/logs/' + site

def create_plot_all(savefig = False, showfig = False):
    wd = os.getcwd() + '/logs/' # this is where to get the files
    sites = os.listdir(wd) # the list of sites in the directory
    for site in sites:
        f = open(wd + site) # open individual site



def create_plot_all(savefig = False, showfig = False):
    wd = os.getcwd() + "/logs/"
    sites = os.listdir(wd)
    #create_plot_cdf()
    for site in sites:
        f = open(wd + site)
        values = []
        for line in f.readlines():
            valuesLine = line.split(',')
            for value in valuesLine:
                values.append(value)
        values = sort_and_cast(values)
        max = np.amax(values)
        perc = np.percentile(values, 95)
        create_plot_cdf(site, perc, savefig, showfig)
        print(max)
        f.close()

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
