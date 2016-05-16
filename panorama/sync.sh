rsync -r ./ pi:panorama/
ssh pi "cd panorama && python panorama.py"
rsync -r pi:panorama/data* .

