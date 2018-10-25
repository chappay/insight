# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 19:41:30 2018
Title: Insight Data Engineering Challenge
Description: Data extraction and analysis of H1B Census Data
@author: Sebastian Jayaraj, (c) 2018

# Desired output
TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
SOFTWARE DEVELOPERS, APPLICATIONS;6;60.0%
ACCOUNTANTS AND AUDITORS;1;10.0%
COMPUTER OCCUPATIONS, ALL OTHER;1;10.0% 
COMPUTER SYSTEMS ANALYST;1;10.0%
DATABASE ADMINISTRATORS;1;10.0%
"""

def getData(filename):
  """ Reading H1B CSV files """
  sep = ';'
  occupations = {}
  states = {}
  total_certified = 0
  
  # get Indexes for required fields - 'STATUS', 'LCA_CASE_EMPLOYER_STATE', 'LCA_CASE_SOC_NAME'
  firstline = open(filename).readline()
  firstline = firstline.split(';')

  for i in firstline:
      if 'STATUS' in i:
          statusIndex = firstline.index(i)
      if 'EMPLOYER_STATE' in i:
          stateIndex = firstline.index(i)
      if 'SOC_NAME' in i:
          occupIndex = firstline.index(i)
  
  for line in open(filename):   
    row = line.split(sep)
    status = row[statusIndex].strip()
    status = status.upper()
    state = row[stateIndex].strip()
    state = state.upper()
    socname = row[occupIndex].strip()
    socname = socname.upper()

    # categorizing the data into dictionaries
    if status == 'CERTIFIED':
        if occupations.has_key(socname): # OCCUPATIONS
            tmpsoc = occupations[socname]
            tmpsoc +=1
            occupations[socname] = tmpsoc
        else:
            occupations[socname] = 1 
        if states.has_key(state):# STATES
            tmpsoc = states[state]
            tmpsoc +=1
            states[state] = tmpsoc
        else:
            states[state] = 1 
        total_certified +=1

  return occupations, states, total_certified

def getOccupationStatistics(occupations, total_certified, topcount):
    """ Generate custom statistics - Occupations """
    sep = ';'
    # get top occupations using heapq
    from heapq import nlargest
    top_hits = nlargest(topcount, occupations, key=occupations.get)
    # print to file top certified occupations
    f = open('../output/top_10_occupations.txt', 'w')
    print >>f, 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    for i in top_hits:
        percent = (float(occupations[i])/total_certified)*100
        print >>f, i + sep + str(occupations[i]) + sep + str("%.1f" % percent) + '%' 
    f.close()
    return top_hits

def getStateStatistics(states, total_certified, topcount):
    """ Generate custom statistics - States """
    sep = ';'
    # get top occupations using heapq
    from heapq import nlargest
    top_hits = nlargest(topcount, states, key=states.get)
    # print to file top states
    f = open('../output/top_10_states.txt', 'w')
    print >>f, 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    for i in top_hits:
        percent = (float(states[i])/total_certified)*100
        print >>f, i + sep + str(states[i]) + sep + str("%.1f" % percent) + '%' 
    f.close()
    return top_hits



# Testing
#filename = 'H1B_Sample_2014.csv' # sample 100
#filename = 'h1b_test.csv'
#filename = 'H1B_FY_2016.csv' # real data

topcount = 10
#test = getData(filename)
#occ_stats = getOccupationStatistics(test[0], test[2], topcount)
#state_stats = getStateStatistics(test[1], test[2], topcount)


import sys, getopt

def main(argv):
   inputfile = ''
   
   try:
       inputfile = argv[1]
       test = getData(inputfile)
       occ_stats = getOccupationStatistics(test[0], test[2], topcount)
       state_stats = getStateStatistics(test[1], test[2], topcount)
   except:
       print 'Please enter the H1B input file name'
       sys.exit(1)  # abort


if __name__ == "__main__":
   main(sys.argv)



