import requests
import pandas as pd


def fetch_general_cc_by_data(rows=3000):
    # PLOS API URL
    base_url = "http://api.plos.org/search"

    # Parametreler
    # q: '*:*' demek "her şey" demektir. doc_type:full ile tam makaleleri hedefliyoruz.
    # sort: En yeniden eskiye sırala (güncel konular olsun)
    params = {
        'q': '*:* AND doc_type:full',
        'rows': rows,
        'fl': 'id,abstract,title_display,publication_date',  # İhtiyaç olan alanlar
        'wt': 'json',
        'sort': 'publication_date desc'
    }

    print("PLOS üzerinden rastgele konularda, CC-BY lisanslı makaleler çekiliyor...")

    try:
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            docs = data['response']['docs']

            cleaned_data = []
            print(f"API Yanıt Verdi. {len(docs)} makale işleniyor...")

            for doc in docs:
                abstract_text = doc.get('abstract', [''])[0] if isinstance(doc.get('abstract'), list) else doc.get(
                    'abstract', '')
                title_text = doc.get('title_display', '')

                # Çok kısa veya boş özetleri ele
                if not abstract_text or len(abstract_text) < 50:
                    continue

                cleaned_data.append({
                    "text": abstract_text.replace("\n", " "),  # Özet
                    "title": title_text,  # AI üretimi için başlığı saklıyoruz
                    "label": 0,  # 0 = İnsan
                    "source_license": "CC-BY (PLOS)"  # Hepsi CC-BY garantili
                })

            return pd.DataFrame(cleaned_data)

        else:
            print(f"API Hatası: {response.status_code}")
            return pd.DataFrame()

    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return pd.DataFrame()


# Çalıştırır
df_human = fetch_general_cc_by_data(rows=3500)  # Fire payı için biraz fazla istiyoruz

if not df_human.empty:
    # Tam 3000 taneye eşitle
    df_human = df_human.head(3000)
    df_human.to_csv("human_data_general.csv", index=False)
    print(f"\n{len(df_human)} adet CC-BY lisanslı makale 'human_data_general.csv' dosyasına kaydedildi.")
else:
    print("Veri çekilemedi.")