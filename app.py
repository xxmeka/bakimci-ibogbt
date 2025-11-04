from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI istemcisini başlat
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    try:
        # Yeni OpenAI API sistemi
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # gerekirse "gpt-4o" da kullanabilirsin
            messages=[
                {"role": "system", "content": "Sen bir bakım asistanısın. Makine arızalarını analiz et, çözüm önerileri sun."},
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Render'da otomatik port alır ama lokalde test için 10000 portu açık
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
