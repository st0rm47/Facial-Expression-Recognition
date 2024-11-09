# Facial-Expression-Recognition
The project is about recognizing facial expressions using Convolutional Neural Networks. The dataset used is FER2013. The model is trained using Keras and OpenCV is used to capture the video feed from the webcam. The model is then used to predict the facial expression in real-time.

## Dataset
The dataset used is FER2013. It consists of 48x48 pixel grayscale images of faces. The faces have been automatically registered so that the face is more or less centered and occupies about the same amount of space in each image. The task is to categorize each face based on the emotion shown in the facial expression in to one of seven categories.

# Features
- **Real-time Detection**: Identifies emotions such as happiness, sadness, surprise, and anger from facial expressions.
- **User-Friendly Interface**: Simple web interface built with Flask.
- **Model Training**: Ability to train and retrain the model using custom datasets.
- **Customizable**: Easily configurable to add or modify expression categories.

## Usage
1. Clone the repository to your local machine:
```bash
git clone https://github.com/st0rm47/Facial-Expression-Recognition
```
2. Install the required libraries using
```
pip install -r requirements.txt
```
3. Open *`FER.ipynb`* in Jupyter Notebook and run the cells to train the model
4. Run *`app.py`* to start the application







