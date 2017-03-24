cd /home/pi

sudo rm  -f ./media/PPT/.~*#
slide_delay=$1
window_name="LibreOffice*"

echo "Delay = $slide_delay, Window Name=$window_name"
echo "Waiting for PPT to load in $window_name"

xvkbd -text "\x2000 \y2000"
cmd_result="?"
while [[ ! -z  $cmd_result  ]]
do 
    #echo "Result was $cmd_result... Waiting 5 secs"
    sleep 3
    #cmd_result=$(xdotool search --name "LibreOffice 4.3")
     cmd_result=$(xvkbd -window $window_name -delay $slide_delay -text "\[Right]" 2>&1 | grep -m 1 "no such")
    
done


echo "PPT Loaded - so Running it Now"
sleep 1
cmd_result=" "
while [[ ! -z  $cmd_result  ]]
do 
	sleep .1
    #echo "Next..."
	if [ $slide_delay != "0" ]; then
       result=$(xvkbd -window $window_name -delay $slide_delay -text "\[Right]" 2>&1 | grep -m 1 "no such")
       echo "Next..."
	fi

    cmd_result=$(xdotool search --name "LibreOffice 4.3")
    
done

echo "PPT Unloaded now."
killall soffice.bin
sudo rm  -f ./media/PPT/.~*#
