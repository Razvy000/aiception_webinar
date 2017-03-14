# run 'raspistill' with no args in bash to see all the options

import subprocess

subprocess.call("raspistill --output image.jpg", shell=True)

# subprocess.call("raspistill -w 400 -h 300 --roi 0.45,0.4,0.3,0.3" +
#                 "--nopreview --vflip --hflip --timeout 1000 --output image.jpg",
#                 shell=True)
