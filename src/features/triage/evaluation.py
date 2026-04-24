import time
from src.features.data_generation.generator import generate_synthetic_alerts
from src.features.triage.service import process_triage

def evaluate_system(num_test_cases: int = 5):
    """
    Evaluasi performa RAG SOC Triage Assistant.
    Mengukur waktu respons rata-rata dan distribusi keputusan.
    """
    print(f"Mengumpulkan {num_test_cases} alert sintetis...")
    alerts = generate_synthetic_alerts(num_test_cases)
    
    results = []
    total_time = 0
    
    print("-" * 50)
    for i, alert in enumerate(alerts):
        print(f"Memproses Alert {i+1}: {alert['alert_type']}")
        start_time = time.time()
        
        try:
            result = process_triage(alert)
        except Exception as e:
            result = {"decision": "Error", "analysis": str(e), "confidence_score": 0.0}
            
        end_time = time.time()
        
        duration = end_time - start_time
        total_time += duration
        
        results.append({
            "alert": alert,
            "triage": result,
            "duration": duration
        })
        print(f"Keputusan: {result.get('decision', 'Unknown')} (Waktu: {duration:.2f} detik)")
        
    avg_time = total_time / num_test_cases
    print("-" * 50)
    print("HASIL EVALUASI")
    print(f"Total waktu: {total_time:.2f} detik")
    print(f"Waktu rata-rata per alert: {avg_time:.2f} detik")
    
    # Distribusi keputusan
    decisions = {}
    for r in results:
        d = r["triage"].get("decision", "Unknown")
        decisions[d] = decisions.get(d, 0) + 1
        
    print("Distribusi Keputusan:")
    for k, v in decisions.items():
        print(f"- {k}: {v} ({(v/num_test_cases)*100:.1f}%)")
        
    return results

if __name__ == "__main__":
    evaluate_system(5)
