rsync -r ./ pi:webcam
ssh pi "cd webcam && python app.py"

