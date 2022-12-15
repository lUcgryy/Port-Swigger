<div align='center'>

# **Information Disclosure**

</div>

## **Lab:** Information disclosure in version control history

**Goal:** Login as administrator and delete Carlos's account

**Solution:**

1.  Use gobuster to scan the website for common dicrectory and file by the command in Kali Linux

```zsh
gobuster dir -e -u your URL -w /usr/share/wordlists/dirb/common.txt
```

Looking at the result, we see an interesting dicrectory called .git

![](./img/1.png)

2.  Go to the /.git endpoint, we see that this look like a git repository

![](./img/2.png)

Download a whole dicrectory by using

```zsh
wget -rq your URL
```

3.  Using `git log`, we see that there are two commits, the interesting one is the one with the message 'Remove admin password from config'

![](./img/3.png)

4.  Using `git show` to see the changes that have been made, we see the line that look like an administrator's password

![](./img/4.png)

5.  Trying to login as administrator using that password, we log in sucessfully

![](./img/5.png)

6.  Delete Carlos's account to solve the lab

![](./img/6.png)
