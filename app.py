from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# OpenAI istemcisi (Render ortamında API key Environment olarak ayarlanacak)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return render_template(
        "index.html",
        title="Bakımcı İboGBT",
        message="Makine arızalarında hızlı çözüm ortağınız!"
    )

@app.route("/ai", methods=["POST"])
def ai_response():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "prompt gerekli"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sen bir makine bakım uzmanısın. Kısa, net ve teknik yanıtlar ver."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
