import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 🎓 Load student data
@st.cache_data
def load_data():
    return pd.read_excel("student_marks.xlsx")

df = load_data()

st.title("🎓 Student Performance Dashboard (Chat Mode)")

# 🗨️ Chat input box
user_input = st.text_input("Ask about student performance:", "")

if user_input:
    user_input = user_input.lower()

    if "top" in user_input:
        top5 = df.sort_values(by="Total", ascending=False).head(5)
        st.subheader("🏆 Top 5 Students")
        st.dataframe(top5[["Roll No", "Name", "Total", "Average"]])

        # Pie Chart
        fig, ax = plt.subplots(figsize=(5,5))
        ax.pie(top5["Total"], labels=top5["Name"], autopct="%1.1f%%", startangle=140)
        st.pyplot(fig)

    elif "average" in user_input:
        st.subheader("📊 Subject-wise Average Marks")
        averages = df[["English", "Maths", "Science", "Social", "Computer"]].mean()
        st.bar_chart(averages)

    elif "fail" in user_input or "failed" in user_input:
        failed = df[(df["English"] < 40) | (df["Maths"] < 40) | 
                    (df["Science"] < 40) | (df["Social"] < 40) | 
                    (df["Computer"] < 40)]
        st.subheader("❌ Students Who Failed in Any Subject")
        st.dataframe(failed[["Roll No", "Name"]])

    elif "all" in user_input or "show all" in user_input:
        st.subheader("📘 All Students Data")
        st.dataframe(df)

    else:
        st.warning("⚠️ Sorry, I didn’t understand. Try asking:\n"
                   "- 'show top students'\n"
                   "- 'average marks'\n"
                   "- 'failed students'\n"
                   "- 'show all data'")

else:
    st.info("💬 Type a question like 'show top students' or 'average marks' to begin.")
