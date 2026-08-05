# 1. استيراد مكتبة Streamlit لبناء واجهات المستخدم التفاعلية الخاصة بالتطبيق
import streamlit as st

# 2. استيراد مكتبة time للتحكم في زمن تنفيذ العمليات والتأخير الزمني عند الحاجة
import time

# 3. استيراد وحدة التعامل مع النموذج المحلي لتنبؤ الأخطاء والعيوب من مجلد src
from src import model_helper

# 4. استيراد وحدة الاتصال بنموذج Gemini لشرح وتصحيح الكود من مجلد src
from src import gemini_helper

# 5. استيراد وحدة إدارة وحفظ سجل العمليات السابقة من مجلد src
from src import history_helper

# 6. ضبط إعدادات الواجهة الرئيسية (عنوان الصفحة، الأيقونة، وتنسيق العرض العريض)
st.set_page_config(page_title="لوحة الفحص والتحليل", page_icon="🩺", layout="wide")

# 7. فتح ملف المظهر الخارجي CSS بدعم الترميز UTF-8 وحقنه كـ CSS داخل الصفحة
with open("assets/style.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 8. تعريف دالة تستعرض المحتوى الرئيسي للوحة الفحص والتحليل
def show_main_page():
    # 9. عرض الوسم النصي العلوي الصغير كشعار بصري للمنصة فوق العنوان
    st.markdown("<div class='eyebrow'>ANALYZER // LIVE SCAN</div>", unsafe_allow_html=True)

    # 10. كتابة العنوان الرئيسي للصفحة بطاقم خط كبير وعريض
    st.markdown("<h1>لوحة الفحص والتحليل</h1>", unsafe_allow_html=True)

    # 11. كتابة الوصف التوضيحي للخدمة باللون الخفيف تحت العنوان
    st.markdown(
        "<p style='color:var(--text-muted); margin-top:-8px;'>"
        "الصق الكود البرمجي ليقوم النموذج المحلي بكشف الأخطاء، ثم يشرحه Gemini."
        "</p>", unsafe_allow_html=True
    )

    # 12. عرض خط النبضات البصري SVG كفاصل جمالي بين العنوان ومربع الإدخال
    st.markdown("""
    <div class="vitals-divider">
        <svg viewBox="0 0 600 34" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:34px;">
            <polyline fill="none" stroke="#22D3B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            points="0,17 90,17 110,5 130,30 150,17 240,17 260,8 280,17 380,17 400,3 420,32 440,17 600,17" />
        </svg>
    </div>
    """, unsafe_allow_html=True)

    # 13. تقسيم مساحة الشاشة إلى عمودين بنسبة (2 للإدخال : 1 للإرشادات)
    col_input, col_info = st.columns([2, 1])

    # 14. تخصيص محتوى العمود الأول الخاص بإدخال النص والزر
    with col_input:
        # 15. إنشاء مربع نصي كبير يتسع للكود البرمجي بحد ارتفاع 260 بكسل
        code_input = st.text_area(
            "الكود البرمجي",
            height=260,
            placeholder="# ألصق الكود هنا...",
            label_visibility="collapsed"
        )
        # 16. إنشاء زر تفاعلي لبدء عملية الفحص عند الضغط عليه
        scan_clicked = st.button("🩺  فحص الكود")

    # 17. تخصيص محتوى العمود الثاني لبطاقة التعليمات
    with col_info:
        # 18. عرض بطاقة الإرشادات التي تشرح خطوات التحليل الثلاث للمستخدم
        st.markdown("""
        <div class="card">
            <div class="eyebrow">HOW IT WORKS</div>
            <p style="color:var(--text-muted); font-size:0.85rem; line-height:1.9; margin-top:8px;">
                1) النموذج المحلي يتوقع نسبة الخطورة من الميزات البرمجية<br>
                2) يقيم Gemini الكود ويقدم النصائح أو التصحيح دائماً<br>
                3) تُحفظ النتيجة تلقائياً في سجل العمليات
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 19. إضافة مسافة عمودية قدرها 20 بكسل للفصل بين أدوات الإدخال والنتائج
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # 20. اختبار ما إذا قام المستخدم بنقر زر الفحص
    if scan_clicked:
        # 21. التحقق من حالة مربع النص في حال تم تركه فارغاً أو يحتوي على مسافات فقط
        if not code_input.strip():
            # 22. إظهار رسالة تحذيرية للمستخدم تطلب منه إدخال الكود أولاً
            st.warning("الرجاء لصق كود أولاً قبل الفحص.")
        else:
            # 23. إظهار حلقة التحميل والتأشير ببدء معالجة واستدعاء النماذج
            with st.spinner("جاري تحليل الكود عبر النموذج المحلي وGemini AI..."):
                
                # 24. استدعاء النموذج المحلي للتنبؤ بوجود خطر وحساب نسبة الخطورة الفعلية (0% - 100%)
                is_risk, confidence = model_helper.predict_defect(code_input)

                # 25. تحديد الفئة واللون والرمز بناءً على النسبة المئوية للخطورة
                if confidence >= 70:
                    # حالة الخطر المرتفع (70% فأعلى) -> اللون الأحمر
                    risk_status = "High"
                    verdict_class = "verdict-risk"
                    verdict_icon = "🚨"
                    verdict_title = "خطر مرتفع: تم رصد احتمالية تعقيد أو أخطاء عالية"
                    gauge_color = "#F2545B"
                elif 40 <= confidence < 70:
                    # حالة الخطر المتوسط (40% - 69%) -> اللون الأصفر
                    risk_status = "Medium"
                    verdict_class = "verdict-warning"
                    verdict_icon = "⚠️"
                    verdict_title = "خطر متوسط: الكود يحتاج مراجعة وتحسين"
                    gauge_color = "#F59E0B"
                else:
                    # حالة الخطر المنخفض (أقل من 40%) -> اللون الأخضر
                    risk_status = "Low"
                    verdict_class = "verdict-clean"
                    verdict_icon = "✅"
                    verdict_title = "الكود يبدو سليماً ومنخفض الخطورة"
                    gauge_color = "#22D3B8"

                # 26. استدعاء نموذج Gemini دائماً لكافة الحالات الثلاث (Low, Medium, High)
                ai_explanation = gemini_helper.analyze_code(code_input, risk_status=risk_status)

                # 27. حفظ تفاصيل عملية الفحص بالكامل في سجل التاريخ محلياً عبر history_helper
                history_helper.add_record(code_input, is_risk, confidence, ai_explanation)

            # 28. عرض بطاقة النتيجة والتقييم بحسب المستوى المحدد (أحمر، أصفر، أخضر)
            st.markdown(f"""
            <div class="verdict {verdict_class}">
                <div class="verdict-icon">{verdict_icon}</div>
                <div>
                    <div class="verdict-title">{verdict_title}</div>
                    <div class="verdict-sub">نسبة الخطورة المتوقعة: {confidence}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 29. عرض شريط قياس نسبة الخطورة ديناميكياً باللون المتوافق مع مستوى الخطر
            st.markdown(f"""
            <div class="gauge-track">
                <div class="gauge-fill" style="width:{confidence}%; background:{gauge_color};"></div>
            </div>
            """, unsafe_allow_html=True)

            # 30. عرض بطاقة الشرح المولد من Gemini دائماً لجميع الحالات وبشكل مؤكد
            st.markdown(f"""
            <div class="ai-card">
                <span class="ai-tag">✦ Gemini — الشرح والتحليل الشامل</span>
                <div style="margin-top:10px; line-height:1.8; white-space: pre-wrap;">{ai_explanation}</div>
            </div>
            """, unsafe_allow_html=True)

# 31. إعداد تعريف صفحة الفحص الرئيسية بربطها بدالة العرض وتعيين العنوان والأيقونة
main_page = st.Page(show_main_page, title="لوحة الفحص", icon="🩺", default=True)

# 32. إعداد تعريف صفحة أداء النموذج بمسار ملفها الأصلي وتعيين العنوان العربي والأيقونة
perf_page = st.Page("pages/1_Model_Performance.py", title="أداء النموذج", icon="📊")

# 33. إعداد تعريف صفحة سجل الفحوصات بمسار ملفها الأصلي وتعيين العنوان العربي والأيقونة
hist_page = st.Page("pages/2_History.py", title="سجل الفحوصات", icon="📜")

# 34. إنشاء هيكل التنقل وتمرير قائمة الصفحات الثلاث المنظمة
pg = st.navigation([main_page, perf_page, hist_page])

# 35. تشغيل وعرض الصفحة المحددة حالياً من قبل المستخدم
pg.run()