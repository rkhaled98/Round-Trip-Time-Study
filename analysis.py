import matplotlib.pyplot as plt
import numpy as np

import statsmodels.api as sm
from scipy import stats
import collections

import os

def main():
    vals = get_values()
    #create_plot_all(savefig = True)
    #create_plot_cdf(showfig = True)
    #create_plot_cdf(showfig = True, day = "2018-02-11 Sunday")
    #create_plot_cdf(showfig = True, day = "2018-02-12 Monday")
    #create_plot_cdf(showfig = True, day = "2018-02-13 Tuesday")
    create_plot_cdf(site = "www.google.com", xlim = 100, showfig = True)
    create_plot_cdf(site = "www.google.com", xlim = 100, day = "2018-02-11", showfig = True)
    create_plot_cdf(site = "www.google.com", xlim = 100, day = "2018-02-12", showfig = True)
    create_plot_cdf(site = "www.google.com", xlim = 100, day = "2018-02-13", showfig = True)
    create_plot_cdf(site = "www.google.com", xlim = 100, day = "2018-02-14", showfig = True)
    create_plot_cdf(site = "www.google.com", xlim = 100, day = "2018-02-16", showfig = True)
    create_plot_cdf(site = "www.google.com", xlim = 100, day = "2018-02-17", showfig = True)
    create_plot_cdf(site = "www.google.com", xlim = 100, day = "2018-02-18", showfig = True)


#the purpose of this function is to create
#a separate log file for each website in the
#directory folder logs.
def makeFiles():
    f = open('aggregatelog.txt', 'r')
    website_logs = collections.defaultdict(list)
    for line in f.readlines():
        values = line.split(',')
        sitename = values[1].replace("https://", "").replace("/", "-")
        time = values[0]
        RTT = values[-3].replace('\n','')
        RTTstwo = values[-2].replace('\n','')
        pRTT = values[-1].replace('\n','')

        if sitename != 'sitename':
            website_logs[sitename].append((time, RTT, RTTstwo, pRTT))

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
            line = "%s,%s,%s,%s\n" % (RTT[0],RTT[1],RTT[2], RTT[3])
            f.writelines(line)

    f.close()

def get_values(site = "aggregatelog.txt", day = ""):
    #by default, if this function gets no parameters,
    #then it will do an aggregate log. But if the user
    #specifies a specific website, then it will
    #go get values for that site.
    if site != "aggregatelog.txt":
        f = open(get_location(site))
    else:
        f = open("aggregatelog.txt", 'r')
    pR = []
    RTTs = []
    RTTv2s = []

    for line in f.readlines():
        values = line.split(',')
        if day == "" :
            RTTs.append(values[-3].replace('\n',''))
            RTTv2s.append(values[-2].replace('\n',''))
            pR.append(values[-1].replace('\n',''))
        elif day[:10] in values[0]:
            RTTs.append(values[-3].replace('\n',''))
            RTTv2s.append(values[-2].replace('\n',''))
            pR.append(values[-1].replace('\n',''))


    pR = [x for x in pR if x.replace('.','',1).isdigit()]
    RTTs = [x for x in RTTs if x.replace('.','',1).isdigit()]
    RTTv2s = [x for x in RTTv2s if x.replace('.','',1).isdigit()]

    f.close()
    return (RTTs, RTTv2s, pR)

def get_location(site):
    cwd = os.getcwd()
    return cwd + '/logs/' + site

#the purpose of this function is to
#cast each value in the array to a float
#and then add this to a new array,
#which is returned. it doesn't
#actually do any sorting, but this
#should be added??
def sort_and_cast(arr):
    new_arr = []
    for val in arr:
        try:
            f_val = (float(val))
            new_arr.append(f_val)
        except:
            print('error')

    return new_arr

def create_plot_all(savefig = False, showfig = False):
    wd = os.getcwd() + "/logs/"
    sites = os.listdir(wd)
    create_plot_cdf()
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


def create_plot_cdf(site = "aggregatelog.txt", xlim = 1000, savefig = False, showfig = False
, day = ""):
    #a is a sorted list of RTTs
    #y is a sorted list of second load RTTs
    #d is a sorted list of ping RTTs

    vals = get_values(site, day)

    a = sort_and_cast(vals[0])
    y = sort_and_cast(vals[1])
    d = sort_and_cast(vals[2])

    plt.plot(np.sort(a), np.linspace(0, 1, len(a), endpoint=False))
    plt.plot(np.sort(d), np.linspace(0, 1, len(d), endpoint=False))
    plt.plot(np.sort(y), np.linspace(0, 1, len(y), endpoint=False))
    plt.xlabel('RTT (ms)')
    plt.ylabel('CDF')
    if site == 'aggregatelog.txt':
        plt.title('Aggregate CDF for RTTs of the top 100 websites (%i) on %s'
        % (len(a) + len(y) + len(d), day))
    else:
        plt.title('CDF for RTTs of %s (%i) on %s'
        % (site, len(a) + len(y) + len(d), day))
    plt.legend(['TTFB - PRET', 'ping RTT', 'TTFB - PRET 2ND LOAD'])
    ax1 = plt.subplot(111)
    ax1.set_xlim([0, xlim])
    ax1.grid(color='#C0C0C0', linestyle='-', linewidth=1,)
    plt.savefig('graphs/CDF OF RTTs ' + site.replace('www.','') + '.png') if savefig else {}
    plt.show() if showfig else {plt.close()}
    return ax1


makeFiles()
main()
