import pandas as pd
from utils.gemini_api import GeminiAPI

class ReviewAgent:
    """
    Ürün yorumlarını özetlemekten sorumlu ajan.
    """
    def __init__(self, reviews_df: pd.DataFrame, gemini_client: GeminiAPI):
        """
        ReviewAgent'ı başlatır.

        Args:
            reviews_df (pd.DataFrame): Yorum verilerini içeren DataFrame.
            gemini_client (GeminiAPI): Gemini API istemcisi.
        """
        self.reviews_df = reviews_df
        self.gemini_client = gemini_client

    def get_reviews_for_product(self, product_id: str) -> pd.DataFrame:
        """
        Belirli bir ürünün yorumlarını alır.

        Args:
            product_id (str): Ürünün ID'si.

        Returns:
            pd.DataFrame: Ürüne ait yorumların DataFrame'i.
        """
        return self.reviews_df[self.reviews_df['productId'] == product_id]

    def summarize_reviews(self, product_name: str, reviews: pd.DataFrame) -> str:
        """
        Verilen yorumları özetler.

        Args:
            product_name (str): Yorumların ait olduğu ürünün adı.
            reviews (pd.DataFrame): Özetlenecek yorumların DataFrame'i.

        Returns:
            str: Yorumların üretilen özeti.
        """
        if reviews.empty:
            return f"{product_name} için henüz yorum bulunamadı."

        review_texts = "\n".join([f"- Derecelendirme: {row['rating']}/5, Yorum: '{row['text']}'" for index, row in reviews.iterrows()])

        prompt = (
            f"Sen bir yorum özetleme ajanısın. Aşağıdaki yorumları özetleyeceksin:\n\n"
            f"Ürün Adı: {product_name}\n"
            f"Yorumlar:\n{review_texts}\n\n"
            f"Bu yorumları, ürünün genel algısını ve hem olumlu hem de olumsuz yönlerini vurgulayarak 3-4 cümlelik kısa bir paragraf halinde özetle."
        )
        return self.gemini_client.generate_content(prompt)
