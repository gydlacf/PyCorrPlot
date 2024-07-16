#!/usr/bin/python3

import pandas as pd
import numpy as np
import pylab as pl

class PyCorrPlot:
    def __init__(self, 
                 rmatrix:pd.DataFrame,
                 pmatrix:pd.DataFrame,
                 ax=None,
                 plim=0.05,
                 **kwargs):
                     
        cmap = kwargs.get('cmap', 'seismic')
                     
        rows, cols = rmatrix.shape
                     
        shift = 1 / (rows * 2)
        
        steps = np.linspace(shift, 
                            1 - shift, 
                            rows)
                     
        grid = np.meshgrid(steps, steps[::-1])
         
        grid = np.stack([gr.ravel() for gr in grid]).T
        
        if ax is None:
            fig, ax = pl.subplots(figsize=(8, 6),
                                  facecolor='white')
        
        # set aspect ratio to 1
        ax.set_aspect('equal')
        
        #perform the changes
        fig.canvas.draw()
        
                                  
        # set marker size
        bbox = ax.get_window_extent()
        
        s = (bbox.width * 72 / (rmatrix.shape[0] * fig.dpi) * 0.8)
        
        lines = ax.scatter(grid[:, 0], grid[:, 1],
                           c=rmatrix.values.ravel(),
                           s=np.abs(rmatrix.values.ravel()) * s**2,
                           cmap=cmap)
                     
        ax.set_xticks(steps,
                      labels=rmatrix.index)
        ax.set_yticks(steps,
                      labels=rmatrix.columns[::-1])
                      
        if pmatrix is not None:
            for (x, y), p, r in zip(grid, 
                                    pmatrix.values.ravel(),
                                    rmatrix.values.ravel()):
                if not np.isnan(p) and p < plim:
                    #annot = '***' if p < 1e-3 else '**' if p < 1e-2 else '*'
                    fontcolor = 'w' if np.abs(p) > 0.9 else 'k'
                    ax.text(x, y, f'{p:.4f}',
                            fontsize=s / 4,
                            color=fontcolor,
                            horizontalalignment='center',
                            verticalalignment='center_baseline')
                           

        fig.colorbar(lines,
                     cmap=cmap)
                     
        pl.show()

        
def pycorrplot(rmatrix,
               pmatrix=None,
               **kwargs):
    plot = PyCorrPlot(rmatrix,
                      pmatrix,
                      **kwargs)
                      
                      
if __name__ == '__main__':
    from numpy.random import random
    
    rmat = random(size=(8, 8)) * 2 - 1
    pmat = random(size=(8, 8))
    
    np.fill_diagonal(rmat, 1.)
    
    pycorrplot(pd.DataFrame(rmat),
               pd.DataFrame(pmat))
               
