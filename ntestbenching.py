import matplotlib.pyplot as plt
import numpy as np

import statsmodels.api as sm
from scipy import stats
import collections


'''
per site cdf vs rtt
compare ping with pycurl

'''

def main():
    RTTs = get_rtts_log()
    pR = get_ping_rtts_log()
    RTTstwo = get_rtts_two_log()

    print("printing sorted ping rtts")
    print(np.sort(pR))
    #RTTsite = get_rtts_site("www.google.com")
    print("printing sorted rtts")
    print(np.sort(RTTs))
    #create the generalized plot of all the websites
    create_plot2(RTTs, pR, RTTstwo)


    #create_plot_specific_site("www.google.com",100)
    #   create_plot_specific_site("bet365.com-en-",200)
    #create_plot_specific_site("www.imgur.com",40)
    #create_plot_specific_site("www.mail.ru",400)
    #create_plot_specific_site("www.github.com",150)
    #create_plot_specific_site("www.yahoo.com",150)
    #create_plot_specific_site("www.ok.ru",400)
    #create_plot_specific_site("www.instagram.com",150)

#the purpose of this function is to create
#a separate log file for each website in the
#directory folder logs.
def makeFiles():
    f = open('xxnlog.txt', 'r')
    website_logs = collections.defaultdict(list)
    for line in f.readlines():
        values = line.split(',')
        sitename = values[1].replace("https://", "").replace("/", "-")
        RTT = values[-3]
        RTTstwo = values[-2]
        pRTT = values[-1]

        if sitename != 'sitename':
            website_logs[sitename].append((RTT, pRTT, RTTstwo))

    f.close()
    #will go through the sites
    for site in website_logs.keys():
        #creates a
        #f = open("/logs/" + site, 'w')
        f = open("C:\\Users\\delah\\PycharmProjects\\untitled1\logs\\" + site, 'w')
        #will add each RTT to a log
        '''
        RTT = website_logs[site]
        for tuple in RTT:
            f.writelines(RTT[0])
            f.writelines(',')
            f.writelines(RTT[1])
            f.writelines(',')
            f.writelines(RTT[2])
            '''
        for RTT in website_logs[site]:
            #f.writelines(RTT[0] + ',\n' + RTT[1] + ',\n' + RTT[2])
            line = "%f,%f,%f" % (RTT[0],RTT[1],RTT[2])



    '''
    d['js'].append({'foo', 'bar'})
    d['js'].append({'other', 'thing'})
    print(d)
    '''
    f.close()

def get_ping_rtts_log():
    f = open("xnlog.txt", 'r')
    pR = []
    for line in f.readlines():
        values = line.split(',')
        pR.append(values[-1].replace('\n',''))

    for num in pR:
        if (num == 'pingRTT\r' or num == 'pingRTT' or num == None):
            pR.remove(num)
        elif (num == ''):
            pR.remove('')
    f.close()
    return pR

def get_rtts_two_log():
    f = open("xxnlog.txt", 'r')
    RTTstwo = []
    for line in f.readlines():
        values = line.split(',')
        RTTstwo.append(values[-2].replace('\n', ''))

    for num in RTTstwo:
        if (num == 'RTTtwo\r' or num == 'RTTtwo'):
            RTTstwo.remove(num)
        elif (num == ''):
            RTTstwo.remove('')
    # RTTs.remove('')
    f.close()
    return RTTstwo

#will parse through the log.txt file and get the RTTs of all the website
#in the new iteration of the file the rtt is the third value
#and the rtt two is the second.
def get_rtts_log():
    f = open("xnlog.txt", 'r')
    RTTs = []
    #will only get the RTTs of each website
    for line in f.readlines():
        values = line.split(',')
        RTTs.append(values[-3].replace('\n', ''))

    for num in RTTs:
        if (num == 'RTT\r' or num == 'RTT'):
            RTTs.remove(num)
        elif (num == ''):
            RTTs.remove('')
    # RTTs.remove('')
    f.close()
    return RTTs


def get_location(site):
    return "C:\\Users\\delah\\PycharmProjects\\untitled1\logs\\" + site


#gets RTTs of a specific website using the specific log file of that
#site in the logs directory...
def get_rtts_site(site):
    f = open(get_location(site), 'r')
    RTTs = []
    #will only get the RTTs of each website
    for line in f.readlines():
        #values = line.split(',')
        RTT = line.split(',')[0]
        RTTs.append(RTT)

    f.close()
    return RTTs

def get_prtts_site(site):
    f = open(get_location(site), 'r')
    pRTTs = []
    for line in f.readlines():
        pRTT = line.split(',')[1]
        pRTTs.append(pRTT)
    f.close()
    return pRTTs

def get_rttstwo_site(site):
    f = open(get_location(site), 'r')
    rttstwo = []
    for line in f.readlines():
        rttstwo = line.split(',')[2]
        rttstwo.append(pRTT)
    f.close()
    return rttstwo

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

def create_plot2(b, c, z):
    #b is a list of RTTs
    #c will be ping RTT
    #a is a sorted list of RTTs
    #d is a sorted list of ping RTTs

    a = sort_and_cast(b)
    d = sort_and_cast(c)
    y = sort_and_cast(z)
    print(a)
    #prints out vals in sorted list of RTTs
    print("now printing vals:")
    for val in np.sort(a):
        print(val)

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
    ax1.set_xlim([0, 1000])
    plt.show()
    return ax1

def create_plot_specific_site(site, limx):
    RTTsite = get_rtts_site(site)
    b = sort_and_cast(RTTsite)
    pRTTsite = get_prtts_site(site)
    c = sort_and_cast(pRTTsite)
    RTTtwosite = get_rttstwo_site()
    z = sort_and_cast(RTTtwosite)
    a = sort_and_cast(b)#rtt
    d = sort_and_cast(c)#ping rtt
    y = sort_and_cast(z)#rtt two

    #print(a)
    #print("now printing vals:")
    #for val in np.sort(a):
    #    print(val)
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






#misc code

    #for time in pR:
    #    if time is "None":
    #        pR.remove(time)
    #L = [x for x in pR if x is not None]
    #filter(None, L)
    #filter('None', L)
    #f = open('PINGLOGNUMBERS','w')
    #for v in L:
    #    f.write(v + '\n')

'''
    def create_plot4(sample):
        quantiles, idx = np.unique(sample, return_inverse=True)
        counts = np.bincount(idx)
        # a normal distribution with a mean of 0 and standard deviation of 1
        n = stats.norm(loc=0, scale=1)

        # draw some random samples from it
        sample = n.rvs(100)

        # compute the ECDF of the samples
        ecdf = sm.distributions.ECDF(sample)
        qe, pe = ecdf(sample)

        # evaluate the theoretical CDF over the same range
        q = np.linspace(qe[0], qe[-1], 1000)
        p = n.cdf(q)

        # plot
        fig, ax = plt.subplots(1, 1)
        ax.hold(True)
        ax.plot(q, p, '-k', lw=2, label='Theoretical CDF')
        ax.plot(qe, pe, '-r', lw=2, label='Empirical CDF')
        ax.set_xlabel('Quantile')
        ax.set_ylabel('Cumulative probability')
        ax.legend(fancybox=True, loc='right')

        plt.show()
'''
