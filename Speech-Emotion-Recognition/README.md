# Speech Emotion Recognition
<div align="center">
  <img src="Speech Emotion Recognition/GUI/start.png" width="700px" />
</div>

## Summary
Recognition desktop application can categorize human voice into 6 different emotions, enabling users to record or upload customized voices. Using python libraries: Keras for Deep Learning, librosa for signal processing, PyAudio for recording voices and PyQt for GUI.

## Abstract
Speech emotion recognition (SER) plays a significant role in many real-time applications, such as human behavior assessment, human-robot interaction, virtual reality, and emergency centers to analyze the emotional state of speakers. In this work, we employed deep learning techniques to boost the recognition accuracy of speech emotions. In specific, convolutional neural network (CNN) and long short-term memory (LSTM) were constructed in sequence to learn local and global emotion-related features from speech and log-mel spectrogram.The designed network consists of four local feature-learning blocks
(LFLBs) and one long short-term memory (LSTM) layer. LFLB, which mainly contains one convolutional layer and one max-pooling layer, is built for learning local correlations in addition to extracting hierarchical correlations. LSTM layer is adopted to learn long-term dependencies from the learned local features. To improve overall performance of the deep network, the training dataset is augmented with additional speech utterances after adding noise at different signal-to-noise (SNR) ratios.The designed deep learning network is evaluated in terms of the IEMOCAP dataset as a benchmark. Experimental results show that the designed network achieved a significant and promising performance on the task of recognizing speech emotions. The achieved recognition accuracy is **99.30%** when tested on the speaker-dependent part of IEMOCAP dataset.

## Experimental results
### Speaker-dependent experiments
<div align="center">
  <img src="Speech Emotion Recognition/GUI/result.png" width="700px" />
</div>

## Tools
* Python – programing language.
* Anaconda – editor for python.
* PyCharm – editor for python.
* Librosa – python package for music and audio analysis.
* Numpy – python library used for working with arrays.
* Keras – open-source neural-network library written in Python.
* PyQt - python library used for building GUI

## References
- [1D & 2D CNN LSTM networks](https://www.sciencedirect.com/science/article/abs/pii/S1746809418302337). Zhao, Jianfeng, Xia Mao, and Lijiang Chen. "Speech emotion recognition using deep 1D & 2D CNN LSTM networks." Biomedical signal processing and control 47 (2019): 312-323.
- [Merged deep CNN](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-spr.2017.0320). Zhao, Jianfeng, Xia Mao, and Lijiang Chen. "Learning deep features to recognise speech emotion using merged deep CNN." IET Signal Processing 12.6 (2018): 713-721.

Demo Link:

https://drive.google.com/file/d/1NJRvs6_-o7t4GFylSeI4afJitaFMhYKB/view?usp=sharing
