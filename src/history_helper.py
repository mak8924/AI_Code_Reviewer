# 1. استيراد مكتبة os للتعامل مع مسارات نظام التشغيل وتفقد الملفات والمجلدات
import os

# 2. استيراد مكتبة json لقراءة وتشفير الملفات بصيغة JSON
import json

# 3. استيراد وحدة datetime لتسجيل تاريخ ووقت إجراء عمليات الفحص تلقائياً
from datetime import datetime

# 4. تحديد المسار المعياري لملف السجل داخل مجلد البيانات data
HISTORY_FILE = os.path.join("data", "history.json")


# 5. دالة لقراءة واسترجاع كافة السجلات المخزنة من ملف JSON
def load_history():
    # 6. التحقق مما إذا كان مجلد البيانات غير موجود، وفي هذه الحالة يتم إنشاؤه
    if not os.path.exists("data"):
        # 7. إنشاء مجلد data لضمان توفر المكان المخصص لحفظ السجل
        os.makedirs("data")

    # 8. التحقق مما إذا كان الملف غير موجود أو كان حجمه 0 بايت (فارغ)
    if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
        # 9. إرجاع قائمة فارغة عند عدم وجود بيانات سابقة
        return []

    # 10. محاولة فتح وقراءة الملف مع التعامل مع الأخطاء
    try:
        # 11. فتح ملف history.json بوضع القراءة وبترميز utf-8 لدعم اللغة العربية
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            # 12. تحويل النص البرمجي بصيغة JSON إلى قائمة Python وإرجاعها
            return json.load(f)
    # 13. التقاط خطأ فك تشفير JSON في حال كان الملف تالفاً أو غير مكتمل
    except json.JSONDecodeError:
        # 14. إرجاع قائمة فارغة لتفادي إيقاف التطبيق عند وجود ملف تالف
        return []


# 15. دالة لحفظ سجل فحص جديد ككائن/قاموس ممرر مباشر
def save_to_history(record):
    # 16. قراءة وتحميل السجلات القديمة المخزنة سابقاً
    history = load_history()

    # 17. إضافة السجل الجديد إلى نهاية قائمة السجلات
    history.append(record)

    # 18. فتح ملف السجل بوضع الكتابة لإعادة حفظ السجلات كاملة
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        # 19. كتابة القائمة المحدثة بتنسيق JSON مرتب ودعم للغة العربية
        json.dump(history, f, ensure_ascii=False, indent=4)


# 20. دالة مخصصة يستدعيها app.py لإنشاء السجل وإضافته بخطوة واحدة
def add_record(code, is_risk, confidence, ai_explanation=""):
    # 21. توليد النص الزمني الحالي للعملية بصيغة (السنة-الشهر-اليوم الساعات:الدقائق)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 22. بناء القاموس الخاص بالسجل وتجميع كافة بيانات الفحص
    record = {
        "timestamp": timestamp,
        "code": code,
        "is_risk": is_risk,
        "confidence": confidence,
        "ai_explanation": ai_explanation,
    }

    # 23. تمرير القاموس لدالة الحفظ لتخزينه داخل الملف
    save_to_history(record)