# from flask import Flask, request, jsonify
# import pandas as pd
# import os

# # Ajan sınıflarını ve yardımcı programı içe aktarın
# from utils.gemini_api import GeminiAPI
# from agents.product_agent import ProductAgent
# from agents.review_agent import ReviewAgent
# from agents.decision_agent import DecisionAgent
# from agents.writer_agent import WriterAgent

# app = Flask(__name__)

# # --- Veri Yükleme ---
# def load_data():
#     """Ürün ve yorum verilerini yükler."""
#     try:
#         products_df = pd.read_csv('data/products.csv')
#         reviews_df = pd.read_csv('data/reviews.csv')
#         return products_df, reviews_df
#     except FileNotFoundError:
#         # Flask uygulamasında hata yönetimi farklıdır, doğrudan hata fırlatabiliriz
#         raise FileNotFoundError("Veri dosyaları bulunamadı. Lütfen 'data/products.csv' ve 'data/reviews.csv' dosyalarının mevcut olduğundan emin olun.")
#     except Exception as e:
#         raise Exception(f"Veri yüklenirken bir hata oluştu: {e}")

# # Uygulama başlangıcında verileri yükleyin
# products_df, reviews_df = load_data()

# # --- Gemini API ve Ajanları Başlatma ---
# # API anahtarını ortam değişkeninden doğrudan app.py içinde alın
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     # Eğer anahtar bulunamazsa, uygulamayı başlatmadan önce net bir hata mesajı verin
#     raise ValueError("Gemini API anahtarı sağlanmadı. Lütfen 'GEMINI_API_KEY' ortam değişkenini ayarlayın.")

# print(f"DEBUG: Gemini API Anahtarı bulundu: {'Evet' if GEMINI_API_KEY else 'Hayır'}") # Hata ayıklama için

# try:
#     # API anahtarını GeminiAPI sınıfına doğrudan iletin
#     gemini_client = GeminiAPI(api_key=GEMINI_API_KEY)
# except ValueError as e:
#     # Bu hata normalde yukarıdaki kontrol tarafından yakalanmalı, ancak yine de burada bırakalım.
#     raise ValueError(f"Gemini API istemcisi başlatılırken hata: {e}")

# product_agent = ProductAgent(products_df, gemini_client)
# review_agent = ReviewAgent(reviews_df, gemini_client)
# decision_agent = DecisionAgent(products_df, gemini_client)
# writer_agent = WriterAgent(gemini_client)

# # --- Flask Rotaları ---

# @app.route('/')
# def index():
#     """Ana sayfa veya API'nin çalıştığını gösteren basit bir mesaj."""
#     return "ShopAgent Flask Backend Çalışıyor! /chat adresine POST isteği gönderin."

# @app.route('/chat', methods=['POST'])
# def chat():
#     """Kullanıcı sorgularını işler ve ajan yanıtlarını döndürür."""
#     data = request.json
#     if not data:
#         return jsonify({"error": "Geçersiz JSON verisi"}), 400

#     prompt = data.get('prompt')
#     user_intent = data.get('intent', 'general') # Varsayılan 'general'
    
#     if not prompt:
#         return jsonify({"error": "Lütfen bir 'prompt' sağlayın"}), 400

#     lower_case_prompt = prompt.lower()
#     response_content = "Üzgünüm, isteğinizi anlayamadım veya işleyemedim."
#     agent_type = "ShopAgent" # Varsayılan

#     # Basit ajan yönlendirme mantığı
#     if "yorum" in lower_case_prompt or "geri bildirim" in lower_case_prompt:
#         agent_type = "Yorum Özetleme Ajanı"
#         # Ürün adını sorgudan çıkarmaya çalışın
#         product_name_query = next((p['name'] for p in products_df.to_dict('records') if p['name'].lower() in lower_case_prompt), None)
        
#         if product_name_query:
#             product_id = products_df[products_df['name'].str.lower() == product_name_query.lower()]['id'].iloc[0]
#             product_reviews = review_agent.get_reviews_for_product(product_id)
#             response_content = review_agent.summarize_reviews(product_name_query, product_reviews)
#         else:
#             response_content = "Hangi ürünün yorumlarını özetlememi istersiniz? Lütfen ürün adını belirtin."
    
#     elif "öner" in lower_case_prompt or "tavsiye" in lower_case_prompt or "hangisi iyi" in lower_case_prompt:
#         agent_type = "Kişiselleştirilmiş Öneriler Ajanı"
#         recommended_products = decision_agent.get_recommendations(prompt, user_intent)
#         response_content = decision_agent.generate_recommendation_summary(recommended_products, prompt, user_intent)

