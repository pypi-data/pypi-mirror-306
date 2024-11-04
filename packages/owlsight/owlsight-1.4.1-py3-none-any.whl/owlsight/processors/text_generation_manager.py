from typing import Any, Optional
import traceback
import pkgutil

from owlsight.processors.text_generation_processor import (
    TextGenerationProcessor,
    select_processor_type,
)
from owlsight.configurations.config_manager import ConfigManager
from owlsight.utils.helper_functions import convert_to_real_type
from owlsight.utils.deep_learning import free_memory
from owlsight.rag.python_lib_search import search_python_libs
from owlsight.utils.constants import get_pickle_cache
from owlsight.utils.logger_manager import LoggerManager

logger = LoggerManager.get_logger(__name__)


class TextGenerationManager:
    def __init__(self, config_manager: ConfigManager):
        """
        Manage the lifecycle of a TextGenerationProcessor and its interaction with the configuration.

        Parameters
        ----------
        processor : TextGenerationProcessor
            An instance of the processor (either Transformers or Onnx).
        config_manager : ConfigManager
            Configuration dictionary to manage settings for the processor.
        """
        self.config_manager = config_manager
        self.processor: Optional[TextGenerationProcessor] = None

    def generate(self, input_text: str):
        """
        Generate text using the processor.
        """
        kwargs = self.config_manager.get("generate", {})
        generated_text = self.processor.generate(input_text, **kwargs)
        return generated_text

    def update_config(self, key: str, value: Any):
        """
        Update the configuration dynamically. If 'model_id' is updated, reload the processor.
        """
        if key.endswith(".back"):
            return  # Do not set the "back" key
        try:
            value = convert_to_real_type(value)
            self.config_manager.set(key, value)
            logger.info(f"Configuration updated: {key} = {value}")
        except Exception:
            logger.error(
                f"Error updating configuration for key '{key}': {traceback.format_exc()}"
            )
            return

        # If 'model_id' is updated, reload the processor
        outer_key, inner_key = key.split(".", 1)
        if outer_key == "model":
            if inner_key == "model_id":
                self.load_model_processor(reload=self.processor is not None)
            else:
                if self.processor is None:
                    logger.error(
                        "Processor is not initialized yet. Assign a model_id first, to initialize a model for the processor."
                    )
                    return
                if hasattr(self.processor, inner_key):
                    setattr(self.processor, inner_key, value)
                    logger.info(f"Processor updated: {inner_key} = {value}")
                else:
                    logger.warning(
                        f"'{inner_key}' not found in self.processor, meaning it was not updated"
                    )
                    logger.warning(
                        "It is possible that this value is only set during initialization of self.processor."
                    )
                    logger.warning(
                        "Consider loading the model from a config file to update this value."
                    )
        elif outer_key == "rag":
            rag_is_active = self.config_manager.get("rag.active", False)
            if rag_is_active:
                library = self.config_manager.get("rag.target_library", "")
                if not library:
                    logger.error(
                        "No library provided. Please set a library in the configuration."
                    )
                    return

                # get all libs without the _ prefix and in sorted order
                available_libraries = [module.name for module in pkgutil.iter_modules() if not module.name.startswith("_")]
                if library not in available_libraries:
                    logger.error(
                        f"Library '{library}' not found in the current Python session."
                    )
                    logger.error(f"available libraries: {sorted(available_libraries)}")
                    return
                elif inner_key == "search_query":
                    search_query = self.config_manager.get("rag.search_query", "")
                    if not search_query:
                        logger.error(
                            "No example prompt provided. Please set an example prompt in the configuration."
                        )
                        return
                    top_k = self.config_manager.get("rag.top_k", 3)
                    context = search_python_libs(library, search_query, top_k, cache_dir=get_pickle_cache())
                    print(f"Context for library '{library}' with top_k={top_k}:\n{context}")


    def save_config(self, path: str):
        """
        Save the configuration to a file.
        """
        self.config_manager.save(path)

    def load_config(self, path: str):
        """
        Load the configuration from a file.
        """
        loading_succesful = self.config_manager.load(path)
        if loading_succesful:
            self.load_model_processor(reload=self.processor is not None)

    def load_model_processor(self, reload=False):
        """
        Load the model processor with a 'model_id', to load the correct model and tokenizer.

        Parameters
        ----------
        reload : bool, optional
            If True, reload the processor with the same model_id, by default False.
            Assumes that the processor is already initialized with another model.
        """
        model_id = self.config_manager.get("model.model_id", "")
        if not model_id:
            logger.error(
                "No model_id provided. Please set a model_id in the configuration."
            )
            return

        logger.info(f"Loading processor with new model_id: {model_id}")

        try:
            if reload:
                if self.processor is None:
                    raise ValueError("Processor is not initialized yet. Cannot reload.")
                # Save the history from the old processor
                old_history = self.processor.history
                processor_type = self.processor.__class__

                # Inmediately overwrite the processor with a new instance to save memory
                self.processor = None
                free_memory()

                self.processor = processor_type(**self.config_manager.get("model", {}))
                self.processor.history = old_history
            else:
                processor_type = select_processor_type(model_id)
                self.processor = processor_type(**self.config_manager.get("model", {}))
        except Exception:
            logger.error(f"Error loading  model_processor: {traceback.format_exc()}")
            return

        logger.info(f"Processor reloaded with model_id: {model_id}")

    def get_processor(self) -> TextGenerationProcessor:
        """
        Return the current processor instance.
        """
        return self.processor

    def get_config(self) -> dict:
        """
        Return the current configuration as dictionary.
        """
        return self.config_manager._config

    def get_config_choices(self) -> dict:
        """
        Return the available configuration choices.

        Returns
        -------
        dict
            Dictionary with the available configuration choices.
        """
        return self.config_manager.config_choices

    def get_config_key(self, key: str, default: Any = None) -> Any:
        """
        Get the value of a key in the configuration.
        """
        return self.config_manager.get(key, default)
