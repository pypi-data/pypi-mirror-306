"""
Módulo que implementa una capa Platonic para redes neuronales usando JAX/Flax.

Este módulo proporciona una implementación de la capa Platonic, que utiliza
embeddings de frases para transformar texto de entrada en conceptos abstractos o ideas.

Clases:
    PlatonicLayer: Implementa una capa Platonic.

Dependencias:
    - jax: Para operaciones de arrays y diferenciación automática.
    - flax: Para definiciones de módulos de redes neuronales.
    - transformers: Para modelos de lenguaje compatibles con JAX/Flax.
"""

import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
from flax import linen as nn  # type: ignore
from typing import List, Dict, Tuple, Any
import logging
from transformers import FlaxAutoModel, AutoTokenizer  # type: ignore
import os

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


class Platonic(nn.Module):
    """
    Una implementación de la capa Platonic que transforma texto en conceptos abstractos.

    Esta capa utiliza embeddings de frases generados por un modelo compatible con JAX/Flax
    para comparar el texto de entrada con conceptos arquetípicos predefinidos y determinar
    la idea abstracta más relevante.

    Atributos:
        model_name (str): Nombre del modelo pre-entrenado para generar embeddings.
        archetypes_texts (List[str]): Lista de conceptos arquetípicos.
        similarity_threshold (float): Umbral para considerar una idea como relevante.
    """

    model_name: str
    archetypes_texts: List[str]
    similarity_threshold: float = 0.5

    def setup(self):
        # Cargar el modelo y el tokenizer de transformers compatible con Flax
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.embedding_model = FlaxAutoModel.from_pretrained(self.model_name)

        # Generar embeddings para los arquetipos
        self.archetypes = self.generate_archetypes_embeddings(
            self.archetypes_texts)

    def generate_archetypes_embeddings(self, texts: List[str]) -> Dict[str, jnp.ndarray]:
        """
        Genera embeddings para una lista de textos que representan conceptos arquetípicos.

        Args:
            texts: Lista de conceptos arquetípicos.
        Returns:
            Dict[str, jnp.ndarray]: Diccionario de {concepto: embedding}.
        """
        embeddings = {}
        for text in texts:
            inputs = self.tokenizer(
                text, return_tensors='jax', padding=True, truncation=True)
            outputs = self.embedding_model(**inputs)
            # Usamos la representación del token [CLS] como embedding
            embedding = outputs.last_hidden_state[:, 0, :]
            embeddings[text] = embedding.squeeze(0)
        return embeddings

    @nn.compact
    def __call__(self, input_texts: List[str]) -> Tuple[List[str], jnp.ndarray, Dict[str, jnp.ndarray]]:
        """
        Paso hacia adelante de PlatonicLayer.

        Args:
            input_texts (List[str]): Lista de textos de entrada.

        Returns:
            Tuple[List[str], jnp.ndarray, Dict[str, jnp.ndarray]]: Una tupla que contiene
            las ideas principales, sus puntuaciones de similitud y un diccionario con todas
            las similitudes.
        """
        self._validate_input(input_texts)

        # Generar embeddings para los textos de entrada
        inputs = self.tokenizer(
            input_texts, return_tensors='jax', padding=True, truncation=True)
        outputs = self.embedding_model(**inputs)
        # (batch_size, hidden_size)
        input_embeddings = outputs.last_hidden_state[:, 0, :]

        # Transformar los embeddings en ideas
        main_ideas, similarities, all_similarities = self.transform_to_idea(
            input_embeddings)

        return main_ideas, similarities, all_similarities

    def cosine_similarity(self, vector1: jnp.ndarray, vector2: jnp.ndarray) -> jnp.ndarray:
        """
        Calcula la similitud coseno entre dos matrices de vectores.

        Args:
            vector1 (jnp.ndarray): Matriz de vectores de forma (batch_size, hidden_size).
            vector2 (jnp.ndarray): Matriz de vectores de forma (num_archetypes, hidden_size).

        Returns:
            jnp.ndarray: Matriz de similitudes normalizada en [-1, 1].
        """
        vector1_norm = vector1 / \
            jnp.linalg.norm(vector1, axis=1, keepdims=True)
        vector2_norm = vector2 / \
            jnp.linalg.norm(vector2, axis=1, keepdims=True)
        similarity = jnp.matmul(vector1_norm, vector2_norm.T)
        return similarity

    def transform_to_idea(self, input_embeddings: jnp.ndarray) -> Tuple[List[str], jnp.ndarray, Dict[str, jnp.ndarray]]:
        """
        Transforma los embeddings de entrada en conceptos abstractos comparándolos con los arquetipos.

        Args:
            input_embeddings (jnp.ndarray): Embeddings de los textos de entrada.

        Returns:
            Tuple[List[str], jnp.ndarray, Dict[str, jnp.ndarray]]: Ideas principales, similitudes máximas y todas las similitudes.
        """
        # Obtener los embeddings de los arquetipos
        # (num_archetypes, hidden_size)
        archetype_embeddings = jnp.stack(list(self.archetypes.values()))

        # Calcular similitudes
        similarities = self.cosine_similarity(
            # (batch_size, num_archetypes)
            input_embeddings, archetype_embeddings)

        # Obtener las ideas principales y sus similitudes
        max_indices = jnp.argmax(similarities, axis=1)
        max_similarities = jnp.max(similarities, axis=1)

        main_ideas = [list(self.archetypes.keys())[idx] for idx in max_indices]
        all_similarities = {concept: similarities[:, idx] for idx, concept in enumerate(
            self.archetypes.keys())}

        return main_ideas, max_similarities, all_similarities

    def _validate_input(self, input_texts: List[str]):
        """Valida los textos de entrada."""
        if not isinstance(input_texts, list):
            raise ValueError(f"Expected input to be a list of strings, but got {
                             type(input_texts)}.")
        if not all(isinstance(text, str) for text in input_texts):
            raise ValueError("All elements in input_texts must be strings.")
        if len(input_texts) == 0:
            raise ValueError("Input list cannot be empty.")

    def get_config(self) -> Dict[str, Any]:
        """
        Obtiene la configuración de la PlatonicLayer.

        Returns:
            Dict[str, Any]: Un diccionario que contiene la configuración de la capa.
        """
        return {
            "model_name": self.model_name,
            "archetypes": self.archetypes_texts,
            "similarity_threshold": self.similarity_threshold
        }

    def interpret_result(self, main_ideas: List[str], similarities: jnp.ndarray, all_similarities: Dict[str, jnp.ndarray]) -> List[str]:
        """
        Interpreta el resultado de la transformación de ideas.

        Args:
            main_ideas (List[str]): Las ideas principales identificadas.
            similarities (jnp.ndarray): Las puntuaciones de similitud de las ideas principales.
            all_similarities (Dict[str, jnp.ndarray]): Diccionario con todas las similitudes.

        Returns:
            List[str]: Lista de interpretaciones en lenguaje natural de los resultados.
        """
        interpretations = []
        for idx, (idea, sim) in enumerate(zip(main_ideas, similarities)):
            sim_value = sim.item()
            if sim_value < self.similarity_threshold:
                interpretation = f"El texto no se alinea fuertemente con ningún concepto platónico. La idea más cercana es '{
                    idea}' con una similitud de {sim_value:.2f}."
            else:
                other_ideas = [f"'{concept}' ({all_similarities[concept][idx]:.2f})"
                               for concept in self.archetypes_texts if concept != idea]
                interpretation = f"El texto se alinea principalmente con el concepto platónico de '{
                    idea}' (similitud: {sim_value:.2f}). También muestra alineación con {', '.join(other_ideas)}."
            interpretations.append(interpretation)
        return interpretations


