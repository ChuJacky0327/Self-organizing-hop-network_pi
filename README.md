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
* Raspberry Pi 本身具備網卡(wlan0)，由於要做跳點網路需要地個個網路介面，因此要再添加一隻額外的 Wifi dongle。  
* 由於使用 AC600 這隻 Wifi dongle，因此需要進行這一步驟，若不是使用 AC600 或已有第二個 interface，可自行略過此步驟。  
* 參考來源與使用 : 
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
> 備註 :  
> 1. 在安裝 Driver 時，```sudo dpkg -i *.deb``` 可能要重複下指令，要確定 linux-header 有成功裝到。  
> 2. ```sudo make dkms_install``` 後的狀態要為 install，不是 add。  
> 3. 若安裝完後，```ifconfig``` 沒有 wlan1 出現，則下```sudo dkms remove xxxx/xxx --all```，在重新安裝一次。  









