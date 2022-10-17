# Self-organizing-hop-network
在 Raspberry Pi 中使用自組織跳點網路
***
## Step1. Raspberry Pi Update
```shell
$ sudo apt update
$ sudo apt install dkms git
$ sudo apt-get update
$ sudo apt upgrade
$ sudo apt-get dist-upgrade
```
## Step2. Wifi dongle tp-link archer T2U plus AC600 driver install
這一步驟是因為
```shell
$ cd AC600/
$ sudo rm /var/lib/dpkg/lock-frontend 
$ sudo rm /var/lib/dpkg/lock
$ sudo dpkg -i *.deb
$ cd rtl8812au/
$ sudo make dkms_install
$ reboot
$ sudo dkms status
$ ifconfig
```

