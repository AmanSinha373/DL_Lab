# -*- coding: utf-8 -*-
"""Dl Final Lab Exam (Aman Kumar Sinha).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MgnkqDdiDsXYPRHu9TL1aLvv-kGYn0FM
"""

import kagglehub

# Downloading the latest version
path = kagglehub.dataset_download("jonathanoheix/face-expression-recognition-dataset")

print("Path to dataset files:", path)

import os

# Defining the correct dataset path
dataset_path = "/root/.cache/kagglehub/datasets/jonathanoheix/face-expression-recognition-dataset/versions/1"

# Checking the directory structure at the root level
print("Dataset contents:", os.listdir(dataset_path))

# Defining the path to the 'images' folder
images_dir = os.path.join(dataset_path, 'images')

# Checking the contents inside the 'images' folder
print("Images directory contents:", os.listdir(images_dir))

# Checking the contents of 'train' and 'validation' directories
train_dir = os.path.join(images_dir, 'train')
validation_dir = os.path.join(images_dir, 'validation')

# Also Listing the contents of both directories
print("Train directory contents:", os.listdir(train_dir))
print("Validation directory contents:", os.listdir(validation_dir))

#Importing libraries
import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator # ImageDataGenerator is part of tf.keras
from tensorflow.keras.layers import Dense, Input, Dropout,Flatten, Conv2D
from tensorflow.keras.layers import BatchNormalization, Activation, MaxPooling2D
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.utils import load_img, img_to_array # Use tensorflow.keras.utils for load_img and img_to_array
#from keras.preprocessing.image import load_img, img_to_array # No longer needed
#from keras.preprocessing.image import ImageDataGenerator # No longer needed
from tensorflow.keras.layers import Dense, Input, Dropout # Use tensorflow.keras.layers
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import Adam

"""###Displaying some images"""

folder_path = '/root/.cache/kagglehub/datasets/jonathanoheix/face-expression-recognition-dataset/versions/1/images/'
picture_size = (48, 48)  # 48x48 image size

# Expression to display, I will be picking happy
expression = 'happy'

# Plotting the images
plt.figure(figsize=(12, 12))
for i in range(1, 10):
    # Getting the image file path
    img_path = os.path.join(folder_path, 'train', expression, os.listdir(os.path.join(folder_path, 'train', expression))[i])

    # Loading the image and display it
    img = load_img(img_path, target_size=picture_size)
    plt.subplot(3, 3, i)
    plt.imshow(img)
    plt.axis('off')  # It will Hide axis

plt.show()

"""#Data Augmentation (To prevent overfitting)"""

batch_size  = 128

datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=10,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range = 0.1, # Randomly zoom image
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=False,  # randomly flip images
        vertical_flip=False)  # randomly flip images

train_set = datagen.flow_from_directory(folder_path+"train",
                                              target_size = (picture_size,picture_size),
                                              color_mode = "grayscale",
                                              batch_size=batch_size,
                                              class_mode='categorical',
                                              shuffle=True)


test_set = datagen.flow_from_directory(folder_path+"validation",
                                              target_size = (picture_size,picture_size),
                                              color_mode = "grayscale",
                                              batch_size=batch_size,
                                              class_mode='categorical',
                                              shuffle=False)

"""#Displaying the generated data"""

plt.figure(figsize= (10,10))
for i in range(1,5,1):
    img, label = next(train_set) # Use next(train_set) instead of train_set.next()
    print(img.shape)
    plt.subplot(3,4,i)
    plt.imshow(img[1,:,:,0], cmap='gray') # Displaying the image with grayscale colormap
    plt.title(f"Label: {np.argmax(label[1])}") # Displaying the label of the image
plt.show()

"""#CNN Architecture"""

no_of_classes = 7

model = Sequential()

#1st CNN layer
model.add(Conv2D(64,(3,3),padding = 'same',input_shape = (48,48,1)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout(0.25))

#2nd CNN layer
model.add(Conv2D(128,(5,5),padding = 'same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout (0.25))

#3rd CNN layer
model.add(Conv2D(512,(3,3),padding = 'same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size = (2,2)))
model.add(Dropout (0.25))

#4th CNN layer
model.add(Conv2D(512,(3,3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())

#Fully connected 1st layer
model.add(Dense(256))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))


# Fully connected layer 2nd layer
model.add(Dense(512))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(no_of_classes, activation='softmax'))

model.compile(optimizer=Adam(learning_rate=0.0001),loss='categorical_crossentropy', metrics=['accuracy'])

from IPython.display import Image
plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)
Image('model.png',width=1000, height=3000)

model.summary()

"""#Saving Model by checkpoint"""

from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

checkpoint = ModelCheckpoint("./model.h5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')

early_stopping = EarlyStopping(monitor='val_loss',
                          min_delta=0,
                          patience=3,
                          verbose=1,
                          restore_best_weights=True
                          )

reduce_learningrate = ReduceLROnPlateau(monitor='val_loss',
                              factor=0.2,
                              patience=3,
                              verbose=1,
                              min_delta=0.0001)

callbacks_list = [early_stopping,checkpoint,reduce_learningrate]

"""#Compile model"""

model.compile(loss='categorical_crossentropy',
              optimizer = Adam(learning_rate=0.001),
              metrics=['accuracy'])

"""#Train the model"""

history = model.fit(x=train_set,
                                steps_per_epoch=train_set.n//train_set.batch_size,
                                epochs=10,
                                validation_data = test_set,
                                validation_steps = test_set.n//test_set.batch_size,
                                callbacks=callbacks_list
                                )

"""#Predicting one value from test_set"""

img, label = test_set[0]
print(img.shape)
print(img[1].shape)

plt.imshow(img[1])

y_pred = model.predict(img)
y_pred = np.argmax(y_pred, axis=1)
print(class_names[y_pred[0]])
print('class:'+ str(y_pred[0]))

"""#Display Stats"""

plt.figure(figsize=(20,10))
plt.subplot(1, 2, 1)
plt.suptitle('Optimizer : Adam', fontsize=10)
plt.ylabel('Loss', fontsize=16)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')

plt.subplot(1, 2, 2)
plt.ylabel('Accuracy', fontsize=16)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.show()

#Accuracy of the model
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
#Loss of the model
loss = history.history['loss']
val_loss = history.history['val_loss']

#printing accuracy of the model
print("Accuracy of the model is: ", acc)

# List of accuracy values from different steps
acc1 = [0.28163662552833557, 0.265625, 0.3843097686767578, 0.390625, 0.4454047977924347,
       0.3984375, 0.4824173152446747, 0.5546875, 0.5104032158851624, 0.484375]

# Calculate overall accuracy by taking the mean of the list
overall_accuracy = np.mean(acc1)

# Print the overall accuracy
print("Overall accuracy of the model is: ", overall_accuracy)

"""#Our code uses a Convolutional Neural Network (CNN) to classify facial expressions from the 'face-expression-recognition-dataset.' The dataset is augmented using various transformations to prevent overfitting. The model consists of multiple convolutional layers followed by dense layers, with dropout applied to avoid overfitting. It is trained for 10 epochs using the Adam optimizer. The model's performance is tracked through training and validation accuracy and loss. After training, the model predicts facial expressions on test data, and overall accuracy is calculated, giving an insight into its classification capabilities for facial emotions."""

