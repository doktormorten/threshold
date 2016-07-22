# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:54:22 2016

@author: eugenio
"""
#from pandas import DataFrame
#import numpy as np
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix, coo_matrix

def DataFrame_to_lG(df, directed=False, weighted=False, source='source', target='target', time='time'):
    
    ti, tf = df[time].min(), df[time].max()+1
    
    if directed:
        graph = nx.DiGraph
    else:
        graph = nx.Graph
        
    if weighted:
        assert 'weight' in df.columns, 'No "weight" column.'
        attr = 'weight'
        
    else:
        attr = None
        
    lG = []
    for t in range(ti,tf):
        
        cut = df[df[time]==t]
        if cut.shape[0]==0:
            G = graph()
        else:
            G = nx.from_pandas_dataframe(cut, source=source, target=target, edge_attr=attr, create_using=graph())
        
        lG.append(G)
        
    return lG
    
    
    
def DataFrame_to_lA(df, directed=False, source='source', target='target', time='time', weight='weight', dtype=np.float128, force_beg=None, force_end=None):
    
    """
    Assumes IDs are integers from 0 to N
    """
    
    ti, tf = df[time].min(), df[time].max()+1
    N = max( df[source].max(), df[target].max() )+1
    
    if force_beg is None:
        force_beg = ti
    if force_end is None:
        force_end = tf
    
    lA = []
    for t in range(force_beg,force_end):
        
        cut = df[df[time]==t]
        if cut.shape[0]==0:
            # empty timestep
            A = csr_matrix((N,N), dtype=dtype)
        else:
            
            data = np.array(cut[weight])
            rows = np.array(cut[source])  
            cols = np.array(cut[target])
            if not directed:
                data = np.concatenate((data,data))
                rows, cols = np.concatenate((rows,cols)), np.concatenate((cols,rows))
            
            A = coo_matrix( (data, (rows,cols)), shape=(N,N), dtype=dtype).tocsr()
        
        lA.append(A)
        
    
        
    return lA