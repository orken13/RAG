# 📄 PDF Question Answering — Flask + FAISS + SentenceTransformers

PDF dosyalarını yükleyip içerikleri FAISS vektör veritabanına kaydeden, ardından doğal dil sorularıyla anlamsal arama yapabilen bir Flask web uygulaması.

---

## 🚀 Özellikler

- PDF yükleme ve otomatik metin çıkarma (`pypdf`)
- Metni cümle bazlı parçalara (chunk) bölme
- `all-MiniLM-L6-v2` modeliyle yerel embedding (Hugging Face)
- FAISS ile hızlı vektör benzerlik araması
- REST API üzerinden soru-cevap desteği

---

## 🗂️ Proje Yapısı

```
project/
│
├── app.py                  # Ana Flask uygulaması
├── uploads/                # Yüklenen PDF'lerin kaydedildiği klasör (otomatik oluşur)
├── templates/
│   └── index.html          # Arayüz şablonu
└── requirements.txt
```

---

## ⚙️ Kurulum

### 1. Gereksinimler

Python 3.9+ önerilir.

```bash
pip install flask pypdf faiss-cpu sentence-transformers numpy
```

> GPU kullanıyorsan `faiss-cpu` yerine `faiss-gpu` kurabilirsin.

### 2. Uygulamayı Başlat

```bash
python app.py
```

Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışır.

---

## 🔌 API Kullanımı

### `POST /upload` — PDF Yükle

PDF dosyasını yükler, metni çıkarır ve FAISS'e ekler.

**İstek (form-data):**
```
file: <pdf_dosyası>
```

**Başarılı Yanıt:**
```json
{
  "message": "ornek.pdf işlendi ve FAISS veri tabanına eklendi!"
}
```

---

### `POST /ask` — Soru Sor

Yüklenen PDF içeriğine anlamsal arama yaparak en alakalı 3 cümleyi döner.

**İstek (JSON):**
```json
{
  "question": "Makine öğrenmesi nedir?"
}
```

**Yanıt:**
```json
{
  "answer": [
    "Makine öğrenmesi, verilerden öğrenen algoritmaların bütünüdür.",
    "Bu yöntem, gözetimli ve gözetimsiz öğrenme olarak ikiye ayrılır.",
    "..."
  ]
}
```

---

## 🧠 Teknik Detaylar

| Bileşen | Kullanılan Araç |
|---|---|
| Web Framework | Flask |
| PDF Okuma | pypdf |
| Embedding Modeli | `all-MiniLM-L6-v2` (384 boyut) |
| Vektör Veritabanı | FAISS (IndexFlatL2) |
| Metin Bölme | Nokta (`. `) bazlı basit chunk'lama |

---