# Ejemplo de uso
if __name__ == "__main__":
    try:
        logger.info("Iniciando ejemplo de PlatonicLayer")

        # Definir los conceptos arquetípicos
        archetypes = ["Justicia", "Belleza", "Bondad", "Verdad"]

        # Inicializar la PlatonicLayer
        layer = Platonic(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            archetypes_texts=archetypes,
            similarity_threshold=0.5
        )

        # Crear textos de entrada
        input_texts = [
            "La importancia de la verdad en la sociedad actual",
            "La belleza de la naturaleza es inspiradora",
            "Debemos luchar por la justicia y la igualdad",
            "Actuar con bondad hacia los demás"
        ]

        # Inicializar parámetros (aunque no es necesario en este caso)
        params = layer.init(jax.random.PRNGKey(0), input_texts)

        # Realizar el paso hacia adelante
        main_ideas, similarities, all_similarities = layer.apply(
            params, input_texts)

        # Interpretar los resultados
        interpretations = layer.interpret_result(
            main_ideas, similarities, all_similarities)

        for text, idea, sim, interpretation in zip(input_texts, main_ideas, similarities, interpretations):
            print(f"Texto de entrada: {text}")
            print(f"Idea principal: {idea}")
            print(f"Similitud: {sim:.2f}")
            print(f"Interpretación: {interpretation}")
            print("-" * 50)

        logger.info("El ejemplo de PlatonicLayer se completó exitosamente")
    except Exception as e:
        logger.exception(
            "Ocurrió un error durante el ejemplo de PlatonicLayer: %s", str(e))
