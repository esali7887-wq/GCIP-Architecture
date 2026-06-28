import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"
TENANT_ID = "TR-IST-044"
PROJECT_ID = "PRJ-TEST-RAG-999"

def run_e2e_rag_test():
    headers = {
        "X-Tenant-ID": TENANT_ID,
        "Content-Type": "application/json"
    }

    # Detect if we are using mock embeddings (no API key configured)
    is_mock_embedding = False
    try:
        from app.services.embedding_service import embedding_service
        if not embedding_service.api_key:
            is_mock_embedding = True
    except Exception:
        is_mock_embedding = True

    print("=== GCIP RAG E2E TEST RUN ===")
    if is_mock_embedding:
        print("[WARNING] Gemini API key is missing. Using mock embeddings (semantic assertions relaxed).")
    
    print("1. Checking API Health Status...")
    try:
        r_health = requests.get(f"{BASE_URL}/health", timeout=5.0)
        print(f"Health Response Status: {r_health.status_code}")
        print(f"Health Response Content: {r_health.json()}\n")
        if r_health.status_code != 200:
            print("API or database connection is offline. Make sure docker databases are running.")
            sys.exit(1)
    except Exception as e:
        print(f"Failed to connect to API on {BASE_URL}. Ensure uvicorn server is running: {e}")
        sys.exit(1)

    print("2. Initializing Project Onboarding...")
    onboarding_payload = {
        "project_id": PROJECT_ID,
        "project_name": "RAG Test Refinery Project",
        "total_budget_usd": 15000000.00,
        "is_takeover": False,
        "historical_leakage_audit": True,
        "baseline_version": "Rev0",
        "boq_items": [
            {
                "poz_no": "POZ-CIV-001",
                "description": "Cast-in-place concrete C30/37",
                "quantity": 2500.0,
                "unit": "m3",
                "unit_price": 120.0,
                "total_price": 300000.0,
                "discipline": "CIVIL"
            }
        ],
        "subcontractors": [
            {
                "name": "Beta Concrete Inc."
            }
        ]
    }
    
    r_onboard = requests.post(f"{BASE_URL}/onboarding/start", json=onboarding_payload, headers=headers)
    print(f"Onboarding Status Code: {r_onboard.status_code}")
    print(f"Onboarding Response: {r_onboard.json()}\n")
    assert r_onboard.status_code == 201, f"Expected 201, got {r_onboard.status_code}"

    print("3. Uploading Contract Clauses to RAG...")
    clauses = [
        "Sözleşme bedelinin %10'u oranında avans verilecektir. Avans, ilk hakedişten itibaren mahsup edilmeye başlanır.",
        "Geçici kabul işlemleri tamamlandığında teminat mektubunun yarısı iade edilecektir.",
        "Mücbir sebep halleri deprem, sel, heyelan ve grev durumlarını kapsar. Ek süre talebi 10 gün içinde yapılmalıdır."
    ]

    for idx, clause in enumerate(clauses):
        upload_payload = {
            "project_id": PROJECT_ID,
            "source_name": f"test_contract_clause_{idx + 1}",
            "text": clause
        }
        r_upload = requests.post(f"{BASE_URL}/rag/upload", json=upload_payload, headers=headers)
        print(f"Upload {idx + 1} Status Code: {r_upload.status_code}")
        print(f"Upload {idx + 1} Response: {r_upload.json()}")
        assert r_upload.status_code == 201, f"Expected 201, got {r_upload.status_code}"
    print()

    print("4. Executing Semantic Similarity Query 1...")
    # Query related to "avans" (prepayment)
    query_payload_1 = {
        "project_id": PROJECT_ID,
        "query": "Ön ödeme ve avans kuralları",
        "k": 2
    }
    r_query_1 = requests.post(f"{BASE_URL}/rag/query", json=query_payload_1, headers=headers)
    print(f"Query 1 Status Code: {r_query_1.status_code}")
    q1_json = r_query_1.json()
    print("Query 1 Results:")
    for result in q1_json.get("results", []):
        print(f" - Source: {result['source']}, Score: {result['score']:.4f}")
        print(f"   Text: {result['text']}")
    print()
    assert r_query_1.status_code == 200, f"Expected 200, got {r_query_1.status_code}"
    assert len(q1_json.get("results", [])) > 0, "Expected at least 1 match."
    
    if not is_mock_embedding:
        # Ensure the prepayment clause came out first or has highest score
        assert "avans" in q1_json["results"][0]["text"].lower(), "Expected prepayment clause to rank first."
    else:
        print("Mock Mode: Bypassing strict semantic assertion for Query 1.")

    print("5. Executing Semantic Similarity Query 2...")
    # Query related to "deprem" (earthquake/force majeure)
    query_payload_2 = {
        "project_id": PROJECT_ID,
        "query": "Doğal afet ve mücbir sebepler ek süre talebi",
        "k": 1
    }
    r_query_2 = requests.post(f"{BASE_URL}/rag/query", json=query_payload_2, headers=headers)
    print(f"Query 2 Status Code: {r_query_2.status_code}")
    q2_json = r_query_2.json()
    print("Query 2 Results:")
    for result in q2_json.get("results", []):
        print(f" - Source: {result['source']}, Score: {result['score']:.4f}")
        print(f"   Text: {result['text']}")
    print()
    assert r_query_2.status_code == 200, f"Expected 200, got {r_query_2.status_code}"
    assert len(q2_json.get("results", [])) > 0, "Expected at least 1 match."
    
    if not is_mock_embedding:
        assert "mücbir" in q2_json["results"][0]["text"].lower(), "Expected force majeure clause to be matched."
    else:
        print("Mock Mode: Bypassing strict semantic assertion for Query 2.")

    print("=== RAG E2E TEST RUN SUCCESSFUL ===")

if __name__ == "__main__":
    run_e2e_rag_test()
