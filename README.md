# Dose_Sofeware_Beta
Started at: 2023/12/22
---

## Notes
### 1\Ownership

**Problems**
After running "docker compose up", the local file's ownership will be changed into the container's user. And set the "user: '1000:1000'" is not working.

**Solution**
**(The best way I found)** Forcely set the ownership by root in a .sh file or command.
```
sudo chown -R 1000:1000 .
```
