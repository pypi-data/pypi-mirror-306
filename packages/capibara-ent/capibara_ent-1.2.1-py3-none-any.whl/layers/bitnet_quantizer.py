"""
Módulo que implementa un cuantizador BitNet para redes neuronales usando JAX/Flax.

Este módulo proporciona una capa de cuantización que puede utilizarse
para reducir la precisión de pesos y activaciones en una red neuronal,
resultando en modelos más eficientes en términos de memoria y computación.

Clases:
    BitNetQuantizer: Implementa cuantización estilo BitNet.

Dependencias:
    - jax: Para operaciones de arrays y diferenciación automática.
    - flax: Para definiciones de módulos de redes neuronales.
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


class BitNetQuantizer(nn.Module):
    """
    Módulo de cuantización para cuantización estilo BitNet.

    Este módulo realiza la cuantización de arrays de entrada a una anchura de bits especificada,
    soportando cuantización simétrica y asimétrica, y permitiendo la estimación del gradiente
    durante la retropropagación.

    Atributos:
        bit_width (int): El número de bits a utilizar para la cuantización.
        symmetric (bool): Si se utiliza cuantización simétrica.
        eps (float): Un valor pequeño para evitar división por cero.
    """
    bit_width: int
    symmetric: bool = True
    eps: float = 1e-5

    def __post_init__(self):
        self.validate_bit_width(self.bit_width)

    def quantize(self, x):
        # Implementación de la lógica de cuantización
        if self.symmetric:
            max_val = jnp.max(jnp.abs(x), axis=None, keepdims=True)
            scale = max_val / (2**(self.bit_width - 1) - 1 + self.eps)
            x_quantized = jnp.round(x / scale)
            x_clipped = jnp.clip(
                x_quantized, -2**(self.bit_width - 1), 2**(self.bit_width - 1) - 1)
            x_dequantized = x_clipped * scale
        else:
            min_val = jnp.min(x, axis=None, keepdims=True)
            max_val = jnp.max(x, axis=None, keepdims=True)
            scale = (max_val - min_val) / (2**self.bit_width - 1 + self.eps)
            zero_point = jnp.round(-min_val / scale)
            x_quantized = jnp.round(x / scale + zero_point)
            x_clipped = jnp.clip(x_quantized, 0, 2**self.bit_width - 1)
            x_dequantized = (x_clipped - zero_point) * scale
        return x_dequantized

    @nn.compact
    def __call__(self, x):
        # Aplicamos la cuantización al tensor de entrada
        return self.quantize(x)

    @staticmethod
    def validate_bit_width(bit_width: int):
        """Valida la anchura de bits."""
        if not isinstance(bit_width, int) or bit_width < 2:
            error_msg = "`bit_width` debe ser un entero mayor o igual a 2."
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.debug(f"La anchura de bits {bit_width} es válida")

    def get_quantization_params(self, x: jnp.ndarray) -> dict:
        """
        Obtiene los parámetros de cuantización para un array dado.

        Este método es útil para análisis y depuración.

        Args:
            x (jnp.ndarray): El array de entrada.

        Returns:
            dict: Un diccionario que contiene los parámetros de cuantización.
        """
        logger.debug("Calculando parámetros de cuantización")
        if self.symmetric:
            max_val = jnp.max(jnp.abs(x))
            min_val = -max_val
            zero_point = 0.0
        else:
            max_val = jnp.max(x)
            min_val = jnp.min(x)
            zero_point = -min_val / \
                ((max_val - min_val) / (2**self.bit_width - 1 + self.eps))

        scale = (max_val - min_val) / (2**self.bit_width - 1 + self.eps)

        params = {
            "max_val": float(max_val),
            "min_val": float(min_val),
            "scale": float(scale),
            "zero_point": float(zero_point),
            "bit_width": self.bit_width,
            "symmetric": self.symmetric
        }
        logger.info(f"Parámetros de cuantización calculados: {params}")
        return params


# Ejemplo de uso
if __name__ == "__main__":
    try:
        logger.info("Iniciando ejemplo de BitNetQuantizer")

        # Crear un array de ejemplo
        key = jax.random.PRNGKey(0)
        x = jax.random.normal(key, (5, 5))
        logger.info(f"Array de ejemplo creado con forma: {x.shape}")

        # Inicializar el cuantizador
        quantizer = BitNetQuantizer(bit_width=4, symmetric=True)
        logger.info("BitNetQuantizer inicializado")

        # Inicializar parámetros (aunque no hay parámetros aprendibles)
        variables = quantizer.init(key, x)

        # Realizar cuantización
        x_quantized = quantizer.apply(variables, x)
        logger.info("Cuantización realizada")

        # Obtener parámetros de cuantización
        params = quantizer.get_quantization_params(x)
        logger.info("Parámetros de cuantización obtenidos")

        print("Array original:")
        print(x)
        print("\nArray cuantizado:")
        print(x_quantized)
        print("\nParámetros de cuantización:")
        for key, value in params.items():
            print(f"{key}: {value}")

        logger.info("El ejemplo de BitNetQuantizer se completó exitosamente")
    except Exception as e:
        logger.exception(
            f"Ocurrió un error durante el ejemplo de BitNetQuantizer: {str(e)}")
