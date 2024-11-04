import tensorflow as tf
import numpy as np
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from CRM_tensorflow import ComplexRatioMask

def test_ComplexRatioMask():
    # Define the input shape and create some dummy data
    batch_size = 32
    time_steps = 100
    freq_bins = 257  # Complex input: real and imaginary parts
    
    # Dummy input data
    x_real = np.random.randn(batch_size, time_steps, freq_bins)
    x_imag = np.random.randn(batch_size, time_steps, freq_bins)
    mask_real = np.ones([batch_size, time_steps, freq_bins])
    mask_imag = np.ones([batch_size, time_steps, freq_bins])
    
    # Create an instance of CRMLayer with every mode
    crm_layer_e = ComplexRatioMask(masking_mode='E')
    crm_layer_c = ComplexRatioMask(masking_mode='C')
    crm_layer_r = ComplexRatioMask(masking_mode='R')
    
    # Forward pass through the layers
    estimated_speech = crm_layer_e(x_real, x_imag ,mask_real, mask_imag)
    assert estimated_speech.shape == (batch_size, time_steps, freq_bins)

    estimated_speech = crm_layer_c(x_real, x_imag ,mask_real, mask_imag)
    assert estimated_speech.shape == (batch_size, time_steps, freq_bins)

    estimated_speech = crm_layer_r(x_real, x_imag ,mask_real, mask_imag)
    assert estimated_speech.shape == (batch_size, time_steps, freq_bins)
    
    # Print a summary of the test
    print("\nComplexRatioMask test passed successfully.")

test_ComplexRatioMask()
