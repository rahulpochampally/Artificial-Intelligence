#!/usr/bin/env python3
#This is Assignment 1 Question 2.
#
#Data Representation:
#    Here we consider everything as a numpy array.
#    For the following input
#                djcran 3 zehzhang,chen464 kapadia
#                chen464 1 _ _
#                fan6 0 chen464 djcran
#                zehzhang 1 _ kapadia
#                kapadia 3 zehzhang,fan6 djcran
#                steflee 0 _ _
#                
#    we get the following arrays
#    
#    1)Student List- It is a numpy array of the list of students.
#                ['djcran' 'chen464' 'fan6' 'zehzhang' 'kapadia' 'steflee']
#            
#    2)Student Group Size Preference- The ith element in this is the preference for group size of the ith student in #the student list.
#                [3 1 0 1 3 0]
#                
#    3) Student Partner Preference- Here, if the [i, j] is 1 then the ith student in the student list wants the jth #student in the list to be his group member.
#                [[ 0.  1.  0.  1.  0.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]
#                 [ 0.  1.  0.  0.  0.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]
#                 [ 0.  0.  1.  1.  0.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]]
#        
#    4)Student Anti Partner Preference- Here, if the [i, j] is 1 then the ith student in the student list  does not #want the jth student in the list to be his group member.
#                [[ 0.  0.  0.  0.  1.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]
#                 [ 1.  0.  0.  0.  0.  0.]
#                 [ 0.  0.  0.  0.  1.  0.]
#                 [ 1.  0.  0.  0.  0.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]]
#                
#                
#                
#                
#                
#State Representation:
#    To present each state, we have a numpy array which is a square matrix of the size of the number of students. If [i, j] is 1 then the jth student in the student list is the group of the ith student. Logically,  if [i, j] is 1, then [j, i] will also be 1 as the ith student in the student list is also the group of the jth student.
#    Initially, all the students are in their own individual groups. So all diagonals, [i, i] are 1 only. The rest of the matrix is 0.
#                [[ 1.  0.  0.  0.  0.  0.]
#                 [ 0.  1.  0.  0.  0.  0.]
#                 [ 0.  0.  1.  0.  0.  0.]
#                 [ 0.  0.  0.  1.  0.  0.]
#                 [ 0.  0.  0.  0.  1.  0.]
#                 [ 0.  0.  0.  0.  0.  1.]]
#    
#    
#    
#    
#    
#State Generation:
#    To generate the successor of the current state, we create a copy of the state using 
#                groups = group[np.arange(group.shape[0])]
#                
#    This creates a duplicate copy of the group in another variable called groups. Here we merge 2 teams together, if the new groups still have 3 or fewer members. So for the above we can have something like the following
#                [[ 1.  0.  1.  0.  0.  0.]
#                 [ 0.  1.  0.  0.  0.  0.]
#                 [ 1.  0.  1.  0.  0.  0.]
#                 [ 0.  0.  0.  1.  0.  0.]
#                 [ 0.  0.  0.  0.  1.  0.]
#                 [ 0.  0.  0.  0.  0.  1.]]
#    When we merge 2 teams we are essetially merging  them by index [i, j], i.e. merging the teams of the ith and jth students. so if [i, k] and [k, i] is 1 before the merger with j, then during the merger, me must also set [j, k] and [k, j] as 1 as noe the kth and jth students are also part of the same group with the ith students.
#    We will push will the successor out into our heap and find the successors of the states with the lowest cost. 
#    
#
#
#
#
#Cost Calculations:
#    To calculate the cost we need to find the number of groups formed(groupNo), number students who did not get their preferred group size(call this groupSize), the number partners that had been requested but not assigned according to the requests(call this prefs) and the number of anti-partners requested but assigned even though they were requested(call this antiprefs).
#    To get groupNo, its faitrly straightforward. We call the get_group_numbers and pass the current state. This will return the number of groups in our current state.
#    To get the number of students who did not get their preferred groups, we sum up the rows of our current state. This will give us thee group size of each student. We compare element wise with Student Group Size Preference and track the number of students whose current group size and preffered group size differ. 
#    To get the 'prefs', it is a little bit tricky. We perform a dot product between Student Partner Preference and current state. The diagonals of the resulting matrix will correspond to the number of requests that have been met. If we subtract the ith diagonal from the  total number of request for made by the ith student, we get how many requests were not assigned to their group. We can sum over all the students to get our pref.
#    To get 'antiprefs' its similar, with a sligth twist. We perform the same matrix multiplication and diagonalize the result to cpature only the diagonals. This will represent the count of the students that every student didnt want in his team but ends up working with him. So summing over the diagonals, will give us 'antiprefs'
#    
#    
#    
#    
#    
#Working example for prefs and antiprefs calculations:
#    The final group list according to question is
#                [[ 1.  1.  0.  0.  0.  0.]
#                 [ 1.  1.  0.  0.  0.  0.]
#                 [ 0.  0.  1.  1.  1.  0.]
#                 [ 0.  0.  1.  1.  1.  0.]
#                 [ 0.  0.  1.  1.  1.  0.]
#                 [ 0.  0.  0.  0.  0.  1.]]
#                
#    np.dot(Student Partner Preference List , group)=
#                [[ 0.  1.  0.  1.  0.  0.]           [[ 1.  1.  0.  0.  0.  0.]           [[ 1.  1.  1.  1.  1.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]            [ 1.  1.  0.  0.  0.  0.]            [ 0.  0.  0.  0.  0.  0.]
#                 [ 0.  1.  0.  0.  0.  0.]     .      [ 0.  0.  1.  1.  1.  0.]    =       [ 1.  1.  0.  0.  0.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]            [ 0.  0.  1.  1.  1.  0.]            [ 0.  0.  0.  0.  0.  0.]
#                 [ 0.  0.  1.  1.  0.  0.]            [ 0.  0.  1.  1.  1.  0.]            [ 0.  0.  2.  2.  2.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]]           [ 0.  0.  0.  0.  0.  1.]]           [ 0.  0.  0.  0.  0.  0.]]
#                
#    Diagonalizing the result, we get
#                 [1. 0. 0. 0. 2. 0.]
#                 
#    and the marginals of Student Partner Preference List is 
#                 [2. 0. 1. 0. 2. 0.]
#
#    Subtracting diagonals from marginals and summing over the difference, we get our prefs as 2. djcran did not get to work with zehzhang and fan6 did not get to work with chen464
#    
#    
#    Similary for the antiprefs, 
#                [[ 0.  0.  0.  0.  1.  0.]           [[ 1.  1.  0.  0.  0.  0.]           [[ 0.  0.  1.  1.  1.  1.]
#                 [ 0.  0.  0.  0.  0.  0.]            [ 1.  1.  0.  0.  0.  0.]            [ 0.  0.  0.  0.  0.  0.]
#                 [ 1.  0.  0.  0.  0.  0.]     .      [ 0.  0.  1.  1.  1.  0.]    =       [ 1.  1.  0.  0.  0.  0.]
#                 [ 0.  0.  0.  0.  1.  0.]            [ 0.  0.  1.  1.  1.  0.]            [ 0.  0.  1.  1.  0.  0.]
#                 [ 1.  0.  0.  0.  0.  0.]            [ 0.  0.  1.  1.  1.  0.]            [ 1.  1.  0.  0.  0.  0.]
#                 [ 0.  0.  0.  0.  0.  0.]]           [ 0.  0.  0.  0.  0.  1.]]           [ 0.  0.  0.  0.  0.  0.]]    
#    
#    Diagonalizing that summing over that we get our antiprefs as 1. In our case zehzhang did not wish to work with kapadia, but they were still assigned in similar teams.
#    
#    
#    From the question we know that there are 3 teams. There are 3 students did not get their preferred group sizes., djcran, chen464 and zehzhang did not get their choice of groups.
#    
#    Taking the values k=160, m=31, n=10 and l=1, we get our cost as
#                3*160 + 1*31 + 2*10 + 3*1 = 534
#                
#                
#                
#
#                
#Issues with the Implementation:
#    One serious problem our implementation faces is that when find successors, it always allocates new memory to the variables. This is very time consuming is the bottleneck of our approach.   
#    
#        Users- MyCost (running time)         
#        3-     342    (0.00s)
#        10-    765    (0.06s)
#        15-    1056   (0.28s)
#        20-    1483   (0.65s)
#        50-    3626   (44.5s)
#
#    Uptil, 20 users, our run time is pretty good. However, at 50 users, we take a significant leap. This was discussed with Professor Crandall and he gave the green light that it was okay.
import numpy as np
import heapq
import sys
import time

