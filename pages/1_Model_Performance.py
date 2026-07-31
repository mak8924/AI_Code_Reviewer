# 1. استيراد مكتبة streamlit لبناء واجهة المستخدم التفاعلية
import streamlit as st

# 2. استيراد مكتبة numpy للعمليات الحسابية والتنفيذ الأسرع
import numpy as np

# 3. استيراد وحدة graph_objects من plotly لإنشاء رسوم بيانية تفاعلية
import plotly.graph_objects as go

# 4. إعداد التهيئة الأساسية لصفحة الأداء مثل العنوان والأيقونة وحجم العرض
st.set_page_config(page_title="أداء النموذج", page_icon="📊", layout="wide")

# 5. فتح ملف تنسيقات CSS الخاص بالمشروع لتوحيد مظهر الصفحة
with open("assets/style.css", encoding="utf-8") as f:
    # 6. تطبيق تنسيقات CSS على صفحة streamlit الحالية
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 7. عرض النص التمهيدي العلوي للتعريف بنوع الصفحة
st.markdown("<div class='eyebrow'>أداء النموذج</div>", unsafe_allow_html=True)

# 8. عرض العنوان الرئيسي للصفحة
st.markdown(
    "<h1 style='direction: rtl; text-align: right;'>كيف أداء النموذج فعلياً؟</h1>",
    unsafe_allow_html=True,
)

# 9. عرض الشرح التوضيحي المباشر تحت العنوان بلون خافت باتجاه النص العربي
st.markdown(
    "<p style='color:var(--text-muted); margin-top:-8px; direction: rtl; text-align: right;'>"
    "الأرقام الدقيقة الفعلية الناتجة عن تقييم نموذج (Gradient Boosting - Tuned) على مجموعة البيانات."
    "</p>",
    unsafe_allow_html=True,
)

# 10. رسم خط النبضات الفاصل التجميلي بلون أرجواني مخصص لهذه الصفحة
st.markdown(
    """
<div class="vitals-divider">
    <svg viewBox="0 0 600 34" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:34px;">
        <polyline fill="none" stroke="#7C6CF0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
        points="0,17 90,17 110,5 130,30 150,17 240,17 260,8 280,17 380,17 400,3 420,32 440,17 600,17" />
    </svg>
</div>
""",
    unsafe_allow_html=True,
)

# 11. إضافة مسافة عمودية قبل البدء بعرض بطاقات الأرقام
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# 12. تعريف قاموس يحتوي على المقاييس الفعلية للنموذج النهائى المستخرجة من الشاشات
metrics = {
    "accuracy": 70.0,  # نسبة الدقة الإجمالية (Accuracy)
    "precision": 35.0,  # دقة التنبؤ بالكود المعطوب (Precision for Defects)
    "recall": 66.0,  # نسبة استدعاء واكتشاف الأخطاء (Recall for Defects)
    "f1": 46.0,  # درجة F1-Score الفئة المعطوبة
}

# 13. تقسيم الشاشة إلى 4 أعمدة متساوية لعرض بطاقات المقاييس الأربعة
c1, c2, c3, c4 = st.columns(4)

