#!/bin/bash
cd /home/student334/CPSC334-alice-zhang
git pull
ifconfig > /home/student334/CPSC334-alice-zhang/rasp-config/ip.md


git add -A
git commit -m "upload current IP"
git push 


