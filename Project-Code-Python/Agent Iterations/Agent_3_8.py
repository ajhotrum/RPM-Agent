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
        self.dpr_similarity_threshold = 0.0005
        self.ipr_similarity_threshold = 0.2
        self.union_threshold = 150
        self.intersection_threshold = 150
        self.xor_threshold = 150

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
            A = np.where(A < self.grey_threshold, 0, 1)

            image = Image.open(problem.figures['B'].visualFilename)
            image = image.convert("L")
            B = np.array(image)
            B = np.where(B < self.grey_threshold, 0, 1)

            image = Image.open(problem.figures['C'].visualFilename)
            image = image.convert("L")
            C = np.array(image)
            C = np.where(C < self.grey_threshold, 0, 1)

            image = Image.open(problem.figures['D'].visualFilename)
            image = image.convert("L")
            D = np.array(image)
            D = np.where(D < self.grey_threshold, 0, 1)

            image = Image.open(problem.figures['E'].visualFilename)
            image = image.convert("L")
            E = np.array(image)
            E = np.where(E < self.grey_threshold, 0, 1)

            image = Image.open(problem.figures['F'].visualFilename)
            image = image.convert("L")
            F = np.array(image)
            F = np.where(F < self.grey_threshold, 0, 1)
            
            image = Image.open(problem.figures['G'].visualFilename)
            image = image.convert("L")
            G = np.array(image)
            G = np.where(G < self.grey_threshold, 0, 1)

            image = Image.open(problem.figures['H'].visualFilename)
            image = image.convert("L")
            H = np.array(image)
            H = np.where(H < self.grey_threshold, 0, 1)

            #check for unions and subtractions
            horizontal_union = self.is_union(A, B, C)
            vertical_union = self.is_union(A, D, G)
            horizontal_subtraction = self.is_subtraction(A, B, C)
            vertical_subtraction = self.is_subtraction(A, D, G)

            #check for intersections
            horizontal_intersection = self.is_intersection(A, B, C)
            vertical_intersection = self.is_intersection(A, D, G)

            #check for xor
            horizontal_xor = self.is_xor(A, B, C)
            vertical_xor = self.is_xor(A, D, G)


            if horizontal_union:
                answer = self.union_calc(G, H, problem)
                print(answer, 1)
                return answer

            if vertical_union:
                answer = self.union_calc(C, F, problem)
                print(answer, 2)
                return answer

            if horizontal_subtraction:
                answer = self.subtraction_calc(G, H, problem)
                print(answer, 3)
                return answer

            if vertical_subtraction:
                answer = self.subtraction_calc(C, F, problem)
                print(answer, 4)
                return answer

            if horizontal_intersection:
                answer = self.intersection_calc(G, H, problem)
                print(answer, 5)
                return answer
            
            if vertical_intersection:
                answer = self.intersection_calc(C, F, problem)
                print(answer, 6)
                return answer

            if horizontal_xor:
                answer = self.xor_calc(G, H, problem)
                print(answer, 7)
                return answer
            
            if vertical_xor:
                answer = self.xor_calc(C, F, problem)
                print(answer, 8)
                return answer



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

            IPR_vals = {}

            IPR_vals['AB'] = self.getIPR(A, B)
            IPR_vals['AD'] = self.getIPR(A, D)
            IPR_vals['BC'] = self.getIPR(B, C)
            IPR_vals['BE'] = self.getIPR(B, E)
            IPR_vals['CF'] = self.getIPR(C, F)
            IPR_vals['DE'] = self.getIPR(D, E)
            IPR_vals['DG'] = self.getIPR(D, G)
            IPR_vals['EF'] = self.getIPR(E, F)
            IPR_vals['EH'] = self.getIPR(E, H)
            IPR_vals['GH'] = self.getIPR(G, H)
            IPR_vals['AE'] = self.getIPR(A, E)
            IPR_vals['DH'] = self.getIPR(D, H)
            IPR_vals['BF'] = self.getIPR(B, F)

            
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
                current_ans = np.where(current_ans < self.grey_threshold, 0, 1)

                #Find DPR between answer and F/H/E
                H_DPR = self.getDPR(H, current_ans)
                F_DPR = self.getDPR(F, current_ans)
                E_DPR = self.getDPR(E, current_ans)

                #Find IPR between answer and F/H/E
                H_IPR = self.getIPR(H, current_ans)
                F_IPR = self.getIPR(F, current_ans)
                E_IPR = self.getIPR(E, current_ans)


                
                #Iterate through all other relations
                for j in range(len(horizontal)):
                    if abs(H_DPR - DPR_vals[horizontal[j]]) < self.dpr_similarity_threshold:
                        vote_count = vote_count + 1
                    if abs(H_IPR - IPR_vals[horizontal[j]]) < self.ipr_similarity_threshold:
                        vote_count = vote_count + 1
                
                for j in range(len(vertical)):
                    if abs(F_DPR - DPR_vals[vertical[j]]) < self.dpr_similarity_threshold:
                        vote_count = vote_count + 1
                    if abs(F_IPR - IPR_vals[vertical[j]]) < self.ipr_similarity_threshold:
                        vote_count = vote_count + 1
                
                for j in range(len(diagonal)):
                    if abs(E_DPR - DPR_vals[diagonal[j]]) < self.dpr_similarity_threshold:
                        vote_count = vote_count + 1
                    if abs(E_IPR - IPR_vals[diagonal[j]]) < self.ipr_similarity_threshold:
                        vote_count = vote_count + 1
                

                
                votes[i-1] = vote_count


            #answer = np.argmax(votes) + 1
            #print(votes)
            
            current_max = 0
            for i in range(len(votes)):
                if votes[i] >= current_max:
                    answer = i + 1
                    current_max = votes[i]
            

            print(answer)
            #dummy = input()
            
        return answer



    def getDPR(self,A, B):
        
        #compute dark pixels in Image A and B
        a_total = np.sum(A < 1)
        b_total = np.sum(B < 1)

        DPR = (a_total / (33856.0 * 2.0)) - (b_total / (33856.0 * 2.0))

        return DPR


    def getIPR(self,A, B):
        
        #compute intersection for Image A and B
        ab_intersection = np.sum(np.add(A, B) == 0)

        #compute union for Image A and B
        ab_union = np.sum(np.add(A, B) < 2)

        IPR = ab_intersection / (ab_union + ab_intersection)

        return IPR


    def is_union(self, A, B, C):
        union = False
        ab_union = np.sum(np.add(A, B) < 2)
        c_total = np.sum(C < 1)
        
        if abs(ab_union - c_total) < self.union_threshold:
            union = True
        
        return union

    def is_subtraction(self, A, B, C):
        subtraction = False
        c_total = np.sum(C < 1)
        a_total = np.sum(A < 1)
        b_total = np.sum(B < 1)

        ab_subtraction = abs(a_total - b_total)

        if abs(ab_subtraction - c_total) < self.union_threshold:
            subtraction = True
        
        return subtraction

    
    def is_intersection(self, A, B, C):
        intersection = False
        ab_intersection = np.sum(np.add(A, B) == 0)
        c_total = np.sum(C < 1)

        if abs(ab_intersection - c_total) < self.intersection_threshold:
            intersection = True

        return intersection


    def is_xor(self, A, B, C):
        xor = False
        ab_xor = np.sum(np.add(A, B) == 1)
        c_total = np.sum(C < 1)

        if abs(ab_xor - c_total) < self.xor_threshold:
            xor = True

        return xor


    def union_calc(self, A, B, problem):
        current_min = 100000
        current_choice = 0
        for i in range(1, 9):
            current = str(i)
            image = Image.open(problem.figures[current].visualFilename)
            image = image.convert("L")
            current_ans = np.array(image)
            current_ans = np.where(current_ans < self.grey_threshold, 0, 1)

            ab_union = np.sum(np.add(A, B) < 2)
            c_total = np.sum(current_ans < 1)
            diff = abs(ab_union - c_total)
            if diff < current_min:
                current_min = diff
                current_choice = i

        return current_choice


    
    def subtraction_calc(self, A, B, problem):
        current_min = 100000
        current_choice = 0
        for i in range(1, 9):
            current = str(i)
            image = Image.open(problem.figures[current].visualFilename)
            image = image.convert("L")
            current_ans = np.array(image)
            current_ans = np.where(current_ans < self.grey_threshold, 0, 1)


            a_total = np.sum(A < 1)
            b_total = np.sum(B < 1)

            ab_subtraction = abs(a_total - b_total)


            c_total = np.sum(current_ans < 1)
            diff = abs(ab_subtraction - c_total)
            if diff <= current_min:
                current_min = diff
                current_choice = i

        return current_choice


    def intersection_calc(self, A, B, problem):
        current_min = 100000
        current_choice = 0
        for i in range(1, 9):
            current = str(i)
            image = Image.open(problem.figures[current].visualFilename)
            image = image.convert("L")
            current_ans = np.array(image)
            current_ans = np.where(current_ans < self.grey_threshold, 0, 1)

            ab_intersection = np.sum(np.add(A, B) == 0)
            c_total = np.sum(current_ans < 1)
            diff = abs(ab_intersection - c_total)
            if diff < current_min:
                current_min = diff
                current_choice = i

        return current_choice