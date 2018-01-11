#!/bin/bash
source_path="/opis/ftp/users/opis"
backup_path="/opis/ftp/temp"
cd $source_path
ftp_31_days_old_files=$(find -type f -mtime +31 | sed 's/.//')
today_date=$(date "+%d-%m-%Y")
echo "$ftp_31_days_old_files" >> "$backup_path/"ftp_31_days_old_files_$today_date
file_name=$(ls "$backup_path/"ftp_31_days_old_files_$today_date)
file_list=$(cat $file_name)
for files in $file_list
do
cp -v --parents -p $source_path$files $backup_path >> "$backup_path/"files_moved_logs_$today_date 
done
for files in $file_list
do
rm -vf $source_path$files >> "$backup_path/"files_moved_logs_$today_date
done