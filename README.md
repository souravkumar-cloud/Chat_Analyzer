# 💬 WhatsApp Chat Analyzer

A modern and interactive **WhatsApp Chat Analysis** application built using **Python** and **Streamlit**. This project provides detailed insights into WhatsApp conversations through beautiful visualizations and analytics.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

- 📊 Total Messages, Words, Media, and Links Statistics
- 📈 Monthly and Daily Activity Timeline
- 🔥 Weekly and Monthly Activity Analysis
- 👥 Most Active Participants Analysis
- ☁️ Word Cloud Generation
- 📝 Most Frequently Used Words
- 😀 Emoji Usage Analysis
- 🌙 Light and Dark Theme Support
- 🎨 Modern and Responsive User Interface

---

## 🛠️ Tech Stack

- **Frontend/UI:** Streamlit
- **Backend:** Python
- **Visualization:** Matplotlib
- **Data Processing:** Pandas
- **Word Cloud:** WordCloud Library

---

## 📂 Project Structure

```bash
WhatsApp-Chat-Analyzer/
│
├── app.py                 # Main Streamlit application
├── helper.py              # Helper functions for analytics
├── preprocessor.py        # Chat preprocessing logic
├── stop_hinglish.txt      # Stop words file
├── requirements.txt       # Required dependencies
├── README.md
└── sample_chat.txt        # Sample exported chat
```

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/WhatsApp-Chat-Analyzer.git
cd WhatsApp-Chat-Analyzer
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/Mac**

```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser.

---

## 📱 How to Export WhatsApp Chat

1. Open WhatsApp.
2. Select any individual or group chat.
3. Tap **⋮ (Options)** → **More** → **Export Chat**.
4. Choose **Without Media**.
5. Upload the exported `.txt` file into the application.

---

## 📸 Screenshots

Add screenshots of your application here.

```md
![Dashboard](screenshots/dashboard.png)
```

---

## 📊 Analytics Provided

- Total number of messages
- Total words exchanged
- Media shared count
- Links shared count
- Monthly activity trend
- Daily messaging trend
- Weekly activity heatmap
- Most active users
- Most common words
- Word cloud visualization
- Emoji analysis

---

## 🌟 Future Improvements

- Sentiment Analysis
- Chat Heatmaps
- User Interaction Network Graph
- PDF Report Generation
- AI-based Chat Insights

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create your feature branch.

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes.

```bash
git commit -m "Add AmazingFeature"
```

4. Push to the branch.

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Sourav Kumar (Bala)**

GitHub: https://github.com/souravkumar-cloud

---

⭐ If you found this project useful, please give it a star on GitHub!