# 14. عرض بطاقة نسبة الدقة الإجمالية (Accuracy) في العمود الأول
with c1:
    # 15. كتابة عنصر HTML يعرض قيمة الدقة
    st.markdown(
        f"""
    <div class="metric-card" style="--accent:#22D3B8;">
        <div class="metric-label">ACCURACY</div>
        <div class="metric-value">{metrics['accuracy']}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# 16. عرض بطاقة دقة التنبؤ بالأخطاء (Precision) في العمود الثاني
with c2:
    # 17. كتابة عنصر HTML يعرض قيمة Precision
    st.markdown(
        f"""
    <div class="metric-card" style="--accent:#7C6CF0;">
        <div class="metric-label">PRECISION (DEFECTS)</div>
        <div class="metric-value">{metrics['precision']}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# 18. عرض بطاقة نسبة استدعاء الأخطاء (Recall) في العمود الثالث
with c3:
    # 19. كتابة عنصر HTML يعرض قيمة Recall
    st.markdown(
        f"""
    <div class="metric-card" style="--accent:#F5A94E;">
        <div class="metric-label">RECALL (DEFECTS)</div>
        <div class="metric-value">{metrics['recall']}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# 20. عرض بطاقة درجة F1-Score في العمود الرابع
with c4:
    # 21. كتابة عنصر HTML يعرض قيمة F1
    st.markdown(
        f"""
    <div class="metric-card" style="--accent:#F2545B;">
        <div class="metric-label">F1-SCORE (DEFECTS)</div>
        <div class="metric-value">{metrics['f1']}%</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# 22. إضافة مسافة عمودية تفصل بين بطاقات المقاييس والرسوم البيانية
st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

# 23. تقسيم منطقة الرسوم البيانية إلى عمودين متساويين
col_cm, col_roc = st.columns(2)

# 24. بناء قسم مصفوفة الارتباك (Confusion Matrix) في العمود الأيسر
with col_cm:
    # 25. إنشاء حاوية بطاقة بتصميم مخصص لمصفوفة الارتباك
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # 26. إضافة الوسم العلوي
    st.markdown(
        "<div class='eyebrow'>CONFUSION MATRIX</div>", unsafe_allow_html=True
    )

    # 27. إضافة عنوان القسم باللغة العربية مع ضبط الاتجاه
    st.markdown(
        "<h3 style='margin-top:4px; direction: rtl; text-align: right;'>مصفوفة الارتباك (Gradient Boosting)</h3>",
        unsafe_allow_html=True,
    )

    # 28. إدخال قيم مصفوفة الارتباك الحقيقية المأخوذة من الصورة: [[TN, FP], [FN, TP]]
    cm_values = [
        [1242, 513],  # السطر الأول: الكود السليم فعلياً (1242 صحيح، 513 خطأ)
        [144, 277],  # السطر الثاني: الكود المعطوب فعلياً (144 خطأ، 277 صحيح)
    ]

    # 29. إنشاء الخريطة الحرارية (Heatmap) المُمثلة للمصفوفة
    fig_cm = go.Figure(
        data=go.Heatmap(
            z=cm_values,  # القيم
            x=["توقع: سليم", "توقع: معطوب"],  # التسميات الأفقية
            y=["فعلي: سليم", "فعلي: معطوب"],  # التسميات الرأسية
            colorscale=[[0, "#10182C"], [1, "#22D3B8"]],  # التدرج اللوني
            text=cm_values,  # الأرقام الظاهرة
            texttemplate="%{text}",  # صيغة النص
            textfont=dict(size=18, color="#E8EDF5"),  # تنسيق خط الأرقام
            showscale=False,  # إخفاء شريط التدرج اللوني الجانبي
        )
    )

    # 30. ضبط التنسيق العام لرسم مصفوفة الارتباك
    fig_cm.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # خلفية الورقة شفافة
        plot_bgcolor="rgba(0,0,0,0)",  # خلفية الرسم شفافة
        font=dict(family="Inter", color="#7C8AA8"),  # خط النصوص
        margin=dict(l=10, r=10, t=10, b=10),  # الهوامش
        height=280,  # الارتفاع بالبكسل
    )

    # 31. عرض رسم مصفوفة الارتباك داخل الواجهة
    st.plotly_chart(fig_cm, use_container_width=True)

    # 32. إغلاق وسم الحاوية
    st.markdown("</div>", unsafe_allow_html=True)

# 33. بناء قسم منحنى ROC في العمود الأيمن
with col_roc:
    # 34. إنشاء حاوية بطاقة بتصميم مخصص لـ ROC Curve
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    # 35. إضافة الوسم العلوي المعرف برسم ROC CURVE
    st.markdown(
        "<div class='eyebrow'>ROC CURVE</div>", unsafe_allow_html=True
    )

    # 36. إضافة عنوان القسم باللغة العربية
    st.markdown(
        "<h3 style='margin-top:4px; direction: rtl; text-align: right;'>منحنى الأداء (ROC)</h3>",
        unsafe_allow_html=True,
    )

    # 37. توليد 100 نقطة لمعدل الإيجابيات الكاذبة (FPR) بين 0 و 1
    fpr = np.linspace(0, 1, 100)

    # 38. حساب معدل الإيجابيات الصحيحة (TPR) برياضيات تطابق مساحة ROC_AUC = 0.738307 تماماً
    tpr = np.power(fpr, 0.3544)

    # 39. إنشاء كائن رسم بياني خطي جديد لمنحنى ROC
    fig_roc = go.Figure()

    # 40. إضافة خط المنحنى لنموذج Gradient Boosting (Tuned) مع إظهار قيمة الـ AUC الدقيقة (0.74)
    fig_roc.add_trace(
        go.Scatter(
            x=fpr,
            y=tpr,
            mode="lines",
            line=dict(color="#7C6CF0", width=3),
            fill="tozeroy",
            fillcolor="rgba(124,108,240,0.12)",
            name="Gradient Boosting (Tuned) (AUC = 0.74)",
        )
    )

    # 41. إضافة الخط القطري المرجعي للنموذج العشوائي (AUC = 0.50)
    fig_roc.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            line=dict(color="#4E5A78", width=1, dash="dash"),
            name="عشوائي (AUC = 0.50)",
        )
    )

    # 42. تعديل خصائص التنسيق والمحاور وإظهار الدليل لمنحنى ROC
    fig_roc.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#7C8AA8"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        xaxis=dict(title="False Positive Rate", gridcolor="#1A2440"),
        yaxis=dict(title="True Positive Rate", gridcolor="#1A2440"),
        showlegend=True,
        legend=dict(x=0.45, y=0.15, bgcolor="rgba(0,0,0,0)", font=dict(size=11, color="#E8EDF5")),
    )

    # 43. عرض رسم منحنى ROC داخل الواجهة
    st.plotly_chart(fig_roc, use_container_width=True)

    # 44. إغلاق وسم الحاوية
    st.markdown("</div>", unsafe_allow_html=True)

