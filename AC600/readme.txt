Install AC600's driver to JetPack 4.3

1. Delete lock file

$ sudo rm /var/lib/dpkg/lock
$ sudo rm /var/lib/dpkg/lock-frontend

2. Copy AC600 to /home/dlinano

3. Run the command to install relatived packages

$ cd AC600
$ sudo dpkg -i *.deb

4. Install 8812au driver

$ cd rtl8812au
$ sudo make dkms_install

5. reboot

$ reboot

6. check dkms

$ dkms status

>> 8812au, 5.6.4.2_35491.20191025, 4.9.140-tegra, aarch64: installed

