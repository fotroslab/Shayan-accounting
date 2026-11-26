from pathlib import Path
import base64
import html
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
ASOF = pd.Timestamp('2025-03-20')
ORDER = ['جاری', '۱ تا ۳۰ روز', '۳۱ تا ۶۰ روز', '۶۱ تا ۹۰ روز', 'بیش از ۹۰ روز']
st.set_page_config(page_title='نگاه مالی | نمونه اتصال شایان', page_icon='◈', layout='wide', initial_sidebar_state='auto')

font = base64.b64encode((ROOT / 'assets/fonts/Vazirmatn-FD-Regular.woff2').read_bytes()).decode()
st.markdown(f'''<style>
@font-face{{font-family:VazirFD;src:url(data:font/woff2;base64,{font}) format('woff2');font-display:swap}}
html,body,[class*="st-"]:not([data-testid="stIconMaterial"]){{font-family:VazirFD, sans-serif}}
.stApp{{background:#f7f6f3;color:#302e32;direction:rtl}}
[data-testid="stMain"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stMain"] [data-testid="stMarkdownContainer"] :is(h1,h2,h3,h4,h5,h6,p,li),
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] :is(h1,h2,h3,h4,h5,h6,p,li),
[data-testid="stMain"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stWidgetLabel"], .kicker, .lead, .footer, .notice, .data-note{{direction:rtl;text-align:right}}
[data-testid="stMain"] [data-testid="stHeadingWithActionElements"]{{direction:rtl;text-align:right;justify-content:flex-start}}
[data-testid="stMain"] .block-container{{max-width:1370px;padding:4.7rem 3.8rem 3rem}}
[data-testid="stHeader"]{{background:rgba(247,246,243,.96)}}
[data-testid="stMain"] h1{{font-size:1.9rem!important;line-height:1.55!important;letter-spacing:-.035em;margin:0!important;padding:0!important;color:#29252b!important}}
[data-testid="stMain"] h2,[data-testid="stMain"] h3{{font-size:1.02rem!important;line-height:1.8!important;letter-spacing:0!important;padding:0!important;color:#302a31!important}}
[data-testid="stMain"] p{{line-height:2;color:#49434a}}
[data-testid="stCaptionContainer"] p{{color:#6f6870!important;font-size:.875rem!important;line-height:1.8!important}}
.kicker{{font-size:.76rem;color:#74686f;margin-bottom:.45rem}}
.lead{{color:#6c656d;font-size:.94rem;line-height:2;margin-top:.25rem}}
.notice{{background:#f5eee4;border:1px solid #eadcc9;border-radius:8px;color:#725c45;padding:.85rem 1rem;font-size:.82rem;line-height:1.9;margin:.7rem 0 .65rem}}
.notice strong{{color:#624c3d}}
.section-rule{{height:1px;background:#e7e3df;margin:1.8rem 0 1.15rem}}
.footer{{border-top:1px solid #e7e3df;margin-top:2.1rem;padding-top:1rem;color:#8a8388;font-size:.75rem}}
/* The sidebar keeps the navigation simple and avoids decorative clutter. */
section[data-testid="stSidebar"]{{background:#322b33;direction:rtl}}
section[data-testid="stSidebar"][data-collapsed="true"]{{display:none!important}}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{{padding:1.1rem .7rem}}
section[data-testid="stSidebar"] *{{color:#f6f3f0!important}}
section[data-testid="stSidebar"] h3{{font-size:1.03rem!important;line-height:1.8!important}}
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{{color:#d3cbd2!important;font-size:.86rem!important}}
section[data-testid="stSidebar"] [role="radiogroup"]{{gap:.15rem}}
section[data-testid="stSidebar"] [role="radiogroup"] label{{padding:.56rem .65rem;border-radius:6px;direction:rtl;text-align:right}}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover{{background:#453b46}}
section[data-testid="stSidebar"] hr{{border-color:#5a505b;margin:1.25rem 0}}
[data-testid="stMetric"]{{border:1px solid #e9e5e1;background:#fff;border-radius:9px;padding:1.05rem 1.1rem .85rem;min-height:118px;box-shadow:0 1px 2px rgba(33,25,31,.025);direction:rtl;text-align:right}}
[data-testid="stMetricLabel"]{{color:#716971!important}}
[data-testid="stMetricLabel"] p{{font-size:.875rem!important}}
[data-testid="stMetricValue"]{{font-size:1.35rem!important;line-height:1.6!important;color:#302932!important;letter-spacing:-.02em}}
[data-testid="stMetricValue"] > div{{overflow:visible!important;white-space:normal!important}}
[data-testid="stMain"] [data-baseweb="input"], [data-testid="stMain"] [data-baseweb="select"] > div{{background:#fff;border-radius:7px}}
[data-testid="stMain"] input{{direction:rtl;text-align:right}}
[data-testid="stMain"] [data-baseweb="select"]{{direction:rtl;text-align:right}}
.js-plotly-plot{{direction:ltr}}
.report-table-wrap{{width:100%;overflow-x:auto;border:1px solid #e7e3df;border-radius:8px;background:#fff;direction:rtl}}
table.report-table{{width:100%;border-collapse:collapse;text-align:right;direction:rtl;font-size:.875rem;white-space:nowrap}}
.report-table th{{background:#f3f1ee;color:#665d65;font-weight:600;padding:.75rem .9rem;border-bottom:1px solid #e7e3df;text-align:right}}
.report-table td{{padding:.72rem .9rem;color:#403940;border-bottom:1px solid #f0eeeb;text-align:right}}
.report-table tr:last-child td{{border-bottom:0}} .report-table tbody tr:hover{{background:#faf8f5}}
.report-table .mono{{direction:ltr;unicode-bidi:isolate;text-align:right;font-variant-numeric:tabular-nums}}
.data-note{{color:#746c73;font-size:.85rem;line-height:1.8}}
@media(max-width:768px){{[data-testid="stMain"] .block-container{{padding:4.5rem 1.1rem 2rem}} [data-testid="stMain"] h1{{font-size:1.5rem!important}} [data-testid="stMetric"]{{min-height:105px}}}}
</style>''', unsafe_allow_html=True)

