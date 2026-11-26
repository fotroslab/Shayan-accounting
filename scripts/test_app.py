"""Smoke test all Streamlit pages using Streamlit's built-in test runner."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
PAGES=['نمای کلی مالی','دفتر کل و اسناد','حساب‌های دریافتنی و سررسید','حساب‌های پرداختنی','دربارهٔ سامانه و داده']
app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=30).run()
for page in PAGES:
    app.radio[0].set_value(page).run()
    assert not app.exception, f'{page}: {app.exception}'
    print('OK:',page)
