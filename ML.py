import os
from pyAudioAnalysis import audioTrainTest as aT
from pyAudioAnalysis import MidTermFeatures as aF


def extract_features(music_parent_directory):

    # List all the subdirectories

    subdirectories = os.listdir(music_parent_directory)

    for i in range(0, len(subdirectories)):

        if subdirectories[i] == '.DS_Store':
            subdirectories.pop(i)
            break

    subdirectories = [music_parent_directory + '/' + subdirectory for subdirectory in subdirectories]

    return aF.multiple_directory_feature_extraction(subdirectories, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, True)


def train_segment_classifier_and_create_model(music_parent_directory, model_name):

    # List all the subdirectories

    subdirectories = os.listdir(music_parent_directory)

    for i in range(0, len(subdirectories)):

        if subdirectories[i] == '.DS_Store':
            subdirectories.pop(i)
            break

    subdirectories = [music_parent_directory + '/' + subdirectory for subdirectory in subdirectories]

    aT.extract_features_and_train(subdirectories, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "randomforest",
                                  'data/' + model_name, True)


def single_file_classification(wav_path, classifier_model_path):

    class_id, probability, classes = aT.file_classification(wav_path, classifier_model_path, "randomforest")

    return class_id, probability, classes
