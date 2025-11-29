import pandas as pd

# 1. Metni okur
with open("ai_essay_prompts.txt", "r", encoding="utf-8") as f:
    full_text = f.read()

# 2. '###' işaretinden bölüp listeye çevirir
abstracts = full_text.split("###")

# 3. Temizler ve tablo yapar
data = []
for text in abstracts:
    clean_text = text.strip()
    if len(clean_text) > 50: # Boşlukları atlar
        data.append({
            "text": clean_text,
            "label": 1,
            "source": "AI Generated (Gemini Studio)"
        })

# 4. Kaydeder
df = pd.DataFrame(data)
df.to_csv("ai_manual_data.csv", index=False)

print(f"Toplam {len(df)} adet gerçek AI verisi Excel formatına çevrildi.")