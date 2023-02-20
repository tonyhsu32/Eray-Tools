#!/bin/bash

host=127.0.0.1
port=27017
authDB=admin
db=test
user=root
pwd=80661707
collections=test_data
input_folder="/home/eray/Documents/xml_2_json/小揚_20220428_xml_2_json/q1_json/"

for file in $(ls $input_folder) 
do
	echo ""${input_folder}""${file}""
  	mongoimport --host $host --port $port -u $user -p $pwd --authenticationDatabase $authDB --collection $collections --db $db --file ${input_folder}${file}
done