@st.cache_data
def load(name):
    return pd.read_csv(DATA / f'{name}.csv', dtype={'account_code': str})

j, sales, bills, accounts = (load(name) for name in ('journal_entries', 'sales_invoices', 'bills_payable', 'chart_of_accounts'))

def fa(value):
    return str(value).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))

def num(value):
    return fa(f'{int(value):,}'.replace(',', '٬'))

def money(value):
    return num(value) + ' ریال'

def intro(title, subtitle):
    st.markdown('<div class="kicker">نمونه‌کار هوش تجاری &nbsp; / &nbsp; حسابداری شایان</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<div class="lead">{html.escape(subtitle)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="notice"><strong>دادهٔ نمونه</strong> &nbsp; این داشبورد به سامانهٔ واقعی متصل نیست. تاریخ مبنای محاسبات: ۳۰ اسفند ۱۴۰۳.</div>', unsafe_allow_html=True)

def section(title, caption=None):
    st.subheader(title)
    if caption:
        st.caption(caption)

def divider():
    st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)

def style_fig(fig, height=310):
    fig.update_layout(font=dict(family='VazirFD, sans-serif', color='#716a70', size=12), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=35,r=30,t=20,b=45),height=height,showlegend=False,hoverlabel=dict(bgcolor='#fff',font_color='#302932'),uniformtext_minsize=9)
    fig.update_traces(cliponaxis=False)
    return fig

