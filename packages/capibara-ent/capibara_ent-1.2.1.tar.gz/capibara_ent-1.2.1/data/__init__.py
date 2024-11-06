"""
Data package for CapibaraENT model.

This package provides utilities for data loading and preprocessing.

Modules:
    data_loader: Provides data loading functionality.
    dataset: Provides dataset handling functionality.
"""

# Importar las clases necesarias
# Importar la clase CapibaraDataLoader
from .data_loader import CapibaraDataLoader
# Importar la clase MultilingualDataset
from .dataset import MultilingualDataset

__all__ = [
    'CapibaraDataLoader',
    'MultilingualDataset'
]
