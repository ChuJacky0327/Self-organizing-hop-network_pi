# Self-organizing-hop-network
在 Raspberry Pi 中使用自組織跳點網路，實現畫面協作共享  
#### 模擬情景 :  
車輛所看到的畫面要進行畫面共享給後方車輛，但距離過遠無法進行傳輸，需透過中間節點進行協作  
pig-r1 和 pig-r3 因為距離過遠無法直接通訊，因此運用跳點網路先將數據傳給 pig-r2，在由 pig-r2 傳輸給 pig-r3，以此這三個節點將會形成**自組織跳點網路，只有這自組織內的節點能夠相互溝通**
> 以下為範例圖 :  

![image](https://github.com/ChuJacky0327/Self-organizing-hop-network/blob/main/HopNetwork.jpg)
***
## Step1. Raspberry Pi Update
```shell
$ sudo apt update
$ sudo apt install dkms git
$ sudo apt-get update
$ sudo apt upgrade
$ sudo apt-get dist-upgrade
$ git clone https://github.com/ChuJacky0327/Self-organizing-hop-network.git
$ cd Self-organizing-hop-network
```
***
## Step2. Wifi dongle tp-link archer T2U plus AC600 driver install
* Raspberry Pi 本身具備網卡(wlan0)，由於要做**跳點網路**需要第二個網路介面，因此要再添加一隻額外的 Wifi dongle(wlan1)。  
* 由於使用 AC600 這隻 Wifi dongle，因此需要進行這一步驟，若不是使用 AC600 或已有第二個 interface，可自行略過此步驟。  
* 參考來源與使用 : [https://blog.cavedu.com/2021/05/13/tp-link-archer-t2u-plus-ac600/](https://blog.cavedu.com/2021/05/13/tp-link-archer-t2u-plus-ac600/)
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
* ifconfig 後若有兩個 interface (wlan0)(wlan1)，即完成。  
### 備註 :  
> 1. 在安裝 Driver 時，```sudo dpkg -i *.deb``` 可能要重複下指令，要確定 **linux-header** 有成功裝到。  
> 2. ```sudo make dkms_install``` 後的狀態要為 install，不是 add。  
> 3. 若安裝完後，```ifconfig``` 沒有 wlan1 出現，則下```sudo dkms remove xxxx/xxx --all```，在重新安裝一次。  
***
## Step3. Raspberry Pi AP model
將 wlan1 改成 AP model。
```shell
$ sudo apt install gedit
$ sudo apt install hostapd dnsmasq -y
$ sudo systemctl stop dnsmasq
$ sudo systemctl stop hostapd
$ sudo gedit /etc/dhcpcd.conf
```
**將 dhcpcd.conf 裡的內容改成 :**
```
interface wlan1
    static ip_address=192.168.51.1/24
    nohook wpa_supplicant
```
> ip address 可自行設定為 192.168.xx.1  

&emsp;
```shell
$ sudo service dhcpcd restart
$ sudo gedit /etc/dnsmasq.conf
```
**將 dnsmasq.conf 裡的內容改成 :**
```
interface=wlan1
bind-interfaces 
server=8.8.8.8
domain-needed
bogus-priv
dhcp-range=192.168.51.2,192.168.51.20,24h
```
> interface 要設定為變更成 AP model 的那個網卡  

&emsp;
```shell
$ sudo gedit /etc/hostapd/hostapd.conf
```
**將 hostapd.conf 裡的內容改成 :**
```
ctrl_interface=/var/run/hostapd
ctrl_interface_group=0
interface=wlan1
driver=nl80211
ssid=pig-r1
hw_mode=a
channel=44
ieee80211ac=1
ieee80211n=1
wmm_enabled=0
macaddr_acl=0
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=relay10327
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```
> ssid 為無線網路名稱(可自行設定)
> wpa_passphrase 為無線網路的密碼(可自行設定)  

&emsp;
```shell
$ sudo gedit /etc/default/hostapd
```
**文件中找到以下字據並修改成 :**
```
DAEMON_CONF="/etc/hostapd/hostapd.conf
```
```shell
$ sudo systemctl unmask hostapd
$ sudo systemctl enable hostapd
$ sudo systemctl unmask hostapd
$ sudo systemctl restart dnsmasq
$ sudo gedit /etc/rc.local 
```
**往下找到 exit 0，並在該行的上方輸入下列內容 :**
```
sudo systemctl unmask hostapd
sudo systemctl restart dnsmasq
```
```shell
$ reboot
```
> 最後要```reboot```設定才會生效 
***
## Step4. RTMP & OpenCV install
* 因為本專案是進行影像畫面的共享傳輸，因此需要安裝 RTMP 串流協定和 OpenCV。
* 需安裝 nginx-1.16.0 和 ffmpeg。
```shell
$ git clone https://github.com/arut/nginx-rtmp-module.git
$ wget http://nginx.org/download/nginx-1.16.0.tar.gz
$ tar zxvf nginx-1.16.0.tar.gz 
$ sudo apt-get install build-essential libpcre3 libpcre3-dev libssl-dev libopencv-dev 
$ cd nginx-1.16.0/
$ ./configure --add-module=../nginx-rtmp-module
$ make
$ sudo make install
$ sudo gedit /usr/local/nginx/conf/nginx.conf
```
**將 nginx.conf 裡的內容新增下段**
```
rtmp {
	server {
		listen 1935;
		ping 30s;
		notify_method get;
		application rtmp {
			live on;
		}
	}
     }
```
```shell
$ sudo /usr/local/nginx/sbin/nginx
$ sudo apt install -y ffmpeg
$ sudo apt install python3-dev
$ sudo pip3 install --upgrade pip
$ pip3 install -U opencv-python
```
### 備註 :  
> 1. Raspberry Pi 開機時，要下```sudo /usr/local/nginx/sbin/nginx```，啟動 nginx 服務。
> 2. 在網頁輸入```localhost```，即可得知 nginx 有無啟動。
***
## Step5. Test and Demo
Raspberry 事先先開好 camera 功能，將 Webcam 接上 Rasberry Pi，使用```ls /dev/video*```，即可得知攝影機是否有接上。
### 測試 Webcam 能否使用 :
```shell
$ python3 cam_test.py
```
### 跳點網路影像傳輸 DEMO :
#### pig-r1:
* pig-r1 連上 pig-r2 的 AP 網路，可下```ifconfig```查看 ip address
* 只有 pig-r1 接上攝影機，將 pig-r1 所看到的畫面推到 RTMP 的 nginx 上
```shell
$ python3 RTMP_push-relay1.py
```
#### pig-r2:
* pig-r2 連上 pig-r3 的 AP 網路，可下```ifconfig```查看 ip address
* pig-r2 去拉 pig-r1 所傳輸的影像畫面，並保存
* 將 pig-r2 所保存的影像推到 RTMP 的 nginx 上
```shell
$ python3 RTMP_pull-relay2.py
$ python3 RTMP_push-relay2.py
```
#### pig-r3:
* pig-r3 去拉 pig-r2 所傳輸的影像畫面
```shell
$ python3 RTMP_pull-relay3.py
```
***
即此完成自組織跳點網路的影像畫面共享傳輸
