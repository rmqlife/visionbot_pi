ssh pi "rm -rf webcam"
rsync -r ./ pi:webcam
ssh pi "cd webcam && killall python && python app.py"

