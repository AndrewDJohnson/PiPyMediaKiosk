
#Remove uneeded modules to free up about 1.5GB so this would fit on a 4GB card.
 sudo apt-get remove coinor-libcbc3 coinor-libcgl1 coinor-libclp1 coinor-libcoinmp1:armhf coinor-libcoinutils3 coinor-libosi1 cups-bsd dc debian-reference-common debian-reference-en dpkg-dev epiphany-browser epiphany-browser-data fakeroot fontconfig-infinality fonts-droid fonts-roboto freepats galculator geany-common gettext-base git git-man gnome-desktop3-data gnupg-agent groff-base gsfonts gsfonts-x11 gstreamer1.0-omx gstreamer1.0-plugins-base gtk2-engines-clearlookspix gvfs-common hdparm idle idle-python2.7 idle-python3.4 idle3 imagemagick imagemagick-common info java-common liba52-0.7.4 libaa1 libabw-0.1-1 libarchive13:armhf libasan1:armhf libasprintf0c2 libass5 libassuan0:armhf libatomic1:armhf libavahi-glib1:armhf libavahi-gobject0:armhf libavc1394-0 libbasicusageenvironment0 libbluetooth3:armhf libbluray1:armhf libboost-atomic1.55.0:armhf libboost-filesystem1.55.0:armhf libboost-program-options1.55.0:armhf libboost-regex1.55.0:armhf libboost-system1.55.0:armhf libboost-thread1.55.0:armhf libc-ares2:armhf libcddb2 libchromaprint0 libcolamd2.8.0:armhf libcupsfilters1:armhf libcupsimage2:armhf libcwiid1 libdc1394-22 libdca0 libdjvulibre-text libdjvulibre21:armhf libdrm-amdgpu1:armhf libdrm-freedreno1:armhf libdrm-nouveau2:armhf libdrm-radeon1:armhf libdv4 libdvbpsi9:armhf libe-book-0.1-1 libebml4:armhf libelf1:armhf libetpan17:armhf libfaad2 libfakeroot:armhf libffi5:armhf libfftw3-single3 libflite1 libfreerdp-cache1.1:armhf libfreerdp-client1.1:armhf libfreerdp-codec1.1:armhf libfreerdp-common1.1.0:armhf libfreerdp-core1.1:armhf libfreerdp-crypto1.1:armhf libfreerdp-gdi1.1:armhf libfreerdp-locale1.1:armhf libfreerdp-primitives1.1:armhf libfreerdp-rail1.1:armhf libfreerdp-utils1.1:armhf libgd3:armhf libgl1-mesa-dri:armhf libgnome-desktop-3-10 libgoa-1.0-0b:armhf libgoa-1.0-common libgpgme11:armhf libgphoto2-6:armhf libgphoto2-port10:armhf libgroupsock1 libgs9 libgs9-common libgstreamer-plugins-bad1.0-0 libgtkglext1 libiec61883-0 libijs-0.35:armhf libilmbase6 libimobiledevice4:armhf libiso9660-8 libjbig2dec0 libkate1 libksba8:armhf liblircclient0 liblivemedia23 libllvm3.7:armhf liblqr-1-0:armhf  liblzo2-2:armhf libmagickcore-6.q16-2:armhf libmagickwand-6.q16-2:armhf libmatroska6:armhf libmimic0 libmjpegutils-2.1-0 libmms0 libmodule-build-perl libmotif-common libmozjs185-1.0 libmpcdec6:armhf libmpeg2-4:armhf libmpeg2encpp-2.1-0 libmpg123-0 libmplex2-2.1-0 libmtp-common libmtp9:armhf libnetpbm10 libofa0 libopencv-calib3d2.4 libopencv-contrib2.4 libopencv-core2.4 libopencv-features2d2.4 libopencv-flann2.4 libopencv-highgui2.4 libopencv-imgproc2.4 libopencv-legacy2.4 libopencv-ml2.4 libopencv-objdetect2.4 libopencv-video2.4 libopenexr6 liborcus-0.8-0 libpaper1:armhf libpisock9 libplist2:armhf libpod-latex-perl libpoppler46:armhf libpostproc52 libproxy-tools libpth20:armhf libqscintilla2-11 libqt4-network:armhf libqt4-xmlpatterns:armhf libqtwebkit4:armhf libraw1394-11 libreoffice-base libreoffice-base-core libreoffice-base-drivers libreoffice-calc libreoffice-math libreoffice-writer libresid-builder0c2a librtimulib-dev librtimulib-utils librtimulib7 libruby1.9.1 libruby2.1:armhf libsbc1 libscsynth1 libshine3:armhf libshout3 libsidplay2 libsoundtouch0 libspandsp2 libsrtp0 libswscale3 libtag1-vanilla libtag1c2a libtcl8.5:armhf libtk8.5:armhf libtxc-dxtn-s2tc0:armhf libubsan0:armhf libudisks2-0:armhf libupnp6 libusageenvironment1 libusbmuxd2:armhf libv8-3.14.5 libva-drm1:armhf libva-x11-1:armhf libvcdinfo0 libvlc5 libvlccore8 libvncclient0:armhf libvo-aacenc0 libwebrtc-audio-processing-0 libwildmidi-config libwildmidi1 libwinpr-crt0.1:armhf libwinpr-crypto0.1:armhf libwinpr-dsparse0.1:armhf libwinpr-environment0.1:armhf libwinpr-file0.1:armhf libwinpr-handle0.1:armhf libwinpr-heap0.1:armhf libwinpr-input0.1:armhf libwinpr-interlocked0.1:armhf libwinpr-library0.1:armhf libwinpr-path0.1:armhf libwinpr-pool0.1:armhf libwinpr-registry0.1:armhf libwinpr-rpc0.1:armhf libwinpr-sspi0.1:armhf libwinpr-synch0.1:armhf libwinpr-sysinfo0.1:armhf libwinpr-thread0.1:armhf libwinpr-utils0.1:armhf libwmf0.2-7:armhf libwnck-3-0:armhf libwnck-3-common libwps-0.3-3 libxcb-composite0:armhf libxcb-keysyms1:armhf libxcb-randr0:armhf libxcb-xv0:armhf libxfce4util-common libxfce4util6 libxfconf-0-2 libxm4:armhf libyaml-0-2:armhf libzbar0 libzvbi-common libzvbi0:armhf lxkeymap make man-db minecraft-pi netsurf-common netsurf-gtk omxplayer patch penguinspuzzle perl-modules poppler-data powermgmt-base pulseaudio python-gobject python-pifacecommon python-pifacedigitalio python-serial python-xklavier python3-gi python3-numpy python3-picamera python3-pifacecommon python3-pifacedigital-scratch-handler python3-pifacedigitalio python3-pil python3-serial raspberrypi-artwork raspi-config realvnc-vnc-server realvnc-vnc-viewer rsync rtkit ruby1.9.1 scratch sgml-base smartsim sonic-pi tcl8.5 tk8.5 triggerhappy udisks2 vlc vlc-data wolfram-engine xml-core xpdf 
