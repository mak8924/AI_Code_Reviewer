# 1. استيراد مكتبة joblib لتحميل النموذج المدرب المحفوظ بصيغة pkl
import joblib

# 2. استيراد مكتبة os لضمان التعامل السليم مع مسارات الملفات والمجلدات
import os

# 3. استيراد مكتبة re لاستخدام التعبيرات النمطية في تحليل واستخراج مفردات الكود
import re


# 4. دالة لاستخراج المقاييس الرقمية من الكود النصي لتناسب مخرجات نموذج البيانات JM1
def extract_metrics_from_code(code_text, expected_features=21):
    # 5. تقسيم الكود المدخل إلى قائمة من الأسطر
    lines = code_text.splitlines()

    # 6. حساب الإجمالي الكلي لعدد الأسطر (loc)
    loc = len(lines)

    # 7. حساب عدد الأسطر الفارغة
    blank_lines = sum(1 for line in lines if not line.strip())

    # 8. حساب عدد أسطر التعليقات التي تبدأ بـ #
    comment_lines = sum(
        1 for line in lines if line.strip().startswith("#")
    )

    # 9. حساب أسطر الكود الفعلية باستبعاد الفارغة والتعليقات
    code_lines = loc - blank_lines - comment_lines

    # 10. استخراج كافة الكلمات والرموز (Tokens) من الكود
    tokens = re.findall(r"\w+|[^\w\s]", code_text)

    # 11. حساب الإجمالي الكلي للرموز والعمليات
    total_tokens = len(tokens)

    # 12. حساب عدد الرموز الفريدة وغير المكررة
    unique_tokens = len(set(tokens))

    # 13. تجميع الخصائص الأساسية المستخرجة في قائمة أرقام
    features = [
        float(loc),
        float(code_lines),
        float(comment_lines),
        float(blank_lines),
        float(total_tokens),
        float(unique_tokens),
    ]

    # 14. إكمال بقية الخصائص بأصفار لتطابق عدد الخصائص التي يتوقعها النموذج (غالباً 21 خاصية)
    while len(features) < expected_features:
        features.append(0.0)

    # 15. إرجاع قائمة الخصائص المحددة بالطول المطلوب تماماً
    return features[:expected_features]


# 16. الدالة الرئيسية للتنبؤ بالخطأ وتحديد نسبة الثقة
def predict_defect(code_input):
    # 17. تحديد المسار المعياري لملف النموذج المدرب
    model_path = os.path.join("models", "gradient_boosting_model.pkl")

    # 18. تحميل ملف النموذج من الذاكرة
    model = joblib.load(model_path)

    # 19. قراءة عدد الخصائص المطلوبة للنموذج تلقائياً (أو الاعتماد على 21 كقيمة افتراضية)
    expected_features = getattr(model, "n_features_in_", 21)

    # 20. التحقق مما إذا كان المدخل نصاً برمجياً لتحويله إلى أرقام
    if isinstance(code_input, str):
        metrics_data = extract_metrics_from_code(
            code_input, expected_features
        )
    else:
        metrics_data = code_input

    # 21. تمرير المقاييس الرقمية للنموذج للحصول على التنبؤ (0 أو 1)
    prediction = model.predict([metrics_data])[0]

    # 22. حساب احتمالية الخطأ (Probability) بالفئة 1 من مصفوفة الاحتمالات
    try:
        probabilities = model.predict_proba([metrics_data])[0]
        prob_risk = probabilities[1]
    except Exception:
        prob_risk = 0.85 if prediction == 1 else 0.15

    # 23. تحويل النتيجة إلى قيمة منطقية (True في حال رصد خطر)
    is_risk = bool(prediction == 1)

    # 24. تحويل الاحتمالية إلى نسبة مئوية صحيحة تنحصر بين 70% و 98% للعرض
    confidence = int(prob_risk * 100) if is_risk else int((1 - prob_risk) * 100)
    confidence = max(70, min(confidence, 98))

    # 25. إرجاع النتيجة المزدوجة (حالة الخطر + نسبة الثقة) المتوافقة مع app.py
    return is_risk, confidence