#     elif "açıklama oluştur" in lower_case_prompt or "seo metni" in lower_case_prompt:
#         agent_type = "İçerik Yazarı Ajanı"
#         # Ürün adını sorgudan çıkarmaya çalışın
#         product_name_query = next((p['name'] for p in products_df.to_dict('records') if p['name'].lower() in lower_case_prompt), None)
        
#         if product_name_query:
#             product_info = products_df[products_df['name'].str.lower() == product_name_query.lower()].iloc[0].to_dict()
#             response_content = writer_agent.generate_seo_description(product_info)
#         else:
#             response_content = "Hangi ürün için açıklama oluşturmamı istersiniz? Lütfen ürün adını belirtin."

#     else: # Varsayılan olarak ürün keşfi
#         agent_type = "Ürün Keşif Ajanı"
#         found_products = product_agent.search_products(prompt)
#         if not found_products.empty:
#             first_product = found_products.iloc[0].to_dict()
#             response_content = product_agent.generate_product_summary(first_product, prompt, user_intent)
#         else:
#             response_content = "Aradığınız ürünle ilgili bir şey bulamadım. Başka bir şey aramak ister misiniz?"

#     return jsonify({
#         "role": "assistant",
#         "content": response_content,
#         "agent_type": agent_type
#     })

# if __name__ == '__main__':
#     # Flask uygulamasını çalıştırmak için
#     # Debug modu sadece geliştirme içindir, üretimde kullanılmamalıdır.
#     # 'use_reloader=False' eklenerek "signal only works in main thread" hatası önlenir.
#     app.run(debug=True, use_reloader=False)
from flask import Flask, request, jsonify, render_template # render_template eklendi
from flask_cors import CORS
import pandas as pd
import os

# Ajan sınıflarını ve yardımcı programı içe aktarın
from utils.gemini_api import GeminiAPI
from agents.product_agent import ProductAgent
from agents.review_agent import ReviewAgent
from agents.decision_agent import DecisionAgent
from agents.writer_agent import WriterAgent

app = Flask(__name__)
# CORS'u sadece Flask sunucusunun kendi kaynağı için etkinleştirir.
# Artık index.html de Flask üzerinden sunulduğu için 'null' kaynağa gerek kalmaz.
CORS(app, origins=["http://127.0.0.1:5000"]) # Güncellenen satır

# --- Veri Yükleme ---
def load_data():
    """Ürün ve yorum verilerini yükler."""
    try:
        products_df = pd.read_csv('data/products.csv')
        reviews_df = pd.read_csv('data/reviews.csv')
        return products_df, reviews_df
    except FileNotFoundError:
        raise FileNotFoundError("Veri dosyaları bulunamadı. Lütfen 'data/products.csv' ve 'data/reviews.csv' dosyalarının mevcut olduğundan emin olun.")
    except Exception as e:
        raise Exception(f"Veri yüklenirken bir hata oluştu: {e}")

products_df, reviews_df = load_data()

# --- Gemini API ve Ajanları Başlatma ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API anahtarı sağlanmadı. Lütfen 'GEMINI_API_KEY' ortam değişkenini ayarlayın.")

print(f"DEBUG: Gemini API Anahtarı bulundu: {'Evet' if GEMINI_API_KEY else 'Hayır'}")

try:
    gemini_client = GeminiAPI(api_key=GEMINI_API_KEY)
except ValueError as e:
    raise ValueError(f"Gemini API istemcisi başlatılırken hata: {e}")

product_agent = ProductAgent(products_df, gemini_client)
review_agent = ReviewAgent(reviews_df, gemini_client)
decision_agent = DecisionAgent(products_df, gemini_client)
writer_agent = WriterAgent(gemini_client)

# --- Flask Rotaları ---

@app.route('/')
def index():
    """Ana sayfa, frontend HTML dosyasını sunar."""
    print("DEBUG: / rotasına istek alındı, index.html sunuluyor.") # Yeni
    return render_template('index.html') # Güncellenen satır

