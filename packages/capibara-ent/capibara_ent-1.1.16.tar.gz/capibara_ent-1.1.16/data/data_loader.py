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

# Third-party imports
import logging
import jax.numpy as jnp
from transformers import PreTrainedTokenizer

# Local imports
from data.dataset import MultilingualDataset
from ..core.config import CapibaraConfig

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
        dataset_path: Union[str, Path],
        batch_size: int = 32,
        shuffle: bool = True,
        num_workers: int = 4
    ):
        self.config = config
        self.tokenizer = tokenizer
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.num_workers = num_workers

        # Inicializar dataset
        self.dataset = MultilingualDataset(
            data=self._load_data(dataset_path),
            supported_languages=config.supported_languages,
            tokenizer=tokenizer,
            max_length=config.max_sequence_length
        )

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

    def _load_data(self, dataset_path: Union[str, Path]) -> List[Dict[str, Any]]:
        # Implementar la lógica para cargar los datos del dataset_path
        try:
            # Aquí iría la lógica real para cargar los datos
            # Por ahora, retornamos una lista vacía como ejemplo
            return []
        except Exception as e:
            logger.error(f"Error al cargar los datos: {e}")
            return []  # Retornamos una lista vacía en caso de error
