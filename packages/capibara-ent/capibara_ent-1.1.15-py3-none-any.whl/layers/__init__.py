# layers/__init__.py

"""
Módulo layers: Contiene todas las capas personalizadas utilizadas en el proyecto Capibara.

Clases disponibles:

Capas básicas:

- SyntheticEmbeddingLayer: Crea representaciones sintéticas mediante transformaciones lineales y activaciones GELU.

Capas Capibara:
- Capibara2: Implementa la arquitectura de red Capibara2.
- CapibaraByte: Implementa una capa tipo Capibara Byte.
- SparseCapibara: Implementa una capa optimizada para operaciones dispersas en TPUs.

Capas de atención:
- SelfAttention: Implementa una capa de auto-atención.


Capas especializadas:
- BitNet: Implementa la arquitectura de red BitNet.
- BitNetQuantizer: Implementa una capa de cuantización para la red BitNet.
- GameTheoryLayer: Implementa una capa basada en teoría de juegos.
- LiquidLayer: Implementa una capa tipo Liquid.
- MetaMAMDPLayer: Implementa una capa tipo Meta-MAMDP.
"""

# Sub_models
from sub_models.capibara_jax_ssm import CapibaraJAXSSM
from sub_models.capibara_byte import CapibaraByte
from sub_models.liquid import Liquid
from sub_models.capibara2 import Capibara2
from sub_models.aleph_Tilde import AlephModule
from sub_models.liquid import Liquid
from sub_models.meta_bamdp import MetaBAMDP
from sub_models.snns_LiCell import SNNS
from sub_models.spike_ssm import spikes

# Capas de atención
from .self_attention import SelfAttention

# Capas especializadas
from .bitnet import BitNet
from .bitnet_quantizer import BitNetQuantizer
from .game_theory import GameTheory
from .platonic import Platonic
from .sparse_capibara import SparseCapibara


__all__ = [
    # Capas básicas
    'SelfAttention',
    'SyntheticEmbedding',

    # Sub-models
    'AlephModule',
    'Capibara2',
    'CapibaraByte',
    'CapibaraJAXSSM',
    'Liquid',
    'MetaBAMDP',
    'SNNS',
    'spikes'

    # Capas especializadas
    'BitNet',
    'BitNetQuantizer',
    'GameTheory',
    'Platonic',
    'SparseCapibara',


]
