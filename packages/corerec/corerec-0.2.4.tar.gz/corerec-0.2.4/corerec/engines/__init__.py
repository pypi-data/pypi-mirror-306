# engines/__init__.py
# this is to be used for the new engine structure

# from .contentFilterEngine import CollaborativeFilteringEngine
# from .unionizedFilterEngine import UnionizedFilterEngine
from .hybrid import HybridEngine   #to be implemented
# from .content_based import ContentBasedFilteringEngine   #not used anymore

# Alias the package to UF_Engine 
# Note: Alias is not used anymore
# import corerec.engines.unionizedFilterEngine as UF_Engine
# import corerec.engines.contentFilterEngine as CF_Engine
  

# __all__ = [
#     'CollaborativeFilteringEngine',
#     'ContentBasedFilteringEngine',
#     'HybridEngine',
#     'UF_Engine',
#     'CF_Engine',
# ]
