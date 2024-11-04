import tensorflow as tf 

class ComplexRatioMask(tf.keras.layers.Layer):
    def __init__(self, masking_mode):
        super(ComplexRatioMask, self).__init__()
        self.masking_mode = masking_mode
        self.eps = 1e-8
        valid_modes = ['E', 'C', 'R'] # Taken from paper
        if masking_mode not in valid_modes:
            raise ValueError(f"Invalid masking_mode: {masking_mode}. Must be one of {valid_modes}")

    def call(self, x_real, x_imag, mask_real, mask_imag):
        '''
        Inputs:
         - x_real: real component of noisy signal
         - x_imag: imaginary component of noisy signal
         - mask_real:  real component of mask
         - mask_imag:  imaginary component of mask
         
         Returns:
         - estimated_speech: complex-valued estimated speech
        '''
        
        if self.masking_mode == 'E':
            # Compute magnitude and phase of noisy signal
            x_mag = tf.math.sqrt(tf.math.square(x_real) + tf.math.square(x_imag))
            x_phase = tf.math.atan2(x_imag,x_real)
            
            # Compute magnitude and phase of mask
            mask_real = mask_real + self.eps
            mask_mag = tf.math.sqrt(tf.square(mask_real) + tf.square(mask_imag))
            mask_mag = tf.math.tanh(mask_mag)
            mask_mag = tf.cast(mask_mag, tf.float32)
            
            # Note: Here, mask_real and mask_imag are divided by the magnitude mask_mag, ensuring the resulting values represent the unit vector in the same direction as the original complex number.
            # In short: The phase information should not be influenced by the mask's magnitude, hence we normalize them.
            #phase_real = (mask_real/(mask_mag+self.eps)) + self.eps
            #phase_imag = (mask_imag/(mask_mag+self.eps)) + self.eps
            
            mask_phase = tf.math.atan2(mask_imag,mask_real)
            mask_phase = tf.cast(mask_phase, tf.float32)
            
            # Apply mask
            est_mags = mask_mag*x_mag 
            est_phase = x_phase + mask_phase
            est_real = est_mags*tf.math.cos(est_phase)
            est_imag = est_mags*tf.math.sin(est_phase)
            
        elif self.masking_mode == 'C':
            # Apply mask
            est_real = tf.cast(x_real*mask_real-x_imag*mask_imag, tf.float32) 
            est_imag = tf.cast(x_real*mask_imag+x_imag*mask_real, tf.float32)
        else:
            # Apply mask
            est_real = tf.cast(x_real*mask_real, tf.float32)
            est_imag = tf.cast(x_imag*mask_imag, tf.float32)
            
            
        estimated_speech = tf.complex(est_real, est_imag)
            
        return estimated_speech