ssh pi "rm -rf test && mkdir test"
rm *.avi
rsync -r ./ pi:test/
ssh pi "cd test && . ~/.profile && workon cv && python ./video_writer_pi.py"
rsync pi:test/*.avi ./
