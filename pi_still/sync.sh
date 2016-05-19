ssh pi "rm -rf test && mkdir test && killall python"
rm result/*
rsync -r ./ pi:test/
ssh pi "cd test && python ./piStill.py"
rsync -r  pi:test/result/ ./result/
