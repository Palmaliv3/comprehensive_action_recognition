def predict____(vid_im):
    import os
    import numpy as np
    import cv2
    from tensorflow.keras.models import Model, Sequential, load_model
    from tensorflow.keras.applications import EfficientNetB0
    from tensorflow.keras import mixed_precision
    import random
    # import tensorflow as tf
    from classes import CLASSES_LIST, IMAGE_HEIGHT, IMAGE_WIDTH, SEQUENCE_LENGTH
    # # To hide warnings (they do not affect operation, just warnings for future compatibility versions) 
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # INFO/WARNING
    # os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # oneDNN optimisation
    # tf.get_logger().setLevel('ERROR')  # warning from Keras
 
   


    # Load pre-trained model for features extraction
    base_model = EfficientNetB0(weights="imagenet", include_top=False, 
                            pooling="avg", input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3))
    # Run the data through this variable to pull out the features
    feature_extractor = Model(inputs=base_model.input, outputs=base_model.output)

    # Load our model
    if os.path.exists("trained_model_.keras"):
        model = load_model("trained_model_.keras")
        print("✅ Loaded existing model for testing")
    else:
        print("Model not found")

    # Check for video
    def is_vid(vid_im):
        video_exts = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm']
        ext = os.path.splitext(vid_im)[1].lower()
        return ext in video_exts

    # Action prediction by features
    def predict_action(features_array, SEQUENCE_LENGTH):
        if features_array.shape != (SEQUENCE_LENGTH, 1280):
            print("! The array of features does not match. Impossible to predict.")
            return

        predicted_lab_prob1 = model.predict(np.expand_dims(features_array, axis=0))[0]
        predicted_lab1 = np.argmax(predicted_lab_prob1)
        predicted_class_name1 = CLASSES_LIST[predicted_lab1]
        conf = (predicted_lab_prob1[predicted_lab1]) * 100

        print(f'Recognised action: {predicted_class_name1}\nConfidence: {conf:.1f}%')
        return predicted_class_name1, conf

    # Frames extraction
    def smart_frame_extraction(vid_im, SEQUENCE_LENGTH):
        frames = []
        cap = cv2.VideoCapture(vid_im)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Key frames selection
        if total_frames <= SEQUENCE_LENGTH:
            indices = range(total_frames)
        elif total_frames == 0:
            print("File has no frames")
            return None
        else:
            middle = total_frames // 2
            radius = SEQUENCE_LENGTH // 2
            indices = range(max(0, middle - radius), min(total_frames, middle + radius))
            if len(indices) < SEQUENCE_LENGTH:
                indices = sorted(random.sample(range(total_frames), SEQUENCE_LENGTH))

        # Read selected frames
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame)

        # Sequence completion if there are not enough frames
        while len(frames) < SEQUENCE_LENGTH:
            frames.append(np.flip(frames[-1], axis=0))

        cap.release()
        return np.array(frames, dtype=np.float16)

    # Video processing
    def process_video(vid_im, SEQUENCE_LENGTH):
        try:
            frames = smart_frame_extraction(vid_im, SEQUENCE_LENGTH)
            features = feature_extractor.predict(frames, verbose=0)
            features = features.astype(np.float16)

            if features.shape == (SEQUENCE_LENGTH, 1280):
                print(f"The shape of the extracted objects: {features.shape}")
                return predict_action(features, SEQUENCE_LENGTH)
            else:
                print(f"! Form mismatch {features.shape}")
                return None
        except Exception as e:
            print(f" Error of video processing {vid_im}: {e}")
            return None

    # The main function of file processing
    def process_med(vid_im, SEQUENCE_LENGTH):
        try:
            if not os.path.exists(vid_im):
                print(f"File {vid_im} does not exists")
                return None

            if is_vid(vid_im):
                print(f"Video processing: {vid_im}")
                return process_video(vid_im, SEQUENCE_LENGTH)
            else:
                print(f"Unsupported file format")
                return None
        except Exception as e:
            print(f"Processing error {vid_im}: {e}")
            return None

    # the main function calling
    pred_class, prob = process_med(vid_im, SEQUENCE_LENGTH)
    return pred_class, prob




video_path = f'D:\\Boss\\job things\\my projects\\ML\\Li Bronislav diploma\\test_videos\\test_1.mp4'
res = predict____(video_path)