class MAIN:
    """
    This is the main class.
    We make a call to function in here from __main__.
    """


    @staticmethod
    def get_student_partner_pref(name, preflist):
        """
This is get_student_partner_pref. It returns a numpy array of the student preferences.
The inputs are
                    1)name- List of the names of all the students in the class
                    2)preflist- List of the names of all the students partner preferences in the class

There outputs are
                    1)pref- Numerical numpy array of preflist.
        """
        pref = np.zeros((len(name), len(name)))
        for i in range(len(name)):
            prefnames = preflist[i].split(',')
            for n in prefnames:
                j = np.where(name == n)
                pref[i, j] = 1
        return pref


    @staticmethod
    def get_student_antipartner_pref(name, antipreflist):
        """
This is get_student_antipartner_pref. It returns a numpy array of the student anti-preferences.
The inputs are
                    1)name- List of the names of all the students in the class
                    2)antipreflist- List of the names of all the students anti-partner preferences in the class

There outputs are
                    1)antipref- Numerical numpy array of antipreflist.
        """
        antipref = np.zeros((len(name), len(name)))
        for i in range(len(name)):
            antiprefnames = antipreflist[i].split(',')
            for n in antiprefnames:
                j = np.where(name == n)
                antipref[i, j] = 1
        return antipref


    @staticmethod
    def get_data(filename):
        """
This is the get_data() function. It converts input file into numpy arrays.
The inputs are
                    1)filename- Actual Path of the file.

There outputs are
                    1)studentlist- List of the names of all the students in the class
                    2)studentgroupsizepref- The size of group preferences of all the students.
                    3)studentpartnerpref- The group partner preferences of all the students.
                    4)studentantipartnerpref- The group anti-partner preferences of all the students.
        """
        fileline = open(filename)
        data = np.asarray([line.split() for line in fileline.readlines()])
        studentlist = np.asarray([row[0] for row in data])
        studentgroupsizepref = np.asarray([int(row[1]) for row in data])
        studentpartnerpref = MAIN.get_student_partner_pref(\
                                         studentlist, [row[2] for row in data])
        studentantipartnerpref = MAIN.get_student_antipartner_pref(\
                                         studentlist, [row[3] for row in data])
        
        return studentlist, studentgroupsizepref, \
                studentpartnerpref, studentantipartnerpref


    @staticmethod
    def get_group_numbers(group):
        """
This is get_group_numbers. It returns the number of groups that we have formed.
The inputs are
                    1)group- Current group.
                    
There output is
                    1)groupCount-  The total number of groups in group.
        """
        groupCount = 0
        groupCheck = np.zeros(len(group))
        for i in range(len(group)):
            if groupCheck[i] == 0:
                x = MAIN.get_group(group, i)
                for j in x:
                    groupCheck[j] += 1
                groupCount +=1 
        return groupCount
    
    
    @staticmethod
    def calcost(groups, studentgroupsizepref, studentpartnerpref, 
                studentantipartnerpref, k, m, n, l):
        """
This is solv function. It searches for groups with minimum cost
The inputs are
                    1)groups- Initial group where everyone is working alone.
                    2)studentgroupsizepref- The size of group preferences of all the students.
                    3)studentpartnerpref- The group partner preferences of all the students.
                    4)studentantipartnerpref- The group anti-partner preferences of all the students.
                    5)k- cost paid per group.
                    6)m- cost paid of assigning someone they do not want to work with.
                    7)n- cost paid of not assigning someone they want to work with.
                    8)l- cost paid of not assigning their preferred group size. Default is 1.

There outputs are
                    1)The cost associated with groups.
        """
        partnerprefD = (np.dot(studentpartnerpref, groups)).diagonal()
        partnerprefM = ([sum(rows) for rows in studentpartnerpref])
                             
        antipartnerprefD = (np.dot(studentantipartnerpref, groups)).diagonal()

        partnerprefCost = (sum(partnerprefM)-sum(partnerprefD))*n
        antipartnerprefCost = sum(antipartnerprefD)*m

        groupCost=MAIN.get_group_numbers(groups)
        groupsizeCost = 0
        if l > 0:
            groupSize = ([sum(rows) for rows in groups])
            for i in range(len(groupSize)):
                if (groupSize[i] != studentgroupsizepref[i] and 
                    studentgroupsizepref[i] != 0):
                    groupsizeCost += l
                                 
        return partnerprefCost + antipartnerprefCost + \
                groupsizeCost +(groupCost*k)
    
    
    @staticmethod
    def get_group(groups, member):
        """
This is get_ group function. It returns the indices of group members of member.
The inputs are
                    1)group- Initial group where everyone is working alone.
                    2)member- Index whose group member indices we want.
                    
There output is
                    1)List of indices of group members of student whose index is member.
        """
        return [x for x in range(len(groups)) if groups[member, x]==1]
    
    
    @staticmethod
    def merge_groups(group, i, j):
        """
This is the merge_groups function. It merges together groups i and j.
The inputs are
                    1)group- Initial group where everyone is working alone.
                    2)i- Index of first group to merge.
                    3)j- Index of second group to merge.
                    
There output is
                    1)groups- The new set of groups with group i and group j merged together.
        """
        groups = group[np.arange(group.shape[0])]
        for x in MAIN.get_group(groups, i):
            for y in MAIN.get_group(groups, j):
                groups[x, y] = 1
                groups[y, x] = 1
        return groups
    
    
    @staticmethod
    def succ(group):
        """
This is the successor function. It returns successors of group by merging groups together.
The inputs are
                    1)group- Initial group where everyone is working alone.
                    
There output is
                    1)List of successors that satisfy the condition that the group size is still less than 3.
        """
        return [MAIN.merge_groups(group, i, j) 
                for i in range(len(group))
                for j in range(i)
                if ((i != j) and 
                    sum(group[i])+sum(group[j]))<4]


    @staticmethod
    def solv(groups, studentlist, studentgroupsizepref, 
             studentpartnerpref, studentantipartnerpref, k, m, n, l):
        """
This is solv function. It searches for groups with minimum cost.
The inputs are
                    1)groups- Initial group where everyone is working alone.
                    2)studentlist- List of the names of all the students in the class
                    3)studentgroupsizepref- The size of group preferences of all the students.
                    4)studentpartnerpref- The group partner preferences of all the students.
                    5)studentantipartnerpref- The group anti-partner preferences of all the students.
                    6)k- cost paid per group.
                    7)m- cost paid of assigning someone they do not want to work with.
                    8)n- cost paid of not assigning someone they want to work with.
                    9)l- cost paid of not assigning their preferred group size. Default is 1.

There outputs are
                    1)minGroup- The optimal group.
                    2)minCost- The cost associated with minGroup.
        """
        
        fringe = []
        cost = MAIN.calcost(groups, studentgroupsizepref, studentpartnerpref, 
                            studentantipartnerpref, k, m, n, l)
        
        heapq.heappush(fringe, (cost, groups))
        minCost = cost
        minGroup = groups
        itr = 0
        
        while(fringe):
            tup = heapq.heappop(fringe)
            state = tup[1]
            for s in MAIN.succ(state):
                
                c = MAIN.calcost(s, studentgroupsizepref, studentpartnerpref, 
                                 studentantipartnerpref, k, m, n, l)

                if c < minCost:
                    itr = 0
                    minCost = c
                    minGroup = s
                    
                    groupSize = ([sum(rows) for rows in s])
                    if (np.bincount(groupSize)[1] > 0):
                        heapq.heappush(fringe, (c, s))
            itr += 1            
                    
            if(itr == len(groups)):
                break
        return(minGroup, minCost)


    @staticmethod
    def print_Groups(groups, studentlist, cost):
        """
This is print_Groups function. It prints the optimal groups in the desired format along with the optimal cost.
The inputs are
                    1)groups- Optimal group.
                    2)studentlist- List of the names of all the students in the class
                    3)cost- The cost associated with groups.

There are no outputs.    
        """
        for i in range(len(groups)):
            stud = 0
            if groups[i, i] == 1:
                stud = ' '.join(studentlist[j] for j in MAIN.get_group(groups, i))
                for x in MAIN.get_group(groups, i):
                        groups[x, x] = 0
            if(stud):
                print(stud)
        print(cost)
                    
        
    @staticmethod
    def main(filename, k, m, n, l=1):
        """
This is the main function. It initializes all the variables, and calls solv() to find the optimal groups. It also calls print_Groups() to print the optimal groups and final cost.
The inputs are
                    1)filename- Actual Path of the file.
                    2)k- cost paid per group.
                    3)m- cost paid of assigning someone they do not want to work with.
                    4)n- cost paid of not assigning someone they want to work with.
                    5)l- cost paid of not assigning their preferred group size. Default is 1.

There are no outputs.                    
        """
        studentlist, studentgroupsizepref, studentpartnerpref, \
        studentantipartnerpref = MAIN.get_data(filename)
        
        groups = np.identity(len(studentlist))

        groups, cost = MAIN.solv(groups, 
                                 studentlist, 
                                 studentgroupsizepref, 
                                 studentpartnerpref, 
                                 studentantipartnerpref, 
                                 k=k, 
                                 m=m, 
                                 n=n, 
                                 l=l)
        
        MAIN.print_Groups(groups, studentlist, cost)


if __name__ == '__main__':
    start=time.time()
    args = sys.argv
    MAIN.main(args[1], int(args[2]), int(args[3]), int(args[4]))
#    print(time.time()-start)    
    