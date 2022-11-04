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
        #self.tri_dict = {"0":"270", "90":"180", "270":"0", "180":"90"}
        #self.pac_dict = {"45":"135", "315":"225", "135":"45", "225":"315", "0":"180", "180":"0"}
        self.directions = {"up":{"bottom-left":"top-left", "bottom-right": "top-right"}, "down":{"top-left":"bottom-left", "top-right": "bottom-right"},
                            "left":{"top-right":"top-left", "bottom-right":"bottom-left"}, "right":{"top-left":"top-right", "bottom-left":"bottom-right"}}
        self.alignments = ["inside", "above", "below", "left-of", "right-of"]

        self.sizes = ["very small", "small", "medium", "large", "very large", "huge"]

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
        counter = 0

        if 'D' in problem.figures:

            #Set up figures
                #Use A, C, and G
            A = problem.figures['A']
            B = problem.figures['B']
            C = problem.figures['C']
            D = problem.figures['D']
            E = problem.figures['E']
            F = problem.figures['F']
            G = problem.figures['G']
            H = problem.figures['H']

            #for each object put its name in the dict of dicts
            for object in A.objects:
                all_attributes[object]=A.objects[object].attributes

            for object in C.objects:
                all_attributes[object]=C.objects[object].attributes

            for object in G.objects:
                all_attributes[object]=G.objects[object].attributes


            #change the alignment dict to an array like dict = {'left-of' : ['f', 'g']}
                #Can access with dict['left-of'][0]
            for object in all_attributes:
                for attribute in all_attributes[object]:
                    for i in range(len(self.alignments)):
                        if self.alignments[i] == attribute:
                            all_attributes[object][attribute] = all_attributes[object][attribute].split(',')


            #if there are multiple objects, compare them
            ac_pairs = self.match(A, C)
            ag_pairs = self.match(A, G)


            #self.alignment_array(C)


            #arrays to hold which objects were added
            ac_added = []
            ag_added = []


            #Get A/B and A/C differences.
            differences_ac = {}
            #go through all pairs
            for object in ac_pairs:
                pair = ac_pairs[object]
                #if the object wasn't deleted or added
                if pair != "deleted" and pair != "added":
                    #if object being analyzed is from Figure A (so that b:a doesnt get analyzed after a:b)
                    if pair not in A.objects:
                        diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                        differences_ac[object] = diffs
                elif pair == "deleted":
                    differences_ac[object] = 'deleted'
                elif pair == "added":
                    differences_ac[object] = 'added'
                    ac_added.append(object)


            differences_ag = {}
            for object in ag_pairs:
                pair = ag_pairs[object]
                #if the object wasn't deleted or added
                if pair != "deleted" and pair != "added":
                    #if object being analyzed is from Figure A (so that c:a doesnt get analyzed after a:c)
                    if pair not in A.objects:
                        diffs = self.get_differences(all_attributes[object], all_attributes[pair])
                        differences_ag[object] = diffs
                elif pair == "deleted":
                    differences_ag[object] = 'deleted'
                elif pair == "added":
                    differences_ag[object] = 'added'
                    ag_added.append(object)

            """

            #code to remove the "inside" attributes from the differences dicts if the objects match
                #so if 'a' and 'c' are matched, then 'inside' : 'a' and 'inside' : 'c' will not be counted as a difference
            for i in range(len(self.alignments)):
                for object in differences_ac:
                    if self.alignments[i] in differences_ac[object] and self.alignments[i] in all_attributes[ac_pairs[object]]:
                        if differences_ab[object][self.alignments[i]] in ab_pairs and self.alignments[i] in all_attributes[ab_pairs[object]]:
                            if differences_ab[object][self.alignments[i]] == all_attributes[ab_pairs[object]][self.alignments[i]]:
                                del differences_ab[object][self.alignments[i]]


            #code to remove the "inside" attributes from the differences dicts if the objects match
                #so if 'a' and 'c' are matched, then 'inside' : 'a' and 'inside' : 'c' will not be counted as a difference
            for i in range(len(self.alignments)):
                for object in differences_ac:
                    if self.alignments[i] in differences_ac[object] and self.alignments[i] in all_attributes[ac_pairs[object]]:
                        if differences_ac[object][self.alignments[i]] in ac_pairs and self.alignments[i] in all_attributes[ac_pairs[object]]:
                            if differences_ac[object][self.alignments[i]] == all_attributes[ac_pairs[object]][self.alignments[i]]:
                                del differences_ac[object][self.alignments[i]]

            """

            #Dict for the new I value coming from G
            I_G = {}
            #make same as G
            for object in G.objects:
                I_G[object] = all_attributes[object]


            #Go through all the A/C changes and apply them to G
            for difference in differences_ac:
                #check to see if the corresponding G object was deleted (To reduce redundency)
                    #NOTE: Does not include objects that were added
                if difference in ag_pairs:
                    if ag_pairs[difference] != "deleted":
                        #check to see if the object was added from A -> B
                        if difference in ac_pairs:
                            #check to see if the object was deleted from A -> C
                            if ac_pairs[difference] == "deleted":
                                #if so, delete it from I_G
                                del I_G[ac_pairs[difference]]

                            #if the object was neither deleted nor added between A -> C
                            else:
                                c_object = ac_pairs[difference]
                                g_object = ag_pairs[difference]
                                for attribute_name, attribute in differences_ac[difference].items():
                                    #fill check
                                    if attribute_name == 'fill':
                                        I_G[g_object][attribute_name] = all_attributes[c_object][attribute_name]
                                    #if shape changed, change G shape to whatever C shape is
                                    elif attribute_name == 'shape':
                                        #if it didn't change from a square to a rectangle
                                        if attribute != "rectangle" and  all_attributes[object]["shape"] != 'sqare':
                                            #if it didnt change from a rectangle to a square 
                                            if attribute != "sqare" and  all_attributes[object]["shape"] != 'rectangle':
                                                if c_object in I_G:
                                                    I_G[c_object][attribute_name] = all_attributes[c_object][attribute_name]
                                        
                                        #if there was a change to a rectangle from a square (or vice versa)
                                        else:
                                            #Get heights and widths of A, C, and G. Check if each is a square or rectangle
                                            if attribute == "rectangle":
                                                c_height = all_attributes[c_object]['height']
                                                c_width = all_attributes[c_object]['width']
                                            elif attribute == "square":
                                                c_height = all_attributes[c_object]['size']
                                                c_width = c_height
                                            if all_attributes[difference]["shape"] == 'square':
                                                a_height = all_attributes[difference]['size']
                                                a_width = a_height
                                            elif all_attributes[difference]["shape"] == 'rectangle':
                                                a_height = all_attributes[difference]['height']
                                                a_width = all_attributes[difference]['width']
                                            if I_G[g_object]["shape"] == 'rectangle':
                                                g_height = I_G[g_object]['height']
                                                g_width = I_G[g_object]['width']
                                            elif I_G[g_object]["shape"] == 'square':
                                                g_height = I_G[g_object]['size']
                                                g_width = g_height
                                            
                                            #fugure out what the I height will be
                                            if g_height in self.sizes and a_height in self.sizes and c_height in self.sizes:
                                                diff = self.sizes.index(c_height) - self.sizes.index(a_height)
                                                i_height = self.sizes[self.sizes.index(g_height) + diff]

                                            
                                            #fugure out what the I width will be
                                            if g_width in self.sizes and a_width in self.sizes and c_width in self.sizes:
                                                diff = self.sizes.index(c_width) - self.sizes.index(a_width)
                                                i_width = self.sizes[self.sizes.index(g_width) + diff]
                                            

                                            #if height and width are the same, make I a square, if they are different, make it a rectangle
                                            if i_height == i_width:
                                                I_G[g_object]['shape'] = 'square'
                                                I_G[g_object]['size'] = i_width
                                                #if it had a width and height (from previously being a rectangle) delete them
                                                if 'width' in I_G[g_object]:
                                                    del I_G[g_object]['width']
                                                if 'height' in I_G[g_object]:
                                                    del I_G[g_object]['height']
                                            
                                            #if heigh and width are different
                                            else:
                                                I_G[g_object]['shape'] = 'rectangle'
                                                I_G[g_object]['width'] = i_width
                                                I_G[g_object]['height'] = i_height
                                                #if it had a size (from previously being a square) delete it
                                                if 'size' in I_G[g_object]:
                                                    del I_G[g_object]['size']


                                    #if size changed from A->C, do the appropriate size jump from G -> I
                                    elif attribute_name == 'size':
                                        if differences_ac[difference]['size'] != "deleted":
                                            a_size = ""
                                            c_size = ""
                                            g_size = ""
                                            #get the sizes for a, c, g
                                            for i in range(len(self.sizes)):
                                                if attribute_name in all_attributes[c_object]:
                                                    if self.sizes[i] == all_attributes[c_object][attribute_name]:
                                                        c_size = i
                                                    if self.sizes[i] == all_attributes[difference][attribute_name]:
                                                        a_size = i
                                                    if self.sizes[i] == all_attributes[g_object][attribute_name]:
                                                        g_size = i

                                            #if no change between a and c, no change between g and i, which is already true so nothing needs to happen
                                            #if change between a and c, apply that same change from G to I
                                            if a_size != c_size:
                                                diff_ac = c_size - a_size
                                                i_size = g_size + diff_ac
                                                I_G[g_object][attribute_name] = self.sizes[i_size]

                                    elif attribute_name == "alignment":
                                        #go through the directions attribute to find the pair that describes what is happening from A to C
                                        for direction in self.directions:
                                            for first, second in self.directions[direction].items():
                                                if all_attributes[difference][attribute_name] == first and all_attributes[c_object][attribute_name] == second:
                                                    #once found, record the direction
                                                    ac_direction = direction
                                        #Use the direction and the G starting position to set the position of I
                                        for first1, second1 in self.directions[ac_direction].items():
                                            if first1 == I_G[g_object][attribute_name]:
                                                I_G[g_object][attribute_name] = second1




                                    #if the same shape, check if angle has changed
                                    if all_attributes[difference]['shape'] == all_attributes[g_object]['shape']:
                                        if attribute_name == 'angle':
                                            #check for mirroring from A to G
                                            mirrored = self.is_mirrored(all_attributes[difference]['angle'], all_attributes[g_object]['angle'], all_attributes[difference]['shape'])

                                            #if it was mirrored, get corresponding mirrored angle
                                            if mirrored:
                                                if I_G[g_object]['shape'] == 'right triangle':
                                                    new_angle = (270.0 - float(I_G[g_object][attribute_name])) % 360.0
                                                    #if there is a decimal, include it in the string. Otherwise just make it an int then a string
                                                    if new_angle == int(new_angle):
                                                        I_G[g_object][attribute_name] = str(int(new_angle))
                                                    else:
                                                        I_G[g_object][attribute_name] = str(new_angle)
                                                elif I_G[g_object]['shape'] == 'pac-man':
                                                    new_angle = (180.0 - float(I_G[g_object][attribute_name])) % 360.0
                                                    if new_angle == int(new_angle):
                                                        I_G[g_object][attribute_name] = str(int(new_angle))
                                                    else:
                                                        I_G[g_object][attribute_name] = str(new_angle)
                                            else:
                                                #if not mirrored, subtract the c angle from the a angle
                                                angle_c = all_attributes[c_object][attribute_name]
                                                angle_a = all_attributes[difference][attribute_name]
                                                delta_angle = (float(angle_c) - float(angle_a))
                                                #apply the change in angle to the current I_G angle to get the final I angle
                                                new_angle = (float(I_G[g_object][attribute_name]) + delta_angle) % 360.0
                                                I_G[g_object][attribute_name] = str(new_angle)

                #if the object has been added between A -> C
                elif differences_ac[difference]=='added':
                    #if the number of objects in E equals the sum of the objects in D and B
                    if len(B.objects) + len(D.objects) == len(E.objects):
                        #for each object originally in G, add this object for I
                        for object in G.objects:
                            #update the counter, this makes the variables "var1", "var2", etc
                            counter = counter + 1
                            #add the object, then manipulate the alignment
                            I_G["var{0}".format(counter)] = all_attributes[difference]


                            #make the left-of and above attributes line up
                            if "above" in I_G["var{0}".format(counter)]:
                                for k in range(len(I_G["var{0}".format(counter)]["above"])):
                                    if I_G["var{0}".format(counter)]["above"][k] in ac_pairs:
                                        if ac_pairs[I_G["var{0}".format(counter)]["above"][k]] != "added":
                                            if ac_pairs[I_G["var{0}".format(counter)]["above"][k]] in ag_pairs:
                                                if ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["above"][k]]] != "deleted":
                                                    I_G["var{0}".format(counter)]["above"][k] = ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["above"][k]]]

                            if "left-of" in I_G["var{0}".format(counter)]:
                                for k in range(len(I_G["var{0}".format(counter)]["left-of"])):
                                    if I_G["var{0}".format(counter)]["left-of"][k] in ac_pairs:
                                        if ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]] != "added":
                                            if ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]] in ag_pairs:
                                                if ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]]] != "deleted":
                                                    I_G["var{0}".format(counter)]["left-of"][k] = ag_pairs[ac_pairs[I_G["var{0}".format(counter)]["left-of"][k]]]

                    #otherwise, just add the one object
                    else:
                        I_G[difference] = all_attributes[difference]

                        #make the left-of and above attributes line up
                        if "above" in I_G[difference]:
                            for k in range(len(I_G[difference]["above"])):
                                if I_G[difference]["above"][k] in ac_pairs:
                                    if ac_pairs[I_G[difference]["above"][k]] != "added":
                                        if ac_pairs[I_G[difference]["above"][k]] in ag_pairs:
                                            if ag_pairs[ac_pairs[I_G[difference]["above"][k]]] != "deleted":
                                                I_G[difference]["above"][k] = ag_pairs[ac_pairs[I_G[difference]["above"][k]]]

                        if "left-of" in I_G[difference]:
                            for k in range(len(I_G[difference]["left-of"])):
                                if I_G[difference]["left-of"][k] in ac_pairs:
                                    if ac_pairs[I_G[difference]["left-of"][k]] != "added":
                                        if ac_pairs[I_G[difference]["left-of"][k]] in ag_pairs:
                                            if ag_pairs[ac_pairs[I_G[difference]["left-of"][k]]] != "deleted":
                                                I_G[difference]["left-of"][k] = ag_pairs[ac_pairs[I_G[difference]["left-of"][k]]]
                        

            #print(I_G)
            #dummy = input()


            #initialize min for changes
            diffs = 300

            #Loop through the answers,
            for i in range(1, 9):
                current = str(i)
                Option = problem.figures[current]
                fig_total_diff = 0

                #if the answer has the same number of objects as the generated guess (I_G)
                if len(Option.objects) == len(I_G):
                    #get the changes between the answer and the object
                    for object in Option.objects:
                        #match the object with a I_G object
                        current_min = 100
                        current_match = 'H'
                        for ig_obj in I_G:
                            diff = len(self.get_differences(Option.objects[object].attributes, I_G[ig_obj]))
                            if diff < current_min:
                                current_min = diff
                                current_match = ig_obj

                        fig_total_diff = fig_total_diff + current_min

                    if fig_total_diff < diffs:
                        diffs = fig_total_diff
                        answer = i
                else:
                    fig_total_diff = 100



            #print("the answer is ", answer)
            #dummy = input()

        return answer


    def is_mirrored(self, angle_A, angle_B, shape):
        mirrored = False

        #Check triangle mirroring
        if shape == 'right triangle':
            mirrored_angle = (270.0 - float(angle_A)) % 360.0
            if mirrored_angle == float(angle_B):
                mirrored = True

        #check pac-man mirroring
        if shape == 'pac-man':
            mirrored_angle = (180.0 - float(angle_A)) % 360.0
            if mirrored_angle == float(angle_B):
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

        #iterate through the objects in the smaller figure
        for object_i in iterate.objects:
            current_min = 100
            current_obj = 'W'

            #go through the yet unmatched objects of the bigger figure
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

