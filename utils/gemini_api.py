import os
import google.generativeai as genai

class GeminiAPI:
    """
    Gemini API'si ile etkileşim kurmak için bir sarmalayıcı sınıfı.
    """
    def __init__(self, api_key=None, model_name="gemini-2.0-flash"):
        """
        GeminiAPI sınıfını başlatır.

        Args:
            api_key (str, optional): Gemini API anahtarı. Sağlanmazsa,
                                     GEMINI_API_KEY ortam değişkeninden alınır.
            model_name (str): Kullanılacak Gemini modelinin adı.
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Gemini API anahtarı sağlanmadı. Lütfen 'GEMINI_API_KEY' ortam değişkenini ayarlayın veya başlatırken 'api_key' parametresini iletin.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt: str) -> str:
        """
        Verilen istemle içerik üretir.

        Args:
            prompt (str): İçerik üretmek için kullanılacak istem.

        Returns:
            str: Üretilen metin.
        """
        try:
            response = self.model.generate_content(prompt)
            # Eğer candidates mevcutsa ve ilk candidate'in text'i varsa
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            return "Üretilen içerik bulunamadı."
        except Exception as e:
            print(f"Gemini API çağrısında hata: {e}")
            return f"Üzgünüm, şu anda isteğinizi işleyemiyorum. Hata: {e}"

# Örnek kullanım (test amaçlı)
if __name__ == "__main__":
    # Ortam değişkeni olarak GEMINI_API_KEY'i ayarladığınızdan emin olun
    # Örneğin: export GEMINI_API_KEY="YOUR_API_KEY"
    try:
        gemini_client = GeminiAPI()
        test_prompt = "Merhaba, sen kimsin?"
        print(f"İstem: {test_prompt}")
        response = gemini_client.generate_content(test_prompt)
        print(f"Yanıt: {response}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
