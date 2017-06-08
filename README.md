# SequoiaStacking

Script to combine any 3 spectral bands from the Parrot Sequoia into an RGB false color composite using OpenCV3 and the extra contributor packages in Python 3.x

This script is prepared by Tyler Pubben and is licensed under the MIT license framework.
It is free to use and distribute however please reference http://www.tjscientific.com or my 
GIT repository at https://github.com/tpubben/SequoiaStacking/

TO USE:

1. Install your preferred Python 3.x distribution. You need the following libraries:
    a. OpenCV3.4 with the contrib packages for SIFT (keep in mind, SIFT is a patented algorithm. Please do not place this into a commercial        software package.
    b. numpy
2. Copy all of the Parrot Sequioa individual band images into a single folder.
3. Create an output folder where you want your composite images to be saved.
4. Run the script - the way you do this varies based on OS and installation. If you don't know how to run a Python script from terminal I
   suggest you look at an introductory Python course.
5. When the script prompts you for which band you want in each channel keep in mind that channel 1 == blue, channel 2 == green and channel    3 == red in the false color composite.
6. Enter the full path to the output and input folders. eg. "C:\Users\<username>\inputFolder" the quotes are not necessary.
7. Let it run, it can take a while (I'm not great at optimizing code).

Enjoy.
    
