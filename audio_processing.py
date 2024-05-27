import librosa
import numpy as np
import joblib

classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad' ,'surprise']
std_scalar = joblib.load('std.pkl')  

def rmse(data, frame_length=2048, hop_length=512):
    rmse = librosa.feature.rms(y=data, frame_length=frame_length, hop_length=hop_length)
    return np.squeeze(rmse)

def extract_features(data, frame_length=2048, hop_length=512):
    result = np.array([])
    result = np.hstack((result, rmse(data, frame_length, hop_length)))
    return result

def pad_or_truncate(features, target_length=108):
    if len(features) > target_length:
        return features[:target_length]
    elif len(features) < target_length:
        return np.pad(features, (0, target_length - len(features)), 'constant')
    return features

def get_features(path, target_length=108):
    data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
    features = extract_features(data, sample_rate)
    features = pad_or_truncate(features, target_length)
    features = std_scalar.transform(features.reshape(1, -1))
    return np.expand_dims(features, axis=2)