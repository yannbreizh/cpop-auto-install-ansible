#!/bin/bash

echo "Gather information on data disk (RAID5 volume)..."
echo "`date` - Gather information on data disk (RAID5 volume)..." >> $logfile
echo "Output of 'fdisk -l':"
fdisk -l

datadisk="sdb"
newdatadisk=$datadisk
while [ "$Rep0" != 'y' ];
do
  read -p "Data disk is sdb, is that right? (y/n) " Rep0
  if [ "$Rep0" = 'n' ]
  then
    read -p "Please specify the data disk: " newdatadisk
    echo -e "\033[31mYou said data disk is $newdatadisk, are you sure? (y/n) \033[0m \c"
    read Rep0
  fi
done
datadisk=$newdatadisk

echo "Start data disk configuration..."
sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | fdisk /dev/$datadisk
  g # create a new empty GPT partition table
  n # add a new partition
  1 # partition number 1
    # first sector - use default: start at beginning of disk (sector 2048)
    # last sector - use default: extend partition to end of disk
  w # write the partition table
  q # and we're done
EOF
datapart="$datadisk""1"
mke2fs -t ext4 /dev/$datapart
mountpoint="/mnt/data/"
mkdir $mountpoint
echo "/dev/$datapart $mountpoint ext4 defaults 0 2" >> /etc/fstab
echo -e "[  \033[1m\033[32mOK\033[0m  ] disk config"
