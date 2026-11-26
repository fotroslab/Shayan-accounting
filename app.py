from pathlib import Path
import base64
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parent; DATA=ROOT/'data'
st.set_page_config(page_title='نمایش اتصال شایان | داشبورد مالی',page_icon='◈',layout='wide',initial_sidebar_state='expanded')
font=base64.b64encode((ROOT/'assets/fonts/Vazirmatn-FD-Regular.woff2').read_bytes()).decode()
st.markdown(f'''<style>
@font-face{{font-family:VazirFD;src:url(data:font/woff2;base64,{font}) format('woff2')}}
html,body,[class*="st-"]{{font-family:VazirFD,sans-serif}} .stApp{{background:#faf7f5;color:#3e2c41;direction:rtl}}
section[data-testid="stSidebar"]{{background:#3e2c41;direction:rtl}} section[data-testid="stSidebar"] *{{color:#f8f1eb!important}} section[data-testid="stSidebar"] [role="radiogroup"] label{{padding:9px 7px;border-radius:8px}} section[data-testid="stSidebar"] [role="radiogroup"] label:hover{{background:#58435a}}
.block-container{{padding-top:4.5rem;max-width:1450px}} h1,h2,h3{{color:#3e2c41!important}} h1{{font-size:2rem!important}} h3{{font-size:1.12rem!important}}
[data-testid="stMetric"]{{border:1px solid #eadfdc;background:#fff;border-radius:14px;padding:20px;min-height:145px;box-shadow:0 5px 20px #3e2c4108;direction:rtl}} [data-testid="stMetricLabel"]{{color:#796b78}} [data-testid="stMetricValue"]{{font-size:1.55rem;color:#3e2c41}}
.js-plotly-plot{{direction:ltr}} [data-testid="stDataFrame"]{{direction:ltr}} .tag{{display:inline-block;background:#f3e6d6;color:#815833;padding:5px 14px;border-radius:30px;font-size:13px}} .eyebrow{{color:#a97a47;font-size:13px;letter-spacing:1px}} .sub{{color:#817482;font-size:14px;line-height:2}} .notice{{background:#f6ece2;border:1px solid #eed7bd;border-radius:12px;padding:15px 20px;color:#745536;font-size:14px;margin:12px 0 24px}} .section{{border-top:1px solid #e9dedb;padding-top:23px;margin-top:18px}}
</style>''',unsafe_allow_html=True)
@st.cache_data
def load(name): return pd.read_csv(DATA/f'{name}.csv',dtype={'account_code':str})
j=load('journal_entries'); sales=load('sales_invoices'); bills=load('bills_payable'); accounts=load('chart_of_accounts')
ASOF=pd.Timestamp('2025-03-20'); order=['جاری','۱ تا ۳۰ روز','۳۱ تا ۶۰ روز','۶۱ تا ۹۰ روز','بیش از ۹۰ روز']
def fa(x): return str(x).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
def num(x): return fa(f'{int(x):,}'.replace(',','٬'))
def money(x): return num(x)+' ریال'
def style_fig(fig):
    fig.update_layout(font=dict(family='VazirFD, sans-serif',color='#574457',size=13),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=35,r=35,t=35,b=45),height=330,showlegend=False,xaxis=dict(showgrid=False),yaxis=dict(gridcolor='#eee5e2'),uniformtext_minsize=8)
    fig.update_traces(cliponaxis=False); return fig
def aging_table(df):
    x=df[df.balance_irr>0].groupby('aging_bucket',as_index=False).balance_irr.sum(); x['aging_bucket']=pd.Categorical(x.aging_bucket,order,ordered=True); return x.sort_values('aging_bucket')
def chart_age(df):
    a=aging_table(df); a['نمایش']=a.balance_irr.map(num); fig=px.bar(a,x='aging_bucket',y='balance_irr',text='نمایش',color_discrete_sequence=['#a87867']); fig.update_traces(textposition='outside',hovertemplate='%{x}<br>%{y:,.0f} ریال<extra></extra>'); maximum=int(a.balance_irr.max()) if len(a) else 0; ticks=[round(maximum*i/4) for i in range(5)] if maximum else [0]; fig.update_yaxes(title='ریال',rangemode='tozero',tickvals=ticks,ticktext=[num(v) for v in ticks]); fig.update_xaxes(title=''); return style_fig(fig)
def intro(title,subtitle):
    st.markdown('<div class="eyebrow">نمونه‌کار هوش تجاری &nbsp; / &nbsp; حسابداری شایان</div>',unsafe_allow_html=True)
    st.title(title); st.markdown(f'<div class="sub">{subtitle}</div>',unsafe_allow_html=True)
    st.markdown('<div class="notice">◈ &nbsp; نمایش معماری اتصال با داده‌های ساختگی؛ به شایان یا هیچ سامانهٔ واقعی متصل نیست. تاریخ مبنای نمونه: ۳۰ اسفند ۱۴۰۳.</div>',unsafe_allow_html=True)
