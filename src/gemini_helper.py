# 1. استيراد مكتبة Streamlit للوصول إلى البيانات السرية ومفاتيح الأمان
import streamlit as st

# 2. استيراد مكتبة Google Generative AI المخصصة للتواصل مع نماذج Gemini
import google.generativeai as genai

# 3. جلب مفتاح الـ API بشكل آمن باستخدام .get() لتفادي حدوث KeyError في حال عدم وجوده
api_key = st.secrets.get("GEMINI_API_KEY", "")

# 4. التثبت من وجود المفتاح وتهيئة المكتبة بشرط توفره
if api_key:
    # 5. تهيئة مكتبة جوجل وتمرير المفتاح المستخرج
    genai.configure(api_key=api_key)


# 6. دالة فرعية لبناء النص التوجيهي (Prompt) وتدعم استقبال أي معاملات مرنة عبر **kwargs
def build_dynamic_prompt(code_text, risk_status="Low", **kwargs):
    # 7. تحويل القيمة المنطقية (True/False) أو النصية لحالة الخطورة إلى نص عربي وأنجليزي واضحة
    if isinstance(risk_status, bool):
        # 8. تحويل True إلى "عالية (High)" وتحويل False إلى "منخفضة (Low)"
        status_str = "عالية (High)" if risk_status else "منخفضة (Low)"
    else:
        # 9. اعتماد النص الممرر كما هو في حال كان نصاً
        status_str = str(risk_status)

    # 10. صياغة النص التوجيهي المخصص لنموذج الذكاء الاصطناعي
    prompt = f"""
    أنت خبير فحص جودة وأمن برمجيات. قم بتحليل الكود البرمجي التالي (تقييم المخاطر الهيكلية المحسوبة محلياً: {status_str}):
    
    ```python
    {code_text}
    ```
    
    المطلوب منك بالتحديد:
    1. تقييم جودة وأمان الكود، وتحديد أي ثغرات أو أخطاء برمجية إن وُجدت، أو التأكيد على سلامته ونظافته إن كان خالياً منها.
    2. تحديد درجة الخطورة الأمنية الفعلية (High, Medium, Low).
    3. تقديم الكود المصحح أو المحسن بالكامل مع كتابة جميع التعليقات الشارحة داخل الكود باللغة العربية.
    4. تقديم شرح سريع ومختصر جداً للتعديلات أو أفضل الممارسات المقترحة.
    
    قواعد صارمة للغة والتنسيق:
    - يجب أن تكون جميع الشروحات والنصوص والتعليقات المكتوبة داخل الكود وخارجه باللغة العربية فقط.
    - يُسمح بترك الأكواد البرمجية والمصطلحات التقنية الأساسية فقط باللغة الإنجليزية.
    """
    # 11. إرجاع النص التوجيهي المكتمل للجهة المستدعية
    return prompt


# 12. الدالة الرئيسية لتحليل الكود وتدعم استقبال المعاملات المرنة **kwargs لمنع أخطاء TypeError
def analyze_code(code_text, risk_status="Low", **kwargs):
    # 13. التحقق من توفر مفتاح API قبل إطلاق الاتصال
    if not api_key:
        # 14. إرجاع رسالة تنبيهية عند عدم ضبط المفتاح في Secrets
        return "⚠️ مفتاح GEMINI_API_KEY غير متوفر في إعدادات Streamlit Secrets."

    # 15. بناء النص التوجيهي المخصص عبر الدالة الفرعية
    prompt = build_dynamic_prompt(code_text, risk_status, **kwargs)

    # 16. قائمة النماذج المتاحة للتجربة بالترتيب
    candidate_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

    # 17. التكرار على جميع النماذج لتجربة الاستجابة
    for model_name in candidate_models:
        # 18. بداية كتلة تجربة التنفيذ للنموذج الحالي
        try:
            # 19. إنشاء كائن النموذج باستخدام الاسم الحالي
            model = genai.GenerativeModel(model_name)

            # 20. إرسال الطلب واستقبال النتيجة
            response = model.generate_content(prompt)

            # 21. إرجاع النتيجة النصية فور النجاح
            return response.text
        # 22. التقاط الخطأ والسيطرة عليه في حال تعذر النموذج
        except Exception:
            # 23. الانتقال للنموذج التالي في القائمة
            continue

    # 24. إرجاع نص توضيحي عند استنفاد جميع النماذج
    return "⚠️ تم تجاوز الحد المسموح لطلبات Gemini API مؤقتاً. تم الاعتماد على تقييم النموذج المحلي."


# 25. دالة تحليل الكود بنظام البث المباشر وتدعم **kwargs لضمان التوافق مع app.py
def analyze_code_with_gemini_stream(code_text, risk_status="Low", **kwargs):
    # 26. التحقق من توفر المفتاح قبل إطلاق البث
    if not api_key:
        # 27. إرجاع رسالة التنبيه تدريجياً عبر yield
        yield "⚠️ مفتاح GEMINI_API_KEY غير متوفر في إعدادات Streamlit Secrets."
        # 28. الخروج من الدالة
        return

    # 29. بناء النص التوجيهي بالدالة الفرعية
    prompt = build_dynamic_prompt(code_text, risk_status, **kwargs)

    # 30. قائمة النماذج المتاحة للتجربة
    candidate_models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

    # 31. التكرار على النماذج لإيجاد النموذج الشغال
    for model_name in candidate_models:
        # 32. بداية كتلة تجربة البث المباشر
        try:
            # 33. إنشاء كائن النموذج
            model = genai.GenerativeModel(model_name)

            # 34. طلب التوليد بنظام البث المباشر stream=True
            response = model.generate_content(prompt, stream=True)

            # 35. التكرار على الأجزاء الواصلة وإرجاعها
            for chunk in response:
                # 36. التأكد من وجود نص في الجزء الحالي
                if chunk.text:
                    # 37. إرجاع الجزء النصي تدريجياً
                    yield chunk.text

            # 38. الخروج من الدالة فور اكتمال البث بنجاح
            return
        # 39. التقاط الخطأ وتجربة النموذج التالي
        except Exception:
            # 40. الانتقال للنموذج التالي
            continue

    # 41. إرجاع رسالة تنبيهية عند تعذر كافة النماذج
    yield "⚠️ تم تجاوز الحد المسموح لطلبات Gemini API مؤقتاً. تم الاعتماد على تقييم النموذج المحلي."