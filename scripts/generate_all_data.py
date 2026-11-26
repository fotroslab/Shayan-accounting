#!/usr/bin/env python3
"""Deterministic synthetic demo; no actual accounting-system data."""
from pathlib import Path
import csv, random, datetime as dt
import jdatetime
R=Path(__file__).resolve().parents[1]; OUT=R/'data'; OUT.mkdir(exist_ok=True)
rng=random.Random(14030303); ASOF=dt.date(2025,3,20); TARGET=649_279_581_770

def date_fields(d): return d.isoformat(), jdatetime.date.fromgregorian(date=d).strftime('%Y/%m/%d')
def write(name, rows):
    with (OUT/f'{name}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def bucket(d):
    days=(ASOF-d).days
    return 'جاری' if days<=0 else ('۱ تا ۳۰ روز' if days<=30 else '۳۱ تا ۶۰ روز' if days<=60 else '۶۱ تا ۹۰ روز' if days<=90 else 'بیش از ۹۰ روز')
accounts=[('101','صندوق','دارایی'),('102','بانک','دارایی'),('103','حساب‌های دریافتنی','دارایی'),('104','موجودی کالا','دارایی'),('105','پیش‌پرداخت','دارایی'),('201','حساب‌های پرداختنی','بدهی'),('202','اسناد پرداختنی','بدهی'),('301','سرمایه','حقوق مالکانه'),('401','درآمد فروش','درآمد'),('501','هزینه عمومی','هزینه')]
write('chart_of_accounts',[dict(account_code=a,account_name=n,account_type=t) for a,n,t in accounts])
customers=[dict(customer_id=f'C{i:03}',customer_name=f'مشتری نمونه {i:03}') for i in range(1,81)]
suppliers=[dict(supplier_id=f'S{i:03}',supplier_name=f'تأمین‌کننده نمونه {i:03}') for i in range(1,41)]
write('customers',customers); write('suppliers',suppliers)
# Allocate exact specified demo total across 1,500 documents, with 2 lines per document.
weights=[rng.randint(1000,9000) for _ in range(1500)]; sw=sum(weights)
amounts=[TARGET*w//sw for w in weights]; amounts[-1]+=TARGET-sum(amounts)
journal=[]
for i,amount in enumerate(amounts,1):
    d=ASOF-dt.timedelta(days=rng.randrange(365)); iso,jal=date_fields(d)
    a,b=rng.sample(accounts,2)
    for line,(account,debit,credit) in enumerate(((a,amount,0),(b,0,amount)),1):
        journal.append(dict(entry_id=f'J{i:04}',line_id=line,date_iso=iso,date_jalali=jal,account_code=account[0],debit_irr=debit,credit_irr=credit,description='سند نمونه'))
write('journal_entries',journal)
trial=[]
for code,name,_ in accounts:
    deb=sum(x['debit_irr'] for x in journal if x['account_code']==code); cred=sum(x['credit_irr'] for x in journal if x['account_code']==code)
    trial.append(dict(account_code=code,account_name=name,debit_irr=deb,credit_irr=cred,balance_irr=deb-cred))
write('trial_balance_sample',trial)
sales=[]; payments=[]
for i in range(1,2501):
    invoice=ASOF-dt.timedelta(days=rng.randrange(365)); due=invoice+dt.timedelta(days=rng.choice([15,30,45,60,90,120])); amount=rng.randrange(1_000_000,150_000_000,1000); cid=rng.choice(customers)['customer_id']
    pct=rng.choice([0,25,50,75,100,100]); paid=(amount*pct//100)//1000*1000; balance=amount-paid
    iso,jal=date_fields(invoice); diso,djal=date_fields(due)
    sales.append(dict(invoice_id=f'I{i:05}',customer_id=cid,invoice_date_iso=iso,invoice_date_jalali=jal,due_date_iso=diso,due_date_jalali=djal,amount_irr=amount,paid_irr=paid,balance_irr=balance,aging_bucket=bucket(due) if balance else 'تسویه‌شده'))
    if paid:
        pdate=invoice+dt.timedelta(days=rng.randrange((ASOF-invoice).days+1)); piso,pjal=date_fields(pdate)
        payments.append(dict(payment_id=f'P{i:05}',invoice_id=f'I{i:05}',customer_id=cid,payment_date_iso=piso,payment_date_jalali=pjal,amount_irr=paid))
write('sales_invoices',sales); write('payments_received',payments)
bills=[]
for i in range(1,601):
    d=ASOF-dt.timedelta(days=rng.randrange(365)); due=d+dt.timedelta(days=rng.choice([15,30,45,60,90,120])); amount=rng.randrange(1_000_000,100_000_000,1000); paid=(amount*rng.choice([0,25,50,100])//100)//1000*1000
    iso,jal=date_fields(d); diso,djal=date_fields(due)
    bills.append(dict(bill_id=f'B{i:04}',supplier_id=rng.choice(suppliers)['supplier_id'],bill_date_iso=iso,bill_date_jalali=jal,due_date_iso=diso,due_date_jalali=djal,amount_irr=amount,paid_irr=paid,balance_irr=amount-paid,aging_bucket=bucket(due) if amount-paid else 'تسویه‌شده'))
write('bills_payable',bills)
# A daily date dimension covering all fact dates and due dates.
all_dates=[dt.date.fromisoformat(row[k]) for rows in (journal,sales,payments,bills) for row in rows for k in row if k.endswith('_date_iso') or k=='date_iso']
dates=[]; d=min(all_dates)
while d<=max(all_dates):
    iso,jal=date_fields(d); jd=jdatetime.date.fromgregorian(date=d)
    dates.append(dict(date_iso=iso,date_jalali=jal,jalali_year=jd.year,jalali_month=jd.month,jalali_day=jd.day)); d+=dt.timedelta(days=1)
write('dim_date',dates)
print('Synthetic dataset created:', len(journal),'journal lines,',len(sales),'invoices,',len(payments),'receipts,',len(bills),'bills. Per-side total:',TARGET)
