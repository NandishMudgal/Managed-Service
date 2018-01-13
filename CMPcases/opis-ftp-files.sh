#!/bin/bash
source_path="/opis/ftp/users/opis"
log_path="/opis/ftp/temp"
backup_path="/bk-opis/backup"
cd $source_path
today_date=$(date "+%d-%m-%Y")
find -type f -mtime +31 | sed 's/.//' > "$log_path/"ftp_31_days_old_files_$today_date
file_name=$(ls "$backup_path/"ftp_31_days_old_files_$today_date)
file_list=$(cat $file_name)

for files in $file_list
do
cp -v --parents -p $source_path$files $backup_path >> "$backup_path/"files_moved_logs_$today_date 
rm -vf $source_path$files >> "$backup_path/"files_moved_logs_$today_date
done
