import os
import numpy as np
import pypdf
import faiss
from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer

# Flask başlat
app = Flask(__name__)

# Hugging Face gömme modelini yükle
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# FAISS vektör veritabanını oluştur
dimension = 384  # MiniLM modelinin vektör boyutu
index = faiss.IndexFlatL2(dimension)
documents = []  # Metinleri saklamak için bir liste


def extract_text_from_pdf(pdf_path):
    """PDF'den metni çıkarır."""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    """PDF yükleyip FAISS'e ekler."""
    if 'file' not in request.files:
        return jsonify({"error": "Dosya yüklenmedi!"}), 400

    file = request.files['file']
    pdf_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(pdf_path)

    text = extract_text_from_pdf(pdf_path)
    chunks = text.split(". ")  # Noktalara göre metni bölelim

    global documents
    documents.extend(chunks)

    vectors = embedding_model.encode(chunks)  # Metni vektörleştir
    index.add(np.array(vectors, dtype=np.float32))  # FAISS’e ekle

    return jsonify({"message": f"{file.filename} işlendi ve FAISS veri tabanına eklendi!"})


@app.route('/ask', methods=['POST'])
def ask_question():
    """Kullanıcının sorusunu FAISS ile eşleştirip en iyi cevabı bulur."""
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Soru girilmedi!"}), 400

    question_vector = embedding_model.encode([question]).astype(np.float32)
    scores, indices = index.search(question_vector, k=3)

    results = [documents[i] for i in indices[0] if i < len(documents)]
    return jsonify({"answer": results})


if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
