import pandas as pd
from utils.gemini_api import GeminiAPI

class ProductAgent:
    """
    Ürün keşfi ve detayları sağlamaktan sorumlu ajan.
    """
    def __init__(self, products_df: pd.DataFrame, gemini_client: GeminiAPI):
        """
        ProductAgent'ı başlatır.

        Args:
            products_df (pd.DataFrame): Ürün verilerini içeren DataFrame.
            gemini_client (GeminiAPI): Gemini API istemcisi.
        """
        self.products_df = products_df
        self.gemini_client = gemini_client

    def search_products(self, query: str) -> pd.DataFrame:
        """
        Sorguya göre ürünleri arar.

        Args:
            query (str): Kullanıcının ürün arama sorgusu.

        Returns:
            pd.DataFrame: Eşleşen ürünlerin DataFrame'i.
        """
        query_lower = query.lower()
        # Ürün adı, açıklaması veya kategorisinde eşleşme arayın
        matching_products = self.products_df[
            self.products_df['name'].str.lower().str.contains(query_lower) |
            self.products_df['description'].str.lower().str.contains(query_lower) |
            self.products_df['category'].str.lower().str.contains(query_lower)
        ]
        return matching_products

    def get_product_details(self, product_id: str) -> dict:
        """
        Belirli bir ürünün detaylarını alır.

        Args:
            product_id (str): Ürünün ID'si.

        Returns:
            dict: Ürün detayları veya boş bir dict eğer bulunamazsa.
        """
        product = self.products_df[self.products_df['id'] == product_id]
        if not product.empty:
            return product.iloc[0].to_dict()
        return {}

    def generate_product_summary(self, product_info: dict, user_query: str, intent: str) -> str:
        """
        Ürün bilgileri ve kullanıcı amacına göre bir ürün özeti oluşturur.

        Args:
            product_info (dict): Ürün detayları.
            user_query (str): Kullanıcının orijinal sorgusu.
            intent (str): Kullanıcının amacı ('general', 'budget', 'quality').

        Returns:
            str: Üretilen ürün özeti.
        """
        if not product_info:
            return "Ürün bilgisi bulunamadı."

        product_details_str = (
            f"Ürün Adı: {product_info['name']}\n"
            f"Açıklama: {product_info['description']}\n"
            f"Fiyat: ${product_info['price']}\n"
            f"Kategori: {product_info['category']}\n"
            f"Değerlendirme: {product_info.get('rating', 'N/A')}/5"
        )

        intent_prompt = ""
        if intent == 'budget':
            intent_prompt = "Kullanıcı bütçe odaklı, bu yüzden ürünün uygun fiyatlı veya fiyat-performans açısından değerini vurgulayın."
        elif intent == 'quality':
            intent_prompt = "Kullanıcı kalite odaklı, bu yüzden ürünün yüksek kalitesini, dayanıklılığını ve üstün özelliklerini vurgulayın."

        prompt = (
            f"Sen bir ürün keşif ajanısın. Kullanıcıya bir ürün hakkında bilgi veriyorsun.\n"
            f"İşte ürün detayları:\n{product_details_str}\n\n"
            f"Kullanıcının orijinal sorgusu: '{user_query}'\n"
            f"{intent_prompt}\n"
            f"Bu ürünü kullanıcıya açıklayan, 2-3 cümlelik kısa ve bilgilendirici bir özet oluştur."
        )
        return self.gemini_client.generate_content(prompt)
