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

### 2\Volumes mounted not existed
In some containers like python, the mounted folder will not displayed in the docker desktop app. But we can actually get all the files by this terminal code:
```
    volumes:
      - ./src:/usr/src/app
    working_dir: /usr/src/app
    command: ["ls", "/usr/src/app"]
```
Actually, through this command, we can see all the mounted files.