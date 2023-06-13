# Digital Image Processing
## Implementing Adaptive Mean Filter

### Language used: 
<b>Python<b>

### Libraries used:

```python
import cv2      
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk 
```
    
### Explanation:
The following is the explanation of the code along with code snippets.

#### Image Reading
```python
# Select an image 
    filename = filedialog.askopenfilename()
    if filename:
        # Load the image
        img = cv2.imread(filename)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
    
The code above is used to read the file that is the image and then converts into gray scale. 


#### Salt and Pepper Noise generation
```python
        noise = np.zeros_like(gray)
        salt = np.ceil(amount * gray.size * probability)            
        pepper = np.ceil(amount * gray.size * (1 - probability))     
        coords = [np.random.randint(1, i, int(salt)) for i in gray.shape]
        noise[coords] = 255
        coords = [np.random.randint(1, i, int(pepper)) for i in gray.shape]
        noise[coords] = 0
        noisy_gray = np.clip(gray + noise, 0, 255).astype(np.uint8)
```

The above code is the one where salt and pepper noise is added to the image. Moreover, the probability of salt and pepper is taken on run time form the user along with the kernel and window size of the image. "np.clip" basically limits the values to stay bewteen 0 and 255. Since the two values which are being added may result in a value bigger than 255, thus any value greater than 255 is clipped to 255 and any value less than 0 is clipped to 0. 

#### Applying the Filter
```python
        for i in range(0, noisy_gray.shape[0] - window_size, window_size):
            for j in range(0, noisy_gray.shape[1] - window_size, window_size):
                window = noisy_gray[i:i+window_size, j:j+window_size]
                local_mean = np.mean(window)

                # Determine the new kernel size
                variance = np.var(window)
                global_mean = np.mean(noisy_gray)
                temp = int(variance / (global_mean * kernel_size))
                new_kernel_size = kernel_size + temp

                # Apply the adaptive mean filter
                filtered_window = cv2.blur(window, (new_kernel_size, new_kernel_size))
                noisy_gray[i:i+window_size, j:j+window_size] = filtered_window
```
The above code is used to determine the adaptive mean filter when applied and takes into consideration the algorithm steps. 
