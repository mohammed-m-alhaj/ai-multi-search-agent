import streamlit as st
from main import graph  # نفترض الكود السابق محفوظ هنا
import datetime
import time

st.set_page_config(page_title="Multi-Source Research Agent", layout="wide")
st.title("🤖 Multi-Source Research Agent")
st.write("اسأل أي شيء عن أي موضوع، وسأبحث في Google وBing وReddit وأعطيك الإجابة النهائية.")

# إدخال السؤال
user_question = st.text_input("اكتب سؤالك هنا:")

if st.button("بحث") and user_question.strip():
    # عرض شريط تقدم لكل مصدر
    progress_google = st.progress(0, text="جاري البحث في Google...")
    progress_bing = st.progress(0, text="جاري البحث في Bing...")
    progress_reddit = st.progress(0, text="جاري البحث في Reddit...")

    # الحالة المبدئية
    state = {
        "messages": [{"role": "user", "content": user_question}],
        "user_question": user_question,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "selected_reddit_urls": None,
        "reddit_post_data": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
    }

    # تحديث تدريجي للـ progress (للمظهر التفاعلي فقط)
    for i in range(0, 101, 20):
        progress_google.progress(i, text=f"جاري البحث في Google... {i}%")
        progress_bing.progress(i, text=f"جاري البحث في Bing... {i}%")
        progress_reddit.progress(i, text=f"جاري البحث في Reddit... {i}%")
        time.sleep(0.1)

    # تشغيل الـ graph
    final_state = graph.invoke(state)

    # إخفاء الـ progress بعد الانتهاء
    progress_google.empty()
    progress_bing.empty()
    progress_reddit.empty()

    # عرض النتائج في Tabs
    tabs = st.tabs(["Google", "Bing", "Reddit", "الإجابة النهائية"])

    # Google Tab
    with tabs[0]:
        st.subheader("نتائج Google الأولية:")
        google_results = final_state.get("google_results")
        st.write(google_results or "لا توجد نتائج.")
        st.subheader("تحليل Google:")
        st.write(final_state.get("google_analysis") or "لم يتم التحليل بعد.")

    # Bing Tab
    with tabs[1]:
        st.subheader("نتائج Bing الأولية:")
        bing_results = final_state.get("bing_results")
        st.write(bing_results or "لا توجد نتائج.")
        st.subheader("تحليل Bing:")
        st.write(final_state.get("bing_analysis") or "لم يتم التحليل بعد.")

    # Reddit Tab
    with tabs[2]:
        st.subheader("نتائج Reddit الأولية:")
        reddit_results = final_state.get("reddit_results")
        selected_urls = final_state.get("selected_reddit_urls") or []

        if reddit_results:
            # عرض نتائج Reddit مع روابط قابلة للنقر
            for idx, url in enumerate(selected_urls, 1):
                st.markdown(f"{idx}. [ {url} ]({url})")
        else:
            st.write("لا توجد نتائج Reddit.")

        st.subheader("تحليل Reddit:")
        st.write(final_state.get("reddit_analysis") or "لم يتم التحليل بعد.")

    # Final Answer Tab
    with tabs[3]:
        st.subheader("💡 الإجابة النهائية:")
        final_answer = final_state.get("final_answer")
        if final_answer:
            st.write(final_answer)
            filename = f"answer_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            st.download_button("💾 حفظ الإجابة", final_answer, file_name=filename, mime="text/plain")
        else:
            st.warning("لم يتم الحصول على إجابة.")
