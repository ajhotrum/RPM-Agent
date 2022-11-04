# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy as np
import copy


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.grey_threshold = 254
        self.similarity_threshold = 0.0009

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        answer = -1
        
        if 'D' in problem.figures:
            #Set up figures

            image = Image.open(problem.figures['A'].visualFilename)
            image = image.convert("L")
            A = np.array(image)

            image = Image.open(problem.figures['B'].visualFilename)
            image = image.convert("L")
            B = np.array(image)

            image = Image.open(problem.figures['C'].visualFilename)
            image = image.convert("L")
            C = np.array(image)

            image = Image.open(problem.figures['D'].visualFilename)
            image = image.convert("L")
            D = np.array(image)

            image = Image.open(problem.figures['E'].visualFilename)
            image = image.convert("L")
            E = np.array(image)

            image = Image.open(problem.figures['F'].visualFilename)
            image = image.convert("L")
            F = np.array(image)
            
            image = Image.open(problem.figures['G'].visualFilename)
            image = image.convert("L")
            G = np.array(image)

            image = Image.open(problem.figures['H'].visualFilename)
            image = image.convert("L")
            H = np.array(image)

            
            #get the applicable dark pixel ratios and put them into dictionaries
            DPR_vals = {}

            DPR_vals['AB'] = self.getDPR(A, B)
            DPR_vals['AD'] = self.getDPR(A, D)
            DPR_vals['BC'] = self.getDPR(B, C)
            DPR_vals['BE'] = self.getDPR(B, E)
            DPR_vals['CF'] = self.getDPR(C, F)
            DPR_vals['DE'] = self.getDPR(D, E)
            DPR_vals['DG'] = self.getDPR(D, G)
            DPR_vals['EF'] = self.getDPR(E, F)
            DPR_vals['EH'] = self.getDPR(E, H)
            DPR_vals['GH'] = self.getDPR(G, H)
            DPR_vals['AE'] = self.getDPR(A, E)
            DPR_vals['DH'] = self.getDPR(D, H)
            DPR_vals['BF'] = self.getDPR(B, F)

            horizontal = ['AB', 'BC', 'DE', 'EF', 'GH']
            vertical = ['AD', 'DG', 'BE', 'EH', 'CF']
            diagonal = ['AE', 'DH', 'BF']

            # Go through all of the answers
            votes = np.array([0, 0, 0, 0, 0, 0, 0, 0])


            for i in range(1, 9):
                vote_count = 0
                current = str(i)
                image = Image.open(problem.figures[current].visualFilename)
                image = image.convert("L")
                current_ans = np.array(image)

                #Find DPR between answer and F/H/E
                H_DPR = self.getDPR(H, current_ans)
                F_DPR = self.getDPR(F, current_ans)
                E_DPR = self.getDPR(E, current_ans)


                #Iterate through all other relations
                for j in range(len(horizontal)):
                    if abs(H_DPR - DPR_vals[horizontal[j]]) < self.similarity_threshold:
                        vote_count = vote_count + 1
                
                for j in range(len(vertical)):
                    if abs(F_DPR - DPR_vals[vertical[j]]) < self.similarity_threshold:
                        vote_count = vote_count + 1
                
                for j in range(len(diagonal)):
                    if abs(E_DPR - DPR_vals[diagonal[j]]) < self.similarity_threshold:
                        vote_count = vote_count + 1

                
                
                votes[i-1] = vote_count


            answer = np.argmax(votes) + 1

            #print(answer)
            
        return answer



    def getDPR(self,A, B):
        
        #compute dark pixels in Image A and B
        a_total = np.sum(A < self.grey_threshold)
        b_total = np.sum(B < self.grey_threshold)

        DPR = (a_total / (33856.0)) - (b_total / (33856.0))

        return DPR