rsync -r --delete-before ./ pi:webcam
ssh pi "cd webcam && python app.py"

