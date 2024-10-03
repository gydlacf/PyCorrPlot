#!/usr/bin/python3

import pandas as pd
import numpy as np
import pylab as pl

class PyCorrPlot:
    def __init__(self, 
                 rmatrix:pd.DataFrame,
                 pmatrix:pd.DataFrame,
                 ax,
                 plim=0.05,
                 **kwargs):
                     
        cmap = kwargs.get('cmap', 'seismic')
        label = kwargs.get('label', 'significance')
        
        rows, cols = rmatrix.shape
        
        grid = np.meshgrid(np.arange(rows),
                           np.flipud(np.arange(cols)))
                           
        grid = np.stack([gr.ravel() for gr in grid]).T
           
        # set aspect ratio
        ax.set_aspect('equal')
        
        #perform the changes
        ax.figure.canvas.draw()
        
        # set marker size
        bbox = ax.get_window_extent()
        
        rmatrix.dtype = float
        
        ss = 320 * rmatrix.values.ravel()**2
        ss = ss.astype(float)
        
        lines = ax.scatter(grid[:, 0], grid[:, 1],
                           c=rmatrix.values.ravel(),
                           s=ss,
                           cmap=cmap)
        ax.set_xticks(np.arange(rows),
                      labels=rmatrix.index)
        ax.set_yticks(np.arange(cols),
                      labels=rmatrix.columns[::-1])
        
        ax.tick_params(axis='x',
                       labelrotation=90)
        
        ax.set_xlim([-1, rows])
        ax.set_ylim([-1, cols])
                       
        prav = pmatrix[pmatrix < plim].values.ravel().astype(float)
        
        
        ind = ~np.isnan(prav)
        
        if label == 'significance':              
            ax.scatter(grid[ind, 0], grid[ind, 1],
                       c='white',
                       s=32,
                       marker='*')
        elif label == 'pvalue':
            if pmatrix is not None:
                for (x, y), p, r in zip(grid, 
                                        pmatrix.values.ravel(),
                                        rmatrix.values.ravel()):
                    if not np.isnan(p) and p < plim:
                        fontcolor = 'w' if np.abs(p) > 0.9 else 'k'
                        ax.text(x, y, f'{p:.4f}',
                                fontsize=s / 4,
                                color=fontcolor,
                                horizontalalignment='center',
                                verticalalignment='center_baseline')
                           
        
                                
        ax.figure.colorbar(lines,
                           cmap=cmap)
                     
        
def pycorrplot(rmatrix,
               pmatrix=None,
               ax=None,
               **kwargs):
    if ax is None:
        fig, ax = pl.subplots(figsize=(8, 6),
                              facecolor='white')

                   
    plot = PyCorrPlot(rmatrix,
                      pmatrix,
                      ax=ax,
                      **kwargs)
                      
    pl.show()
                      
    return ax.figure, ax
                      
if __name__ == '__main__':
    from numpy.random import random
    
    rmat = random(size=(8, 8)) * 2 - 1
    pmat = random(size=(8, 8))
    
    np.fill_diagonal(rmat, 1.)
    
    pycorrplot(pd.DataFrame(rmat),
               pd.DataFrame(pmat))
               
