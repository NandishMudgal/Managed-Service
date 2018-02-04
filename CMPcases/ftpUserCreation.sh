ftpusername=$1
ftpuserpasswd=$2

# adding the user
useradd -s /bin/false -m $ftpusername
echo $ftpuserpasswd | passwd --stdin $ftpusername

# creating the dir with the user and group
su -c "mkdir /home/$ftpusername/.ssh" $ftpusername
# chown $ftpusername:$ftpusername /home/$ftpusername/.ssh

# changing the permission
chmod 700 /home/$ftpusername/.ssh

# Creating the authorized_keys file for ssh
su -c "touch /home/$ftpusername/.ssh/authorized_keys" $ftpusername
#chown $ftpusername:$ftpusername /home/$ftpusername/.ssh/authorized_keys

# changing the permission
chmod 600 /home/$ftpusername/.ssh/authorized_keys