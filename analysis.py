import matplotlib.pyplot as plt
import numpy as np

import statsmodels.api as sm
from scipy import stats
import collections

import os

def main():
    vals = get_values()

    create_plot_cdf()

    valsgoog = get_values(site = "www.google.com")
    create_plot_cdf(site = "www.google.com", xlim = 100)

    '''
    create_plot_specific_site("www.google.com",100)
    create_plot_specific_site("bet365.com-en-",200)
    create_plot_specific_site("www.imgur.com",40)
    create_plot_specific_site("www.mail.ru",400)
    create_plot_specific_site("www.github.com",150)
    create_plot_specific_site("www.yahoo.com",150)
    create_plot_specific_site("www.ok.ru",400)
    create_plot_specific_site("www.instagram.com",150)
    create_plot_specific_site("www.tripadvisor.com", 150)
    create_plot_specific_site("www.reddit.com", 150)
    '''

#the purpose of this function is to create
#a separate log file for each website in the
#directory folder logs.
def makeFiles():
    f = open('aggregatelog.txt', 'r')
    website_logs = collections.defaultdict(list)
    for line in f.readlines():
        values = line.split(',')
        sitename = values[1].replace("https://", "").replace("/", "-")
        RTT = values[-3].replace('\n','')
        RTTstwo = values[-2].replace('\n','')
        pRTT = values[-1].replace('\n','')

        if sitename != 'sitename':
            website_logs[sitename].append((RTT, RTTstwo, pRTT))

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
            line = "%s,%s,%s\n" % (RTT[0],RTT[1],RTT[2])
            f.writelines(line)

    f.close()

def get_values(site = "aggregatelog.txt"):
    if site != "aggregatelog.txt":
        f = open(get_location(site))
    else:
        f = open("aggregatelog.txt", 'r')
    pR = []
    RTTs = []
    RTTv2s = []

    for line in f.readlines():
        values = line.split(',')
        pR.append(values[-1].replace('\n',''))
        RTTs.append(values[-3].replace('\n',''))
        RTTv2s.append(values[-2].replace('\n',''))

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

def create_plot_cdf(site = "aggregatelog.txt", xlim = 1000):
    #a is a sorted list of RTTs
    #d is a sorted list of ping RTTs
    #y is a sorted list of second load RTTs

    vals = get_values(site)

    a = sort_and_cast(vals[0])
    d = sort_and_cast(vals[2])
    y = sort_and_cast(vals[1])

    plt.plot(np.sort(a), np.linspace(0, 1, len(a), endpoint=False))
    plt.plot(np.sort(d), np.linspace(0, 1, len(d), endpoint=False))
    plt.plot(np.sort(y), np.linspace(0, 1, len(y), endpoint=False))
    plt.xlabel('RTT (ms)')
    plt.ylabel('CDF')
    plt.title('RTTs of top 100 websites and CDF')
    plt.legend(['TTFB - PRET', 'ping RTT', 'TTFB - PRET 2ND LOAD'])
    ax1 = plt.subplot(111)
    # fig, ax = plt.subplots()
    # ax.set_xlim([0,2000])
    ax1.set_xlim([0, xlim])
    plt.show()
    return ax1

def create_plot_specific_site(site, limx):
    RTTsite = get_rtts_site(site)
    b = sort_and_cast(RTTsite)
    pRTTsite = get_prtts_site(site)
    c = sort_and_cast(pRTTsite)
    RTTtwosite = get_rttstwo_site(site)
    z = sort_and_cast(RTTtwosite)
    a = sort_and_cast(b)#rtt
    d = sort_and_cast(c)#ping rtt
    y = sort_and_cast(z)#rtt two

    '''
    average = np.average(a)
    sdev = np.std(a)
    print(average)
    print(np.std(a))
    plt.plot(np.sort(a), np.linspace(0, 1, len(a), endpoint=False))
    plt.xlabel('RTT (ms)')
    plt.ylabel('CDF')
    plt.title('RTTs of ' + site + ' vs CDF')
    #ax1 = plt.subplot(111)
    # fig, ax = plt.subplots()
    # ax.set_xlim([0,2000])
    #ax1.set_xlim([average-(sdev), average+(sdev)])
    plt.show()
    '''
    plt.title('RTTs of ' + site + ' vs CDF')
    plt.plot(np.sort(a), np.linspace(0, 1, len(a), endpoint=False))
    plt.plot(np.sort(d), np.linspace(0, 1, len(d), endpoint=False))
    plt.plot(np.sort(y), np.linspace(0, 1, len(y), endpoint=False))
    plt.xlabel('RTT (ms)')
    plt.ylabel('CDF')
    #plt.title('RTTs of top 100 websites and CDF')
    plt.legend(['TTFB - PRET w/pyCurl', 'ping RTT', 'TTFB - PRET 2ND LOAD'])
    ax1 = plt.subplot(111)
    # fig, ax = plt.subplots()
    # ax.set_xlim([0,2000])
    ax1.set_xlim([0, limx])
    plt.show()

    return ax1



makeFiles()
main()
