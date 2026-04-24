import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_synthetic_alerts(num_alerts: int = 5) -> list[dict]:
    """
    Generate synthetic SIEM alerts untuk keperluan demo.
    """
    alert_types = [
        "Multiple Failed Login Attempts",
        "Suspicious PowerShell Execution",
        "Malware Detected by EDR",
        "Unusual Data Exfiltration",
        "Possible SQL Injection"
    ]
    
    severities = ["Low", "Medium", "High", "Critical"]
    
    alerts = []
    
    for _ in range(num_alerts):
        alert_type = random.choice(alert_types)
        severity = random.choice(severities)
        src_ip = fake.ipv4()
        dst_ip = fake.ipv4()
        timestamp = fake.date_time_between(start_date="-1d", end_date="now").isoformat()
        
        # Simulasi false positive:
        # Jika alert "Multiple Failed Login" dan severity Low, biasanya false positive dari user lupa password.
        
        alert = {
            "alert_id": fake.uuid4(),
            "timestamp": timestamp,
            "alert_type": alert_type,
            "severity": severity,
            "source_ip": src_ip,
            "destination_ip": dst_ip,
            "user_account": fake.user_name(),
            "description": f"Detected {alert_type} from {src_ip} targeting {dst_ip}.",
            "raw_log": f"{timestamp} {alert_type} src={src_ip} dst={dst_ip} user={fake.user_name()} action=blocked"
        }
        
        alerts.append(alert)
        
    return alerts

if __name__ == "__main__":
    print(json.dumps(generate_synthetic_alerts(2), indent=2))
