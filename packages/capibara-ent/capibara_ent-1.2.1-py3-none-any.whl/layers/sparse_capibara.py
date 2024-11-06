"""
Module that implements a SparseLayer for neural networks using JAX/Flax.

This module provides an implementation of a sparse layer,
which applies sparse operations to input data efficiently.

Classes:
    SparseLayer: Implements a sparse layer.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
"""

import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
from flax import linen as nn  # type: ignore
import logging

# Configuración de logging consistente
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Base class para layers


class BaseLayer(nn.Module):
    """Base class for all Capibara layers."""

    def get_config(self) -> dict:
        """Get layer configuration."""
        raise NotImplementedError


class SparseCapibara(nn.Module):
    """
    SparseLayer: A neural network layer that applies sparse operations
    to input data efficiently.

    Attributes:
        input_dim (int): Input dimension.
        output_dim (int): Output dimension.
        sparsity (float): Fraction of weights to set to zero (e.g., 0.5 for 50% sparsity).
    """
    input_dim: int
    output_dim: int
    sparsity: float = 0.5  # Default to 50% sparsity

    @nn.compact
    def __call__(self, x):
        """
        Forward pass of the SparseLayer.

        Args:
            x (jnp.ndarray): Input array of shape (batch_size, seq_len, input_dim).

        Returns:
            jnp.ndarray: Output array of shape (batch_size, seq_len, output_dim).
        """
        self._validate_input(x)
        batch_size, seq_len, _ = x.shape

        # Initialize the dense layer
        dense_layer = nn.Dense(self.output_dim)
        params = dense_layer.init(self.make_rng('params'), x)
        weights = params['params']['kernel']  # Shape: (input_dim, output_dim)

        # Create a mask to enforce sparsity
        mask_key = self.make_rng('dropout')
        mask = jax.random.bernoulli(
            mask_key, p=1.0 - self.sparsity, shape=weights.shape)
        sparse_weights = weights * mask

        # Replace the weights in the parameters
        params['params']['kernel'] = sparse_weights

        # Apply the dense layer with sparse weights
        # Shape: (batch_size * seq_len, input_dim)
        x_flat = x.reshape(-1, self.input_dim)
        y_flat = dense_layer.apply(params, x_flat)

        # Reshape back to (batch_size, seq_len, output_dim)
        y = y_flat.reshape(batch_size, seq_len, self.output_dim)
        return y

    def _validate_input(self, x: jnp.ndarray):
        """Validate the input array dimensions."""
        if x.ndim != 3:
            error_msg = f"Expected input array with 3 dimensions (batch_size, seq_len, input_dim), but got {
                x.ndim} dimensions."
            logger.error(error_msg)
            raise ValueError(error_msg)
        if x.shape[-1] != self.input_dim:
            error_msg = f"Expected input_dim to be {
                self.input_dim}, but got {x.shape[-1]}."
            logger.error(error_msg)
            raise ValueError(error_msg)

    def get_config(self) -> dict:
        """
        Get the configuration of the SparseLayer.

        Returns:
            dict: A dictionary containing the layer's configuration.
        """
        return {
            "input_dim": self.input_dim,
            "output_dim": self.output_dim,
            "sparsity": self.sparsity
        }


# Example usage
if __name__ == "__main__":
    try:
        # Set up logging
        logging.basicConfig(level=logging.DEBUG)

        # Create a sample input array
        batch_size, seq_len, input_dim = 32, 10, 256
        output_dim = 512
        key = jax.random.PRNGKey(0)
        x = jax.random.normal(key, (batch_size, seq_len, input_dim))

        # Initialize the SparseLayer
        layer = SparseCapibara(input_dim=input_dim,
                               output_dim=output_dim, sparsity=0.5)

        # Initialize parameters
        variables = layer.init(key, x)

        # Perform forward pass
        output = layer.apply(variables, x)

        print(f"Input shape: {x.shape}")
        print(f"Output shape: {output.shape}")
        print(f"Layer config: {layer.get_config()}")

        logger.info("SparseLayer example completed successfully")
    except Exception as e:
        logger.exception(
            f"An error occurred during the SparseLayer example: {str(e)}")