def table(df): st.dataframe(df,hide_index=True,use_container_width=True)
with st.sidebar:
    st.markdown('### ◈ &nbsp; شایان | نگاه مالی')
    st.caption('نمونه‌کار داشبورد مدیریتی')
    st.markdown('---')
    page=st.radio('بخش‌های داشبورد',['نمای کلی مالی','دفتر کل و اسناد','حساب‌های دریافتنی و سررسید','حساب‌های پرداختنی','دربارهٔ سامانه و داده'])
    st.markdown('---'); st.markdown('**وضعیت اتصال**'); st.caption('● دادهٔ نمونهٔ آفلاین')
    st.caption('واحد: ریال  |  مبنا: ۱۴۰۳/۱۲/۳۰')
    st.markdown('---'); st.caption('نمایش مفهومی؛ بدون وابستگی یا انتساب تجاری')
if page=='نمای کلی مالی':
    intro('نمای کلی مالی','تصویری ساده از دفتر کل، فروش و مانده‌های باز در یک سناریوی نمونه.')
    overdue=sales[(sales.balance_irr>0)&(pd.to_datetime(sales.due_date_iso)<ASOF)].balance_irr.sum()
    cols=st.columns(4)
    for c,label,value,helptext in zip(cols,['حجم دفتر کل','تعداد فاکتور فروش','دریافتنی سررسید گذشته','ماندهٔ دریافتنی'],[money(j.debit_irr.sum()),num(len(sales)),money(overdue),money(sales.balance_irr.sum())],['جمع بدهکار؛ نه جمع دو طرف','تمام فاکتورهای نمونه','ماندهٔ باز با سررسید قبل از مبنا','مبلغ فاکتور منهای پرداخت']):
        with c: st.metric(label,value,help=helptext)
    st.markdown('<div class="section"></div>',unsafe_allow_html=True)
    left,right=st.columns([1.15,1])
    with left:
        st.subheader('ترکیب سررسید دریافتنی‌ها'); st.caption('توزیع مانده‌های باز، نسبت به تاریخ مبنای نمونه')
        st.plotly_chart(chart_age(sales),use_container_width=True)
    with right:
        st.subheader('روند فروش نمونه'); st.caption('مبلغ ناخالص فاکتور به تفکیک ماه صدور شمسی')
        monthly=sales.assign(month=sales.invoice_date_jalali.str[:7]).groupby('month',as_index=False).amount_irr.sum()
        fig=px.area(monthly,x='month',y='amount_irr',markers=True,color_discrete_sequence=['#765d75']); fig.update_traces(line_width=3,fillcolor='rgba(224,172,105,.22)',hovertemplate='%{x}<br>%{y:,.0f} ریال<extra></extra>'); fig.update_xaxes(title=''); maxv=int(monthly.amount_irr.max()); ticks=[round(maxv*i/4) for i in range(5)]; fig.update_yaxes(title='ریال',tickvals=ticks,ticktext=[num(v) for v in ticks]); st.plotly_chart(style_fig(fig),use_container_width=True)
    st.markdown('<div class="section"></div>',unsafe_allow_html=True)
    st.subheader('نبض دفتر کل')
    c1,c2,c3=st.columns(3)
    c1.metric('تعداد اسناد نمونه',num(j.entry_id.nunique())); c2.metric('جمع بدهکار',money(j.debit_irr.sum())); c3.metric('جمع بستانکار',money(j.credit_irr.sum()))
    st.caption('دفتر کل و فروش مجموعه‌های مستقل نمونه‌اند؛ تطبیق حسابداری میان آن‌ها فرض نشده است.')
elif page=='دفتر کل و اسناد':
    intro('دفتر کل و اسناد','مرور ردیف‌های سند و توازن مجموعهٔ نمونه.')
    c1,c2,c3=st.columns(3); c1.metric('اسناد',num(j.entry_id.nunique())); c2.metric('بدهکار',money(j.debit_irr.sum())); c3.metric('بستانکار',money(j.credit_irr.sum()))
    st.subheader('خلاصه به تفکیک حساب'); trial=load('trial_balance_sample'); table(trial.rename(columns={'account_code':'کد','account_name':'حساب','debit_irr':'بدهکار (ریال)','credit_irr':'بستانکار (ریال)','balance_irr':'مانده (ریال)'}))
    st.subheader('ردیف‌های اسناد'); account=st.selectbox('فیلتر حساب',['همه']+accounts.account_code.tolist(),format_func=lambda x:'همه' if x=='همه' else x+' — '+accounts.set_index('account_code').loc[x,'account_name'])
    view=j if account=='همه' else j[j.account_code==account]; table(view.rename(columns={'entry_id':'سند','line_id':'ردیف','date_jalali':'تاریخ شمسی','account_code':'کد حساب','debit_irr':'بدهکار (ریال)','credit_irr':'بستانکار (ریال)'}).drop(columns=['date_iso','description']))