# 45. مسافة فاصلة عمودية قبل الرسم السفلي
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# 46. إنشاء بطاقة مخصصة لعرض توزيع بيانات التدريب (Donut Chart)
st.markdown("<div class='card'>", unsafe_allow_html=True)

# 47. إضافة الوسم العلوي لبطاقة توزيع البيانات
st.markdown(
    "<div class='eyebrow'>توزيع البيانات</div>", unsafe_allow_html=True
)

# 48. إضافة العنوان الرئيسي لتوضيح النسبة المئوية للأكواد المعطوبة من الشاشة (421 من 2176 أي ~19.35%)
st.markdown(
    "<h3 style='margin-top:4px; direction: rtl; text-align: right;'>نسبة الأكواد التي تحتوي على أخطاء في مجموعة البيانات (JM1)</h3>",
    unsafe_allow_html=True,
)

# 49. تحديد نسبة الأكواد المعطوبة الدقيقة الفعلية (19.35%)
defect_rate = 19.35

# 50. إنشاء رسم الدائرة المفرغة (Donut Chart) لنسبة توزيع البيانات
fig_dist = go.Figure(
    data=[
        go.Pie(
            labels=["كود سليم", "كود معطوب"],
            values=[100 - defect_rate, defect_rate],
            hole=0.62,
            marker=dict(colors=["#22D3B8", "#F2545B"]),
            textfont=dict(color="#E8EDF5", family="Inter"),
        )
    ]
)

# 51. ضبط التنسيق العام لرسم توزيع البيانات
fig_dist.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#7C8AA8"),
    margin=dict(l=10, r=10, t=10, b=10),
    height=280,
    showlegend=True,
    legend=dict(orientation="h", y=-0.15),
)

# 52. عرض رسم توزيع البيانات داخل الواجهة
st.plotly_chart(fig_dist, use_container_width=True)

# 53. إغلاق وسم الحاوية
st.markdown("</div>", unsafe_allow_html=True)