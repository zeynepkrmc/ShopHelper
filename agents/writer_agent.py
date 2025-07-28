import pandas as pd
from utils.gemini_api import GeminiAPI

class WriterAgent:
    """
    SEO uyumlu ürün açıklamaları veya diğer metin içerikleri üretmekten sorumlu ajan.
    """
    def __init__(self, gemini_client: GeminiAPI):
        """
        WriterAgent'ı başlatır.

        Args:
            gemini_client (GeminiAPI): Gemini API istemcisi.
        """
        self.gemini_client = gemini_client

    def generate_seo_description(self, product_info: dict, keywords: list = None) -> str:
        """
        Belirli bir ürün için SEO uyumlu bir açıklama oluşturur.

        Args:
            product_info (dict): Ürün detayları (name, description, category, price vb.).
            keywords (list, optional): Açıklamaya dahil edilecek anahtar kelimeler.

        Returns:
            str: Üretilen SEO uyumlu ürün açıklaması.
        """
        if not product_info:
            return "Ürün bilgisi sağlanmadı."

        product_details_str = (
            f"Ürün Adı: {product_info.get('name', 'Bilinmeyen Ürün')}\n"
            f"Kategori: {product_info.get('category', 'Genel')}\n"
            f"Mevcut Açıklama: {product_info.get('description', 'Yok')}\n"
            f"Fiyat: ${product_info.get('price', 'N/A')}"
        )

        keyword_prompt = ""
        if keywords:
            keyword_prompt = f"Açıklamaya şu anahtar kelimeleri dahil etmeye çalış: {', '.join(keywords)}."

        prompt = (
            f"Sen bir içerik yazarı ajanısın. Aşağıdaki ürün bilgileri için SEO dostu, "
            f"ikna edici ve bilgilendirici bir ürün açıklaması oluştur.\n"
            f"Açıklama 3-5 cümle uzunluğunda olmalı ve ürünün temel faydalarını ve özelliklerini vurgulamalıdır.\n"
            f"{keyword_prompt}\n\n"
            f"Ürün Detayları:\n{product_details_str}\n\n"
            f"SEO uyumlu ürün açıklamasını şimdi oluştur:"
        )
        return self.gemini_client.generate_content(prompt)

    def generate_marketing_copy(self, topic: str, context: str) -> str:
        """
        Belirli bir konu ve bağlam için genel pazarlama metni oluşturur.

        Args:
            topic (str): Pazarlama metninin konusu (örn. "yeni kulaklıklar").
            context (str): Metnin oluşturulması için ek bağlam veya detaylar.

        Returns:
            str: Üretilen pazarlama metni.
        """
        prompt = (
            f"Sen bir pazarlama metni yazarı ajanısın. Aşağıdaki konu ve bağlama göre "
            f"kısa ve çekici bir pazarlama metni oluştur.\n\n"
            f"Konu: {topic}\n"
            f"Bağlam: {context}\n\n"
            f"Pazarlama metnini şimdi oluştur (2-4 cümle):"
        )
        return self.gemini_client.generate_content(prompt)
