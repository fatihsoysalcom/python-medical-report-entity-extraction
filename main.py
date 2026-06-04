import re

def analyze_medical_report(report_text):
    """
    Analyzes a medical report text to extract key entities using basic pattern matching.
    This simulates a very simple NLP process without external libraries.
    """
    extracted_data = {
        "symptoms": [],
        "diagnoses": [],
        "medications": [],
        "measurements": []
    }

    # Define keywords/patterns for different entity types (in Turkish)
    # --- Article's concept: Identifying key information from unstructured text ---

    symptom_keywords = ["baş ağrısı", "mide bulantısı", "ateş", "öksürük", "nefes darlığı", "hırıltı"]
    diagnosis_keywords = ["migren", "diyabet", "hipertansiyon", "grip", "bronşit", "akut migren"]
    medication_keywords = ["parasetamol", "metoklopramid", "ibuprofen", "amoksisilin", "insülin"]

    # --- Extract Symptoms ---
    for symptom in symptom_keywords:
        if re.search(r'\b' + re.escape(symptom) + r'\b', report_text, re.IGNORECASE | re.UNICODE):
            # Add to extracted data if found
            if symptom not in extracted_data["symptoms"]:
                extracted_data["symptoms"].append(symptom)

    # --- Extract Diagnoses ---
    for diagnosis in diagnosis_keywords:
        if re.search(r'\b' + re.escape(diagnosis) + r'\b', report_text, re.IGNORECASE | re.UNICODE):
            if diagnosis not in extracted_data["diagnoses"]:
                extracted_data["diagnoses"].append(diagnosis)
    # Also look for "tanısı konuldu" (diagnosed with) pattern
    diagnosis_pattern_with_phrase = r"(\w+\s?\w*)\s+tanısı konuldu"
    matches = re.findall(diagnosis_pattern_with_phrase, report_text, re.IGNORECASE | re.UNICODE)
    for match in matches:
        # Clean up and add if not already present
        clean_match = match.strip().lower()
        if clean_match not in [d.lower() for d in extracted_data["diagnoses"]]:
            extracted_data["diagnoses"].append(match.strip())

    # --- Extract Medications ---
    for medication in medication_keywords:
        # Pattern to find medication name potentially followed by number+unit (e.g., "500mg")
        med_pattern = r'\b' + re.escape(medication) + r'\s*(\d+(?:[.,]\d+)?\s*(?:mg|gr|ml|mcg|IU|tablet|kapsül))?'
        matches = re.findall(med_pattern, report_text, re.IGNORECASE | re.UNICODE)
        for match in matches:
            full_med = medication
            if match: # If dosage/form was found
                full_med += f" {match.strip()}"
            if full_med not in extracted_data["medications"]:
                extracted_data["medications"].append(full_med)

    # --- Extract Measurements (e.g., blood pressure, temperature, blood sugar) ---
    # Blood pressure: Tansiyon 140/90 mmHg
    bp_pattern = r"(tansiyon(?:u)?)\s*(\d{2,3}\/\d{2,3}\s*mmHg)"
    matches = re.findall(bp_pattern, report_text, re.IGNORECASE | re.UNICODE)
    for match in matches:
        extracted_data["measurements"].append(f"{match[0].capitalize()} {match[1]}")

    # Temperature: ateşi 38.5°C
    temperature_pattern = r"(ateşi?)\s*(\d{1,2}(?:[.,]\d)?\s*°C)"
    matches = re.findall(temperature_pattern, report_text, re.IGNORECASE | re.UNICODE)
    for match in matches:
        extracted_data["measurements"].append(f"{match[0].capitalize()} {match[1]}")

    # Blood sugar: Kan şekeri ölçümü 180 mg/dL
    blood_sugar_pattern = r"(kan şekeri(?: ölçümü)?)\s*(\d{2,3}(?:[.,]\d)?\s*mg/dL)"
    matches = re.findall(blood_sugar_pattern, report_text, re.IGNORECASE | re.UNICODE)
    for match in matches:
        extracted_data["measurements"].append(f"{match[0].capitalize()} {match[1]}")

    return extracted_data

# Sample Medical Report in Turkish
sample_report = """
Hasta, şiddetli baş ağrısı ve mide bulantısı şikayetleriyle başvurdu.
Yapılan muayenede tansiyonu 140/90 mmHg olarak ölçüldü.
Akut migren tanısı konuldu.
Parasetamol 500mg ve Metoklopramid 10mg reçete edildi.
Ayrıca hastanın ateşi 38.5°C olarak kaydedildi.
Kontrol için bir hafta sonra gelmesi önerildi.
"""

# Perform analysis
analysis_result = analyze_medical_report(sample_report)

# Output the results
print("--- Medical Report Analysis ---")
print(f"Original Report:\n{sample_report}\n")
print("Extracted Entities:")
# --- Article's concept: Converting unstructured data to structured format ---
for category, items in analysis_result.items():
    print(f"- {category.capitalize()}: {', '.join(items) if items else 'None'}")

# --- Demonstrating another report ---
print("\n--- Another Report Analysis ---")
another_report = """
Ayşe Hanım, son bir aydır devam eden öksürük ve nefes darlığı şikayetleriyle geldi.
Muayenede akciğerlerinde hırıltı duyuldu.
Bronşit tanısı düşünüldü ve Amoksisilin 250mg reçete edildi.
Kan şekeri ölçümü 180 mg/dL çıktı, bu da diyabet riskini gösteriyor.
"""
analysis_result_2 = analyze_medical_report(another_report)
print(f"Original Report:\n{another_report}\n")
print("Extracted Entities:")
for category, items in analysis_result_2.items():
    print(f"- {category.capitalize()}: {', '.join(items) if items else 'None'}")
