import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="מחולל התוכן של TAU", page_icon="🌾")
st.title("🌾 מחולל פוסטים לרשתות החברתיות")
st.subheader("אגף השיווק - אוניברסיטת תל אביב")

# קריאת מפתח ה-API מתוך ה-Secrets של Streamlit
api_key = st.secrets.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")

user_text = st.text_area("הדביקי כאן את הטקסט הגולמי / הודעה לעיתונות / מאמר:", height=200)

if st.button("צור פוסטים! ✨"):
    if not api_key:
        st.error("מפתח API לא מוגדר במערכת. בבקשה הגדירי OPENAI_API_KEY ב-Secrets.")
    elif not user_text:
        st.warning("בבקשה הדביקי טקסט ליצירת פוסטים.")
    else:
        with st.spinner("מנסח את הפוסטים מחדש..."):
            try:
                client = OpenAI(api_key=api_key)
                prompt = f"""
אתה מנהל תוכן מומחה ברשתות חברתיות עבור אוניברסיטת תל אביב. 
עליך לקחת את הטקסט הגולמי ולייצר 3 גרסאות שונות המותאמות לרשתות:

1. Instagram: קליט, ויזואלי, מינימום אימוג'ים, קריאה לפעולה (CTA) בסגנון 'קישור בביו'.
2. LinkedIn: טון מקצועי, אקדמי אך נגיש, מתרכז באימפקט/במחקר/בהזדמנויות קריירה, כולל האשטאגים.
3. Facebook: מידעי ומסקרן, פונה לקהל הרחב, תמציתי + הצעה רעיונית לוויזואל/תמונה.

הטקסט הגולמי:
{user_text}
"""
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.success("הפוסטים מוכנים!")
                st.markdown(response.choices[0].message.content)

            except Exception as e:
                st.error(f"ארעה שגיאה: {e}")
