import random
import sqlite3

# Predefined Alert Categories
ALERT_CATEGORIES = {
    "etcdInsufficientMembers": ("Infrastructure", "Kubernetes Core", "Insufficient etcd cluster members detected."),
    "KubeControllerManagerDown": ("Infrastructure", "Kubernetes Core", "The Kubernetes Controller Manager is down."),
    "TargetDown": ("Infrastructure", "Kubernetes Core", "A monitored target (e.g., node, service) is unreachable."),
    "KubePodCrashLooping": ("Application", "Pod Issue", "A pod is stuck in CrashLoopBackOff state."),
    "KubeDeploymentReplicasMismatch": ("Application", "Deployment Issue", "The actual number of replicas does not match the desired count."),
    "CrashLoopBackOff": ("Application", "Pod Issue", "A pod is repeatedly failing and restarting."),
    "PrometheusOperatorSyncFailed": ("Monitoring", "Monitoring Issue", "Prometheus Operator failed to sync configurations."),
    "kube-state-metrics Down": ("Monitoring", "Monitoring Issue", "The kube-state-metrics service is down."),
    "AlertmanagerDown": ("Monitoring", "Monitoring Issue", "The Alertmanager service is unavailable."),
    "NodeMemoryUsageHigh": ("Resource", "Memory Usage", "A node's memory usage has exceeded the threshold."),
    "CPUThrottlingHigh": ("Resource", "CPU Usage", "CPU throttling is occurring at a high rate."),
    "OutOfDisk": ("Resource", "Storage Issue", "The node is running out of disk space."),
    "FilesystemFull": ("Resource", "Storage Issue", "The filesystem has reached full capacity."),
    "FailedAuth": ("Security", "Authentication Failure", "A failed authentication attempt was detected."),
    "UnauthorizedAccess": ("Security", "Access Violation", "Unauthorized access to a resource was attempted."),
    "NetworkPolicyViolation": ("Security", "Network Security", "A Kubernetes network policy violation was detected.")
}

def categorize_alert(title):
    """Categorize alerts based on predefined mappings."""
    for keyword, (alert_type, category, description) in ALERT_CATEGORIES.items():
        if keyword.lower() in title.lower():
            return {
                "alert_name": keyword,
                "alert_type": alert_type,
                "category": category,
                "description": description
            }
    
    # Default categorization if no match is found
    return {
        "alert_name": "Unknown",
        "alert_type": "General",
        "category": "Uncategorized",
        "description": "No specific details available."
    }

def train_model():
    """Simulate AI model training using feedback data."""
    print("✅ AI Model Training Started...")
    print("✅ AI Model Training Completed!")

def predict(incident_id):
    """Predict the root cause of an incident based on past feedback data."""
    conn = sqlite3.connect("pagerduty_feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT feedback FROM feedback WHERE incident_id = ?", (incident_id,))
    feedback_entries = cursor.fetchall()
    conn.close()

    if not feedback_entries:
        return "Unknown", 50.0  # Default RCA with 50% confidence if no past feedback exists

    # Count feedback responses
    correct_count = sum(1 for feedback in feedback_entries if feedback[0] == "Correct")
    partial_count = sum(1 for feedback in feedback_entries if feedback[0] == "Partially Correct")
    total_feedback = len(feedback_entries)

    # Compute Accuracy
    accuracy = ((correct_count + 0.5 * partial_count) / total_feedback) * 100

    # Simulate RCA prediction based on historical feedback
    possible_rcas = ["Network Issue", "Database Overload", "Security Breach", "Memory Leak"]
    predicted_rca = random.choice(possible_rcas)

    return predicted_rca, round(accuracy, 2)

def calculate_accuracy():
    """Calculate the overall accuracy of past RCA predictions."""
    conn = sqlite3.connect("pagerduty_feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT feedback FROM feedback")
    feedback_entries = cursor.fetchall()
    conn.close()

    if not feedback_entries:
        return 0  # Avoid division by zero

    correct_count = sum(1 for feedback in feedback_entries if feedback[0] == "Correct")
    partial_count = sum(1 for feedback in feedback_entries if feedback[0] == "Partially Correct")
    total_feedback = len(feedback_entries)

    accuracy = ((correct_count + 0.5 * partial_count) / total_feedback) * 100
    return round(accuracy, 2)
