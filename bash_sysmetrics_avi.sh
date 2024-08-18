#!/bin/bash

#1. Identify the system's public IP.
publicip () {
	ip=$(curl -s ifconfig.co -4)
	if [ "$ip" != "" ]; then
	echo "Your Public IP is: $ip"
	else
	echo 'There are problems with your network connection. please retry.'
	sleep 10
	fi
}
#2. Identify the private IP address assigned to the system's network interface.
privateip () {
	pip=$(ifconfig eth0 | grep -w inet | awk '{print $2}')
	echo "Your private IP address is: $pip"
	sleep 10
}

#3 Get the default gateway for the router
dgateway () {
	dg=$(ip route | grep default | awk '{print $3}')
	echo "Your default gateway is $dg"
	sleep 10
}

#4. Display the MAC address 
macad () {
	mid=$(ifconfig eth0 | grep -w ether | awk '{print $2}')
	echo "Your MAC address is: $mid"
	sleep 10
}

#5. Display the percentage of CPU usage for the top 5 processes.
cpusage () {
	cid=$(ps -eo pid,comm,%cpu --sort=-%cpu | head -6)
	echo "Your top 5 processes by % of CPU use are:"
	echo "$cid"
	sleep 10
}

#6. Display memory usage statistics: total and available memory.
memstat () {
	tm=$(free -h | grep Mem | awk '{print $2}')
	am=$(free -h | grep Mem | awk '{print $7}')
	um=$(free -h | grep Mem | awk '{print $3}')
	echo "Total memory: $tm"
	echo "Available memory: $am"
	echo "Used Memory: $um"
	sleep 10
}

	
#7. List active system services with their status.
asysser () {
	asys=$(systemctl list-units --type=service --state=active | awk '{print $1,$2,$4,$5}' | column -t)
	echo 'Active system services:'
	echo "$asys"
	sleep 10
}
		
	
#8. Locate the Top 10 Largest Files in /home.
lfiles () {
	lf=$(find /home -type f -exec du -h {} + | sort -rh | head -10)
	echo 'Largest files in /home:'
	echo "$lf"
	sleep 10
}

all () {
publicip
privateip
dgateway
macad
cpusage
memstat
asysser
lfiles
}

echo "Welcome to System Info Checker"
echo "You are running $(uname -v | awk '{print $4,$5,$6}')"

main () {
	read -p "What do you want to check?
	1. Public IP
	2. Private IP
	3. Default gateway
	4. MAC Address
	5. CPU Usage
	6. Memory Usage
	7. Active System Service
	8. 10 Largest files in /home
	9. View All
	Press Enter"
	
}
while true; do
main
read -p "Enter your choice: " userinput
echo
case "$userinput" in
1) publicip
;;
2) privateip
;;
3) dgateway
;;
4) macad
;;
5) cpusage
;;
6) memstat
;;
7) asysser
;;
8) lfiles
;;
9) all
;;
*) echo "Invalid option entered, Exiting"
break
;;
esac
read -n 1 -srp "Press any key to continue"
echo
done



	



