### AkenoX-Inline
![Image](https://github.com/user-attachments/assets/46938fcc-81aa-434f-beff-e26b684aa52c)
- ⚠️ Disclaimer ⚠️
```
I am not responsible for any misuse of this bot.
Use this bot at your own risk.
Use this userbot wisely.
When you have installed this userbot,
it means you are ready to take the risks.
```
### Required Python 3.11
- Via `Dockerfile` Support (Python3.11)
- Running the application with `python3 -m AkenoX` may encounter module path issues (e.g., ModuleNotFoundError). It is recommended to use the provided Dockerfile, which sets up a working Python 3.11 environment.
### Your problem:
```
Why is ModuleNotFoundError: No module named 'config' happening?

ModuleNotFoundError: No module named 'config'
This happens because Python can't find the config module in your project.

Solution: Use Dockerfile Instead
Doesn’t Work:
python3 -m AkenoX
This won’t work because AkenoX-Inline requires high-performance compiled files (.pyc and .so).
```
```
docker build -t akenox-inline .
docker run akenox-inline
```

### Note:
> [!WARNING]
> <b>Important:</b> Never edit compiled .so or .pyc files to prevent runtime errors or crashes.

### Credits && Developer
- [@Kurigram](https://github.com/KurimuzonAkuma/pyrogram) (pyrogram)
- [@RendyDev](https://t.me/xtdevs) (Full stack Developer)
