ssh pi "killall python && rm -rf test && mkdir test"
rm result/*
rsync -r ./ pi:test/
ssh pi "cd test && python ./video_writer_pi.py"
rsync -r  pi:test/result/ ./result/
