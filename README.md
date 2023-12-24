# Dose_Sofeware_Beta
Started at: 2023/12/22
---

## Notes
- Ownership
After running "docker compose up", the local file's ownership will be changed into the container's user. And set the "user: '1000:1000'" is not working.
Solutions:
1. Forcely set the ownership with root: sudo chown -R 1000:1000 .