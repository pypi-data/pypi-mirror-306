"""
Módulo que implementa una capa de Auto-Atención (Self-Attention) para redes neuronales usando JAX/Flax.

Este módulo proporciona una implementación de la capa de Auto-Atención,
que utiliza atención multi-cabeza y normalización por capas para procesar
arrays de entrada.

Clases:
    SelfAttentionLayer: Implementa una capa de Auto-Atención.

Dependencias:
    - jax: Para operaciones de arrays y diferenciación automática.
    - flax: Para definiciones de módulos de redes neuronales.
"""

import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
from flax import linen as nn  # type: ignore
import logging
from typing import Optional

# Configuración de logging consistente
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseLayer(nn.Module):
    """Base class for all Capibara layers."""

    def get_config(self) -> dict:
        """Get layer configuration."""
        raise NotImplementedError


# Agregar constantes para valores por defecto
DEFAULT_DROPOUT_RATE = 0.1
DEFAULT_LAYER_DROP_PROB = 0.1


class SelfAttention(nn.Module):
    """
    SelfAttentionLayer: Una capa de auto-atención flexible con atención multi-cabeza,
    normalización por capas, dropout y LayerDrop opcional.

    Esta capa implementa atención multi-cabeza con normalización previa,
    dropout para regularización y LayerDrop opcional para eficiencia.

    Atributos:
        embed_dim (int): Dimensión del embedding.
        num_heads (int): Número de cabezas de atención.
        dropout_rate (float): Tasa de dropout para regularización.
        layer_drop_prob (float): Probabilidad de omitir la capa durante el entrenamiento.
    """
    embed_dim: int
    num_heads: int
    dropout_rate: float = DEFAULT_DROPOUT_RATE
    layer_drop_prob: float = DEFAULT_LAYER_DROP_PROB

    def __post_init__(self):
        if self.embed_dim < 1:
            raise ValueError("embed_dim must be at least 1.")
        if self.num_heads < 1:
            raise ValueError("num_heads must be at least 1.")
        if not 0.0 <= self.dropout_rate < 1.0:
            raise ValueError("dropout_rate must be in the range [0.0, 1.0).")
        if not 0.0 <= self.layer_drop_prob < 1.0:
            raise ValueError(
                "layer_drop_prob must be in the range [0.0, 1.0).")
        if self.embed_dim % self.num_heads != 0:
            raise ValueError("embed_dim must be divisible by num_heads.")

    @nn.compact
    def __call__(self,
                 x: jnp.ndarray,
                 attn_mask: Optional[jnp.ndarray] = None,
                 training: bool = True) -> jnp.ndarray:
        """
        Args:
            x: Array de entrada (batch_size, seq_len, embed_dim)
            attn_mask: Máscara de atención opcional
            training: Modo de entrenamiento
        Returns:
            jnp.ndarray: Array de salida (batch_size, seq_len, embed_dim)
        """
        self._validate_input(x)
        logger.debug(f"Input shape: {x.shape}")

        # Aplicar LayerDrop
        if training:
            layerdrop_rng = self.make_rng('layerdrop')
            layerdrop_prob = jax.random.uniform(layerdrop_rng)
            if layerdrop_prob < self.layer_drop_prob:
                logger.debug("Applying LayerDrop: skipping this layer")
                return x

        # Aplicar normalización previa
        normalized_x = nn.LayerNorm()(x)
        logger.debug(f"Normalized input shape: {normalized_x.shape}")

        # Ajustar la máscara de atención si es necesario
        if attn_mask is not None:
            if attn_mask.ndim == 2:
                # Expandir la máscara para que tenga forma (batch_size, 1, seq_len, seq_len)
                attn_mask = attn_mask[None, None, :, :]
            elif attn_mask.ndim == 3:
                # Expandir la máscara para que tenga forma (batch_size, num_heads, seq_len, seq_len)
                attn_mask = attn_mask[:, None, :, :]
            elif attn_mask.ndim != 4:
                raise ValueError("attn_mask must have 2, 3, or 4 dimensions.")

        # Realizar auto-atención
        attn_output = nn.SelfAttention(
            num_heads=self.num_heads,
            dropout_rate=self.dropout_rate
        )(normalized_x, deterministic=not training, mask=attn_mask)
        logger.debug(f"Attention output shape: {attn_output.shape}")

        # Aplicar dropout a la salida de atención
        attn_output = nn.Dropout(rate=self.dropout_rate)(
            attn_output, deterministic=not training)
        logger.debug(f"Attention output shape after dropout: {
                     attn_output.shape}")

        # Agregar conexión residual
        x = x + attn_output
        logger.debug(f"Output shape after residual connection: {x.shape}")

        # Aplicar dropout final
        x = nn.Dropout(rate=self.dropout_rate)(x, deterministic=not training)
        logger.debug(f"Output shape after final dropout: {x.shape}")

        return x

    def _validate_input(self, x: jnp.ndarray):
        """Valida las dimensiones del array de entrada."""
        if x.ndim != 3:
            error_msg = f"Expected input array with 3 dimensions (batch_size, seq_len, embed_dim), but got {
                x.ndim} dimensions."
            logger.error(error_msg)
            raise ValueError(error_msg)
        if x.shape[-1] != self.embed_dim:
            error_msg = f"Expected embed_dim to be {
                self.embed_dim}, but got {x.shape[-1]}."
            logger.error(error_msg)
            raise ValueError(error_msg)

    def get_config(self) -> dict:
        """
        Obtiene la configuración de SelfAttentionLayer.

        Returns:
            dict: Un diccionario que contiene la configuración de la capa.
        """
        config = {
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "dropout_rate": self.dropout_rate,
            "layer_drop_prob": self.layer_drop_prob
        }
        logger.debug(f"Layer config: {config}")
        return config


# Ejemplo de uso
if __name__ == "__main__":
    try:
        logger.info("Iniciando ejemplo de SelfAttentionLayer")

        # Crear un array de entrada de ejemplo
        batch_size, seq_len, embed_dim = 32, 10, 256
        x = jax.random.normal(jax.random.PRNGKey(
            0), (batch_size, seq_len, embed_dim))
        logger.info(f"Array de entrada creado con forma {x.shape}")

        # Crear una máscara de atención de ejemplo
        attn_mask = jnp.tril(jnp.ones((seq_len, seq_len))).astype(
            bool)  # Máscara triangular inferior
        logger.info(f"Máscara de atención creada con forma {attn_mask.shape}")

        # Inicializar SelfAttentionLayer
        layer = SelfAttention(
            embed_dim=256,
            num_heads=8,
            dropout_rate=0.1,
            layer_drop_prob=0.1
        )
        logger.info("SelfAttentionLayer inicializado")

        # Inicializar parámetros
        rngs = {
            'params': jax.random.PRNGKey(1),
            'dropout': jax.random.PRNGKey(2),
            'layerdrop': jax.random.PRNGKey(3)
        }
        params = layer.init(rngs, x, attn_mask, training=True)
        logger.info("Parámetros de la capa inicializados")

        # Realizar el paso hacia adelante
        output = layer.apply(params, x, attn_mask, training=True, rngs=rngs)
        logger.info(f"Paso hacia adelante realizado. Forma de salida: {
                    output.shape}")

        print(f"Forma de entrada: {x.shape}")
        print(f"Forma de salida: {output.shape}")
        print(f"Configuración de la capa: {layer.get_config()}")

        logger.info("El ejemplo de SelfAttentionLayer se completó exitosamente")
    except Exception as e:
        logger.exception(
            f"Ocurrió un error durante el ejemplo de SelfAttentionLayer: {str(e)}")
