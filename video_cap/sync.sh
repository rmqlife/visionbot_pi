ssh pi "rm -rf video && mkdir video"
rsync -r ./ pi:video/
ssh pi "cd video && ./cam.sh"
rsync -r pi:video/ ./
