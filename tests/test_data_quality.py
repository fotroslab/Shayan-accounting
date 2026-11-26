import unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]/'data'; ASOF=pd.Timestamp('2025-03-20')
def read(name): return pd.read_csv(ROOT/(name+'.csv'),dtype={'account_code':str})
class Quality(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.j=read('journal_entries'); cls.a=read('chart_of_accounts'); cls.s=read('sales_invoices'); cls.p=read('payments_received'); cls.b=read('bills_payable'); cls.t=read('trial_balance_sample'); cls.c=read('customers'); cls.v=read('suppliers'); cls.d=read('dim_date')
 def test_journal_per_document(self):
  x=self.j.groupby('entry_id')[['debit_irr','credit_irr']].sum(); self.assertEqual(len(x),1500); self.assertTrue(x.debit_irr.eq(x.credit_irr).all()); self.assertTrue((x.debit_irr>0).all())
 def test_journal_total(self):
  self.assertEqual(self.j.debit_irr.sum(),self.j.credit_irr.sum()); self.assertEqual(self.j.debit_irr.sum(),649279581770)
 def test_lines_unique(self): self.assertFalse(self.j.duplicated(['entry_id','line_id']).any())
 def test_trial_balance(self):
  self.assertEqual(self.t.debit_irr.sum(),self.t.credit_irr.sum()); self.assertTrue((self.t.balance_irr==self.t.debit_irr-self.t.credit_irr).all()); x=self.j.groupby('account_code')[['debit_irr','credit_irr']].sum().sort_index(); y=self.t.set_index('account_code')[['debit_irr','credit_irr']].sort_index(); pd.testing.assert_frame_equal(x,y)
 def test_sales_and_bills(self):
  for df in (self.s,self.b):
   self.assertTrue((df.paid_irr>=0).all()); self.assertTrue((df.paid_irr<=df.amount_irr).all()); self.assertTrue((df.balance_irr==df.amount_irr-df.paid_irr).all())
 def test_payments(self):
  total=self.p.groupby('invoice_id').amount_irr.sum(); inv=self.s.set_index('invoice_id'); self.assertTrue(set(total.index)<=set(inv.index)); self.assertTrue((total<=inv.loc[total.index,'amount_irr']).all()); self.assertTrue((total==inv.loc[total.index,'paid_irr']).all()); self.assertTrue((self.s.loc[~self.s.invoice_id.isin(total.index),'paid_irr']==0).all()); joined=self.p.merge(self.s[['invoice_id','customer_id','invoice_date_iso']],on='invoice_id',suffixes=('_payment','_invoice')); self.assertTrue((joined.customer_id_payment==joined.customer_id_invoice).all()); self.assertTrue((pd.to_datetime(joined.payment_date_iso)>=pd.to_datetime(joined.invoice_date_iso)).all()); self.assertTrue((pd.to_datetime(joined.payment_date_iso)<=ASOF).all())
 def test_foreign_keys(self):
  self.assertTrue(set(self.j.account_code)<=set(self.a.account_code)); self.assertTrue(set(self.t.account_code)<=set(self.a.account_code)); self.assertTrue(set(self.s.customer_id)<=set(self.c.customer_id)); self.assertTrue(set(self.p.customer_id)<=set(self.c.customer_id)); self.assertTrue(set(self.b.supplier_id)<=set(self.v.supplier_id))
  for df,col in [(self.j,'date_iso'),(self.s,'invoice_date_iso'),(self.s,'due_date_iso'),(self.p,'payment_date_iso'),(self.b,'bill_date_iso'),(self.b,'due_date_iso')]: self.assertTrue(set(df[col])<=set(self.d.date_iso))
 def test_unique_keys(self):
  for df,col in [(self.a,'account_code'),(self.s,'invoice_id'),(self.p,'payment_id'),(self.b,'bill_id'),(self.c,'customer_id'),(self.v,'supplier_id'),(self.d,'date_iso'),(self.t,'account_code')]: self.assertTrue(df[col].is_unique,col)
 def test_aging(self):
  allowed={'جاری','۱ تا ۳۰ روز','۳۱ تا ۶۰ روز','۶۱ تا ۹۰ روز','بیش از ۹۰ روز','تسویه‌شده'}
  for df in (self.s,self.b):
   self.assertTrue(set(df.aging_bucket)<=allowed)
   def calc(r):
    if r.balance_irr==0:return 'تسویه‌شده'
    n=(ASOF-pd.Timestamp(r.due_date_iso)).days
    return 'جاری' if n<=0 else '۱ تا ۳۰ روز' if n<=30 else '۳۱ تا ۶۰ روز' if n<=60 else '۶۱ تا ۹۰ روز' if n<=90 else 'بیش از ۹۰ روز'
   self.assertTrue((df.apply(calc,axis=1)==df.aging_bucket).all())
if __name__=='__main__': unittest.main()
