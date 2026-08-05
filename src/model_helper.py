import ast  # استيراد مكتبة ast لتحليل الشجرة المجردة للكود البرمجي
import joblib  # استيراد مكتبة joblib لتحميل نموذج التعلم الآلي المحفوظ
import math  # استيراد مكتبة math لإجراء الحسابات واللوغاريتمات الرياضية
import os  # استيراد مكتبة os لإدارة مسارات الملفات والنظام
import re  # استيراد مكتبة re للبحث عبر التعبيرات النمطية المتقدمة


def detect_security_vulnerabilities(code_text):
    # دالة موحدة وفائقة الدقة لكشف الثغرات الهيكلية والأمنية لكافة اللغات
    patterns = [
        r"(SELECT|INSERT|DELETE|UPDATE)\s+.*\s+(FROM|INTO|SET).*%[s|d]",  # 1. كشف ثغرة SQL Injection عبر التنسيق بـ %
        r"(SELECT|INSERT|DELETE|UPDATE)\s+.*\s+(FROM|INTO|SET).*\+",  # 2. كشف ثغرة SQL Injection عبر الدمج بالنصوص +
        r"(SELECT|INSERT|DELETE|UPDATE)\s+.*\s+(FROM|INTO|SET).*\{",  # 3. كشف ثغرة SQL Injection عبر f-strings أو Format
        r"\b(eval|exec|os\.system|subprocess)\b",  # 4. كشف أوامر النظام المباشرة والتنفيذ الديناميكي في Python
        r"\b(passthru|shell_exec|system|popen)\b",  # 5. كشف تنفيذ أوامر النظام في PHP
        r"Runtime\.getRuntime\(\)\.exec",  # 6. كشف تنفيذ أوامر النظام المباشرة في Java
        r"new\s+\w+\[.*\]",  # 7. كشف تخصيص الذاكرة الديناميكية في C++ (فحص تسريب الذاكرة)
        r"\b(strcpy|strcat|sprintf|gets)\b",  # 8. كشف دوال C/C++ الخطيرة المسببة لتجاوز سعة المجمع Buffer Overflow
        r"catch\s*\([^)]*\)\s*\{[\s\S]*?return\s+null[\s\S]*?\}",  # 9. كشف ابتلاع الاستثناءات وإرجاع null في JS/Java عبر أسطر متعددة
        r"catch\s*\([^)]*\)\s*\{\s*\}",  # 10. كشف كتل catch الفارغة تماماً داخل الكود
    ]
    for pattern in patterns:  # التكرار على جميع أنماط الثغرات المعتمدة
        if re.search(
            pattern, code_text, re.IGNORECASE
        ):  # البحث المباشر بدون التأثر بحالة الأحرف
            return True  # إرجاع True فور مطابقة أي ثغرة أمنية
    return False  # إرجاع False عند سلامة الكود من النماذج الأمنية


def calculate_mccabe_complexity(code_text):
    # دالة حساب التعقيد البنائي v(g) الشاملة لجميع اللغات البرمجية
    try:
        parsed_ast = ast.parse(
            code_text
        )  # تحويل النص لشجرة تعبيرات مجردة إن كان الكود بايثون
        complexity = 1  # تعيين قيمة التعقيد الابتدائية
        for node in ast.walk(parsed_ast):  # المرور على عقد الشجرة البرمجية
            if isinstance(
                node,
                (
                    ast.If,
                    ast.For,
                    ast.While,
                    ast.And,
                    ast.Or,
                    ast.ExceptHandler,
                ),
            ):
                complexity += 1  # زيادة التعقيد مع كل تفرع برمي
        return float(complexity)  # إرجاع القيمة المحسوبة
    except Exception:
        # حساب التفرعات عبر التعبيرات النمطية للغات الأخرى (JS, C++, C#, Java)
        branches = len(
            re.findall(
                r"\b(if|else|elif|for|while|switch|case|catch|and|or)\b",
                code_text,
                re.IGNORECASE,
            )
        )
        return float(max(1, branches + 1))  # إرجاع القيمة النهائية للتعقيد


