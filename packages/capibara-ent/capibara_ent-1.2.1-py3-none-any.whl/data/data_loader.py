"""
Data loader module for CapibaraENT model.

This module provides utilities for loading and preprocessing data
for training and inference.

Classes:
    CapibaraDataLoader: Main data loader class for handling datasets.
"""

# Standard library imports
from typing import Dict, List, Optional, Tuple, Union, Iterator, Any
from pathlib import Path
import tensorflow_datasets as tfds  # type: ignore

# Third-party imports
import logging
import jax.numpy as jnp      # type: ignore
from transformers import PreTrainedTokenizer  # type: ignore

# Local imports
from data.dataset import MultilingualDataset
from ..core.config import CapibaraConfig  # type: ignore

logger = logging.getLogger(__name__)


class CapibaraDataLoader:
    """
    Data loader for CapibaraENT model training and inference.

    Handles data loading, preprocessing, and batching operations.
    """

    def __init__(
        self,
        config: CapibaraConfig,
        tokenizer: PreTrainedTokenizer,
        dataset_name: str,
        batch_size: int = 32,
        shuffle: bool = True,
        num_workers: int = 4
    ):
        self.config = config
        self.tokenizer = tokenizer
        self.dataset = self._load_data(dataset_name)
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers

        # Create data loader
        self._create_loader()

    def _create_loader(self) -> None:
        """Crea un iterador para los datos."""
        self.data_iterator = self._data_generator()

    def _data_generator(self):
        """Generador para iterar sobre los datos en lotes."""
        indices = jnp.arange(len(self.dataset))
        if self.shuffle:
            indices = jax.random.permutation(jax.random.PRNGKey(0), indices)

        for i in range(0, len(indices), self.batch_size):
            batch_indices = indices[i:i+self.batch_size]
            yield self._collate_fn([self.dataset[idx] for idx in batch_indices])

    def _collate_fn(self, batch: List[Dict]) -> Dict[str, jnp.ndarray]:
        """Custom collate function for creating batches."""
        return {
            'input_ids': jnp.array([x['input_ids'] for x in batch]),
            'attention_mask': jnp.array([x['attention_mask'] for x in batch]),
            'labels': jnp.array([x['labels'] for x in batch])
        }

    def __iter__(self) -> Iterator:
        """Retorna el iterador sobre los lotes."""
        return self._data_generator()

    def __len__(self) -> int:
        """Retorna el número de lotes."""
        return (len(self.dataset) + self.batch_size - 1) // self.batch_size

    def _load_data(self, dataset_name: str) -> List[Dict[str, Any]]:
        """Carga el dataset usando TensorFlow Datasets."""
        try:
            dataset, info = tfds.load(
                dataset_name, with_info=True, as_supervised=True)
            return dataset['train']  # Retorna el conjunto de entrenamiento
        except Exception as e:
            logger.error(f"Error al cargar el dataset {dataset_name}: {e}")
            return []  # Retorna una lista vacía en caso de error
