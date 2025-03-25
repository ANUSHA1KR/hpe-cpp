import sqlite3

DB_NAME = "pagerduty_feedback.db"

def create_feedback_table():
    """Create a table to store feedback if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT NOT NULL,
            feedback TEXT CHECK(feedback IN ('Correct', 'Incorrect', 'Partially Correct')) NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def insert_feedback(incident_id, feedback):
    """Insert feedback into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (incident_id, feedback) VALUES (?, ?)", (incident_id, feedback))
    conn.commit()
    conn.close()

def get_all_feedback():
    """Retrieve all feedback from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT incident_id, feedback, timestamp FROM feedback")
    feedback_data = [{"incident_id": row[0], "feedback": row[1], "timestamp": row[2]} for row in cursor.fetchall()]
    conn.close()
    return {"feedback": feedback_data}

def calculate_accuracy():
    """Calculate the accuracy based on the feedback data."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT feedback FROM feedback")
    feedbacks = cursor.fetchall()
    
    total_feedbacks = len(feedbacks)
    correct = sum(1 for feedback in feedbacks if feedback[0] == 'Correct')
    partially_correct = sum(1 for feedback in feedbacks if feedback[0] == 'Partially Correct')
    
    accuracy = (correct + 0.5 * partially_correct) / total_feedbacks * 100 if total_feedbacks > 0 else 0
    conn.close()
    return accuracy

def get_recommendations():
    """Generate recommendations based on feedback trends."""
    accuracy = calculate_accuracy()
    
    if accuracy >= 80:
        return "The recommendations are highly accurate. No major changes required."
    elif accuracy >= 60:
        return "The recommendations are moderately accurate. Consider refining the root cause analysis."
    else:
        return "The recommendations are inaccurate. Significant improvements needed in RCA predictions."
    
# Ensure table is created at startup
create_feedback_table()
