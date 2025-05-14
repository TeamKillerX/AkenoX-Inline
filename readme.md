# AkenoX-Inline Userbot

![Image](https://github.com/user-attachments/assets/46938fcc-81aa-434f-beff-e26b684aa52c)

**AkenoX-Inline** is a lightning-fast Telegram Userbot designed for inline commands, powered by ultra-optimized Docker builds and `.so` compiled extensions for maximum performance and minimal latency.

## Disclaimer
```
I am not responsible for any misuse of this bot.
Use this bot at your own risk.
Use this userbot wisely.
When you have installed this userbot,
it means you are ready to take the risks.
```

## Features

- **Ultra-fast** inline query handling
- **Compiled `.so` modules** for speed and CPU optimization
- Lightweight **Docker-based deployment**
- Hardened with **security best practices**
- Integrated with AkenoX APIs
- Async & scalable

---

## Docker Deployment

Build and run with:

```bash
docker build -t akenox-inline .
docker run akenox-inline
````
---

## Performance Optimization

* Uses **shared objects (`*.so`)** for critical operations
* Built with **low-level C extensions** for tasks like regex, filtering, and command parsing
* Async execution with `uvloop` and `aiohttp`

---

## Security Notes

* All API tokens are managed via **environment variables**
* No plain-text storage of sensitive data
* Optional IP or UUID locking for session access
* Custom `@admin_only` and `@dev_guard` decorators for restricted commands

---

## Coming Soon

* Ryzenth API integration
* Encrypted local `.so` pre-loader
* Anti-spam inline rate limiter

---

## Note:
> [!WARNING]
> <b>Important:</b> Never edit compiled .so or .pyc files to prevent runtime errors or crashes.

## Credits && Developer
- [@Kurigram](https://github.com/KurimuzonAkuma/pyrogram) (pyrogram)
- [@RendyDev](https://t.me/xtdevs) (Full stack Developer)

## License

MIT — Free to use with attribution.

> Made with caffeine & chaos by the AkenoX Team.
