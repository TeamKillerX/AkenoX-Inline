### AkenoX-Inline
- ⚠️ Disclaimer ⚠️
```
I am not responsible for any misuse of this bot.
Use this bot at your own risk.
Use this userbot wisely.
When you have installed this userbot,
it means you are ready to take the risks.
```
### Python [normal easy]
```py
@RENDYDEV.user(
    prefix=["ping"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
    limit=3,
    time_frame=10
)
async def example(client, message):
    await message.reply_text("Pong!")
```
### Pyrogram c++ [extreme hard]
- Now more powerful with <b>high-performance CPU,</b> plus optimization using <code>C++ and .so.</code>

![Screenshot_20250110-094233_Chrome](https://github.com/user-attachments/assets/a3de2d7a-07d7-40b2-b804-d3f43844f0a5)
```py
from AkenoX.plugins.libso.ping import custom_ping # create ping.so
from AkenoX import *

@RENDYDEV.user(
    prefix=["ping"],
    filters=(
        ~filters.scheduled
        & filters.me
        & ~filters.forwarded
    ),
    is_run=False
    limit=3,
    time_frame=10
)
async def example(client, message):
    await custom_ping(client, message)
```
### C/C++
- How to run .so files using through python script
```pyx
# cython: language_level=3

# something.pyx

def hello_world():
    return "hello world"
```
- original python
```py
# create_hello.py

import something

print(something.hello_world())
```
### Answer
Using a .so (shared object) file greatly reduces the risk of reverse engineering compared to plain <code>.py or .pyc</code> files, but it's not 100% foolproof. Here's why:

- <b>Why .so is safer</b>:
1. <b>Obfuscation:</b> The code is compiled into machine-level instructions, making it harder to understand.

2. <b>No direct access to source code:</b> Unlike <code>.py or .pyc,</code> the original Python code is no longer directly accessible.

3. <b>Optimization:</b> .so files often run faster due to pre-compilation, which adds an extra layer of complexity.

- <b>Reverse Engineering Risks:</b>
1. <b>Disassemblers/Decompilers:</b> Tools like Ghidra or IDA Pro can be used to analyze and reverse-engineer .so files.

2. <b>Strings and Symbols:</b> If not stripped, debug symbols or plaintext strings in the .so file can reveal sensitive information.

3. <b>Advanced Hackers:</b> Skilled reverse engineers with enough time and resources can potentially understand the compiled logic.

### Pyc in python
- How to run Python code without direct imports?

- You can convert your Python script into a .pyc file and load it dynamically. Here's how:
```py
# your_script.py
from something import something
import something

def something():
    return "Hello, world!"
# You can add more functions or code here.
```
- Convert it to .pyc:
```py
convert_to_pycache_from("your_script.py")
```
- Now, load and execute the compiled .pyc file:
### Load and execute
```py
run_code = config.loaded_cache("your_script.pyc")
exec(run_code, globals())

# Call the function
print(something())
```
- This method avoids using traditional imports by running precompiled Python code directly.

- <b>Note:</b>  
> [!WARNING]
> <b>Important:</b> Never edit compiled .so or .pyc files to prevent runtime errors or crashes.
### Credits && Developer 
- [@Kurigram](https://github.com/KurimuzonAkuma/pyrogram) (pyrogram)
- [@RendyDev](https://t.me/xtdevs) (Full stack Developer)
