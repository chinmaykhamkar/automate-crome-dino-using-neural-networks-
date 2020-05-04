# Importing the Keras libraries 
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout

# build the cnn model
model = Sequential()
# model structure 
model.add(Convolution2D(32,(3,3),input_shape=(64,64,1),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Convolution2D(64,(3,3),activation='relu'))
model.add(Convolution2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Convolution2D(128,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Convolution2D(256,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Flatten())
model.add(Dense(150,activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(2,activation='softmax'))
# compile the model 
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])


from keras.preprocessing.image import ImageDataGenerator 

train_data = ImageDataGenerator(
            rescale=1/.255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )
test_data = ImageDataGenerator(rescale=1/.255)
train_set = train_data.flow_from_directory('data/train',
                                            target_size=(64, 64),
                                            batch_size=5,
                                            color_mode='grayscale',
                                            class_mode='categorical')

test_set = test_data.flow_from_directory('data/test',
                                            target_size=(64, 64),
                                            batch_size=5,
                                            color_mode='grayscale',
                                            class_mode='categorical')

model.fit(train_set,
          steps_per_epoch=300, #no of images
          epochs=15,
          validation_data=test_set,
          validation_steps=20) #no of images in test data

# save the model
model_json = model.to_json()
with open('model-bw.json','w') as json_file:
    json_file.write(model_json)
model.save_weights('model-bw.h5')

