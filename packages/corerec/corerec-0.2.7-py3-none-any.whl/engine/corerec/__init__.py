"""
###############################################################################################################
                           --CoreRec: Connecting to the Unseen--                            
CoreRec module is designed for graph-based recommendation systems using neural network architectures. It includes:
    1. GraphTransformer: A neural network model using Transformer architecture for processing graph data.
    2. GraphDataset: A custom dataset class for handling graph data.
    3. train_model: A function to train models with options for custom loss functions and training procedures.
    4. predict: Functions to predict top-k nodes based on model outputs, with optional thresholding.
    5. draw_graph: A function to visualize graphs with options to highlight top nodes and recommended nodes.
Note: This module integrates PyTorch for model training and evaluation, and NetworkX for graph manipulation.
###############################################################################################################
"""

# Common imports
from engine.corerec.common_import import *
from engine.corerec.async_ddp import *

# Core models
from engine.corerec.models import *
from engine.corerec.Tmodel import GraphTransformerV2
from engine.corerec.cr_pkg.gat_conv import *
from engine.corerec.cr_pkg.gcn_conv import *
from engine.corerec.cr_pkg.han_conv import *
from engine.corerec.cr_pkg.sage_conv import *

# Training and prediction functions
from engine.corerec.train import train_model
from engine.corerec.predict import predict, explainable_predict
from engine.corerec.metrics import jaccard_similarity, adamic_adar_index, aaj_accuracy

# Dataloaders and datasets
from engine.corerec.cr_utility.dataloader import *
# from engine.corerec.cr_utility.dataset import GraphDataset  # Use GraphDataset from engine.datasets

# Optimizers (Boosters)
from engine.corerec.cr_boosters.adam import *
from engine.corerec.cr_boosters.nadam import *
from engine.corerec.cr_boosters.adamax import *
from engine.corerec.cr_boosters.optimizer import *
from engine.corerec.cr_boosters.adadelta import *
from engine.corerec.cr_boosters.adagrad import *
from engine.corerec.cr_boosters.asgd import *
from engine.corerec.cr_boosters.lbfgs import *
from engine.corerec.cr_boosters.rmsprop import *
from engine.corerec.cr_boosters.sgd import *
from engine.corerec.cr_boosters.sparse_adam import *

# Promoted script to engine.cr_utility.dataset
# from engine.corerec.cr_utility.dataset import GraphDataset

__all__ = [
    # Core models
    "GraphTransformerV2",
    "GATConv",
    "GCNConv",
    "HANConv",
    "SAGEConv",
    
    # Training and prediction functions
    "train_model",
    "predict",
    "explainable_predict",
    "jaccard_similarity",
    "adamic_adar_index",
    "aaj_accuracy",
    
    # Dataloaders and datasets
    "GraphDataset",
    
    # Optimizers (Boosters)
    "Adam",
    "Nadam",
    "Adamax",
    "Optimizer",
    "Adadelta",
    "Adagrad",
    "ASGD",
    "LBFGS",
    "RMSprop",
    "SGD",
    "SparseAdam",
]