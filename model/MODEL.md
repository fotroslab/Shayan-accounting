# طرح ستاره‌ای پیشنهادی — فقط دادهٔ نمونه

کلیدها در همهٔ فایل‌ها متنی‌اند (از جمله account_code)؛ مبالغ Whole Number و تاریخ‌های ISO از نوع Date. تاریخ شمسی متن نمایشی است. جداول از CSV با نام‌های زیر در Power BI بارگذاری/تغییرنام شوند:

| جدول مدل | فایل | گِرِین / کلید |
|---|---|---|
| dim_date | dim_date.csv | یک روز، `date_iso` یکتا |
| dim_account | chart_of_accounts.csv | یک حساب، `account_code` یکتا |
| dim_customer | customers.csv | یک مشتری، `customer_id` یکتا |
| dim_supplier | suppliers.csv | یک تأمین‌کننده، `supplier_id` یکتا |
| fact_journal | journal_entries.csv | یک آرتیکل؛ کلید مرکب `entry_id,line_id` |
| fact_sales_invoice | sales_invoices.csv | یک فاکتور؛ `invoice_id` |
| fact_bill_payable | bills_payable.csv | یک تعهد؛ `bill_id` |
| fact_payment_received | payments_received.csv | یک رسید؛ `payment_id` |
| trial_balance | trial_balance_sample.csv | جمع کل نمونه برای هر حساب؛ `account_code` |

## روابط یک‌به‌چند، فیلتر یک‌طرفه از بُعد به فکت
- dim_account[account_code] → fact_journal[account_code] و trial_balance[account_code].
- dim_customer[customer_id] → fact_sales_invoice[customer_id] و fact_payment_received[customer_id].
- dim_supplier[supplier_id] → fact_bill_payable[supplier_id].
- dim_date[date_iso] → fact_journal[date_iso]، fact_sales_invoice[invoice_date_iso]، fact_payment_received[payment_date_iso]، fact_bill_payable[bill_date_iso] (فعال).
- در صورت نیاز، روابط dim_date → `due_date_iso` دو فکت فاکتور و تعهد را **غیرفعال** تعریف و فقط در اندازه‌های صریح با USERELATIONSHIP فعال کنید؛ یا برای تحلیل مستقل سررسید، بُعد تاریخ نقش‌محور مجزا بسازید. اندازه‌های موجود از تاریخ صدور فعال و فیلتر مستقیم سررسید استفاده می‌کنند.

رابطهٔ فکت به فکت ایجاد نکنید؛ `invoice_id` رسید برای تطبیق ETL است و نه رابطهٔ مدل. فیلتر مستقیم یک فاکتور روی جدول رسید منتشر نمی‌شود؛ برای آن به بُعد فاکتور/طراحی مجزا نیاز است. این یک مدل پیشنهادی است؛ فایل PBIX آماده نیست.

## معنا و محدودیت
`trial_balance` تجمیع تمام دورهٔ دفتر در سطح حساب است نه یک فکت مستقل برای جمع کردن همراه دفتر؛ با فیلتر تاریخ تغییر نمی‌کند، زیرا تاریخ ندارد. همزمان با مبالغ دفتر جمع نشود و برای تأیید آن جمع به تفکیک حساب با فکت مقایسه شود. دفتر و فاکتورها عمداً مستقل تولید شده‌اند؛ هیچ تطبیق میان فروش، دریافت و حساب‌های دفتر فرض نشده است. فیلترهای تاریخِ فعال براساس تاریخ صدور/سند/دریافت هستند و به معنای محاسبهٔ ماندهٔ تاریخی نیستند: مبلغ `paid_irr` و `balance_irr` عکس ثابت ۱۴۰۳/۱۲/۳۰ است. برای ماندهٔ پویا به سوابق پرداخت و سیاست رخداد، و برای پرداختنی به سوابق تسویه نیاز است.