@app.route('/chat', methods=['POST'])
def chat():
    """Kullanıcı sorgularını işler ve ajan yanıtlarını döndürür."""
    print("DEBUG: /chat rotasına POST isteği alındı.")
    data = request.json
    if not data:
        print("DEBUG: Geçersiz JSON verisi.")
        return jsonify({"error": "Geçersiz JSON verisi"}), 400

    prompt = data.get('prompt')
    user_intent = data.get('intent', 'general')
    
    print(f"DEBUG: Alınan istem: '{prompt}', Amaç: '{user_intent}'")

    if not prompt:
        print("DEBUG: Boş istem alındı.")
        return jsonify({"error": "Lütfen bir 'prompt' sağlayın"}), 400

    lower_case_prompt = prompt.lower()
    response_content = "Üzgünüm, isteğinizi anlayamadım veya işleyemedim."
    agent_type = "ShopAgent"

    # Basit ajan yönlendirme mantığı
    if "yorum" in lower_case_prompt or "geri bildirim" in lower_case_prompt:
        agent_type = "Yorum Özetleme Ajanı"
        print(f"DEBUG: Ajan tipi: {agent_type}")
        
        product_name_query = None
        for p_name in products_df['name'].tolist():
            if p_name.lower() in lower_case_prompt:
                product_name_query = p_name
                break
        
        if product_name_query:
            print(f"DEBUG: Yorum için bulunan ürün adı: '{product_name_query}'")
            try:
                product_id = products_df[products_df['name'].str.lower() == product_name_query.lower()]['id'].iloc[0]
                product_reviews = review_agent.get_reviews_for_product(product_id)
                response_content = review_agent.summarize_reviews(product_name_query, product_reviews)
                print(f"DEBUG: Yorum özeti başarıyla oluşturuldu.")
            except IndexError:
                response_content = f"'{product_name_query}' ürünü için ID bulunamadı."
                print(f"DEBUG: Hata: '{product_name_query}' için ID bulunamadı.")
            except Exception as e:
                response_content = f"Yorum özetlenirken bir hata oluştu: {e}"
                print(f"DEBUG: Yorum özetleme hatası: {e}")
        else:
            response_content = "Hangi ürünün yorumlarını özetlememi istersiniz? Lütfen ürün adını belirtin."
            print("DEBUG: Yorum için ürün adı bulunamadı.")
    
    elif "öner" in lower_case_prompt or "tavsiye" in lower_case_prompt or "hangisi iyi" in lower_case_prompt:
        agent_type = "Kişiselleştirilmiş Öneriler Ajanı"
        print(f"DEBUG: Ajan tipi: {agent_type}")
        try:
            recommended_products = decision_agent.get_recommendations(prompt, user_intent)
            response_content = decision_agent.generate_recommendation_summary(recommended_products, prompt, user_intent)
            print(f"DEBUG: Öneri özeti başarıyla oluşturuldu.")
        except Exception as e:
            response_content = f"Öneri oluşturulurken bir hata oluştu: {e}"
            print(f"DEBUG: Öneri oluşturma hatası: {e}")

    elif "açıklama oluştur" in lower_case_prompt or "seo metni" in lower_case_prompt:
        agent_type = "İçerik Yazarı Ajanı"
        print(f"DEBUG: Ajan tipi: {agent_type}")
        
        product_name_query = None
        for p_name in products_df['name'].tolist():
            if p_name.lower() in lower_case_prompt:
                product_name_query = p_name
                break
        
        if product_name_query:
            print(f"DEBUG: Açıklama için bulunan ürün adı: '{product_name_query}'")
            try:
                product_info = products_df[products_df['name'].str.lower() == product_name_query.lower()].iloc[0].to_dict()
                response_content = writer_agent.generate_seo_description(product_info)
                print(f"DEBUG: Açıklama başarıyla oluşturuldu.")
            except IndexError:
                response_content = f"'{product_name_query}' ürünü için ID bulunamadı."
                print(f"DEBUG: Hata: '{product_name_query}' için ID bulunamadı.")
            except Exception as e:
                response_content = f"Açıklama oluşturulurken bir hata oluştu: {e}"
                print(f"DEBUG: Açıklama oluşturma hatası: {e}")
        else:
            response_content = "Hangi ürün için açıklama oluşturmamı istersiniz? Lütfen ürün adını belirtin."
            print("DEBUG: Açıklama için ürün adı bulunamadı.")

    else: # Varsayılan olarak ürün keşfi
        agent_type = "Ürün Keşif Ajanı"
        print(f"DEBUG: Ajan tipi: {agent_type}")
        try:
            found_products = product_agent.search_products(prompt)
            if not found_products.empty:
                first_product = found_products.iloc[0].to_dict()
                response_content = product_agent.generate_product_summary(first_product, prompt, user_intent)
                print(f"DEBUG: Ürün özeti başarıyla oluşturuldu.")
            else:
                response_content = "Aradığınız ürünle ilgili bir şey bulamadım. Başka bir şey aramak ister misiniz?"
                print("DEBUG: Ürün keşfi sonucu: Ürün bulunamadı.")
        except Exception as e:
            response_content = f"Ürün keşfi sırasında bir hata oluştu: {e}"
            print(f"DEBUG: Ürün keşfi hatası: {e}")

    print(f"DEBUG: Yanıt gönderiliyor. Ajan: {agent_type}, İçerik başlangıcı: {response_content[:50]}...")
    return jsonify({
        "role": "assistant",
        "content": response_content,
        "agent_type": agent_type
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
