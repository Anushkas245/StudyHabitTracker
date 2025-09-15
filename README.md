# 📚 Study Habit Tracker

A personal study habit tracker built with Streamlit that helps you stay consistent with your study routine through gamification and visual progress tracking.

## ✨ Features

- **Daily Study Logging**: Track subjects, study hours, and mood
- **Progress Dashboard**: Visualize your study habits with interactive charts
- **Streak System**: Stay motivated with daily streaks and badges
- **Achievement Badges**: Earn badges for consistent study habits
- **Responsive Design**: Works on desktop and mobile devices
- **Data Persistence**: All data is saved locally in a CSV file

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository or download the files
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. Navigate to the project directory
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and go to `http://localhost:8501`

## 📊 Features in Detail

### Daily Log Form
- Add study sessions with subject, hours, and mood
- Automatically saves the current date
- Data is stored in `study_log.csv`

### Dashboard
- **Today's Progress**: Track hours studied today with a progress bar
- **Streaks**: Current and best streak counters
- **Badges**: Earn badges for consistent study habits
  - 🌟 Rising Star (3-day streak)
  - 👑 Consistency Queen (7-day streak)
  - ⚡ Legend (30-day streak)

### Interactive Charts
- **Bar Chart**: Hours studied by subject
- **Line Chart**: Daily study time trends
- **Pie Chart**: Subject-wise distribution of study time

## 🎨 Customization

You can customize the following in the `app.py` file:
- `DAILY_GOAL`: Change the default daily study goal (in hours)
- `MOTIVATIONAL_QUOTES`: Add or modify the random quotes
- `BADGES`: Customize the badge system

## 📝 Notes

- All your study data is stored locally in `study_log.csv`
- The app doesn't require an internet connection to function
- No personal data is collected or shared

## 🤝 Contributing

Feel free to submit issues and enhancement requests.

## 📜 License

This project is licensed under the MIT License.
