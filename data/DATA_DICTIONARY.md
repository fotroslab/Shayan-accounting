# فرهنگ دادهٔ نمونه

CSVها UTF-8 با BOM؛ تاریخ‌های `*_iso` میلادی ISO 8601 برای محاسبه و روابط، ستون‌های `*_jalali` متن شمسی `YYYY/MM/DD`؛ مبالغ `_irr` ریال صحیح. شناسه‌ها متن هستند. تاریخ مبنا 2025-03-20 / ۱۴۰۳/۱۲/۳۰ است. تمام ردیف‌ها ساختگی هستند.

| فایل | ستون‌ها | معنی / گِرِین |
|---|---|---|
| chart_of_accounts | account_code, account_name, account_type | یک حساب نمونه و گروه آن |
| customers | customer_id, customer_name | یک مشتری ساختگی |
| suppliers | supplier_id, supplier_name | یک تأمین‌کننده ساختگی |
| dim_date | date_iso, date_jalali, jalali_year, jalali_month, jalali_day | هر روز؛ کلید date_iso |
| journal_entries | entry_id, line_id, date_iso, date_jalali, account_code, debit_irr, credit_irr, description | هر آرتیکل سند؛ کلید مرکب entry_id,line_id؛ توازن در سطح entry_id |
| trial_balance_sample | account_code, account_name, debit_irr, credit_irr, balance_irr | جمع کل دوره برای هر حساب؛ مانده بدهکار منهای بستانکار |
| sales_invoices | invoice_id, customer_id, invoice_date_iso, invoice_date_jalali, due_date_iso, due_date_jalali, amount_irr, paid_irr, balance_irr, aging_bucket | هر فاکتور؛ مانده مبلغ منهای پرداخت در تاریخ مبنا |
| payments_received | payment_id, invoice_id, customer_id, payment_date_iso, payment_date_jalali, amount_irr | هر رسید؛ در این نمونه حداکثر یک رسید به ازای فاکتور |
| bills_payable | bill_id, supplier_id, bill_date_iso, bill_date_jalali, due_date_iso, due_date_jalali, amount_irr, paid_irr, balance_irr, aging_bucket | هر تعهد ساختگی؛ مانده در تاریخ مبنا |

گروه سنی برای ماندهٔ مثبت از اختلاف تاریخ مبنا منهای سررسید: صفر یا منفی `جاری`، ۱–۳۰، ۳۱–۶۰، ۶۱–۹۰ و بیش از ۹۰ روز؛ ماندهٔ صفر `تسویه‌شده` است. تاریخ‌های پس از مبنا جاری هستند. `paid_irr` و `balance_irr` عکس ثابت‌اند، نه مقادیر تاریخی پویا.