elif page=='حساب‌های دریافتنی و سررسید':
    intro('حساب‌های دریافتنی و سررسید','ماندهٔ باز فاکتورها با مبنای ثابت ۳۰ اسفند ۱۴۰۳.')
    open_=sales[sales.balance_irr>0]; overdue=open_[pd.to_datetime(open_.due_date_iso)<ASOF]
    c1,c2,c3=st.columns(3); c1.metric('ماندهٔ باز',money(open_.balance_irr.sum())); c2.metric('سررسید گذشته',money(overdue.balance_irr.sum())); c3.metric('فاکتورهای باز',num(len(open_)))
    st.subheader('سن ماندهٔ دریافتنی'); st.plotly_chart(chart_age(sales),use_container_width=True)
    st.caption('روز سررسید در گروه جاری است. گروه‌ها با فاصلهٔ روز سررسید تا تاریخ مبنا محاسبه شده‌اند.')
    st.subheader('فاکتورهای باز'); table(open_[['invoice_id','customer_id','invoice_date_jalali','due_date_jalali','amount_irr','paid_irr','balance_irr','aging_bucket']].rename(columns={'invoice_id':'فاکتور','customer_id':'مشتری','invoice_date_jalali':'صدور','due_date_jalali':'سررسید','amount_irr':'مبلغ','paid_irr':'پرداخت','balance_irr':'مانده (ریال)','aging_bucket':'گروه سررسید'}))
elif page=='حساب‌های پرداختنی':
    intro('حساب‌های پرداختنی','نمایی از تعهدات نمونه و تاریخ سررسید آن‌ها.')
    op=bills[bills.balance_irr>0]; past=op[pd.to_datetime(op.due_date_iso)<ASOF]
    c1,c2,c3=st.columns(3); c1.metric('ماندهٔ پرداختنی',money(op.balance_irr.sum())); c2.metric('سررسید گذشته',money(past.balance_irr.sum())); c3.metric('تعهدات باز',num(len(op)))
    st.subheader('سن ماندهٔ پرداختنی'); st.plotly_chart(chart_age(bills),use_container_width=True)
    st.subheader('تعهدات باز'); table(op[['bill_id','supplier_id','bill_date_jalali','due_date_jalali','amount_irr','paid_irr','balance_irr','aging_bucket']].rename(columns={'bill_id':'تعهد','supplier_id':'تأمین‌کننده','bill_date_jalali':'تاریخ','due_date_jalali':'سررسید','amount_irr':'مبلغ','paid_irr':'پرداخت','balance_irr':'مانده (ریال)','aging_bucket':'گروه سررسید'}))
else:
    intro('دربارهٔ سامانه و داده','شفافیت در منبع، دامنه و محدودیت‌های این نمایش.')
    st.markdown('''### یک نمایش، نه اتصال واقعی
این داشبورد تنها برای نمایش الگوی احتمالی اتصال به حسابداری «شایان» ساخته شده است. همهٔ داده‌ها **ساختگی و تکرارپذیر** هستند؛ هیچ فایل، مجوز یا دادهٔ واقعی شایان استفاده نشده است. نگاشت ستون‌ها تحلیلی است، نه قرارداد یا مشخصات تأییدشدهٔ خروجی آن نرم‌افزار.

### روش محاسبه
تاریخ مبنا ۱۴۰۳/۱۲/۳۰ است. سررسید گذشته یعنی سررسید قبل از مبنا و ماندهٔ مثبت؛ مانده برابر مبلغ منهای پرداخت است. ارقام به ریال صحیح نمایش داده می‌شوند. دفتر و فروش مستقل تولید شده‌اند و برای تطبیق با یکدیگر طراحی نشده‌اند.

### گام بعدی
دریافت خروجی واقعی با مجوز و محرمانگی، بررسی ساختار با حسابدار و DBA، توسعهٔ ETL و ساخت و آزمون فایل Power BI. این پروژه فاقد فایل PBIX است و توصیهٔ حسابداری، مالیاتی یا حقوقی نیست.''')
st.markdown('<div class="section sub">نمایش اتصال حسابداری &nbsp; · &nbsp; دادهٔ نمونه &nbsp; · &nbsp; بدون اتصال واقعی</div>',unsafe_allow_html=True)
