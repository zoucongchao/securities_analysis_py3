# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 16:27:56 2018

@author: Administrator
"""
import numpy as np
def rmse(predictions, targets):
    return np.sqrt(((predictions-targets)**2).mean())
