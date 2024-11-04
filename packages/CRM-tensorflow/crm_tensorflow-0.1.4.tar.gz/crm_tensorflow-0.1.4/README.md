
# A non-official implementation of the Complex Ratio Mask (CRM) technique as a Tensorflow layer.

Implementation of the the Complex Ratio Mask (CRM) technique used in ["DCCRN: Deep Complex Convolution Recurrent Network for Phase-Aware Speech Enhancement"](https://arxiv.org/abs/2008.00264).

## Installlation
```bash
pip install CRM_tensorflow
```
## Usage
```python
import tensorflow as tf 
from CRM_tensorflow import ComplexRatioMask

# Input parameters
time_dim = 100
freq_dim = 257
batch_size = 100

# Define layer
crm_layer = ComplexRatioMask(masking_mode='E') # Other modes include 'C' and 'R'. See paper for more information.

# Random noisy signal split in real and imag. components
random_spectrogram_real = tf.random.normal((batch_size,time_dim, freq_dim))
random_spectrogram_imag = tf.random.normal((batch_size,time_dim, freq_dim))

# Random complex mask split in real and imag. components
random_mask_real = tf.random.normal((batch_size,time_dim, freq_dim))
random_mask_imag = tf.random.normal((batch_size,time_dim, freq_dim))

enhanced_speech_signal = crm_layer(random_spectrogram_real, random_spectrogram_imag, random_mask_real, random_mask_imag)

```
