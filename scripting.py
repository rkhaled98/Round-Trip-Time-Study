import os

def main():
    generate_sites_from_logs_folder()

'''generate_sites_from_logs_folder
is a function that makes a list of
websites based on the logs folder'''
def generate_sites_from_logs_folder():
    wd = os.getcwd() + "/logs/"
    wdfiles = os.listdir(wd)
    f = open('sites', 'w')
    for site in wdfiles:
        f.writelines(site + '\n')
    f.close()

main()
