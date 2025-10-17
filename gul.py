import streamlit as st
from main import graph  # الكود السابق محفوظ في chatbot_graph.py

st.set_page_config(page_title="Multi-Source Research Agent", layout="wide")

st.title("🤖 Multi-Source Research Agent")
st.write("اسأل أي شيء عن أي موضوع، وسأبحث في Google وBing وReddit وأعطيك الإجابة النهائية.")

# مربع إدخال السؤال
user_question = st.text_input("اكتب سؤالك هنا:")

if st.button("بحث") and user_question.strip():
    # عرض رسالة انتظار
    with st.spinner("جاري البحث في Google وBing وReddit..."):
        # إعداد الحالة المبدئية
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

        # استدعاء الـ graph
        final_state = graph.invoke(state)

    # عرض النتائج
    if final_state.get("final_answer"):
        st.subheader("💡 الإجابة النهائية:")
        st.write(final_state.get("final_answer"))
    else:
        st.warning("لم يتم الحصول على إجابة.")
