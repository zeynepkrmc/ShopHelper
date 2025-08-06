[videolar.zip](https://github.com/user-attachments/files/21631040/videolar.zip)
# ShopHelper
ShopHelper – LLM Destekli Çoklu Ajan E-ticaret Asistanı
ShopHelper, e-ticaret platformlarında kullanıcıların daha bilinçli alışveriş kararları vermelerine yardımcı olmak amacıyla geliştirilmiş, büyük dil modelleri (LLM'ler) ve akıllı istem stratejileri kullanan yenilikçi bir çoklu ajan sistemidir. Bu proje, kullanıcı sorgularına bağlama dayalı, kişiselleştirilmiş ve zengin yanıtlar sunarak geleneksel alışveriş deneyimini dönüştürmeyi hedeflemektedir.

# Temel Özellikler

Çoklu Ajan Mimarisi:
- Ürün Keşif Ajanı: Kullanıcı sorgularına göre ilgili ürünleri bulur ve detaylarını sunar.
- Yorum Özetleme Ajanı: Belirli ürünler için müşteri yorumlarını özetleyerek hızlı bir genel bakış sağlar.
- Kişiselleştirilmiş Öneriler Ajanı: Kullanıcının amacına (bütçe odaklı, kalite odaklı vb.) göre özelleştirilmiş ürün önerileri sunar.
- İçerik Yazarı Ajanı: Ürünler için SEO uyumlu açıklamalar veya pazarlama metinleri oluşturur.
- Retrieval-Augmented Generation (RAG): Yapılandırılmış ürün ve yorum veri setleri (CSV) kullanılarak, LLM'lere bağlam sağlanır ve böylece daha doğru ve ilgili yanıtlar üretilir.
- Multi-Context Prompting (MCP): Kullanıcı amacını (örn. bütçe, kalite) LLM istemlerine dahil ederek ajan davranışının dinamik olarak uyarlanmasını sağlar.
- LLM Entegrasyonu: Doğal diyalog, dinamik açıklamalar ve ajanlar arası muhakeme için Google Gemini API kullanılır.

# Mimari
- ShopAgent projesi, net bir sorumluluk ayrımı sağlayan katmanlı bir mimariye sahiptir:
- Frontend (Kullanıcı Arayüzü): HTML ve JavaScript ile oluşturulmuş basit ve interaktif bir web arayüzü. Kullanıcı girişlerini alır ve backend API'sine istek gönderir.
- Backend (API ve Ajan Mantığı): Python ve Flask framework'ü kullanılarak geliştirilmiştir. Gelen HTTP isteklerini işler, ajanları koordine eder ve LLM'ler ile etkileşime girerek yanıtları oluşturur.
- Ajan Katmanı: Her biri belirli bir e-ticaret görevine odaklanmış ayrı Python sınıfları olarak tasarlanmış otonom ajanlar.
- Veri Katmanı: Ürün ve yorum bilgilerini içeren sahte CSV veri setleri (RAG için temel).
- LLM Entegrasyonu: google-generativeai kütüphanesi aracılığıyla Gemini API ile iletişim kurar.

# Kullanılan Teknolojiler
- Python: Backend mantığı ve ajan geliştirme için ana dil.
- Flask: Hafif ve esnek bir web framework'ü olarak backend API'sini oluşturmak için kullanılır.
- Pandas: CSV veri setlerini yüklemek ve işlemek için.
- google-generativeai: Gemini API ile etkileşim için Python kütüphanesi.
- flask-cors: Çapraz kaynak isteklerini yönetmek için (frontend'in backend'e erişimi için).
- HTML/CSS/JavaScript: Kullanıcı arayüzü için.
- Tailwind CSS: Hızlı ve modern UI tasarımı için CSS framework'ü.

# Kurulum ve Çalıştırma
- Depoyu klonlayın.
- Gemini API Anahtarınızı Ayarlayın:
  Google AI Studio'dan bir Gemini API anahtarı alın ve bunu bir ortam değişkeni olarak ayarlayın.
  * Windows (CMD):
  set GEMINI_API_KEY=SİZİN_GERÇEK_API_ANAHTARINIZ
  * Windows (PowerShell):
  $env:GEMINI_API_KEY="SİZİN_GERÇEK_API_ANAHTARINIZ"
  * Linux/macOS:
  export GEMINI_API_KEY="SİZİN_GERÇEK_API_ANAHTARINIZ"
- Terminalde flask run veya bat uzantılı dosyaya çift tıklayıp açın.
