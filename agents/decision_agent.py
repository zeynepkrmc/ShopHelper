import pandas as pd
from utils.gemini_api import GeminiAPI

class DecisionAgent:
    """
    Kullanıcı amacına (bütçe odaklı, kalite odaklı) göre kişiselleştirilmiş
    öneriler ve karar desteği sağlamaktan sorumlu ajan.
    """
    def __init__(self, products_df: pd.DataFrame, gemini_client: GeminiAPI):
        """
        DecisionAgent'ı başlatır.

        Args:
            products_df (pd.DataFrame): Ürün verilerini içeren DataFrame.
            gemini_client (GeminiAPI): Gemini API istemcisi.
        """
        self.products_df = products_df
        self.gemini_client = gemini_client

    def get_recommendations(self, user_query: str, intent: str) -> pd.DataFrame:
        """
        Kullanıcı sorgusu ve amacına göre ürün önerileri sunar.

        Args:
            user_query (str): Kullanıcının orijinal sorgusu (örn. "kulaklık önerisi").
            intent (str): Kullanıcının amacı ('general', 'budget', 'quality').

        Returns:
            pd.DataFrame: Önerilen ürünlerin DataFrame'i.
        """
        # Sorgudan anahtar kelimeleri çıkarın (basit bir yaklaşım)
        keywords = [word for word in user_query.lower().split() if len(word) > 3 and word not in ["önerisi", "öner", "için", "en", "iyi", "bir", "ne"]]

        # Kategori veya açıklama bazında filtreleme
        filtered_products = self.products_df[
            self.products_df['name'].str.lower().apply(lambda x: any(k in x for k in keywords)) |
            self.products_df['description'].str.lower().apply(lambda x: any(k in x for k in keywords)) |
            self.products_df['category'].str.lower().apply(lambda x: any(k in x for k in keywords))
        ]

        if filtered_products.empty:
            # Eğer belirli bir eşleşme yoksa, genel popüler ürünleri veya en yüksek puanlıları döndür
            filtered_products = self.products_df.sort_values(by='rating', ascending=False).head(5)

        # Amaca göre sıralama
        if intent == 'budget':
            # Fiyata göre artan sırada sırala
            recommended_products = filtered_products.sort_values(by='price', ascending=True).head(3)
        elif intent == 'quality':
            # Derecelendirmeye göre azalan sırada sırala (veya fiyata göre artan, yüksek fiyat = yüksek kalite varsayımıyla)
            recommended_products = filtered_products.sort_values(by=['rating', 'price'], ascending=[False, False]).head(3)
        else: # 'general'
            # Derecelendirmeye göre azalan sırada sırala
            recommended_products = filtered_products.sort_values(by='rating', ascending=False).head(3)

        return recommended_products

    def generate_recommendation_summary(self, recommended_products: pd.DataFrame, user_query: str, intent: str) -> str:
        """
        Önerilen ürünler için bir özet oluşturur.

        Args:
            recommended_products (pd.DataFrame): Önerilen ürünlerin DataFrame'i.
            user_query (str): Kullanıcının orijinal sorgusu.
            intent (str): Kullanıcının amacı ('general', 'budget', 'quality').

        Returns:
            str: Üretilen öneri özeti.
        """
        if recommended_products.empty:
            return "Maalesef isteğinize uygun bir öneri bulamadım."

        product_list_str = "\n".join([
            f"- {row['name']} ({row['category']}): ${row['price']} - {row.get('rating', 'N/A')}/5 yıldız. Açıklama: {row['description']}"
            for index, row in recommended_products.iterrows()
        ])

        intent_prompt = ""
        if intent == 'budget':
            intent_prompt = "Bu öneriler bütçe dostu seçeneklerdir. Fiyat-performans oranlarını vurgulayın."
        elif intent == 'quality':
            intent_prompt = "Bu öneriler yüksek kaliteli ve performans odaklıdır. Üstün özelliklerini ve dayanıklılıklarını vurgulayın."

        prompt = (
            f"Sen kişiselleştirilmiş bir öneri ajanısın. Kullanıcıya aşağıdaki ürünleri öneriyorsun:\n\n"
            f"Kullanıcının orijinal sorgusu: '{user_query}'\n"
            f"Kullanıcının amacı: {intent}\n"
            f"Önerilen Ürünler:\n{product_list_str}\n\n"
            f"{intent_prompt}\n"
            f"Bu ürünleri kullanıcıya açıklayan, neden uygun olduklarını belirten ve karar vermelerine yardımcı olacak 3-5 cümlelik ikna edici bir özet oluştur."
        )
        return self.gemini_client.generate_content(prompt)
