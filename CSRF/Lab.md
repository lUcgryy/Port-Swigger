# **Bypassing CSRF token**

- Change request method
- Remove CSRF token
- Swap CSRF token from two accounts
- CSRF token do not tied to user session cookie
- CSRF token is predictable
- CSRF token is simply duplicated in a cookie (if we can modify cookie)

# **Bypassing SameSite Cookie**

## **SameSite=Lax**

- Using GET request  
- Refresh Cookie

## **SameSite=Strict**

- Client Redirection
- Sibling Domain

# **Bypassing Referer-based CSRF defenses**

- Remove Referer header

```html
<meta name="referrer" content="never">
```

- Logical Bypass