pip install python-uinput 
sudo apt-get install socat
mkdir rpimpv && cd rpimpv
wget https://awesome.nwgat.ninja/deb/mpv/mpv_0.20.0_armhf.deb https://awesome.nwgat.ninja/deb/mpv/libass_0.13.3-1_armhf.deb https://awesome.nwgat.ninja/deb/mpv/ffmpeg_3.1.3-1_armhf.deb
sudo dpkg -i *.deb
sudo apt-get -f install
sudo apt-get -f install
sudo apt-get install libluajit-5.1
#wget https://awesome.nwgat.ninja/deb/mpv/mpv.conf -O $HOME/.config/mpv/mpv.conf


#grab python file from somewhere
#wget something
#Create the startup file for LXDE Pi
echo #@lxpanel --profile LXDE-pi > .config/lxsession/LXDE-pi/autostart
echo @pcmanfm --desktop --profile LXDE-pi >> .config/lxsession/LXDE-pi/autostart
echo @xscreensaver -no-splash >> .config/lxsession/LXDE-pi/autostart
echo #@point-rpi >> .config/lxsession/LXDE-pi/autostart

echo @sudo python pi-ppt-play.py >> .config/lxsession/LXDE-pi/autostart
#Set some paramaters for mpv player
echo vo=rpi:background=yes > .config/mpv/mpv.conf 
echo ytdl-format=best >> .config/mpv/mpv.conf 
sudo cp  .config/mpv/mpv.conf /root/.config/mpv/mpv.conf 
#Add python uinput to modules list to load at boot.
sudo echo uninput >> /etc/modules
#Delete folders used to build and install the mpv player
sudo rm -r build
sudo rm -r rpimpv
