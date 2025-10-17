import streamlit as st
from main import graph, llm
import datetime
import time
from threading import Thread

st.set_page_config(page_title="Supreme AI Meta Live Dashboard", layout="wide")
st.title("🚀 Supreme AI Meta Live Dashboard + Multi-Source Fusion")
st.write("Multi-Source + Insight + Auto Summary + Priority + Live Answer")

user_question = st.text_input("اكتب سؤالك هنا:")

if user_question.strip():
    st.info("🔎 جاري البحث والتحليل Supreme AI Live...")

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

    # Columns وProgress لكل مصدر
    col1, col2, col3 = st.columns(3)
    with col1:
        google_progress = st.progress(0, text="Google: 0%")
    with col2:
        bing_progress = st.progress(0, text="Bing: 0%")
    with col3:
        reddit_progress = st.progress(0, text="Reddit: 0%")

    # تشغيل graph في Thread
    def run_graph(state):
        global final_state
        final_state = graph.invoke(state)

    thread = Thread(target=run_graph, args=(state,))
    thread.start()

    # Progress ديناميكي
    for i in range(0, 101, 10):
        google_progress.progress(i, text=f"Google: {i}%")
        bing_progress.progress(i, text=f"Bing: {i}%")
        reddit_progress.progress(i, text=f"Reddit: {i}%")
        time.sleep(0.15)

    thread.join()
    google_progress.empty()
    bing_progress.empty()
    reddit_progress.empty()

    col_google, col_bing = st.columns(2)

    def highlight_score(score_text: str) -> str:
        try:
            score = float(score_text.strip())
        except:
            score = 5
        if score >= 7:
            return "background-color:#b3ffb3;padding:5px;border-radius:5px;"
        elif score >= 4:
            return "background-color:#fff3b3;padding:5px;border-radius:5px;"
        else:
            return "background-color:#ffb3b3;padding:5px;border-radius:5px;"

    def get_insight(text: str) -> str:
        messages = [{"role": "user", "content": f"اعطيني Insight سريع ومهم لهذه النتيجة: {text}"}]
        return llm.invoke(messages).content

    def get_summary(results: list, source_name: str) -> str:
        content = "\n".join(results)
        messages = [{"role": "user", "content": f"اعطني ملخص شامل ومختصر لمصدر {source_name}: {content}"}]
        return llm.invoke(messages).content

    # ===== Google Panel =====
    with col_google:
        st.subheader("📊 Google Results with Insights & Priority")
        google_results = final_state.get("google_results") or []
        sorted_google_results = sorted(
            google_results, key=lambda r: float(llm.invoke([{"role":"user","content":f"قيم هذه النتيجة من 0-10: {r}"}]).content or 5), reverse=True
        )
        google_summary = get_summary(sorted_google_results, "Google")
        st.markdown(f"**📝 Google Summary:** {google_summary}")
        for i, result in enumerate(sorted_google_results, 1):
            score = llm.invoke([{"role":"user","content":f"قيم هذه النتيجة من 0-10: {result}"}]).content
            insight = get_insight(result)
            st.markdown(f"<div style='{highlight_score(score)}'><b>Result {i} (Score: {score})</b></div>", unsafe_allow_html=True)
            with st.expander(f"🔹 Insight و Details {i}"):
                st.write("🔹 النتيجة:", result)
                st.write("💡 Insight:", insight)

    # ===== Bing Panel =====
    with col_bing:
        st.subheader("📊 Bing Results with Insights & Priority")
        bing_results = final_state.get("bing_results") or []
        sorted_bing_results = sorted(
            bing_results, key=lambda r: float(llm.invoke([{"role":"user","content":f"قيم هذه النتيجة من 0-10: {r}"}]).content or 5), reverse=True
        )
        bing_summary = get_summary(sorted_bing_results, "Bing")
        st.markdown(f"**📝 Bing Summary:** {bing_summary}")
        for i, result in enumerate(sorted_bing_results, 1):
            score = llm.invoke([{"role":"user","content":f"قيم هذه النتيجة من 0-10: {result}"}]).content
            insight = get_insight(result)
            st.markdown(f"<div style='{highlight_score(score)}'><b>Result {i} (Score: {score})</b></div>", unsafe_allow_html=True)
            with st.expander(f"🔹 Insight و Details {i}"):
                st.write("🔹 النتيجة:", result)
                st.write("💡 Insight:", insight)

    # ===== الإجابة النهائية Supreme =====
    st.subheader("💡 الإجابة النهائية Supreme AI")
    combined_content = "\n".join(
        [r for r in sorted_google_results if r] + [r for r in sorted_bing_results if r]
    )
    if combined_content:
        final_answer = llm.invoke([{"role":"user","content":f"أدمج كل المعلومات السابقة لإجابة شاملة ومكتملة وسهلة القراءة: {combined_content}"}]).content
        st.write(final_answer)

        filename_txt = f"answer_supreme_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        st.download_button("💾 تحميل الإجابة كـ TXT", final_answer, file_name=filename_txt, mime="text/plain")
    else:
        st.write("لم يتم الحصول على إجابة بعد.")
