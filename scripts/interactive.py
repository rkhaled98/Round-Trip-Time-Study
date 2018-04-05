import analysis
import os

getAnother = True

wd = os.getcwd() + '/logs/'
sites = os.listdir(wd)

print('Welcome. Press ENTER/RETURN at any point to exit.')
try:
    VS = input("Please specify if you would like to view images ('V'), save ('S'), or both ('VS'): ")
    showFig = True if 'V' in VS else False
    saveFig = True if 'S' in VS else False
except Exception as e:
    getAnother = False

while getAnother:
    try:
        showOptions = input("Would you like to see a list of possible websites? ('y'/'n'): ")
        showOptions = True if showOptions == 'y' else False
        if showOptions:
            print(sites)
        site = input("What site would you like to view the graph for? ('www.[SITE_NAME].[TLD]'): ")
        analysis.create_plot_cdf(site, showfig = showFig, savefig = saveFig)
    except SyntaxError as e:
        print('Goodbye.')
        getAnother = False
