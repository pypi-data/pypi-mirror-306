"""
Módulo que implementa una capa BitNet para redes neuronales usando JAX/Flax.

Este módulo proporciona una implementación de la capa BitNet, que utiliza
convoluciones 1D agrupadas y una activación GELU para procesar arrays de entrada.

Clases:
    BitNetLayer: Implementa una capa BitNet.

Dependencias:
    - jax: Para operaciones de arrays y diferenciación automática.
    - flax: Para definiciones de módulos de redes neuronales.
"""

import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
import jax.nn  # type: ignore
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


class BitNet(nn.Module):
    """
    Implementación de una capa BitNet con convolución 1D y activación GELU.

    Esta capa aplica una convolución 1D seguida de activación GELU, con opciones
    para agrupamiento, dropout y normalización por capas.

    Atributos:
        in_dim (int): Número de canales de entrada.
        out_dim (int): Número de canales de salida.
        kernel_size (int): Tamaño del kernel de convolución.
        groups (int): Número de grupos para la convolución agrupada.
        dropout_rate (float): Tasa de dropout para regularización.
        use_layer_norm (bool): Si se usa normalización por capas.
    """

    in_dim: int
    out_dim: int
    kernel_size: int = 3
    groups: int = 1  # Cambiado de None a 1
    dropout_rate: float = 0.1
    use_layer_norm: bool = True

    @nn.compact
    def __call__(self, x: jnp.ndarray, training: bool = True) -> jnp.ndarray:
        """
        Paso hacia adelante de BitNetLayer.

        Args:
            x (jnp.ndarray): Array de entrada de forma (batch_size, sequence_length, in_dim).
            training (bool): Indica si el modelo está en modo de entrenamiento.

        Returns:
            jnp.ndarray: Array de salida de forma (batch_size, sequence_length, out_dim).
        """
        logger.debug(
            f"Comenzando el paso hacia adelante con forma de entrada: {x.shape}")
        self._validate_input(x)

        groups = self.groups or self.in_dim
        if self.in_dim % groups != 0 or self.out_dim % groups != 0:
            error_msg = f"La dimensión de entrada ({self.in_dim}) y la dimensión de salida ({self.out_dim}) " \
                f"deben ser divisibles por el número de grupos ({groups})."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Transponemos la entrada para la convolución 1D
        # Ahora x tiene forma (batch_size, in_dim, sequence_length)
        x = jnp.transpose(x, (0, 2, 1))
        logger.debug(f"Forma de entrada transpuesta: {x.shape}")

        # Aplicamos la convolución 1D
        x = nn.Conv(
            features=self.out_dim,
            kernel_size=(self.kernel_size,),
            padding='SAME',  # Usamos padding 'SAME' para mantener la longitud de la secuencia
            feature_group_count=groups,
            use_bias=False
        )(x)
        logger.debug(f"Forma después de la convolución: {x.shape}")

        # Aplicamos la activación GELU
        x = jax.nn.gelu(x)
        logger.debug("Aplicada activación GELU")

        # Aplicamos Dropout si estamos en entrenamiento
        x = nn.Dropout(rate=self.dropout_rate)(x, deterministic=not training)
        logger.debug(f"Aplicado dropout con tasa {self.dropout_rate}")

        # Transponemos de vuelta
        # Regresamos a la forma (batch_size, sequence_length, out_dim)
        x = jnp.transpose(x, (0, 2, 1))
        logger.debug(f"Forma final después de transponer: {x.shape}")

        # Aplicamos LayerNorm si está habilitado
        if self.use_layer_norm:
            x = nn.LayerNorm()(x)
            logger.debug("Aplicada normalización por capas")

        logger.info(
            f"Paso hacia adelante completado. Forma de salida: {x.shape}")
        return x

    def _validate_input(self, x: jnp.ndarray):
        """Valida las dimensiones del array de entrada."""
        if x.ndim != 3:
            error_msg = f"Se esperaba un array de entrada con 3 dimensiones (batch_size, sequence_length, in_dim), " \
                f"pero se obtuvo {x.ndim} dimensiones."
            logger.error(error_msg)
            raise ValueError(error_msg)
        if x.shape[-1] != self.in_dim:
            error_msg = f"Se esperaba un número de canales de entrada {
                self.in_dim}, pero se obtuvo {x.shape[-1]}."
            logger.error(error_msg)
            raise ValueError(error_msg)
        if x.shape[1] < self.kernel_size:
            error_msg = f"La longitud de la secuencia debe ser al menos {self.kernel_size} " \
                f"para aplicar una convolución con kernel_size={
                    self.kernel_size}."
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.debug("Validación de entrada pasada")

    def get_config(self) -> dict:
        """
        Obtiene la configuración de BitNetLayer.

        Returns:
            dict: Un diccionario que contiene la configuración de la capa.
        """
        config = {
            "in_dim": self.in_dim,
            "out_dim": self.out_dim,
            "kernel_size": self.kernel_size,
            "groups": self.groups,
            "dropout_rate": self.dropout_rate,
            "use_layer_norm": self.use_layer_norm
        }
        logger.info(f"Configuración de la capa obtenida: {config}")
        return config


# Ejemplo de uso
if __name__ == "__main__":
    try:
        logger.info("Iniciando ejemplo de BitNetLayer")

        # Crear un array de entrada de ejemplo
        batch_size, in_dim, sequence_length = 32, 64, 128
        x = jax.random.normal(jax.random.PRNGKey(
            0), (batch_size, sequence_length, in_dim))
        logger.info(f"Array de entrada creado con forma: {x.shape}")

        # Inicializar BitNet
        layer = BitNet(in_dim=64, out_dim=128, kernel_size=3,
                       groups=16, dropout_rate=0.1, use_layer_norm=True)
        logger.info("BitNet inicializado")

        # Inicializar parámetros
        params = layer.init(jax.random.PRNGKey(1), x)
        logger.info("Parámetros de la capa inicializados")

        # Realizar el paso hacia adelante
        # Especificamos training=True
        output = layer.apply(params, x, training=True)
        logger.info(f"Paso hacia adelante realizado. Forma de salida: {
                    output.shape}")

        print(f"Forma de entrada: {x.shape}")
        print(f"Forma de salida: {output.shape}")
        print(f"Configuración de la capa: {layer.get_config()}")

        logger.info("El ejemplo de BitNetLayer se completó exitosamente")
    except Exception as e:
        logger.exception(
            f"Ocurrió un error durante el ejemplo de BitNetLayer: {str(e)}")
