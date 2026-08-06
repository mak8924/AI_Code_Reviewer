# 1. استيراد مكتبة streamlit لبناء واجهة المستخدم التفاعلية الخاصة بصفحة السجل
import streamlit as st

# 2. استيراد مكتبة json للتعامل مع قراءة وكتابة ملفات JSON
import json

# 3. استيراد وحدة os للتحقق من وجود الملفات والمسارات في النظام
import os

# 4. تحديد المسار الثابت لملف سجل الفحوصات داخل مجلد data
HISTORY_FILE_PATH = os.path.join("data", "history.json")

# 5. ضبط إعدادات الواجهة الرئيسية لصفحة السجل (عنوان الصفحة، الأيقونة، وتنسيق العرض العريض)
st.set_page_config(page_title="سجل الفحوصات", page_icon="📜", layout="wide")

# 6. فتح ملف المظهر الخارجي CSS بدعم الترميز UTF-8 وحقنه كـ CSS داخل الصفحة
if os.path.exists("assets/style.css"):
    with open("assets/style.css", encoding="utf-8") as f:
        # 7. تطبيق تنسيقات CSS لضمان توحيد الهوية البصرية واتجاهات النصوص
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# 8. دالة لقراءة وقائمة السجلات المخزنة في ملف JSON
def load_history():
    # 9. التحقق مما إذا كان ملف السجل غير موجود في المسار المحدد
    if not os.path.exists(HISTORY_FILE_PATH):
        # 10. إرجاع قائمة فارغة في حال عدم وجود الملف
        return []

    # 11. محاولة فتح وقراءة ملف السجل بصيغة utf-8 لدعم اللغة العربية
    try:
        with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as file:
            # 12. تحويل محتوى ملف JSON إلى قائمة كائنات بايثون وإرجاعها
            return json.load(file)
    # 13. التقاط خطأ قراءة الملف أو إذا كان الملف فارغاً
    except Exception:
        # 14. إرجاع قائمة فارغة لتفادي توقف التطبيق عن العمل
        return []


# 15. دالة لمسح وتفريغ سجل الفحوصات بالكامل
def clear_history():
    # 16. التأكد من وجود مجلد data قبل الكتابة فيه
    os.makedirs(os.path.dirname(HISTORY_FILE_PATH), exist_ok=True)

    # 17. فتح الملف بصيغة الكتابة وإعادة كتابته بقائمة فارغة
    with open(HISTORY_FILE_PATH, "w", encoding="utf-8") as file:
        # 18. حفظ قائمة فارغة [] داخل الملف لتفريغ السجل
        json.dump([], file, ensure_ascii=False, indent=4)


# 19. عرض الوسم النصي العلوي الصغير كشعار بصري لصفحة السجل
st.markdown("<div class='eyebrow'>HISTORY // RECORD LOGS</div>", unsafe_allow_html=True)

# 20. تقسيم المساحة العلوية إلى عمودين (للعنوان وزر المسح)
col_title, col_action = st.columns([3, 1])

# 21. تخصيص محتوى العمود الأول للعنوان والوصف
with col_title:
    # 22. عرض العنوان الرئيسي لصفحة سجل الفحوصات
    st.markdown("<h1>سجل الفحوصات السابقة</h1>", unsafe_allow_html=True)
    # 23. عرض النص التوضيحي المباشر تحت العنوان
    st.markdown(
        "<p style='color:var(--text-muted); margin-top:-8px;'>"
        "استعراض كافة الأكواد المفحوصة سابقاً والنتائج المحفوظة."
        "</p>",
        unsafe_allow_html=True,
    )

# 24. قراءة وتحميل كافة السجلات المخزنة في الملف
history_records = load_history()

# 25. تخصيص محتوى العمود الثاني لزر مسح السجل
with col_action:
    # 26. إضافة مسافة عمودية لمحاذاة الزر مع العنوان
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    # 27. التحقق مما إذا كانت هناك سجلات سابقة لإظهار زر المسح
    if history_records:
        # 28. إنشاء زر تفاعلي لتفريغ ومسح السجل بالكامل عند الضغط عليه
        if st.button("🗑️ مسح السجل بالكامل"):
            # 29. استدعاء دالة مسح السجل لتفريغ البيانات
            clear_history()
            # 30. عرض رسالة نجاح تفيد بتفريغ السجل
            st.success("تم مسح السجل بنجاح!")
            # 31. إعادة تحميل الصفحة لتحديث الواجهة وإخفاء السجلات فوراً
            st.rerun()

# 32. عرض خط النبضات البصري SVG كفاصل جمالي تحت العنوان
st.markdown("""
<div class="vitals-divider">
    <svg viewBox="0 0 600 34" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:34px;">
        <polyline fill="none" stroke="#22D3B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
        points="0,17 90,17 110,5 130,30 150,17 240,17 260,8 280,17 380,17 400,3 420,32 440,17 600,17" />
    </svg>
</div>
""", unsafe_allow_html=True)

# 33. إضافة مسافة عمودية قبل عرض قائمة السجلات
st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)

# 34. التحقق مما إذا كان السجل فارغاً
if not history_records:
    # 35. عرض رسالة تنبيه تفيد بعدم وجود أي فحوصات سابقة
    st.info("لا توجد فحوصات محفوظة في السجل حالياً.")
else:
    # 36. التكرار عبر كافة السجلات بترتيب عكسي (عرض أحدث فحص في الأعلى)
    for index, record in enumerate(reversed(history_records)):
        # 37. استخراج تاريخ ووقت الفحص
        timestamp = record.get("timestamp", "تاريخ غير محدد")
        # 38. استخراج الكود البرمجي المفحوص
        code = record.get("code", "")
        # 39. استخراج نتيجة كشف الخطورة (True أو False)
        is_risk = record.get("is_risk", False)
        # 40. استخراج نسبة ثقة النموذج
        confidence = record.get("confidence", 0)
        # 41. استخراج شرح الذكاء الاصطناعي Gemini
        ai_explanation = record.get("ai_explanation", "")

        # 42. تحديد نص وحالة الشارة (خطأ محتمل أم كود سليم)
        status_label = "⚠️ خطأ محتمل" if is_risk else "✅ كود سليم"

        # 43. إنشاء عنصر القائمة المنسدلة (Expander) لكل عملية فحص
        with st.expander(f"فحص بتاريخ: {timestamp} | {status_label} (ثقة النموذج: {confidence}%)", expanded=(index == 0)):
            # 44. عرض عنوان فرعي للكود
            st.markdown("**الكود البرمجي المفحوص:**")
            # 45. عرض الكود البرمجي داخل مربع كود مخصص لسهولة القراءة والنسخ
            st.code(code, language="python")

            # 46. التحقق من وجود شرح مقدم من Gemini بغض النظر عن حالة الخطورة (سليم أو به خطأ)
            if ai_explanation:
                # 47. عرض الشرح والتصحيح داخل بطاقة منسقة بنفس المظهر الأصلي
                st.markdown(f"""
                <div class="ai-card">
                    <span class="ai-tag">✦ Gemini — الشرح والتحليل</span>
                    <div style="margin-top:10px; line-height:1.8; white-space: pre-wrap;">{ai_explanation}</div>
                </div>
                """, unsafe_allow_html=True)