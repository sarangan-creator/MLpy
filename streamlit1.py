import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Load student data
@st.cache_data
def load_data():
    return pd.read_excel("student_marks.xlsx")

df = load_data()

# Ensure consistent column names
df.columns = [c.strip().title() for c in df.columns]

# 🎓 Dashboard Title
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("🎓 Student Performance Dashboard (AI Chat Mode + Advanced Analytics)")

# Sidebar filters
st.sidebar.header("🔍 Filters")
min_marks = st.sidebar.slider("Minimum Total Marks", 0, int(df["Total"].max()), 0)
filtered_df = df[df["Total"] >= min_marks]

# 🗨️ Chat-like input
user_input = st.text_input("Ask about student performance:", "").lower()

def show_top_students(n=5):
    top_students = df.sort_values(by="Total", ascending=False).head(n)
    st.subheader(f"🏆 Top {n} Students")
    st.dataframe(top_students[["Roll No", "Name", "Total", "Average"]])
    fig, ax = plt.subplots(figsize=(5,5))
    ax.pie(top_students["Total"], labels=top_students["Name"], autopct="%1.1f%%")
    st.pyplot(fig)

def show_failed_students():
    failed = df[(df[["English", "Maths", "Science", "Social", "Computer"]] < 40).any(axis=1)]
    st.subheader("❌ Students Who Failed in Any Subject")
    st.dataframe(failed[["Roll No", "Name", "English", "Maths", "Science", "Social", "Computer"]])

def show_subject_averages():
    st.subheader("📊 Subject-wise Average Marks")
    averages = df[["English", "Maths", "Science", "Social", "Computer"]].mean()
    st.bar_chart(averages)

def show_subject_toppers():
    st.subheader("🏅 Subject Toppers")
    subjects = ["English", "Maths", "Science", "Social", "Computer"]
    toppers = {sub: df.loc[df[sub].idxmax(), "Name"] for sub in subjects}
    st.write(pd.DataFrame(list(toppers.items()), columns=["Subject", "Topper"]))

def show_pass_percentage():
    st.subheader("📈 Pass Percentage")
    total_students = len(df)
    passed = len(df[(df[["English", "Maths", "Science", "Social", "Computer"]] >= 40).all(axis=1)])
    percentage = (passed / total_students) * 100
    st.metric("Pass Percentage", f"{percentage:.2f}%")

def show_correlation():
    st.subheader("🔗 Correlation between Subjects")
    corr = df[["English", "Maths", "Science", "Social", "Computer"]].corr()
    fig, ax = plt.subplots(figsize=(6,4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

def show_all_data():
    st.subheader("📘 All Students Data")
    st.dataframe(df)

# 🧠 Chat understanding logic (basic NLP)
if user_input:
    if "top" in user_input:
        try:
            import re
            n = int(re.findall(r"\d+", user_input)[0])
        except:
            n = 5
        show_top_students(n)
    elif "fail" in user_input or "failed" in user_input:
        show_failed_students()
    elif "average" in user_input:
        show_subject_averages()
    elif "toppers" in user_input or "subject topper" in user_input:
        show_subject_toppers()
    elif "pass" in user_input:
        show_pass_percentage()
    elif "correlation" in user_input or "relation" in user_input:
        show_correlation()
    elif "all" in user_input or "show all" in user_input:
        show_all_data()
    elif "summary" in user_input or "overall" in user_input:
        st.subheader("📚 Overall Summary")
        show_pass_percentage()
        show_subject_averages()
        show_subject_toppers()
    else:
        st.warning("⚠️ Sorry, I didn’t understand. Try asking things like:\n"
                   "- 'show top 5 students'\n"
                   "- 'who are the failed students'\n"
                   "- 'show subject averages'\n"
                   "- 'pass percentage'\n"
                   "- 'subject toppers'\n"
                   "- 'show correlation'\n"
                   "- 'overall summary'")
else:
    st.info("💬 Type a question like 'show top 5 students' or 'overall summary' to begin.")

# 🧩 Extra analytics tab layout
st.sidebar.markdown("---")
if st.sidebar.checkbox("Show Extra Visualizations"):
    tab1, tab2, tab3 = st.tabs(["Marks Distribution", "Subject Correlation", "Pass vs Fail"])
    
    with tab1:
        st.subheader("📈 Marks Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["Total"], bins=10)
        ax.set_xlabel("Total Marks")
        ax.set_ylabel("Number of Students")
        st.pyplot(fig)

    with tab2:
        show_correlation()

    with tab3:
        st.subheader("✅ Pass vs ❌ Fail Count")
        passed = len(df[(df[["English", "Maths", "Science", "Social", "Computer"]] >= 40).all(axis=1)])
        failed = len(df) - passed
        st.bar_chart(pd.Series({"Passed": passed, "Failed": failed}))
