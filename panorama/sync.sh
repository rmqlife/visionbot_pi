rsync -r ./ pi:panorama/
ssh pi "cd panorama && rm ./*.jpg && python panorama.py"
rm ./*.jpg
rsync -r pi:panorama/ ./
