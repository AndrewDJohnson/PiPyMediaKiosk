sudo pip install python-uinput

git clone https://github.com/AndrewDJohnson/PiPyMediaKiosk.git
mv PiPyMediaKiosk/* .
chmod +x runppt.sh
sudo apt-get --yes install socat qiv libluajit-5.1 xvkbd xdotool
mkdir rpimpv && cd rpimpv
wget https://awesome.nwgat.ninja/deb/mpv/mpv_0.20.0_armhf.deb https://awesome.nwgat.ninja/deb/mpv/libass_0.13.3-1_armhf.deb https://awesome.nwgat.ninja/deb/mpv/ffmpeg_3.1.3-1_armhf.deb http://mirrordirector.raspbian.org/raspbian/pool/main/h/hdf5/libhdf5-8_1.8.13+docs-15+deb8u1_armhf.deb
sudo dpkg -i *.deb
sudo apt-get --yes -f install

#Remove uneeded modules to free up about 1.5GB so this would fit on a 4GB card.
sudo apt-get --yes remove dpkg-dev epiphany-browser bluej greenfoot chromium-browser epiphany-browser-data fakeroot hdparm idle idle-python2.7 idle-python3.4 idle3 info java-common dillo claws-mail libreoffice-base libreoffice-base-core libreoffice-base-drivers libreoffice-calc libreoffice-math libreoffice-writer nodejs nodejs-legacy git-man geany-common libstdc++-4.9-dev g++ g++-4.9 debian-reference-common debian-reference-en gstreamer1.0-omx gstreamer1.0-plugins-base ruby1.9.1-examples ruby2.1 rubygems-integration squeak-plugins-scratch squeak-vm supercollider supercollider-common supercollider-ide   supercollider-language supercollider-server supercollider-supernova make man-db minecraft-pi netsurf-common netsurf-gtk omxplayer patch penguinspuzzle perl-modules poppler-data powermgmt-base pulseaudio python-gobject python-pifacecommon python-pifacedigitalio python-serial python-xklavier python3-gi python3-numpy python3-picamera python3-pifacecommon python3-pifacedigital-scratch-handler python3-pifacedigitalio python3-pil python3-serial raspberrypi-artwork raspi-config realvnc-vnc-server realvnc-vnc-viewer rsync rtkit ruby1.9.1 scratch sgml-base smartsim sonic-pi tcl8.5 tk8.5 triggerhappy udisks2 wolfram-engine xml-core xpdf wolfram-engine nodered geany

sudo rm *.deb


sudo rm /usr/share/pixel-wallpaper/*

cd ~
 
#Create the startup file for LXDE Pi
echo #@lxpanel --profile LXDE-pi > .config/lxsession/LXDE-pi/autostart
echo @pcmanfm -d --profile LXDE-pi > .config/lxsession/LXDE-pi/autostart
echo @xset -dpms >> .config/lxsession/LXDE-pi/autostart
echo @xset -s >> .config/lxsession/LXDE-pi/autostart
echo #@point-rpi >> .config/lxsession/LXDE-pi/autostart
echo @xsetroot -solid "#030303" >> .config/lxsession/LXDE-pi/autostart
echo @sudo python pi-ppt-play.py >> .config/lxsession/LXDE-pi/autostart
#Update the PCMANFM config file to disable autorun when a USB stick is inserted
#sed  -i "s/\(autorun *= *\).*/\10/" .config/pcmanfm/LXDE-pi/pcmanfm.conf
sed  -i "s/\(autorun *= *\).*/\10/" .config/pcmanfm/LXDE-pi/pcmanfm.conf
cd .config/lxsession
mkdir LXDE
cd ../pcmanfm
mkdir LXDE
cd ~
cp .config/lxsession/LXDE-pi/autostart .config/lxsession/LXDE
cp .config/pcmanfm/LXDE-pi/pcmanfm.conf .config/pcmanfm/LXDE

#Set some paramaters for mpv player 
mpv > /dev/null && sudo mpv > /dev/null
echo vo=rpi:background=yes > .config/mpv/mpv.conf 
echo ytdl-format=best >> .config/mpv/mpv.conf 
sudo cp  .config/mpv/mpv.conf /root/.config/mpv/mpv.conf 
#Add python uinput to modules list to load at boot.
sudo bash -c "echo \"uinput\" >> /etc/modules"
#Set GPUMEM
sudo bash -c "echo \"gpu_mem=128\" >> /boot/config.txt"

#Delete folders used to build and install the mpv player
sudo rm -r build
sudo rm -r rpimpv
sudo apt-get clean