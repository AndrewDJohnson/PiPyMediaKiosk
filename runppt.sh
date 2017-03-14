slide_delay=$1
window_name="LibreOffice*"
#ppt_file="Collapse of Towers.ppt"
#ppt_path="Desktop/PPTTest/"
advance_slide="xvkbd -window \"LibreOffice 4.3\" -delay $slide_delay -text \" \""
echo "Delay = $slide_delay, Window Name=$window_name"
#soffice --nologo --norestore --show "Desktop/PPTTest/WTC Thermite.ppt" &
soffice --nologo --norestore --show "$2" &
#soffice --nologo --norestore --show "Desktop/PPTTest/NPC.ppt" &
#xvkbd -window Libre* -delay 2000 -text " " 2>&1 | grep -m 1 "no such"
echo "Waiting for PPT to load in $window_name"
#    cmd_result=$(xvkbd -window $window_name -delay $slide_delay -text " " 2>&1 | grep -m 1 "no such")
#    echo "Result is $cmd_result"

#exit
xvkbd -text "\x2000 \y2000"
cmd_result="?"
while [[ ! -z  $cmd_result  ]]
do 
    #echo "Result was $cmd_result... Waiting 5 secs"
    sleep 1
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

    result2=$(xdotool search --name "LibreOffice 4.3")
    cmd_result=$result2
	
    
done

echo "PPT Unloaded now."
killall soffice.bin
#CD to file directory
#.~lock.Collapse of Towers.ppt#
sudo rm  -f media/PPT/.~*#


#until $advance_slide 2>&1 | grep -m 1 "no such"; do sleep .1 ; done
