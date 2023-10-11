## **PHP serialization format**

Consider a `User` object with the attributes

```php
$user->name = "carlos";
$user->isLoggedIn = true;
```

The serialized version of this object would be

```php
O:4:"User":2:{s:4:"name";s:6:"carlos";s:10:"isLoggedIn";b:1;}
```

## **Java serialization format**

Serialized Java objects always begin with the same bytes, which are encoded as `ac ed` in hexadecimal and `rO0` in Base64.

Any class that implements the interface `java.io.Serializable` can be serialized and deserialized. If you have source code access, take note of any code that uses the `readObject()` method, which is used to read and deserialize data from an `InputStream`

## **Java pre-built gadget chains**

- ysoserial

## **PHP pre-built gadget chains**

- PHPGGC