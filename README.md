# fake-news-detection

# 📰 Fake News Detection System using NLP

## 📌 Project Overview

The Fake News Detection System is a Natural Language Processing (NLP) and Machine Learning project designed to classify news articles as **Fake** or **Real**. The model is trained on a dataset containing over 45,000 news articles and uses TF-IDF vectorization with machine learning algorithms for accurate prediction.

This project also includes a Streamlit web application that allows users to verify news articles in real time.

---

## 🚀 Features

* Detects Fake and Real news articles
* NLP-based text preprocessing
* TF-IDF feature extraction
* Machine Learning classification
* Interactive Streamlit web interface
* Real-time prediction
* Confidence score display

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Streamlit
* Natural Language Processing (NLP)

---

## 📂 Dataset

Dataset Used:

**Fake and Real News Dataset**

* Fake.csv
* True.csv

Dataset Source:
https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset

---

## ⚙️ Model Development

### Data Preprocessing

* Text cleaning
* Lowercasing
* Removal of punctuation
* Removal of special characters
* Feature extraction using TF-IDF

### Machine Learning Model

* Passive Aggressive Classifier
* TF-IDF Vectorizer

### Performance

* Dataset Size: 45,000+ News Articles
* Accuracy Achieved: 99%

---

## 📁 Project Structure

```text
fake-news-detection/
│
├── app.py
├── train_model.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
├── README.md
├── Fake.csv
└── True.csv

Run the application:

```bash
python -m streamlit run app.py
```

---

## 🖥️ Application Workflow

1. Enter a news article.
2. Click the Predict button.
3. The system analyzes the text.
4. Prediction is displayed as:

   * Real News
   * Fake News
5. Confidence score is shown.

---

## 📸 Screenshots

Add screenshots of your Streamlit application here.

---

## 🔮 Future Enhancements

* Deep Learning Models (LSTM, BERT)
* News Source Credibility Analysis
* Multi-Class News Classification
* News Summarization
* Explainable AI Visualizations

---

## 👨‍💻 Author

**Pranav Raikar**

B.Tech Computer Science and Design

Dr. D. Y. Patil School of Science and Technology

GitHub: https://github.com/PranavR07-dot

LinkedIn: Add your LinkedIn profile link here.
