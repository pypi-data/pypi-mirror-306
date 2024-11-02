# coding=utf-8
# Copyright 2020 The Gin-Config Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Contains TensorFlow-specific utilities for Gin configuration."""

from typing import Optional, Union
import os

from gin import config

import tensorflow as tf
from tensorflow.keras.callbacks import Callback


# Register TF file reader for Gin's parse_config_file.
config.register_file_reader(tf.io.gfile.GFile, tf.io.gfile.exists)


@config.configurable
def singleton_per_graph(constructor):
    """Create a singleton value per TensorFlow graph.
    
    Args:
        constructor: A callable that creates the singleton value.
        
    Returns:
        The singleton value for the current graph.
    """
    # For modern TF, we can use the default graph name as a key
    graph_key = tf.get_current_graph_name()
    key = (config.current_scope_str(), graph_key)
    return config.singleton_value(key, constructor)


class GinConfigCallback(Callback):
    """A Keras Callback that saves and summarizes the Gin operative config.

    This callback saves Gin's operative configuration to a specified directory and
    optionally summarizes it for visualization in TensorBoard.

    Note: In distributed training setups, this callback should only be used on the
    chief worker to prevent multiple events files from being created.
    """

    def __init__(
        self,
        output_dir: str,
        base_name: str = 'operative_config',
        summarize_config: bool = True,
        summary_writer: Optional[tf.summary.SummaryWriter] = None,
        include_step_in_filename: bool = True,
        save_freq: Union[int, str] = 100,
        chief_only: bool = True
    ):
        """Initialize the GinConfigCallback.

        Args:
            output_dir: Directory to save the operative config.
            base_name: Base name for the config file and summary tag.
            summarize_config: If True, saves a summary for TensorBoard.
            summary_writer: Optional tf.summary.SummaryWriter instance.
            include_step_in_filename: If True, includes step in filename.
            save_freq: Integer (every N batches) or 'epoch' string.
            chief_only: If True, only save config on chief worker in distributed training.
        """
        super().__init__()
        self._output_dir = output_dir
        self._base_name = base_name
        self._summarize_config = summarize_config
        self._summary_writer = summary_writer
        self._include_step_in_filename = include_step_in_filename
        self._save_freq = save_freq
        self._chief_only = chief_only

    def _should_save(self) -> bool:
        """Determines if the config should be saved based on distributed settings."""
        if not self._chief_only:
            return True
            
        # Check if running in a distributed setting
        if tf.distribute.has_strategy():
            strategy = tf.distribute.get_strategy()
            # Only save on chief worker
            return strategy.extended.should_checkpoint
        return True

    def on_train_begin(self, logs=None):
        """Called at the beginning of training."""
        if not self._should_save():
            return

        tf.io.gfile.makedirs(self._output_dir, exist_ok=True)

        if self._summarize_config and not self._summary_writer:
            self._summary_writer = tf.summary.create_file_writer(self._output_dir)

        # Write initial config
        self._write_config(step=0)

    def _write_config(self, step: int):
        """Writes the Gin config to file and optionally adds a summary."""
        if not self._should_save():
            return

        config_str = config.operative_config_str()

        # Save config to file
        filename = (f'{self._base_name}-{step}.gin'
                   if self._include_step_in_filename
                   else f'{self._base_name}.gin')
        
        config_path = os.path.join(self._output_dir, filename)
        with tf.io.gfile.GFile(config_path, 'w') as f:
            f.write(config_str)

        # Add summary if requested
        if self._summarize_config:
            md_config_str = config.markdown(config_str)
            with self._summary_writer.as_default():
                tf.summary.text(f'gin/{self._base_name}', md_config_str, step=step)
            self._summary_writer.flush()

    def on_train_batch_end(self, batch: int, logs=None):
        """Called at the end of each training batch."""
        if isinstance(self._save_freq, int) and batch % self._save_freq == 0:
            step = self.model.optimizer.iterations.numpy()
            self._write_config(step)

    def on_epoch_end(self, epoch: int, logs=None):
        """Called at the end of each epoch."""
        if self._save_freq == 'epoch':
            step = self.model.optimizer.iterations.numpy()
            self._write_config(step)

    def on_train_end(self, logs=None):
        """Called at the end of training."""
        if not self._should_save():
            return
            
        # Write final config
        step = self.model.optimizer.iterations.numpy()
        self._write_config(step)

        if self._summary_writer:
            self._summary_writer.close()