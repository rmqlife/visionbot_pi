folder="test"
ssh pi "rm -rf ${folder} && mkdir ${folder} && killall python"
rm result/*
rsync -r ./ pi:$folder/
ssh pi "cd test && python ./${1}"
rsync -r  pi:$folder/result/ ./result/
