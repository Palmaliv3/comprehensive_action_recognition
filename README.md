### **Action recognition on videos project**

### Project Description 

This project was aimed on learning and was used by me(Li Bronislav) as a diploma defence project at the programming learning centre[proweb](https://proweb.uz).
It performs action recognition on videos in complicated scenarios taken from security cameras.

### Used and Learned technologies, with just some cool stuff 

1. Used splitting the model training into 2 stages: a separate code file for processing training data and a separate one for the model.
2. The model EfficientNetB0 – an image classification model pre-trained on ImageNet.
3. OpenCV library – a library for working with photos and video.
4. OS library – for working with files on the computer.
5. [UCF101 dataset](https://www.kaggle.com/datasets/matthewjansen/ucf101-action-recognition) – a dataset with 101 action classes. 
6. Multi-Head Attention mechanism (MultiHeadAttention) – this mechanism allows the model to focus on different parts of the input data simultaneously.Because of the multi-head attention mechanism, I had to use a functional style of model construction.
7. Functional style of model building – each layer is called as a function on the previous one.
8. Data augmentation and batch generator – thanks to automatic generation of the needed number of batches and augmentation, this results in more effective use of available memory.
9. Callbacks – stops or reduces the learning rate, they monitor certain metrics and if there are no changes, changes are insignificant, or they worsen, the algorithm stops or reduces the learning rate.
10. Verbose – the cool little bars that show the training status.

### Table of Contents 

1. model.ipynb – main fine-tuning file
2. features.ipynb – file for features extraction.
3. test_for_bot.py – file with code for telegram bot.
4. bot.py – telegram bot itself(UI).
5. trained_model_f4.keras– already trained model.

This code can be used by anyone who will find it usefull, mentioning author(Li Bronislav/github:Palmaliv3)



