#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
import pandas as pd
import math


# In[8]:


#Probabilities of keys (0 as a placehodler)
p=[0,0.15,0.1,0.05,0.1,0.2]

# Probabilities of dummy nodes (there are len(keys)+1 dummy nodes)
q=[0.05,0.1,0.05,0.05,0.05,0.1]

# Number of nodes
n=len(p)

# Will store the roots (the k values which lead the lowest total cost)
RootArray= np.zeros([n,n])
# Will store all the minimum costs
CostArr= np.zeros((n,n))
# Will store all the weights
WeightArr= np.zeros((n,n))

def WeightCalculator(i,j):
    # w[i,j] will always be the corresponding dummy weight as w[i,j-1] does not exist
    if i==j:
        return q[j]
    
    elif WeightArr[i][j] != 0:
        return WeightArr[i][j]
    
    WeightArr[i][j]= WeightCalculator(i,j-1)+ p[j]+q[j]
    # The weights are sums of previous weights, starting from inital weights of first key. 
    # ie. W[0,4]= P0+Q0+P1+Q1+P2+Q2+...+P4+Q4. If we know W[0,3], we just need to add P4 and Q4 to get W[0,4].
    return WeightArr[i][j]
    

def CostCalculator(i,j):
    
    
    # Cost[i,j] is always 0 if i == j
    if i==j:
        return 0
    
    # If the value is not already in the Cost Array
    elif CostArr[i,j]!= 0:
        return CostArr[i,j]
    
    # A list that holds all potential costs
    PotentialKValues=[]

    # The largest possible cost regardless of tree
    Mini=math.inf
    
    # k == Key. We are testing the cost when the root is k where i<k<=j
    for k in range(i+1,j+1):
        
        CurrentCost= CostCalculator(i,k-1)+CostCalculator(k,j)
        # If the calcualted cost is less than the current possible cost, 
        # set the calculated cost as the smallest and note the key
        if CurrentCost< Mini:
            Mini=CurrentCost
            KValue=k
            
        # Adds a calculated cost to the list   
        PotentialKValues.append(CurrentCost) 
        
    # Fills the table with the k value that gives the lowest cost
    RootArray[i,j]= KValue
    # Fills the cost array with the lowest cost
    CostArr[i,j]= min(PotentialKValues, default=0)+ WeightCalculator(i,j)
    # Returns the total calculated cost of the subtree
    return CostArr[i,j]



# In[63]:


# The binary search tree node will be implemented using constructor class with attributes left, right and key 
class Node:
    def __init__(self, key = None, dimensions= None):
        self.left  = None
        self.right = None
        self.key = key
        self.dimensions= dimensions
        
def CreateAnOptimalBinarySearchTree():
    
    
    # Two pointers are created, initialy at the upper most right element in the RootArray
    i=0
    j=n-1
    
    # Fills out array 'RootArray' 
    CostCalculator(i,j)
    
    # A root node is created using the upper most right element in the RootArray
    Root= Node(int(RootArray[i,j]), df['Dimensions'].iloc[int(RootArray[i,j])])
    
    # Will create the binary tree and return it
    TreeCreationRecurssion(Root,i,j,int(Root.key))
    
    end = time.time()
    
    return Root


def TreeCreationRecurssion(node,i,j,k):
    LeftChild(node,i,j,k)
    RightChild(node,i,j,k)

    
def LeftChild(node,i,j,k):
    
    # In either case, it is impossible for the current node to have a left child. 
    # Thus we return to the current node.
    if i>=k or k==0:
        return 
    
    # If a left node exists...
    elif RootArray[i,k-1]!= 0:
        node.left= Node(int(RootArray[i,k-1]), df['Dimensions'].iloc[int(RootArray[i,k-1])-1])
        # The left child becomes the new parent 
        TreeCreationRecurssion(node.left,i,k-1,int(node.left.key))


def RightChild(node,i,j,k):
    
    # In either case, it is impossible for the current node to have a right child.
    # Thus we return to the current node.
    if k==j or k==0:
        return
    
    # If a right child exists...
    elif RootArray[k,j] !=0:
        node.right= Node(int(RootArray[k,j]), df['Dimensions'].iloc[int(RootArray[k,j])-1])  
        # The right child becomes the new parent 
        TreeCreationRecurssion(node.right,k,j,int(node.right.key))
        




# In[28]:


#p= np.concatenate([[0], p]).tolist()
#q= np.zeros(len(p)).tolist()
# Probabilities of keys (0 as a placehodler)
p=[0,0.15,0.1,0.05,0.1,0.2]

# Probabilities of dummy nodes (there are len(keys)+1 dummy nodes)
q=[0.05,0.1,0.05,0.05,0.05,0.1]

# Number of nodes
n=len(p)

# Will store the roots (the k values which lead the lowest total cost)
RootArray= np.zeros([n,n])

Root= CreateAnOptimalBinarySearchTree()


# In[70]:


def SearchTree(node, item):
    
    # The part is not in the tree
    if node == None:
        print(str(item)+ " is not in the tree")
    
    # The part is in the tree
    elif node.dimensions == item:
        print(str(item)+ " has been found!")
    
    # Parts less than current key value are to the left of a BST
    elif node.key > item:
        SearchTree(node.left, item)
        
    # Parts more than current key value are to the right of a BST    
    elif node.key < item:
        SearchTree(node.right, item)
        

