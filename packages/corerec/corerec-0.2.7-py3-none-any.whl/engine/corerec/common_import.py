import numpy as np
import pandas as pd
import sklearn
# import torch
import networkx as nx
# import torch.nn as nn

try:
    from torch.utils.data import Dataset
    import torch
    import torch.optim as optim
except ImportError as e:
    raise ImportError("PyTorch is not installed. Please install it to use the GraphDataset class.") from e


import sys
# sys.path.append('/Users/visheshyadav/Documents/GitHub/CoreRec/engine/torch_nn')
from engine.torch_nn import *


from sklearn.metrics.pairwise import cosine_similarity
# from torch.utils.data import Dataset, DataLoader
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
import os

# import for DDP ecosystem
import torch.distributed as dist
from torch.multiprocessing import Process