def extract_metrics_from_code(code_text, expected_features=21):
    # دالة استخراج الميزات الإحصائية الـ 21 القياسية للنموذج المحلي
    lines = code_text.splitlines()  # تقسيم الكود إلى قائمة أسطر
    loc = float(len(lines))  # 1. إجمالي عدد الأسطر

    blank_lines = sum(
        1.0 for line in lines if not line.strip()
    )  # 15. الأسطر الفارغة
    comment_lines = sum(
        1.0
        for line in lines
        if line.strip().startswith(("#", "//", "/*", "*"))
    )  # 14. أسطر التعليقات
    code_lines = max(
        0.0, loc - blank_lines - comment_lines
    )  # 13. الأسطر التنفيذية

    tokens = re.findall(
        r"\w+|[^\w\s]", code_text
    )  # استخراج الرموز والكلمات المفتاحية
    total_tokens = float(len(tokens))  # إجمالي عدد الرموز
    unique_tokens = float(len(set(tokens)))  # عدد الرموز الفريدة

    n1 = max(1.0, unique_tokens)  # 17. الرموز الفريدة
    n2 = float(max(1.0, total_tokens - unique_tokens))  # 18. المتغيرات الفريدة
    N1 = float(max(1.0, total_tokens))  # 19. إجمالي العمليات
    N2 = float(max(1.0, total_tokens))  # 20. إجمالي المتغيرات

    vocabulary = max(1.0, n1 + n2)  # حساب المفردات البرمجية الكلية
    length = max(1.0, N1 + N2)  # 5. الطول البرمجي
    volume = length * math.log2(vocabulary)  # 6. الحجم البرمجي

    difficulty = float((n1 / 2.0) * (N2 / max(1.0, n2)))  # 8. الصعوبة البرمجية
    level = float(1.0 / max(1.0, difficulty))  # 7. المستوى
    intelligence = float(volume / max(1.0, difficulty))  # 9. الذكاء البرمجي
    effort = float(volume * difficulty)  # 10. المجهود البرمجي
    bugs = float(volume / 3000.0)  # 11. الأخطاء البرمجية المتوقعة
    time_est = float(effort / 18.0)  # 12. الوقت المتوقع للتطوير

    v_g = calculate_mccabe_complexity(code_text)  # 2. تعقيد ماكيب
    ev_g = v_g  # 3. التعقيد الأساسي
    iv_g = v_g  # 4. تعقيد التصميم الهيكلي
    branch_count = float(max(1.0, v_g - 1.0))  # 21. عدد التفرعات البرمجية

    features = [
        loc,
        v_g,
        ev_g,
        iv_g,
        length,
        volume,
        level,
        difficulty,
        intelligence,
        effort,
        bugs,
        time_est,
        code_lines,
        comment_lines,
        blank_lines,
        0.0,
        n1,
        n2,
        N1,
        N2,
        branch_count,
    ]

    return features[:expected_features]  # إرجاع المصفوفة بحجم 21 ميزة


def predict_defect(code_input):
    # دالة التنبؤ النهائية الموحدة لجميع اللغات والثغرات
    model_path = os.path.join(
        "models", "gradient_boosting_model.pkl"
    )  # تحديد المسار المباشر لنموذج التعلم الآلي

    if not os.path.exists(
        model_path
    ):  # التحقق من وجود ملف النموذج في مجلد النظام
        raise FileNotFoundError(
            f"ملف النموذج غير موجود: {model_path}"
        )  # إطلاق استثناء واضح عند غياب الملف

    model = joblib.load(
        model_path
    )  # تحميل نموذج Gradient Boosting من القرص الصلب
    expected_features = getattr(
        model, "n_features_in_", 21
    )  # استخراج عدد الميزات المطلوب للنموذج (21)

    if isinstance(code_input, str):  # في حال كان المدخل نصاً برمجياً
        metrics = extract_metrics_from_code(
            code_input, expected_features
        )  # استخراج الميزات الإحصائية الـ 21
        has_security_flaw = detect_security_vulnerabilities(
            code_input
        )  # إجراء الفحص الأمني الموحد
        v_g = calculate_mccabe_complexity(code_input)  # حساب التعقيد البنائي
    else:  # في حال كان المدخل مصفوفة أرقام مباشرة
        metrics = code_input  # اعتماد المصفوفة الرقمية
        has_security_flaw = False  # تعيين عدم وجود ثغرات نصية
        v_g = metrics[1] if len(metrics) > 1 else 1.0  # استخراج تعقيد ماكيب

    probabilities = model.predict_proba([metrics])[
        0
    ]  # حساب الاحتماليات من نموذج التعلم الآلي
    raw_risk_prob = probabilities[1]  # أخذ احتمال الفئة 1 (وجود خطر/عطوبة)
    calculated_risk = int(
        raw_risk_prob * 100
    )  # تحويل الاحتمالية إلى نسبة مئوية صحيحة

    # الهيكلية الموحدة لحساب التقييم النهائي (Unified Architecture)
    if has_security_flaw:  # 1. عند كشف أي ثغرة أمنية في أي لغة
        final_risk = max(
            85, calculated_risk
        )  # تعيين خطورة عالية (85% كحد أدنى)
    elif (
        v_g <= 2
    ):  # 2. عند كون الكود خطياً وخالياً من الثغرات والتفرعات المعقدة
        final_risk = min(
            25, calculated_risk
        )  # تعيين خطورة منخفضة (25% كحد أقصى)
    else:  # 3. الأكواد المعقدة أو المركبة
        final_risk = calculated_risk  # اعتماد نسبة نموذج التعلم الآلي المباشرة

    is_high_risk = bool(
        final_risk >= 50
    )  # تصنيف الخطر بناءً على عتبة الـ 50%

    return (
        is_high_risk,
        final_risk,
    )  # إرجاع النتيجة المنطقية والنسبة المئوية المحسوبة