from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os  # <-- potrzebne do pobierania zmiennej środowiskowej

app = Flask(__name__)
CORS(app)

# Pobierz klucz API z bezpiecznej zmiennej środowiskowej
openai.api_key = os.getenv("OPENAI_API_KEY")

# Mini baza FAQ (możesz potem ją rozbudować)
faq = {
    "czy tworzycie strony": "Tak! Tworzymy nowoczesne strony internetowe – zobacz: https://biznesbot.pl/stronyinternetowe/",
    "czy robicie chatboty": "Tak, to nasza specjalność! Zobacz demo: https://biznesbot.pl/demo-chatboty/",
    "system rezerwacji": "Oczywiście – systemy z integracją Google Kalendarza i e-mail: https://biznesbot.pl/demo-systemy-rezerwacji/",
    "szkolenia": "Oferujemy szkolenia IT – np. Excel, WordPress, automatyzacje: https://biznesbot.pl/szkolenia-it/",
    "asystenci rezerwacji": "Tak – demo znajdziesz tutaj: https://biznesbot.pl/asystenci-rezerwacji/",
    "kontakt": "Napisz na kontakt@biznesbot.pl lub zadzwoń: 725 777 393. Jesteśmy też na WhatsApp!",
    "oferta": "Sprawdź pełną ofertę na: https://biznesbot.pl/oferta/",
    "blog": "Na blogu znajdziesz porady i inspiracje: https://biznesbot.pl/blog/",
}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").lower()

    # Najpierw przeszukaj lokalne FAQ
    for key, answer in faq.items():
        if key in user_input:
            return jsonify({"reply": answer})

    try:
        # Jeśli nie pasuje do FAQ – użyj OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": (
                    "Jesteś Navi – asystent AI projektu BiznesBot.pl. "
                    "Zachowuj się uprzejmie, z klasą. Zawsze gdy to możliwe, przypomnij, że BiznesBot tworzy chatboty, strony internetowe, systemy rezerwacji i szkolenia IT. "
                    "Zachęcaj subtelnie do kontaktu: kontakt@biznesbot.pl, tel. 725 777 393, WhatsApp. "
                    "Jeśli użytkownik pyta o coś niezwiązanego (np. naleśniki), odpowiadaj naturalnie, ale kończ propozycją poznania usług BiznesBot."
                )},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Błąd: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
