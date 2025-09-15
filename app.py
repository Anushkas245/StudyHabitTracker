import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
import os

# Page configuration
st.set_page_config(
    page_title="Study Habit Tracker",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File path for data storage
DATA_FILE = "study_log.csv"
DAILY_GOAL = 4  # hours

# Initialize session state
if 'data' not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.data = pd.read_csv(DATA_FILE)
        st.session_state.data['date'] = pd.to_datetime(st.session_state.data['date']).dt.date
    else:
        st.session_state.data = pd.DataFrame(columns=['date', 'subject', 'hours', 'mood'])

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "Small steps every day lead to big results 🚀",
    "Consistency is the key to success 🔑",
    "You're making progress, keep going! 💪",
    "Every minute counts ⏱️",
    "The expert in anything was once a beginner 🎯"
]

# Badge definitions
BADGES = {
    3: {"emoji": "🌟", "name": "Rising Star", "color": "#FFD700"},
    7: {"emoji": "👑", "name": "Consistency Queen", "color": "#C0C0C0"},
    30: {"emoji": "⚡", "name": "Legend", "color": "#FFA500"}
}

def calculate_streaks(dates):
    """Calculate current and best streaks from a list of dates."""
    if len(dates) == 0:
        return 0, 0
    
    # Convert to datetime and sort
    unique_dates = sorted(list(set(dates)))
    
    current_streak = 1
    best_streak = 1
    
    for i in range(1, len(unique_dates)):
        if (unique_dates[i] - unique_dates[i-1]).days == 1:
            current_streak += 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = 1
    
    return current_streak, best_streak

def get_earned_badges(streak):
    """Return list of badges earned based on streak."""
    return [badge for days, badge in BADGES.items() if streak >= days]

def save_data():
    """Save data to CSV file."""
    st.session_state.data.to_csv(DATA_FILE, index=False)

def add_log_entry(subject, hours, mood):
    """Add a new log entry to the data."""
    today = datetime.now().date()
    new_entry = pd.DataFrame({
        'date': [today],
        'subject': [subject],
        'hours': [hours],
        'mood': [mood]
    })
    st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
    save_data()

# Main App
st.title("📚 Study Habit Tracker")
st.markdown("---")

# Sidebar for input form
with st.sidebar:
    st.header("📝 Log Your Study")
    with st.form("study_form"):
        subject = st.text_input("Subject/Topic", placeholder="What did you study?")
        hours = st.number_input("Hours Studied", min_value=0.5, step=0.5, format="%.1f")
        mood = st.selectbox(
            "How do you feel?",
            ["😃 Great", "🙂 Good", "😐 Okay", "😓 Tired"]
        )
        
        submitted = st.form_submit_button("Add Log")
        if submitted and subject:
            add_log_entry(subject, hours, mood)
            st.success("Study session logged! 🎉")
    
    st.markdown("---")
    st.markdown("### 🔍 View Data")
    view_option = st.radio("Filter by:", ["All Time", "This Month", "This Week"])
    
    # Add some space at the bottom of the sidebar
    st.markdown("---")
    st.markdown("### 📊 Tips")
    st.markdown("- Aim for consistent study sessions")
    st.markdown("- Take short breaks every 50 minutes")
    st.markdown("- Review your progress weekly")

# Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    # Today's Progress
    today = datetime.now().date()
    today_data = st.session_state.data[st.session_state.data['date'] == today]
    today_hours = today_data['hours'].sum()
    
    st.metric("📅 Today's Hours", f"{today_hours:.1f}", f"{today_hours - DAILY_GOAL:+.1f} from goal")
    st.progress(min(today_hours / DAILY_GOAL, 1.0))

with col2:
    # Current Streak
    current_streak, best_streak = calculate_streaks(st.session_state.data['date'].unique())
    st.metric("🔥 Current Streak", f"{current_streak} days")

with col3:
    # Best Streak
    st.metric("🏆 Best Streak", f"{best_streak} days")

# Badges Section
st.markdown("---")
st.subheader("🎖️ Your Badges")

earned_badges = get_earned_badges(current_streak)
if earned_badges:
    cols = st.columns(len(earned_badges))
    for i, badge in enumerate(earned_badges):
        with cols[i]:
            st.markdown(f"""
                <div style='text-align: center; padding: 20px; border-radius: 10px; 
                            background-color: #f0f2f6; margin: 10px;'>
                    <div style='font-size: 2em;'>{badge['emoji']}</div>
                    <div><strong>{badge['name']}</strong></div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("Keep studying to earn badges! Complete 3 consecutive days to get your first badge.")

# Charts Section
st.markdown("---")
st.subheader("📈 Your Progress")

# Filter data based on view option
if view_option == "This Month":
    filter_date = today - timedelta(days=30)
    chart_data = st.session_state.data[st.session_state.data['date'] >= filter_date]
elif view_option == "This Week":
    filter_date = today - timedelta(days=7)
    chart_data = st.session_state.data[st.session_state.data['date'] >= filter_date]
else:
    chart_data = st.session_state.data

# Create charts if there's data
if not chart_data.empty:
    # Bar Chart - Hours by Subject
    st.write("### 📊 Hours by Subject")
    subject_hours = chart_data.groupby('subject')['hours'].sum().reset_index()
    if not subject_hours.empty:
        fig = px.bar(
            subject_hours, 
            x='subject', 
            y='hours',
            labels={'subject': 'Subject', 'hours': 'Total Hours'},
            color='subject'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Line Chart - Daily Progress
    st.write("### 📅 Daily Study Time")
    daily_hours = chart_data.groupby('date')['hours'].sum().reset_index()
    if not daily_hours.empty:
        fig = px.line(
            daily_hours,
            x='date',
            y='hours',
            labels={'date': 'Date', 'hours': 'Hours Studied'},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Pie Chart - Subject Distribution
    st.write("### 📊 Subject Distribution")
    if not subject_hours.empty:
        fig = px.pie(
            subject_hours,
            values='hours',
            names='subject',
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data to display. Start logging your study sessions to see your progress!")

# Motivational Quote
st.markdown("---")
quote = random.choice(MOTIVATIONAL_QUOTES)
st.markdown(f"*{quote}*", help="Refresh the page for a new quote!")
