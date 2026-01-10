# 🤖 AI vs. Human: Academic Text Classification

Bu proje, akademik makale özetlerinin (abstract) **insanlar** tarafından mı yoksa **üretken yapay zeka modelleri** (ChatGPT, Gemini vb.) tarafından mı yazıldığını tespit eden bir Doğal Dil İşleme (NLP) modelidir.

## 🎯 Proje Amacı
Büyük Dil Modellerinin (LLM) akademik yazımda artan kullanımıyla birlikte, bilimsel içeriğin özgünlüğünü ayırt etmek zorlaşmıştır. Bu proje, metin madenciliği yöntemleri kullanarak makine ve insan yazımı metinler arasındaki dilbilgisel ve istatistiksel farkları analiz etmeyi amaçlar.

## 📂 Veri Seti ve Özellikler
Projede akademik makale özetleri kullanılmıştır.
- **Toplam Veri:** 6.000 Adet Makale Özeti
- **Dağılım:** %50 İnsan Yazımı / %50 Yapay Zeka Üretimi (Dengeli Veri Seti)
- **Kaynak:** arXiv API ve OpenAI (Data Augmentation için)

## 🛠️ Kullanılan Teknolojiler ve Yöntemler
- **Dil:** Python
- **Kütüphaneler:** Scikit-learn, Pandas, NLTK, Matplotlib
- **Vektörleştirme (Feature Extraction):** - **TF-IDF (Term Frequency-Inverse Document Frequency):** Kelimelerin metin içindeki önem ağırlıklarını hesaplamak için kullanıldı.
- **Modeller:** - Naive Bayes (MultinomialNB)
  - Logistic Regression
  - Support Vector Machines (SVM)
  - Random Forest

## ⚙️ Veri İşleme Süreci (Pipeline)
Modelin başarısını artırmak için ham metin üzerinde aşağıdaki ön işleme adımları uygulanmıştır:
1. **Cleaning:** Noktalama işaretleri ve özel karakterlerin temizlenmesi.
2. **Normalization:** Tüm metnin küçük harfe çevrilmesi (Lowercasing).
3. **Stopwords Removal:** Anlam taşımayan (the, is, at, vb.) kelimelerin atılması.
4. **Lemmatization/Stemming:** Kelimelerin kök haline indirgenmesi.

## 📊 Sonuçlar
Test verisi üzerinde elde edilen başarı metrikleri:

| Model | Accuracy | F1-Score |
|-------|----------|----------|
| **Naive Bayes** | %[95] | %[94] |
| Logistic Regression | %[92] | %[91] |

> **Analiz:** Yapay zeka tarafından yazılan metinlerin daha düşük varyansa (daha standart kelime kullanımı) sahip olduğu, insan metinlerinin ise daha karmaşık cümle yapıları içerdiği gözlemlenmiştir.

## 🚀 Kurulum ve Kullanım

Projeyi yerel ortamınızda çalıştırmak için:

1. **Repoyu klonlayın:**
   ```bash
   git clone [https://github.com/byigitakbulut/AIorHuman_ML_Model.git]

2. **Terminalde dosyayı açıp app.py dosyasını Python ile çalıştırın:**
   ```bash
   python app.py
