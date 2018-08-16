from GetImages import baseballData
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import time
import pickle

'''
    author:    @Ned Hulseman
    date:      @8/16/2018
    purpose:   This scripts iterates through every MLB team, and their respective rosters and gets each players headshot.

                   The scripts takes the following steps:

                   1. Uses getImages class to iterate through the teams, and the players
                   2. Gets each players headshots, resizes to 60x90, changes image to grey-scale
                   3. Breaks apart the image into 15x15 chunks
                   4. The program will take a given chunk and compare it to each side of every other chunks
                   5. The program saves a numpy array for the image comparisons (x values) and whether the 2 stitched images actually go together

    notes:     I did not compare chunks from different images. For the purpose of implementation and to maintain simplicity, I will only compare chunks
               from the same headshot for training, testing and implementation. This could be an extension of this project.

    run time:  ROughly 20-25 minutes
'''
def getMatches():
    block_size = 15

    observations_list = []
    labels = []


    #####
    # 1 #
    #####
    
    # Creates instance of the baseballData class
    dataGetter = baseballData()


    #Iterates through each baseball team
    for team in dataGetter.getTeams().values():

        start = time.time() #simply for timing purposes to track performance

        # Iterates through each player on a team
        for player in dataGetter.getRoster(team):

            # The baseballData class is not robust enough to get every player, some
            # players names like C.C. Sabathis and J.J. Hardy throw errors
            try:
                
                dataGetter.get_headshot(player)
                
    #####
    # 2 #
    #####
                headshot = np.array(Image.open("headshot.png").convert("L").resize((60, 90)))
                    

    #####
    # 3 #
    #####
               # Iterates through each row and columns by the anchor blocks
                for row_block in range(0, headshot.shape[0], block_size ):
                        
                
                    for col_block in range(0, headshot.shape[1], block_size):

                        
                        # saves the anchor block matrix
                        anchor_block = headshot[row_block : row_block+block_size, col_block : col_block+block_size]

                        # finds each block (not counting anchor block), to compare to the anchor block
                        for comp_row_block in range(0, headshot.shape[0], block_size ):
                            
                        
                            for comp_col_block in range(0, headshot.shape[1], block_size):

                                # saves the comparison_block matrix
                                comparison_block = headshot[comp_row_block : comp_row_block+block_size, comp_col_block : comp_col_block+block_size]


                                '''
                                    Now that we have an anchor block and a comparison block, we need to figure out what to do next,
                                    depending on where the anchor block is in relation to the comparison block

                                    Once that is determined we will have the anchor block on the left and comparison on the left and compare them,
                                    Then rotate the comparison block for each side to get 4 comparisons for each anchor and comparison blocks
                                '''

    #####
    # 4 #
    #####
                                # test if the anchor block is being compared to the comparison block
                                if comp_row_block == row_block and comp_col_block == col_block:
                                    pass

                                # test if comparison is to the top
                                elif comp_row_block == row_block - block_size and comp_col_block == col_block:


                                    for rotation in range(0, 4):
                                        ob = np.concatenate((np.rot90(anchor_block, k=3), np.rot90(comparison_block, k=rotation)), axis=1)
                                        observations_list.append(ob)

                                        if rotation == 3:
                                            labels.append(1)
                                        else:
                                            labels.append(0)
                                
                                    
                                # test if comparison is to the bottom
                                elif comp_row_block == row_block + block_size and comp_col_block == col_block:


                                    for rotation in range(0, 4):
                                        ob = np.concatenate((np.rot90(anchor_block, k=1), np.rot90(comparison_block, k=rotation)), axis=1)
                                        observations_list.append(ob)

                                        if rotation == 1:
                                            labels.append(1)
                                        else:
                                            labels.append(0)
                                

                                # test if comparison is to the right
                                elif comp_row_block == row_block and comp_col_block == col_block + block_size:

        
                                    for rotation in range(0, 4):
                                        ob = np.concatenate((np.rot90(anchor_block, k=0), np.rot90(comparison_block, k=rotation)), axis=1)
                                        observations_list.append(ob)

                                        if rotation == 0:
                                            labels.append(1)
                                        else:
                                            labels.append(0)
                                

                                # test if comparison is to the left
                                elif comp_row_block == row_block  and comp_col_block == col_block - block_size:

                                    for rotation in range(0, 4):
                                        ob = np.concatenate((np.rot90(anchor_block, k=2), np.rot90(comparison_block, k=rotation)), axis=1)
                                        observations_list.append(ob)

                                        if rotation == 2:
                                            labels.append(1)
                                        else:
                                            labels.append(0)

                                # This tests if the comparison and anchor blocks are not next to eachother and therefore will never be a match
                                else:
                                     for rotation in range(0, 4):
                                        ob = np.concatenate((np.rot90(anchor_block, k=2), np.rot90(comparison_block, k=rotation)), axis=1)
                                        observations_list.append(ob)

                                        labels.append(0)
            except IndexError:
                print(player + ' headshot was not able to be found')

                            
        print('Team' + team + ':  Time:' + str(time.time() - start))
        print('')
                                    

    #####
    # 5 #
    #####
    
    # saves each np array to the local directory
    np.save('stitched_images.npy', np.array(observations_list))
    np.save('labels.npy', np.array(labels))





getMatches()















