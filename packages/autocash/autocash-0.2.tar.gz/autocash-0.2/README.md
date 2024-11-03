# AutoCash

مكتبة `AutoCash` مكتبة استلام مدفوعات تلقائى فى مصر و العراق .

## المتطلبات

- Python 3.6 أو أحدث
- مكتبة `requests`

## التثبيت

لتثبيت المكتبة، استخدم الأمر التالي:

```bash
pip install autocash
```

## طريقة الاستخدام

```python

from autocash import AutoCash

# تهيئة المكتبة مع user_id و panel_id
user_id = "YOUR_USER_ID"
panel_id = "YOUR_PANEL_ID"
autocash = AutoCash(user_id, panel_id)

# إنشاء رابط دفع
payment_link = autocash.create_payment_link(extra="username")
print("Payment Link:", payment_link)

# إنشاء رابط دفع ل Payeer
payeer_link = autocash.create_payeer_payment_link(amount=100, callback_link="https://yourcallback.url")
print("Payeer Payment Link:", payeer_link)

# إحضار بيانات العملية
status = autocash.get_payment_status(key="KEY")

#تكون status من نوع dict و تحتوى على بيانات كالمثال التالى :
"""status = {
"amount":"5.00",
"category":"VF-Cash",
"date":"Thu Nov 30 14:43:41 GMT+02:00 2023",
"id":"004952323000",
"phone":"01234567890",
"taken":true,
"user":"uSQ5ho94PQ4a4GreG"
}"""

# التحقق من عملية دفع تلقائيا
check = autocash.check_payment(phone="1234567890", amount=100)

#تكون check من نوع dict و تحتوى على بيانات كالمثال التالى :
"""check = {
"status":true,
"message":"تم إكمال عملية الدفع بنجاح بمبلغ 60 جنية .",
}"""

# الحصول على معلومات لوحة تحكم
info = autocash.get_info()
print("number:", info["number"])
print("rate:", info["rate"])
print("currency:", info["currency"])

# إنشاء رابط إعادة توجيه لاخفاء بيانات رابط الدفع
redirect_link = autocash.redirect(payment_link)
print("Redirect Link:", redirect_link)

```
