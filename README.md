# 🔐 Phishing Website Detection Using Machine Learning

## 📌 Project Overview

Phishing websites are fraudulent websites designed to steal sensitive information such as usernames, passwords, and financial details. This project presents a **Phishing Website Detection System** that uses **Machine Learning (Random Forest Classifier)** to automatically classify a given URL as **Phishing** or **Legitimate** based on URL-based features.

The system is implemented as a **Flask web application**, allowing users to enter a URL, view prediction results with confidence scores, store scan history, and download a PDF report.

---

## 🎯 Objectives

* Detect phishing websites accurately using machine learning
* Extract meaningful URL-based features
* Display prediction results with confidence percentages
* Maintain scan history in a database
* Provide downloadable PDF reports
* Build a user-friendly web interface

---

## 🧠 Machine Learning Algorithm Used

### ✅ Random Forest Classifier

Random Forest is an ensemble learning algorithm that builds multiple decision trees and combines their outputs to improve accuracy and reduce overfitting.

**Why Random Forest?**

* High accuracy
* Handles non-linear data well
* Robust to noise
* Suitable for classification problems like phishing detection

---

## 🔍 Features Extracted from URL

The following features are extracted from the input URL:

* URL Length
* Number of Dots
* Presence of IP Address
* HTTPS Usage
* Number of Hyphens
* Number of Subdomains

These features help the model distinguish between phishing and legitimate URLs.

---

## 🏗️ System Architecture

1. User enters URL via web interface
2. URL is validated
3. Feature extraction is performed
4. Machine Learning model predicts the class
5. Result and confidence scores are displayed
6. Scan result is stored in database
7. User can download PDF report or view history

---

## 🖥️ Technologies Used

### Programming & Frameworks

* Python
* Flask (Web Framework)
* Scikit-learn (Machine Learning)

### Frontend

* HTML
* CSS
* Bootstrap

### Backend & Database

* SQLite
* Python

### Libraries

* Pandas
* NumPy
* Pickle
* ReportLab (PDF generation)

---

## ⚙️ Software Requirements

* Python 3.8 or higher
* Flask
* Scikit-learn
* Pandas
* NumPy

## 💻 Hardware Requirements

* Processor: Intel i3 or above
* RAM: Minimum 4 GB
* Storage: 2 GB free space

---

## ▶️ How to Run the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/Kishor2254/phishing-website-detection.git
cd phishing-website-detection
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

### Step 4: Open in Browser

```
http://127.0.0.1:5000
```

---

## 📊 Output Screens

* URL classification result
* Phishing & Legitimate confidence score
* Scan history table
* Downloadable PDF report

---

## ✅ Results

The system successfully classifies URLs into **Phishing** or **Legitimate** categories with high accuracy. Random Forest provides reliable confidence scores, helping users understand prediction certainty.

---

## 🧪 Sample Test URLs

* [https://www.google.com](https://www.google.com) → Legitimate
* [http://192.168.1.1/login](http://192.168.1.1/login) → Phishing
* [http://secure-login-update.com](http://secure-login-update.com) → Phishing
* [https://www.youtube.com](https://www.youtube.com) → Legitimate

---

## 🔮 Future Enhancements

* Add real-time blacklist checking
* Use deep learning models
* Browser extension integration
* Improve feature set
* Deploy application on cloud

---

## 🎓 Academic Relevance

This project is suitable for:

* Final Year Engineering Project
* Machine Learning Mini Project
* Cyber Security Applications

---

## 👨‍💻 Author

**Kishor R**
Final Year BE Student – Information Science & Engineering
VTU | Bangalore, Karnataka

---

## 📜 License

This project is for academic and educational purposes only.

---

⭐ If you find this project useful, please give it a star on GitHub!
