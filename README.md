# Facial-Expression-Recognition
The project is about recognizing facial expressions using Convolutional Neural Networks. The dataset used is FER2013. The model is trained using Keras and OpenCV is used to capture the video feed from the webcam. The model is then used to predict the facial expression in real-time.

## Dataset
The dataset used is FER2013. It consists of 48x48 pixel grayscale images of faces. The faces have been automatically registered so that the face is more or less centered and occupies about the same amount of space in each image. The task is to categorize each face based on the emotion shown in the facial expression in to one of seven categories (0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral).

## Model
The model is a Convolutional Neural Network. It consists of 3 Convolutional layers followed by max pooling layers and 2 fully connected layers. The activation function used is ReLU. The model is trained using the Adam optimizer and categorical crossentropy is used as the loss function.

## Usage
1. Clone the repository
2. Install the required libraries using `pip install -r requirements.txt`
3. Run `train.py` to train the model

 
