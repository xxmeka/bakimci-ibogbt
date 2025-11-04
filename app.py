from flask import Flask, render_template, request, jsonify
import os
import openai

app = Flask(__name__)

# ✅ OpenAI API anahtarı (Render’da Environment’a ekleyeceksin)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ai', methods=['POST'])
def ai_response():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        if not user_message:
            return jsonify({"response": "Lütfen bir arıza veya sorun yaz."})

        # 🔹 Basit yapay zekâ yanıtı
        prompt = f"Sen bir fabrika bakım asistanısın. Şu soruna çözüm önerisi ver:\n\n{user_message}"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen endüstriyel bakım uzmanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        reply = completion.choices[0].message["content"].strip()
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Hata oluştu: {e}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
