export DISPLAY=:1
Xvfb :1 -screen 0 1920x1080x16 -fbdir /var/tmp &
sleep 1

exec gnome-session &

nohup python -u main.py &
