# 1. استيراد مكتبة Streamlit للوصول إلى مفاتيح الأمان والبيانات السرية
import streamlit as st

# 2. استيراد مكتبة Google Generative AI المخصصة للتواصل مع نماذج Gemini
import google.generativeai as genai

# 3. جلب مفتاح الـ API بشكل آمن من secrets لتفادي أخطاء عدم التواجد
api_key = st.secrets.get("GEMINI_API_KEY", "")

# 4. التثبت من وجود المفتاح وتهيئة المكتبة بشرط توفره
if api_key:
    # 5. تهيئة مكتبة جوجل وتمرير المفتاح المستخرج
    genai.configure(api_key=api_key)


# 6. دالة فرعية لبناء النص التوجيهي (Prompt) بشكل ديناميكي ومستقر
def build_dynamic_prompt(code_text, risk_status="Low", **kwargs):
    # 7. تحويل حالة الخطورة المنطقية أو النصية إلى نص واضح للنموذج
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


# 12. دالة فرعية لجلب أسماء النماذج المتاحة والمستقرة لحسابك ديناميكياً
def get_working_models():
    # 13. قائمة المسميات المتوافقة مع الإكستنشنز الحديثة لـ API
    preferred_models = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]
    # 14. بداية كتلة جلب القائمة الديناميكية في حال فشل المسميات الثابتة
    try:
        # 15. استعلام API للحصول على كافة النماذج المدعومة للـ generateContent
        available = [m.name.replace("models/", "") for m in genai.list_models() if "generateContent" in m.supported_generation_methods]
        # 16. دمج المسميات المفضلة مع المسميات المكتشفة ديناميكياً بدون تكرار
        for m in available:
            # 17. التحقق من عدم وجود النموذج مسبقاً في القائمة
            if m not in preferred_models:
                # 18. إضافة النموذج المكتشف إلى النهاية
                preferred_models.append(m)
    # 19. التقاط خطأ الاستعلام الديناميكي والاعتماد على القائمة المفضلة
    except Exception:
        # 20. الاستمرار بالقائمة الأساسية
        pass
    # 21. إرجاع قائمة النماذج المرشحة للتجربة
    return preferred_models


# 22. الدالة الرئيسية لتحليل الكود مع تجربة النماذج المتاحة بالترتيب
def analyze_code(code_text, risk_status="Low", **kwargs):
    # 23. التحقق من توفر مفتاح API قبل إطلاق الاتصال
    if not api_key:
        # 24. إرجاع رسالة تنبيهية عند عدم ضبط المفتاح في Secrets
        return "⚠️ مفتاح GEMINI_API_KEY غير متوفر في إعدادات Streamlit Secrets."

    # 25. بناء النص التوجيهي المخصص عبر الدالة الفرعية
    prompt = build_dynamic_prompt(code_text, risk_status, **kwargs)

    # 26. الحصول على قائمة النماذج المستقرة والمتاحة لحسابك
    candidate_models = get_working_models()

    # 27. قائمة لتجميع رسائل الأخطاء في حال التعثر
    errors = []

    # 28. التكرار على النماذج لتجربة الأنسب منها
    for model_name in candidate_models:
        # 29. بداية كتلة تجربة التنفيذ للنموذج الحالي
        try:
            # 30. إنشاء كائن النموذج باستخدام الاسم الحالي
            model = genai.GenerativeModel(model_name)

            # 31. إرسال الطلب واستقبال النتيجة
            response = model.generate_content(prompt)

            # 32. إرجاع النتيجة النصية فور النجاح
            return response.text
        # 33. التقاط الاستثناء وتسجيل نص الخطأ الدقيق للنموذج
        except Exception as e:
            # 34. إضافة اسم النموذج ومضمون الخطأ للمصفوفة
            errors.append(f"• {model_name}: {str(e)}")
            # 35. الانتقال للنموذج التالي
            continue

    # 36. تحويل قائمة الأخطاء إلى نص منسق لعرضه للمستخدم
    error_details = "\n".join(errors)

    # 37. إرجاع التفاصيل التقنية الناتجة عن الاتصال
    return f"⚠️ تعذر الاتصال بـ Gemini API. تفاصيل الخطأ:\n{error_details}"


# 38. دالة تحليل الكود بنظام البث المباشر (Stream) مع دعم التسميات الحديثة
def analyze_code_with_gemini_stream(code_text, risk_status="Low", **kwargs):
    # 39. التحقق من توفر المفتاح قبل إطلاق البث
    if not api_key:
        # 40. إرجاع رسالة التنبيه تدريجياً عبر yield
        yield "⚠️ مفتاح GEMINI_API_KEY غير متوفر في إعدادات Streamlit Secrets."
        # 41. الخروج من الدالة
        return

    # 42. بناء النص التوجيهي بالدالة الفرعية
    prompt = build_dynamic_prompt(code_text, risk_status, **kwargs)

    # 43. الحصول على قائمة النماذج المستقرة
    candidate_models = get_working_models()

    # 44. قائمة لتجميع الأخطاء في حال تعثر البث
    errors = []

    # 45. التكرار على النماذج لإيجاد النموذج الشغال
    for model_name in candidate_models:
        # 46. بداية كتلة تجربة البث المباشر
        try:
            # 47. إنشاء كائن النموذج
            model = genai.GenerativeModel(model_name)

            # 48. طلب التوليد بنظام البث المباشر stream=True
            response = model.generate_content(prompt, stream=True)

            # 49. التكرار على الأجزاء الواصلة وإرجاعها
            for chunk in response:
                # 50. التأكد من وجود نص في الجزء الحالي
                if chunk.text:
                    # 51. إرجاع الجزء النصي تدريجياً
                    yield chunk.text

            # 52. الخروج من الدالة فور اكتمال البث بنجاح
            return
        # 53. التقاط الخطأ وتسجيل التفاصيل للتشخيص
        except Exception as e:
            # 54. تسجيل الخطأ مع اسم النموذج
            errors.append(f"• {model_name}: {str(e)}")
            # 55. الانتقال للنموذج التالي
            continue

    # 56. تحويل قائمة الأخطاء إلى نص منسق للبث
    error_details = "\n".join(errors)

    # 57. إرجاع رسالة الخطأ التفصيلية عبر yield
    yield f"⚠️ تعذر الاتصال بـ Gemini API. تفاصيل الخطأ:\n{error_details}"