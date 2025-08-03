    @echo off
    REM Bu dosya, Gemini API anahtarını ortam değişkeni olarak ayarlar ve Streamlit uygulamasını başlatır.

    REM Lütfen "BURAYA_GERCEK_API_ANAHTARINIZI_YAPISTIRIN" kısmını kendi gerçek Gemini API anahtarınızla değiştirin.
    REM Tırnak işareti kullanmayın ve eşittir işaretinin etrafında boşluk bırakmayın.
    set GEMINI_API_KEY=AIzaSyAXoTWdY6f7sMu9zZN2-TuWcEQDMTTmPYg

    REM Ortam değişkeninin doğru ayarlandığını kontrol etmek için (isteğe bağlı, hata ayıklama için)
    echo Ortam degiskeni kontrolu: GEMINI_API_KEY=%AIzaSyAXoTWdY6f7sMu9zZN2-TuWcEQDMTTmPYg%

    REM Streamlit uygulamasını başlat
    streamlit run app.py

    REM Uygulama kapandığında pencerenin hemen kapanmaması için bekler
    pause
    