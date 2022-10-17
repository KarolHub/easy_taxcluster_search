#! /usr/bin/env python3

#Importing system and regular expression support
import os, sys, re  


#======================================================================================
#              This is a basic script for assigning fly morphospecies
#                         10.10.2022 Karol Hubert Nowak 
#      Symbiosis Evolution Research Group, Jagiellonian University, Krakow, Poland
#======================================================================================


#_____________________________________How to use______________________________________
#======================================================================================

#Make a new folder, put the script, list of zotus and your .fasta_clusterlist file inside and run the script

#======================================================================================

#The input file should be a file from Emily Hartop - a file.fasta_clusterlist
#Each new line should represent an increasing level of difference threshold between the clusters 0.0, 0.1, 0.5 etc.
#Input files should be named "zotu_list.txt" and "cluster.fasta_clusterlist". Output will be later named "simple_cluster.txt"
#The output file will appear in the same folder where the input file and script are

#======================================================================================


#___________________________________Data importing____________________________________
#======================================================================================

#Path to your file/script should be automatically set as the working directory
input_path = os.path.dirname(os.path.realpath(sys.argv[0]))

#In case of a  problem, set the path manually below and comment out the previous line
#input_path = "C:\Chamber\SCRIPTS"

#======================================================================================

#Name of the input and output file in .txt format
zotu_file_name = "zotu_list.txt"
cluster_file_name = "cluster.fasta_clusterlist"
output_name = "simple_cluster.txt"

#======================================================================================


#_____________________________________Settings________________________________________
#======================================================================================

#No settings currently available for this version. If you want to change the name for the search, try changing the line #102

#======================================================================================


#OK, let's begin!


#This will import the zotu_list.txt
os.chdir(input_path)
input = open(zotu_file_name,"r")
zotu_list = []
for row in input:
    zotu_list.append(row.strip())
input.close()


#This will import the cluster.fasta_clusterlist
input = open(cluster_file_name, "r")
cluster = []
for row in input:
    cluster.append(row.strip())
input.close()


#For writing into the output file
output_file = open(os.path.join(input_path, output_name), 'w')


#======================================================================================
#                                    MAIN PART
#======================================================================================


#This will be the final string for exporting the data:
final_data=[]


for zotu in zotu_list:
#This is a batch of data for a single zotu, that will be added into the final file one by one
    final_data_part=[]
#First, which zotu are we talking about
    final_data_part.append(zotu)
    line = 0
    for lines in cluster:
#This regular expression below searches for the first zotu occurence in the row, and all the stuff between its "[" and "]" when the zotu occurs. It was a hell to make and it took two days
#It has to be this way, otherwise it's going to search for the firt "[" in a row, which is wrong - we need only the "[" right before the zotu name
        zotu_match = re.search(('\[(?:.(?!\[))+'+zotu+'\'.*?\]'), cluster[line])
        if zotu_match:
            found_zotu = zotu_match.group()
#IF YOU WANT TO SEARCH FOR A DIFFERENT NAME THAN "MORPHO", CHANGE IT HERE!
            morpho_match = re.search('\'morpho.*?\'', found_zotu)
            if morpho_match:
                found_morpho = morpho_match.group()
#Second, which difference threshold was applied to find the morpho? The bigger this number, the less likely is the similarity
                final_data_part.append(cluster[line][0:3])
#Third, which morpho was found for this zotu
                final_data_part.append(found_morpho)
#Lastly, just for the record - what was the group in which the morpho was found?
                group_match = re.search(('\d+:\s\[(?:.(?!\[))+'+zotu+'\'.*?\]'), cluster[line])
                found_group = group_match.group()
                final_data_part.append(found_group)
#Add the _part into the final list
                print('\t'.join(final_data_part))
                final_data.append('\t'.join(final_data_part))
                break
            else:
#If for a specific zotu the morpho was not found, this is going to search for the morpho in a second row -> for a higher difference threshold. If it's not found at all, it will print an error message
                line += 1
                if (line) > len(cluster)-1:
                    print('could not find morpho')
                    final_data_part.append('X')
                    final_data_part.append('morpho not found')
                    final_data_part.append(found_zotu)
                    final_data.append('\t'.join(final_data_part))
                    break
        else:
#If zotu was not found in the cluster
            print('could not find zotu')
            final_data_part.append('zotu not found')
            final_data.append('\t'.join(final_data_part))


#======================================================================================
#                             FINAL CLEANUP AND OUTPUT
#======================================================================================


#Exports each line of the final data into the file
for m in final_data:
    output_file.write(m + '\n')
