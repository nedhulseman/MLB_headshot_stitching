# MLB_headshot_stitching
This project uses Beautiful Soup to iterate through all MLB teams, and their rosters to obtain each player's headshot.
It then chops the images up into pieces, and trains a convolutional neural network to peice the images back together. 

Author: Ned Hulseman
Date: 8/16/2018

# There are 3 scripts in this repository:
   1. getImages  -- This class is implements BeautifulSoup, requests, re and urllib. Its goal is to simply locate the MLB headshots
   2. createData -- This class implements getImages, numpy, PIL, time and pickle and actually creates a full data set. An observation
                    consists of 2 images stitched together and a label that states whether or not these images actually go together
   3. train nn  -- not added yet
   4. demonstration of the model using tkinter? -- not added yet