def axis_ticks(maximum):
    # Whole billions in the axes; full integer IRR remains available in hover.
    step = max(1, math.ceil(maximum / 1_000_000_000 / 4)) * 1_000_000_000
    values = list(range(0, int(maximum) + step, step))
    return values, [num(v // 1_000_000_000) for v in values]

def chart_age(df):
    a = df[df.balance_irr > 0].groupby('aging_bucket', as_index=False).balance_irr.sum().set_index('aging_bucket').reindex(ORDER, fill_value=0).reset_index()
    ticks, texts = axis_ticks(int(a.balance_irr.max()))
    fig = go.Figure(go.Bar(x=a.aging_bucket, y=a.balance_irr, marker=dict(color=['#cbb7aa','#bda198','#a98a84','#90747a','#6a5265']), customdata=[num(x) for x in a.balance_irr], hovertemplate='%{x}<br>%{customdata} ریال<extra></extra>'))
    fig.update_xaxes(title=None, showgrid=False, tickangle=0, automargin=True)
    fig.update_yaxes(title=None, tickvals=ticks, ticktext=texts, gridcolor='#ebe8e5', zeroline=False, automargin=True, rangemode='tozero')
    return style_fig(fig)

def sales_chart():
    m = sales.assign(month=sales.invoice_date_jalali.str[:7]).groupby('month', as_index=False).amount_irr.sum()
    ticks,texts = axis_ticks(int(m.amount_irr.max()))
    fig = go.Figure(go.Scatter(x=m.month.map(fa), y=m.amount_irr, mode='lines+markers', line=dict(color='#715c70',width=2.4), marker=dict(size=5), fill='tozeroy', fillcolor='rgba(211,192,171,.22)', customdata=[num(x) for x in m.amount_irr], hovertemplate='%{x}<br>%{customdata} ریال<extra></extra>'))
    fig.update_xaxes(title=None,showgrid=False, tickangle=-35, automargin=True)
    fig.update_yaxes(title=None,tickvals=ticks,ticktext=texts,gridcolor='#ebe8e5',zeroline=False,automargin=True,rangemode='tozero')
    return style_fig(fig)

def normalize(text):
    return str(text).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩يک', '01234567890123456789یک')).casefold().strip()

def table(df, key):
    """RTL native HTML table with server-side search and pagination, no external JS."""
    controls = st.columns([2.2, 1, 1])
    with controls[0]: query = st.text_input('جست‌وجو در جدول', placeholder='شناسه، نام یا عدد را وارد کنید', key=f'{key}_search')
    with controls[1]: per_page = st.selectbox('ردیف در هر صفحه', [25, 50, 100], key=f'{key}_size')
    view = df
    if query.strip():
        needle = normalize(query).replace('٬','').replace(',','')
        mask = df.astype(str).apply(lambda col: col.map(lambda value: needle in normalize(value).replace('٬','').replace(',',''))).any(axis=1)
        view = df.loc[mask]
    pages = max(1, math.ceil(len(view)/per_page))
    with controls[2]: page = st.number_input('صفحه', min_value=1, max_value=pages, value=1, step=1, key=f'{key}_page') if pages>1 else 1
    start = (page-1)*per_page
    shown = view.iloc[start:start+per_page]
    st.markdown(f'<div class="data-note">{num(len(view))} ردیف &nbsp; · &nbsp; صفحهٔ {num(page)} از {num(pages)} &nbsp; · &nbsp; همهٔ مبلغ‌ها به ریال</div>', unsafe_allow_html=True)
    if view.empty:
        st.info('نتیجه‌ای برای این جست‌وجو پیدا نشد.')
    else:
        headers=''.join(f'<th scope="col">{html.escape(str(col))}</th>' for col in shown.columns)
        rows=[]
        for row in shown.itertuples(index=False, name=None):
            cells=[]
            for value in row:
                if pd.isna(value): text='—'; cls=''
                elif isinstance(value, (int,float)) and not isinstance(value,bool): text=num(value); cls='mono'
                else:
                    value=str(value); text=fa(value); cls='mono' if value[:1].isascii() and (value[:1].isalpha() or value[:1].isdigit()) else ''
                cells.append(f'<td class="{cls}">{html.escape(text)}</td>')
            rows.append('<tr>'+''.join(cells)+'</tr>')
        st.markdown('<div class="report-table-wrap"><table class="report-table"><thead><tr>'+headers+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>',unsafe_allow_html=True)
    st.download_button('دریافت جدول کامل CSV', df.to_csv(index=False).encode('utf-8-sig'), file_name=f'{key}.csv', mime='text/csv', key=f'{key}_download', help='همهٔ ردیف‌های جدول، بدون محدودیت صفحه‌بندی')

with st.sidebar:
    st.markdown('### نگاه مالی')
    st.caption('نمونهٔ داشبورد حسابداری شایان')
    st.markdown('---')
    page = st.radio('بخش‌های گزارش', ['نمای کلی مالی','دفتر کل و اسناد','حساب‌های دریافتنی و سررسید','حساب‌های پرداختنی','دربارهٔ سامانه و داده'])
    st.markdown('---')
    st.markdown('**وضعیت داده**')
    st.caption('دادهٔ نمونه · بدون اتصال واقعی')
    st.caption('تاریخ مبنا: ۱۴۰۳/۱۲/۳۰\n\nواحد گزارش: ریال')

if page == 'نمای کلی مالی':
    intro('نمای کلی مالی', 'خلاصه‌ای از گردش دفتر، فروش و ماندهٔ دریافتنی‌ها در داده‌های نمونه.')
    overdue=sales[(sales.balance_irr>0)&(pd.to_datetime(sales.due_date_iso)<ASOF)].balance_irr.sum()
    cols=st.columns(4)
    for col,label,value,helptext in zip(cols,['گردش دفتر کل','فاکتورهای فروش','دریافتنی سررسیدگذشته','ماندهٔ دریافتنی'],[money(j.debit_irr.sum()),num(len(sales)),money(overdue),money(sales.balance_irr.sum())],['جمع بدهکار؛ جمع دو طرف نیست.','تعداد تمام فاکتورهای نمونه','ماندهٔ باز با سررسید قبل از تاریخ مبنا','مبلغ فاکتورها منهای پرداخت‌های ثبت‌شده']):
        col.metric(label,value,help=helptext)
    divider()
    c1,c2=st.columns(2,gap='large')
    with c1:
        section('سررسید دریافتنی‌ها','ماندهٔ باز به تفکیک فاصله از تاریخ سررسید · محور: میلیارد ریال')
        st.plotly_chart(chart_age(sales),use_container_width=True)
    with c2:
        section('روند فروش','مبلغ فاکتورهای نمونه به تفکیک ماه صدور · محور: میلیارد ریال')
        st.plotly_chart(sales_chart(),use_container_width=True)
    divider()
    section('نگاهی به دفتر کل','جمع دو طرف سندهای نمونه با هم برابر است.')
    c1,c2,c3=st.columns(3); c1.metric('تعداد سند',num(j.entry_id.nunique())); c2.metric('جمع بدهکار',money(j.debit_irr.sum())); c3.metric('جمع بستانکار',money(j.credit_irr.sum()))
    st.caption('دفتر کل و فروش مستقل تولید شده‌اند و برای تطبیق با یکدیگر طراحی نشده‌اند.')
elif page=='دفتر کل و اسناد':
    intro('دفتر کل و اسناد','مرور توازن و ردیف‌های سندهای نمونه.')
    c1,c2,c3=st.columns(3); c1.metric('تعداد سند',num(j.entry_id.nunique())); c2.metric('جمع بدهکار',money(j.debit_irr.sum())); c3.metric('جمع بستانکار',money(j.credit_irr.sum()))
    divider(); section('خلاصهٔ حساب‌ها','جمع کل دوره به تفکیک کد حساب؛ مانده برابر بدهکار منهای بستانکار است.')
    trial=load('trial_balance_sample'); table(trial.rename(columns={'account_code':'کد حساب','account_name':'عنوان حساب','debit_irr':'بدهکار','credit_irr':'بستانکار','balance_irr':'مانده'}),'trial')
    divider(); section('ردیف‌های اسناد','برای محدود کردن نتایج، یک حساب را انتخاب کنید.')
    account=st.selectbox('حساب',['همه']+accounts.account_code.tolist(),format_func=lambda x:'همهٔ حساب‌ها' if x=='همه' else x+' — '+accounts.set_index('account_code').loc[x,'account_name'])
    view=j if account=='همه' else j[j.account_code==account]
    table(view[['entry_id','line_id','date_jalali','account_code','debit_irr','credit_irr']].rename(columns={'entry_id':'شماره سند','line_id':'ردیف','date_jalali':'تاریخ','account_code':'کد حساب','debit_irr':'بدهکار','credit_irr':'بستانکار'}),'journal')
elif page=='حساب‌های دریافتنی و سررسید':
    intro('حساب‌های دریافتنی','ماندهٔ فاکتورهای باز و وضعیت سررسید آن‌ها در تاریخ مبنای نمونه.')
    op=sales[sales.balance_irr>0]; past=op[pd.to_datetime(op.due_date_iso)<ASOF]
    c1,c2,c3=st.columns(3); c1.metric('ماندهٔ باز',money(op.balance_irr.sum())); c2.metric('سررسیدگذشته',money(past.balance_irr.sum())); c3.metric('فاکتورهای باز',num(len(op)))
    divider(); section('وضعیت سررسید','ماندهٔ باز بر اساس روزهای گذشته از سررسید · محور: میلیارد ریال')
    st.plotly_chart(chart_age(sales),use_container_width=True)
    st.caption('روز سررسید در گروه «جاری» قرار می‌گیرد.')
    divider(); section('فاکتورهای باز')
    table(op[['invoice_id','customer_id','invoice_date_jalali','due_date_jalali','amount_irr','paid_irr','balance_irr','aging_bucket']].rename(columns={'invoice_id':'فاکتور','customer_id':'مشتری','invoice_date_jalali':'صدور','due_date_jalali':'سررسید','amount_irr':'مبلغ','paid_irr':'پرداخت','balance_irr':'مانده','aging_bucket':'گروه سررسید'}),'receivables')
elif page=='حساب‌های پرداختنی':
    intro('حساب‌های پرداختنی','مرور تعهدهای باز و زمان سررسید آن‌ها در داده‌های نمونه.')
    op=bills[bills.balance_irr>0]; past=op[pd.to_datetime(op.due_date_iso)<ASOF]
    c1,c2,c3=st.columns(3); c1.metric('ماندهٔ پرداختنی',money(op.balance_irr.sum())); c2.metric('سررسیدگذشته',money(past.balance_irr.sum())); c3.metric('تعهدهای باز',num(len(op)))
    divider(); section('وضعیت سررسید','ماندهٔ باز بر اساس روزهای گذشته از سررسید · محور: میلیارد ریال')
    st.plotly_chart(chart_age(bills),use_container_width=True)
    divider(); section('تعهدهای باز')
    table(op[['bill_id','supplier_id','bill_date_jalali','due_date_jalali','amount_irr','paid_irr','balance_irr','aging_bucket']].rename(columns={'bill_id':'تعهد','supplier_id':'تأمین‌کننده','bill_date_jalali':'تاریخ','due_date_jalali':'سررسید','amount_irr':'مبلغ','paid_irr':'پرداخت','balance_irr':'مانده','aging_bucket':'گروه سررسید'}),'payables')
else:
    intro('دربارهٔ سامانه و داده','منبع داده، روش محاسبه و محدودیت‌های این نمونه‌کار.')
    divider(); section('یک نمایش، نه اتصال واقعی')
    st.markdown('این داشبورد برای نمایش الگوی احتمالی اتصال به حسابداری «شایان» ساخته شده است. همهٔ داده‌ها **ساختگی و تکرارپذیر** هستند؛ هیچ فایل، مجوز یا دادهٔ واقعی شایان در آن استفاده نشده است. نگاشت ستون‌ها تحلیلی است، نه قرارداد یا مشخصات تأییدشدهٔ خروجی نرم‌افزار.')
    divider(); section('روش محاسبه')
    st.markdown('تاریخ مبنا ۱۴۰۳/۱۲/۳۰ است. سررسیدگذشته یعنی سررسید قبل از مبنا با ماندهٔ مثبت؛ مانده برابر مبلغ منهای پرداخت است. ارقام به ریال صحیح نمایش داده می‌شوند. دفتر و فروش مستقل تولید شده‌اند و برای تطبیق با یکدیگر طراحی نشده‌اند.')
    divider(); section('گام بعدی')
    st.markdown('برای اتصال واقعی، ابتدا باید خروجی مجاز و ساختار آن با مسئول سامانه و حسابدار بررسی شود؛ سپس ETL و فایل Power BI ساخته و آزموده شوند. این پروژه فاقد فایل PBIX است و توصیهٔ حسابداری، مالیاتی یا حقوقی نیست.')

st.markdown('<div class="footer">نمایش معماری اتصال &nbsp; · &nbsp; دادهٔ نمونه &nbsp; · &nbsp; بدون اتصال واقعی</div>',unsafe_allow_html=True)
