import joblib  # استيراد مكتبة joblib لتحميل ملف النموذج المدرب pkl من القرص
import os  # استيراد مكتبة os لإدارة وتحديد مسارات الملفات والمجلدات بدقة
import re  # استيراد مكتبة re لاستخدام التعبيرات النمطية في تحليل الرموز البرمجية
import math  # استيراد مكتبة الرياضيات لحساب اللوغاريتم الرياضي المقابل لهالستيد

def extract_metrics_from_code(
    code_text, expected_features=21
):  # دالة استخراج المقاييس الرقمية من الكود البرمجي
    lines = code_text.splitlines()  # تقسيم النص البرمجي إلى قائمة من الأسطر
    loc = len(lines)  # حساب عدد الأسطر الكلي للكود
    blank_lines = sum(
        1 for line in lines if not line.strip()
    )  # حساب عدد الأسطر الفارغة
    comment_lines = sum(
        1 for line in lines if line.strip().startswith("#")
    )  # حساب عدد أسطر التعليقات
    code_lines = (
        loc - blank_lines - comment_lines
    )  # حساب الأسطر الفعلية التي تحتوي كوداً

    tokens = re.findall(
        r"\w+|[^\w\s]", code_text
    )  # استخراج جميع الكلمات والرموز البرمجية (Tokens)
    total_tokens = len(tokens)  # حساب الإجمالي الكلي للرموز البرمجية
    unique_tokens = len(set(tokens))  # حساب عدد الرموز الفريدة بدون تكرار

    # حساب تقريبي لمعاملات هالستيد الأساسية لتجنب وضع أصفار تضر بمدخلات الموديل
    n1 = float(unique_tokens)  # تقدير عدد العمليات والرموز الفريدة
    n2 = float(
        max(1, total_tokens - unique_tokens)
    )  # تقدير عدد المتغيرات والمدخلات الفريدة
    N1 = float(total_tokens)  # تقدير إجمالي عدد العمليات
    N2 = float(total_tokens)  # تقدير إجمالي عدد المتغيرات

    vocabulary = max(1.0, n1 + n2)  # حساب المفردات البرمجية الكلية (Vocabulary)
    length = max(1.0, N1 + N2)  # حساب الطول البرمجي الكلي (Length)
    volume = length * math.log2(
    vocabulary
    )  # حساب الحجم البرمجي باللوغاريتم الرياضي المناسب للأعداد العشرية بدلاً من bit_length
    cyclomatic_complexity = float(
        max(1, code_text.count("if") + code_text.count("for") + 1)
    )  # حساب تعقيد ماكيب البنائي بناءً على الجمل الشرطية والدوران

    features = [  # بناء قائمة الخصائص الـ 21 المتوافقة هيكلياً مع نمط بيانات JM1
        float(loc),  # الميزة 1: إجمالي عدد الأسطر
        cyclomatic_complexity,  # الميزة 2: التعقيد البنائي Cyclomatic Complexity v(g)
        cyclomatic_complexity,  # الميزة 3: التعقيد الأساسي Essential Complexity ev(g)
        cyclomatic_complexity,  # الميزة 4: تعقيد التصميم Design Complexity iv(g)
        float(code_lines),  # الميزة 5: عدد أسطر الكود
        float(comment_lines),  # الميزة 6: عدد أسطر التعليقات
        float(blank_lines),  # الميزة 7: عدد الأسطر الفارغة
        float(total_tokens),  # الميزة 8: عدد الرموز الكلي
        float(unique_tokens),  # الميزة 9: عدد الرموز الفريدة
        n1,  # الميزة 10: الرموز الفريدة n1
        n2,  # الميزة 11: المتغيرات الفريدة n2
        N1,  # الميزة 12: إجمالي الرموز N1
        N2,  # الميزة 13: إجمالي المتغيرات N2
        vocabulary,  # الميزة 14: المفردات البرمجية V
        length,  # الميزة 15: الطول البرمجي N
        volume,  # الميزة 16: الحجم البرمجي Volume
        float(volume / 2.0),  # الميزة 17: المستوى البرمجي Level
        float(volume * 2.0),  # الميزة 18: المجهود البرمجي Effort
        float(volume / 3000.0),  # الميزة 19: عدد الأخطاء المترتبة Bugs
        float(volume / 18.0),  # الميزة 20: الوقت المتوقع للبرمجة Time
        float(code_lines),  # الميزة 21: أسطر التنفيذ المباشر
    ]

    return features[:expected_features]  # إرجاع القائمة بالطول المطلوب تماماً


def predict_defect(code_input):  # دالة التنبؤ المباشر وحساب المخاطر
    # فحص أولي: الأسطر البسيطة جداً (مثل print) لا تعتبر وحدة برمجية مكتملة لتقييم خطئها الهيكلي
    if isinstance(code_input, str) and len(code_input.strip().splitlines()) < 2:
        return False, 5  # إرجاع عدم وجود خطأ بنسبة خطر منخفضة جداً (5%)

    model_path = os.path.join(
        "models", "gradient_boosting_model.pkl"
    )  # تحديد مسار ملف النموذج
    model = joblib.load(model_path)  # تحميل النموذج من الذاكرة

    expected_features = getattr(
        model, "n_features_in_", 21
    )  # قراءة عدد الميزات المتوقعة

    if isinstance(code_input, str):  # تحويل الكود النصي لمقيمات رقمية
        metrics_data = extract_metrics_from_code(code_input, expected_features)
    else:
        metrics_data = code_input

    

    # طباعة المصفوفة في مبوبة التشغيل لغرض الفحص والتدقيق المباشر
    print("DEBUG - Features Array:", metrics_data)

    prediction = model.predict([metrics_data])[0]  # التنبؤ بالفئة (0 أو 1)

    try:
        probabilities = model.predict_proba([metrics_data])[
            0
        ]  # حساب احتمالية الفئات
        prob_risk = probabilities[1]  # أخذ احتمالية فئة وجود الخطر
    except Exception:
        prob_risk = 0.85 if prediction == 1 else 0.15  # قيمة احتياطية عند الفشل

    is_risk = bool(prediction == 1)  # تحويل النتيجة إلى قيمة منطقية
    confidence = (
        int(prob_risk * 100) if is_risk else int((1 - prob_risk) * 100)
    )  # حساب نسبة الثقة الفتعلية الواقعية

    return is_risk, confidence  # إرجاع حالة الخطر ونسبة الثقة للدالة الاستدعائية