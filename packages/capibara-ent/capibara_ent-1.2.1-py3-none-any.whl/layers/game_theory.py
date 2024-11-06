"""
Módulo que implementa una clase y funciones de teoría de juegos utilizando JAX.

Este módulo proporciona una clase `GameTheory` que implementa métodos para analizar
y procesar datos de entrada en el contexto de modelos de aprendizaje automático.

Clases:
    GameTheory: Implementa funciones de teoría de juegos.

Dependencias:
    - jax: Para operaciones de arrays y diferenciación automática.
"""

import jax.numpy as jnp  # type: ignore
from typing import Tuple, List, Any
import logging
from jax import nn  # type: ignore

# Configuración de logging consistente
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GameTheoryError(Exception):
    """Excepción personalizada para errores relacionados con Teoría de Juegos."""
    pass


class GameTheory:
    """Clase que implementa métodos para analizar juegos utilizando teoría de juegos."""

    def __init__(self):
        logger.info("Inicializando la clase GameTheory")

    def prisoners_dilemma(self, player_strategy: str, opponent_strategy: str) -> Tuple[int, int]:
        """
        Simula el juego del Dilema del Prisionero para dos jugadores.

        Args:
            player_strategy (str): Estrategia del jugador ('cooperate' o 'defect').
            opponent_strategy (str): Estrategia del oponente ('cooperate' o 'defect').

        Returns:
            Tuple[int, int]: Recompensas para el jugador y el oponente.

        Raises:
            GameTheoryError: Si se proporcionan estrategias inválidas.
        """
        logger.debug("Simulando Dilema del Prisionero con estrategias: %s, %s",
                     player_strategy, opponent_strategy)
        payoff_matrix = {
            ("cooperate", "cooperate"): (3, 3),
            ("cooperate", "defect"): (0, 5),
            ("defect", "cooperate"): (5, 0),
            ("defect", "defect"): (1, 1)
        }
        result = payoff_matrix.get((player_strategy, opponent_strategy))
        if result is None:
            error_msg = "Estrategias inválidas proporcionadas. Deben ser 'cooperate' o 'defect'."
            logger.error(error_msg)
            raise GameTheoryError(error_msg)
        logger.info("Resultado del Dilema del Prisionero: %s", result)
        return result

    def nash_equilibrium(self, payoff_matrix: jnp.ndarray) -> List[Tuple[int, int]]:
        """
        Encuentra los equilibrios de Nash en un juego de dos jugadores.

        Args:
            payoff_matrix (jnp.ndarray): Matriz de pagos con forma (num_rows, num_cols, 2).

        Returns:
            List[Tuple[int, int]]: Lista de estrategias que son equilibrios de Nash.

        Raises:
            GameTheoryError: Si la matriz de pagos no tiene la forma adecuada.
        """
        logger.debug(
            "Buscando equilibrios de Nash en matriz de pagos de forma %s", payoff_matrix.shape)
        if payoff_matrix.ndim != 3 or payoff_matrix.shape[2] != 2:
            error_msg = "La matriz de pagos debe tener forma (num_rows, num_cols, 2)."
            logger.error(error_msg)
            raise GameTheoryError(error_msg)

        num_rows, num_cols, _ = payoff_matrix.shape
        player1_payoffs = payoff_matrix[:, :, 0]
        best_responses_player1 = (
            player1_payoffs == player1_payoffs.max(axis=0, keepdims=True))
        player2_payoffs = payoff_matrix[:, :, 1]
        best_responses_player2 = (
            player2_payoffs == player2_payoffs.max(axis=1, keepdims=True))
        nash_eq_matrix = best_responses_player1 & best_responses_player2
        nash_eq_indices = jnp.argwhere(nash_eq_matrix)
        nash_eq = [tuple(index.tolist()) for index in nash_eq_indices]
        logger.info("Equilibrios de Nash encontrados: %s", nash_eq)
        return nash_eq

    def minimax(self, payoff_matrix: jnp.ndarray) -> Tuple[int, float]:
        """
        Implementa el algoritmo Minimax para determinar la estrategia óptima.

        Args:
            payoff_matrix (jnp.ndarray): Matriz de pagos del juego.

        Returns:
            Tuple[int, float]: Estrategia óptima y valor esperado.
        """
        logger.debug("Aplicando algoritmo Minimax a la matriz de pagos")
        min_values = payoff_matrix.min(axis=1)
        max_of_min = min_values.max()
        optimal_strategy = min_values.argmax()
        result = (int(optimal_strategy), float(max_of_min))
        logger.info("Resultado de Minimax: estrategia %d con valor %f",
                    optimal_strategy, max_of_min)
        return result

    def dominant_strategy(self, payoff_matrix: jnp.ndarray) -> Tuple[int, int]:
        """
        Encuentra estrategias dominantes para ambos jugadores.

        Args:
            payoff_matrix (jnp.ndarray): Matriz de pagos con forma (num_rows, num_cols, 2).

        Returns:
            Tuple[int, int]: Estrategias dominantes para los jugadores de filas y columnas.
        """
        logger.debug("Buscando estrategias dominantes en la matriz de pagos")
        num_rows, num_cols, _ = payoff_matrix.shape
        player1_payoffs = payoff_matrix[:, :, 0]
        dominant_row = None
        for i in range(num_rows):
            is_dominant = all((player1_payoffs[i, :] >= player1_payoffs[j, :]).all(
            ) for j in range(num_rows) if i != j)
            if is_dominant:
                dominant_row = i
                break

        player2_payoffs = payoff_matrix[:, :, 1]
        dominant_col = None
        for j in range(num_cols):
            is_dominant = all((player2_payoffs[:, j] >= player2_payoffs[:, k]).all(
            ) for k in range(num_cols) if j != k)
            if is_dominant:
                dominant_col = j
                break

        result = (dominant_row, dominant_col)
        logger.info("Estrategias dominantes encontradas: %s", result)
        return result


# Ejemplo de uso
if __name__ == "__main__":
    game_theory = GameTheory()
    payoff_matrix = jnp.array([
        [[3, 3], [0, 5]],
        [[5, 0], [1, 1]]
    ])
    ne_result = game_theory.nash_equilibrium(payoff_matrix)
    print("Equilibrios de Nash:", ne_result)
