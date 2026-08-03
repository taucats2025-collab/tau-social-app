import os
import streamlit as st
from google import genai

st.set_page_config(page_title="מחולל התוכן של TAU", page_icon="🌾")
st.title("🌾 מחולל פוסטים לרשתות החברתיות")
st.subheader("אגף השיווק - אוניברסיטת תל אביב")

# קריאת מפתח ה-API מתוך ה-Secrets של Streamlit
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

user_text = st.text_area("הדביקי כאן את הטקסט הגולמי / הודעה לעיתונות / מאמר:", height=200)

if st.button("צור פוסטים! ✨"):
    if not api_key:
        st.error("מפתח API לא מוגדר במערכת. בבקשה הגדירי אותו ב-Secrets.")
    elif not user_text:
        st.warning("בבקשה הדביקי טקסט ליצירת פוסטים.")
    else:
        with st.spinner("מנסח את הפוסטים מחדש..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
אתה מנהל תוכן מומחה ברשתות חברתיות עבור אוניברסיטת תל אביב. 
עליך לקחת את הטקסט הגולמי ולייצר 3 גרסאות שונות המותאמות לרשתות:

1. Instagram: קליט, ויזואלי, מינימום אימוג'ים, קריאה לפעולה (CTA) בסגנון 'קישור בביו'.
2. LinkedIn: טון מקצועי, אקדמי אך נגיש, מתרכז באימפקט/במחקר/בהזדמנויות קריירה, כולל האשטאגים.
3. Facebook: מידעי ומסקרן, פונה לקהל הרחב, תמציתי + הצעה רעיונית לוויזואל/תמונה.

הטקסט הגולמי:
{user_text}
"""
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                )

                st.success("הפוסטים מוכנים!")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"ארעה שגיאה: {e}")
