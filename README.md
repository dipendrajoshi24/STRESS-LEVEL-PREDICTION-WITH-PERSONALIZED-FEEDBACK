<div align="center">

<br />

<img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-learn"/>
<img src="https://img.shields.io/badge/License-Educational-purple?style=flat-square" alt="License"/>
<img src="https://img.shields.io/badge/Status-Active-22c55e?style=flat-square" alt="Status"/>

<br /><br />

# 🧠 StressAI

**An intelligent, ML-powered web application that predicts stress levels from physiological and lifestyle indicators.**

[Overview](#-overview) · [Features](#-features) · [Architecture](#-architecture) · [Parameters](#-prediction-parameters) · [Tech Stack](#-tech-stack) · [Getting Started](#-getting-started) · [Project Structure](#-project-structure) · [Roadmap](#-roadmap)

</div>

---

## 📖 Overview

Stress has become one of the most prevalent challenges faced by students and working professionals globally. **StressAI** is a machine learning-powered web application that assesses a user's stress level by analysing 13 physiological and lifestyle indicators — including heart rate, sleep duration, anxiety level, work pressure, and more.

The system delivers instant predictions alongside personalised recommendations, while providing secure account management and persistent prediction history with trend analysis.

> **Built as a BCA final project at Graphic Era Hill University by Dipendra Joshi.**

---

## ✨ Features

### 👤 User Management
| Feature | Description |
|---|---|
| Registration | Create an account with email verification |
| Secure login | Session-based authentication |
| Password encryption | Bcrypt hashing for all stored passwords |
| OTP verification | Email-based one-time password via Flask-Mail |
| Forgot password | OTP-driven self-service password recovery |
| Profile management | Update account info and change password |

### 🤖 Stress Prediction
| Feature | Description |
|---|---|
| ML model | Trained Scikit-Learn classifier, serialised with Joblib |
| 13 input parameters | Covers physiological, lifestyle, and psychological factors |
| Three stress tiers | Low · Medium · High |
| Instant assessment | Sub-second inference on any device |
| Personalised suggestions | Contextual recommendations per stress tier |

### 📊 Prediction Tracking
- Per-user prediction history stored in `predictions.csv`
- Stress trend visualisation over time
- Historical analytics dashboard

### 🔒 Security
- Bcrypt password hashing
- Flask session management
- OTP-based email verification
- Stateless, server-side auth workflow

---

## 🏗️ Architecture

```
User
 │
 ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Application                     │
│                                                             │
│  ┌──────────────────────┐   ┌───────────────────────────┐  │
│  │   Auth Module        │   │   Prediction Module       │  │
│  │  ├─ Register         │   │  ├─ Input form (13 params) │  │
│  │  ├─ Login            │   │  ├─ Data preprocessing     │  │
│  │  ├─ OTP verification │   │  └─ ML model (.pkl)        │  │
│  │  └─ Password recovery│   └───────────────────────────┘  │
│  └──────────────────────┘                                   │
│                                                             │
│  ┌──────────────────────┐   ┌───────────────────────────┐  │
│  │   Data Storage       │   │   Results & Analytics     │  │
│  │  ├─ users.csv        │   │  ├─ Stress level result   │  │
│  │  └─ predictions.csv  │   │  ├─ Recommendations       │  │
│  └──────────────────────┘   └─ Prediction history ──────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 Prediction Parameters

The model classifies stress using **13 input features**:

| # | Parameter | Type |
|---|---|---|
| 1 | Heart Rate | Physiological |
| 2 | Systolic Blood Pressure | Physiological |
| 3 | Diastolic Blood Pressure | Physiological |
| 4 | Sleep Hours | Lifestyle |
| 5 | Fatigue Level | Subjective |
| 6 | Headache Frequency | Physiological |
| 7 | Physical Activity | Lifestyle |
| 8 | Screen Time | Lifestyle |
| 9 | Work Pressure | Psychosocial |
| 10 | Study Pressure | Psychosocial |
| 11 | Anxiety Level | Psychological |
| 12 | Mood Swings | Psychological |
| 13 | Concentration Level | Cognitive |

---

## 🎯 Stress Categories

| Level | Indicator | Description |
|---|---|---|
| 🟢 **Low Stress** | 0 | Healthy stress level — no immediate action needed |
| 🟡 **Medium Stress** | 1 | Moderate stress — monitor and take preventive steps |
| 🔴 **High Stress** | 2 | Elevated stress — personalised intervention recommended |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Python 3, Flask |
| **Machine Learning** | Scikit-Learn, Pandas, Joblib |
| **Storage** | CSV-based flat file storage |
| **Auth** | Flask-Sessions, Flask-Mail, Bcrypt |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/stress-ai.git
cd stress-ai
```

**2. (Recommended) Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```env
FLASK_SECRET_KEY=your-secret-key-here
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.

**5. Train the model** *(first-time only)*

```bash
python train_model.py
```

**6. Run the application**

```bash
python app.py
```

**7. Open in your browser**

```
http://127.0.0.1:5000
```

---

## 📂 Project Structure

```
stress_prediction/
│
├── app.py                  # Flask application entry point
├── train_model.py          # ML model training script
├── model.pkl               # Serialised trained model
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore
│
├── dataset/
│   ├── make_dataset.py     # Dataset generation script
│   └── new_stress_dataset.csv
│
├── data/
│   ├── users.csv           # User records
│   └── predictions.csv     # Prediction history
│
├── static/
│   ├── css/
│   └── js/
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── profile.html
    ├── history.html
    ├── result.html
    ├── forgot_password.html
    ├── verify_register.html
    └── verify_reset.html
```

---

## 📸 Application Modules

| Module | Description |
|---|---|
| **Home** | Project introduction and prediction entry point |
| **Register** | Account creation with OTP email verification |
| **Login** | Secure session-based authentication |
| **Predict** | 13-parameter health and lifestyle form |
| **Result** | Stress tier result with personalised suggestions |
| **History** | Previous predictions and stress trend chart |
| **Profile** | Account info management and password change |

> 📷 *Screenshots coming soon — see [Demo Video](#-demo-video)*

---

## 🎥 Demo Video

``

https://github.com/user-attachments/assets/ce39e70a-536d-4141-b871-9586c5843973


```

---

## 🔮 Roadmap

- [ ] Upgrade to a relational database (PostgreSQL / SQLite)
- [ ] Add deep learning models (LSTM, MLP) for improved accuracy
- [ ] Real-time stress monitoring via wearable API integration
- [ ] Mobile application (React Native)
- [ ] Cloud deployment (Render / Railway / AWS)
- [ ] Mental health analytics dashboard
- [ ] Doctor consultation integration
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👨‍💻 Author

**Dipendra Joshi**
Bachelor of Computer Applications (BCA) · Graphic Era Hill University

---

## ⭐ Support

If you found this project helpful:

- ⭐ **Star** the repository
- 🍴 **Fork** it and build something new
- 📢 **Share** it with others

---

## 📜 License

This project is developed for **educational and learning purposes** only.

---

<div align="center">
  <sub>Built with ❤️ by Dipendra Joshi</sub>
</div>
