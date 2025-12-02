from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# --- ÇOKLU MODEL YÜKLEME ---
# Buraya 4. modeli ekliyoruz
models = {
    'Logistic Regression': joblib.load('model_lr.pkl'),
    'Support Vector Machine (SVM)': joblib.load('model_svm.pkl'),
    'Naive Bayes': joblib.load('model_nb.pkl'),
    'Random Forest': joblib.load('model_rf.pkl') # <-- YENİ
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        gelen_metin = request.form['metin_kutusu']
        
        if not gelen_metin:
            return render_template('index.html', sonuc=None)

        results = []

        # Döngü artık 4 kez dönecek
        for model_name, model in models.items():
            prediction = model.predict([gelen_metin])[0]
            ai_probability = model.predict_proba([gelen_metin])[0][1] * 100
            
            if prediction == 1:
                label = "AI (Yapay Zeka)"
                color = "red"
                prob_display = ai_probability
            else:
                label = "İNSAN"
                color = "green"
                prob_display = 100 - ai_probability
            
            results.append({
                'name': model_name,
                'label': label,
                'probability': f"%{prob_display:.1f}",
                'raw_prob': ai_probability,
                'color': color
            })

        return render_template('index.html', results=results, metin=gelen_metin)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)