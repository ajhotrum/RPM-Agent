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
#from PIL import Image
#import numpy

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.tri_dict = {"0":"270", "90":"180", "270":"0", "180":"90"}
        self.pac_dict = {"45":"135", "315":"225", "135":"45", "225":"315"}
        self.directions = {"up":{"bottom-left":"top-left", "bottom-right": "top-right"}, "down":{"top-left":"bottom-left", "top-right": "bottom-right"},
                            "left":{"top-right":"top-left", "bottom-right":"bottom-left"}, "right":{"top-left":"top-right", "bottom-left":"bottom-right"}}

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
        all_attributes = {}

        #Set up figures
        A = problem.figures['A']
        B = problem.figures['B']
        C = problem.figures['C']

        #for each object put its name in the dict of dicts
        for object in A.objects:
            all_attributes[object]=A.objects[object].attributes

        for object in B.objects:
            all_attributes[object]=B.objects[object].attributes

        for object in C.objects:
            all_attributes[object]=C.objects[object].attributes

        #if there are multiple objects, compare them
        ab_pairs = self.match(A, B)
        ac_pairs = self.match(A, C)


        #check if there are duplicates in the matches
        if len(A.objects) > len(B.objects):
            #if there is a duplicate, find which one matches best
            for object1 in A.objects:
                for object2 in A.objects:
                    if object1 != object2:
                        if ab_pairs[object1] == ab_pairs[object2] and ab_pairs[object1] != "deleted":
                            diff1 = self.get_differences(A.objects[object1].attributes, B.objects[ab_pairs[object1]].attributes)
                            diff2 = self.get_differences(A.objects[object2].attributes, B.objects[ab_pairs[object2]].attributes)
                            
                            #make sure the one with the fewest differences is paired with the object (and vice versa) and the one with more differeces is set to deleted
                            if len(diff1) > len(diff2):
                                ab_pairs[object1] = 'deleted'
                                ab_pairs[ab_pairs[object2]] = object2
                            elif len(diff1) < len(diff2):
                                ab_pairs[object2] = 'deleted'
                                ab_pairs[ab_pairs[object1]] = object1
                            
                            #if they have the same number of differences
                            else:
                                similarities1 = 0
                                similarities2 = 0

                                #see which one has more similarities
                                for attribute, value in A.objects[object1].attributes.items():
                                    for attirbute1, value1 in B.objects[ab_pairs[object1]].attributes.items():
                                        if attribute == attirbute1 and value == value1:
                                            similarities1 = similarities1 + 1

                                for attribute, value in A.objects[object2].attributes.items():
                                    for attirbute1, value1 in B.objects[ab_pairs[object2]].attributes.items():
                                        if attribute == attirbute1 and value == value1:
                                            similarities2 = similarities2 + 1
                                
                                #make the one with the most similarities the winner
                                if similarities1 > similarities2:
                                    ab_pairs[object2] = 'deleted'
                                    ab_pairs[ab_pairs[object1]] = object1
                                else:
                                    ab_pairs[object1] = 'deleted'
                                    ab_pairs[ab_pairs[object2]] = object2


        #Get A/B and A/C differences.
        differences_ab = {}
        for object in A.objects:
            pair = ab_pairs[object]
            if pair != "deleted":
                diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                differences_ab[object] = diffs
            else:
                differences_ab[object] = 'deleted'

        differences_ac = {}
        for object in A.objects:
            pair = ac_pairs[object]
            if pair != "deleted":
                diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                differences_ac[object] = diffs
            else:
                differences_ac[object] = 'deleted'



        #Dict for the new D value coming from C
        D_C = {}
        #make same as C
        for object in C.objects:
            D_C[object] = all_attributes[object]

        #go through all objects in C and figure out what transformation their corresponding 
        # objects went through from A->B.
        to_delete = {}
        for object in D_C:
            #find matching A object
            a_pair = "none"
            for key, value in ac_pairs.items():
                if value == object:
                    a_pair = key
                    b_pair = ab_pairs[a_pair]

            #check to see if this object was added to C and does not exist in A
            if a_pair in differences_ab:
                #check if item has been deleted:
                if b_pair != 'deleted':
                    #Go through all changes in A object that happened in A->B transformation
                    for attribute_name, attribute in differences_ab[a_pair].items():
                        #fill check
                        if attribute_name == 'fill':
                            if D_C[object][attribute_name] == 'yes':
                                D_C[object][attribute_name] = 'no'
                            else:
                                D_C[object][attribute_name] = 'yes'
                        #if shape changed, change C shape to whatever B shape is
                        elif attribute_name == 'shape':                    
                            D_C[object][attribute_name] = all_attributes[b_pair][attribute_name]
                        #if shape changed, change C shape to whatever B shape is
                        elif attribute_name == 'size':
                            D_C[object][attribute_name] = all_attributes[b_pair][attribute_name]

                        elif attribute_name == "alignment":
                            #go through the directions attribute to find the pair that describes what is happening from A to B
                            for direction in self.directions:
                                for first, second in self.directions[direction].items():
                                    if all_attributes[a_pair][attribute_name] == first and all_attributes[b_pair][attribute_name] == second:
                                        #once found, record the direction
                                        ab_direction = direction
                            #Use the direction and the C starting position to set the position of D
                            for first1, second1 in self.directions[ab_direction].items():
                                if first1 == D_C[object][attribute_name]:
                                    D_C[object][attribute_name] = second1
                                        


                        
                        #if the same shape, check if angle has changed
                        if all_attributes[a_pair]['shape'] == all_attributes[b_pair]['shape']:
                            if attribute_name == 'angle':
                                #check for mirroring from A to B
                                mirrored = self.is_mirrored(all_attributes[a_pair]['angle'], all_attributes[b_pair]['angle'], all_attributes[a_pair]['shape'])

                                #if it was mirrored, get corresponding mirrored angle
                                if mirrored:
                                    if D_C[object]['shape'] == 'triangle': 
                                        new_angle = self.tri_dict[D_C[object][attribute_name]]
                                        D_C[object][attribute_name] = new_angle
                                    elif D_C[object]['shape'] == 'pac-man': 
                                        new_angle = self.pac_dict[D_C[object][attribute_name]]
                                        D_C[object][attribute_name] = new_angle
                                else:
                                    #if not mirrored, subtract the b angle from the a angle
                                    angle_b = all_attributes[b_pair][attribute_name]
                                    angle_a = all_attributes[a_pair][attribute_name]
                                    delta_angle = (int(angle_b) - int(angle_a)) 
                                    #apply the change in angle to the current D_C angle to get the final D angle
                                    new_angle = (int(D_C[object][attribute_name]) + delta_angle) % 360
                                    D_C[object][attribute_name] = str(new_angle)
                    
                        #if location, change the location
                
                else:
                    #if the object has been deleted from A to B, put this on the to-delete list after itteration.
                    to_delete[object] = object

        
        for object in to_delete:
            del D_C[object]

        #initialize min for changes
        diffs = 3

        #Loop through the answers, 
        for i in range(1, 7):
            current = str(i)
            Option = problem.figures[current]
            fig_total_diff = 0

            #if the answer has the same number of objects as the generated guess (D_C)
            if len(Option.objects) == len(D_C):
                #get the changes between the answer and the object
                for object in Option.objects:
                    #match the object with a D_C object
                    current_min = 100
                    current_match = 'H'
                    for dc_obj in D_C:
                        diff = len(self.get_differences(Option.objects[object].attributes, D_C[dc_obj]))
                        if diff < current_min:
                            current_min = diff
                            current_match = dc_obj

                    fig_total_diff = fig_total_diff + current_min            

                if fig_total_diff < diffs:
                    diffs = fig_total_diff
                    answer = i
            else:
                fig_total_diff = 100


                
        print("the answer is ", answer)
        dummy = input()

        return answer


    def is_mirrored(self, angle_A, angle_B, shape):
        mirrored = False

        #Check triangle mirroring
        if shape == 'triangle':
            if self.tri_dict[angle_A] == angle_B:
                mirrored = True

        #check pac-man mirroring
        if shape == 'pac-man':
            if self.pac_dict[angle_A] == angle_B:
                    mirrored = True
        return mirrored


    def match(self, A, B):
        pairs = {}
        unmatched = []

        #select the figure to iterate through. Should usually be the one with fewer objects. If same number of objects, make it B.
        iterate = B
        tester = A
        if len(A.objects) < len(B.objects):
            iterate = A
            tester = B

        #make an array of the objects that have not yet been matched from the larger figure.
        for object in tester.objects:
            unmatched.append(object) 

        for object_i in iterate.objects:
            current_min = 100
            current_obj = 'deleted'
            for i in range(len(unmatched)):
                num_diff = len(self.get_differences(tester.objects[unmatched[i]].attributes, iterate.objects[object_i].attributes))
                #if it is the smallest number of differences so far
                if num_diff < current_min:
                    current_min = num_diff
                    current_obj = unmatched[i]
                #if it equals the smallest number of differences found so far, find out which one has the most similarities
                if num_diff == current_min:
                    similar1 = 0
                    similar2 = 0

                    #Count similarities for each.
                    for attribute_name, attribute_value in iterate.objects[object_i].attributes.items():
                        if attribute_name in tester.objects[unmatched[i]].attributes:
                            if attribute_value == tester.objects[unmatched[i]].attributes[attribute_name]:
                                similar1 = similar1 + 1
                        if attribute_name in tester.objects[current_obj].attributes:
                            if attribute_value == tester.objects[current_obj].attributes[attribute_name]:
                                similar2 = similar2 + 1
                    
                    #only if the new object has more similarities than the old
                    if similar2 < similar1:
                        current_min = num_diff
                        current_obj = unmatched[i]

            #remove the matched object from the unmatched list  
            unmatched.remove(current_obj)
            
            #add pair to paired list in both directions.
            pairs[object_i] = current_obj
            pairs[current_obj] = object_i

        for i in range(len(unmatched)):
            if iterate == B:
                pairs[unmatched[i]] = 'deleted'
            else:
                pairs[unmatched[i]] = 'added'
        """
        pairs = {}
        #go through all objects in A
        for object_a in A.objects:
            current_min = 100
            current_obj = 'deleted'
            #go through all objects in B
            for object_b in B.objects:
                #for each, get differences between object from A and all objects from B
                num_diff = len(self.get_differences(A.objects[object_a].attributes, B.objects[object_b].attributes))

                #See if object_b has already been taken by another previous A object
                if object_b in pairs:
                    prev_object = pairs[object_b]
                    num_diff_prev = len(self.get_differences(A.objects[prev_object].attributes, B.objects[object_b].attributes))

                    #if the new A object has more similarities than the old
                    if num_diff < num_diff_prev:
                        if num_diff < current_min:
                            current_min = num_diff
                            current_obj = object_b

                            #find the next closest object for the previous object
                            new_current_min = 100
                            new_current_obj = 'W'
                            for new_object_b in B.objects:
                                if new_object_b != object_b:
                                    #for each, get differences between object from A and all objects from B
                                    num_diff = len(self.get_differences(A.objects[prev_object].attributes, B.objects[new_object_b].attributes))
                                    if num_diff < new_current_min:
                                        new_current_min = num_diff
                                        new_current_obj = new_object_b
                            
                            pairs[prev_object] = new_current_obj
                            pairs[new_current_obj] = prev_object

                #figure out which one has the fewest differences
                elif num_diff < current_min:
                    current_min = num_diff
                    current_obj = object_b

            pairs[object_a] = current_obj
            pairs[current_obj] = object_a



            
            #If A has more objects than B, look at which B values are repeated in pairs
            if len(A.objects) > len(B.objects):
                for a1, current in pairs.items():
                    for a2, current_obj in pairs.items():
                        if current == current_obj:
                            #figure out which A object has fewer differences to the B object
                            num_diff_1 = len(self.get_differences(A.objects[a1].attributes, B.objects[current].attributes))
                            num_diff_2 = len(self.get_differences(A.objects[a2].attributes, B.objects[current_obj].attributes))
                            
                            #Make the A object with the fewest differeces match the B object, and the other object read "object : Added"
                            if num_diff_1 < num_diff_2:
                                pairs[a2] = "Added"
                                pairs[current] = a1
                            elif num_diff_2 < num_diff_1: 
                                pairs[a1] = "Added"
                                pairs[current] = a2


            elif len(A.objects) < len(B.objects):
                #see which B objects were not deleted
                for object in B.objects:
                    if object not in pairs:
                        pairs[object] = "Deleted"


        print (pairs)
        dummy = input()
 

            #

        #if B is bigger than A
        #look for the B object that is not yet in pairs
        """
        return pairs

    
    def get_differences(self, A_dict, B_dict):
        diff = {}
        #Go through each element in B, compare to current element in A
        for attribute_name, attribute_a in A_dict.items():
            if attribute_name in B_dict:
                if B_dict[attribute_name] != attribute_a:
                    diff[attribute_name] = B_dict[attribute_name]
            else:
                diff[attribute_name] = 'deleted'
        
        #Go through each element in A, compare to current element in B. This is to make sure nothing added is left out.
        for attribute_name, attribute_b in B_dict.items():
            if attribute_name not in diff:
                if attribute_name in A_dict:
                    if A_dict[attribute_name] != attribute_b:
                        diff[attribute_name] = A_dict[attribute_name]
                else:
                    diff[attribute_name] = 'added'
        return diff