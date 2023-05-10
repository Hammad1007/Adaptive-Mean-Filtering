# Libraries
import cv2                          # for file reading
import numpy as np                  # numpy file for handling arrays
import tkinter as tk                # GUI in python
from tkinter import filedialog
from PIL import Image, ImageTk

# Kernel size, window size, probability of salt and pepper, amount of noise
kernel_size = int(input("Enter the kernel size: "))
window_size = int(input("Enter the window size: "))
probability = float(input("Enter the probability of salt and pepper noise: "))   
amount = float(input("Enter the amount of noise to be added: "))

# Adaptive Mean Filter Function
def adaptive_mean_filter():
    
    # Select an image 
    filename = filedialog.askopenfilename()
    if filename:
        # Load the image
        img = cv2.imread(filename)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Add salt and pepper noise to the image
        var = amount * gray.size
        noise = np.zeros_like(gray)
        pepper = np.ceil(var * (1 - probability))
        salt = np.ceil(var * probability)  
        coords = [np.random.randint(1, i, int(pepper)) for i in gray.shape]
        noise[coords] = 0 
        coords = [np.random.randint(1, i, int(salt)) for i in gray.shape]
        noise[coords] = 255
        noisy_gray = np.clip(gray + noise, 0, 255).astype(np.uint8)

        # Nested for loop to check for each pixel
        for i in range(0, noisy_gray.shape[0] - window_size, window_size):
            for j in range(0, noisy_gray.shape[1] - window_size, window_size):
                window = noisy_gray[i:i+window_size, j:j+window_size]
                local_mean = np.mean(window)

                variance = np.var(window)
                global_mean = np.mean(noisy_gray)
                temp = int(variance / (global_mean * kernel_size))
                new_kernel_size = kernel_size + temp

                # Apply the filter here
                filtered_window = cv2.blur(window, (new_kernel_size, new_kernel_size))
                noisy_gray[i:i+window_size, j:j+window_size] = filtered_window

        # Display the original image in the GUI
        original_image = Image.fromarray(gray)
        original_image_tk = ImageTk.PhotoImage(original_image)
        original_image_label.configure(image=original_image_tk)
        original_image_label.image = original_image_tk

        # Display the filtered image in the GUI
        filtered_image = Image.fromarray(noisy_gray)
        filtered_image_tk = ImageTk.PhotoImage(filtered_image)
        filtered_image_label.configure(image=filtered_image_tk)
        filtered_image_label.image = filtered_image_tk

    # If the file is not opened, then display an error that file not opened
    else:
        print("Error in opening the file.")
        

# Create the main window
main = tk.Tk()
main.title("Assignment 3: Hammad Rashid   19L-1007")

# Print the text on the screen
text1 = tk.Label(main, text="Adaptive Mean Filter", font=("Times Roman", 12, "bold "), fg="blue")
text1.pack(padx=15, pady=15)

# Create a button to open an image file
open_button = tk.Button(main, text="Select an Image", command=adaptive_mean_filter)
open_button.pack(padx=15, pady=15)

# Frame to hold the image labels
image_frame = tk.Frame(main)
image_frame.pack(padx=10, pady=10)

# Display the original image
original_image_label = tk.Label(image_frame)
original_image_label.pack(side=tk.LEFT, padx=10, pady=10)

# Display the filtered image
filtered_image_label = tk.Label(image_frame)
filtered_image_label.pack(side=tk.RIGHT, padx=10, pady=10)

# Main loop is here
main.mainloop()
