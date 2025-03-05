#!/usr/bin/python

###############  Execute this script as below ###################
### python fetch_exec_time.py <LOCAL_DIR_PATH> <OUTPUT_FILE_NAME> #########
### Ex:- python fetch_exec_time.py /home/cdp/metrics-path/tpcds-100G/Benchmarking /home/cdp/metrics-path/tpcds-100G/query_exec_tpcds_100G.csv ####

import os
import json
import sys

#Local Path where the metrics(json) files are present
print("Local Metrics path (Input): " + sys.argv[1] )

#Final csv filename and its location. This contains the query exec time
print("Output Directory: " + sys.argv[2] )

input_dir =  sys.argv[1]
output_dir = sys.argv[2]

output_dict = dict()

file_list = os.listdir(input_dir)
fp = open(output_dir+"default.csv", 'w')
header="Query_Name" + " , " + "Query_Execution_Time" + " , " + "Query_Result"
fp.write(header)
fp.write('\n')

for i in range(1 , len(file_list) ):
   if "json" in file_list[i] and "config" not in file_list[i]:
       print(file_list[i])
       file_path =  input_dir + "/" + file_list[i]
       jsonFile = open(file_path, 'r')
       values = json.load(jsonFile)
       query_name = values[ len(values) - 1]['data']['execution_timer']['query_name']
       query_execution_time = values[ len(values) - 1]['data']['execution_timer']['execution_time_in_ms']/1000.0
       query_result = values[ len(values) - 1]['data']['result']
       if query_name in output_dict:
           value = output_dict[query_name]
           value = value + "," + str(query_execution_time)
           output_dict[query_name] = value
       else:
           output_dict[query_name] = str(query_execution_time)
       final_content = query_name + " , " + str(query_execution_time) + " , " +  query_result
       fp.write(final_content)
       fp.write('\n')

fp.close()

with open(output_dir+"updated.csv", 'w') as updated_file:
    updated_file.write("Query_Name, QET1, QET2, QET3, QET4, QET5")
    updated_file.write('\n')
    for k,v in output_dict.items():
        line = k + "," + v
        updated_file.write(line)
        updated_file.write('\n')

print("Script execution completed successfully.")
