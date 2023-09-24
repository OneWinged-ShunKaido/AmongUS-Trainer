# AmongUS-Trainer
A very basic python trainer for Among Us

Run it normally from `main.py` or with the API in order to inject your own cheats (knowning correct offsets)

```py
from src.client import AmongClient

client = AmongClient()
client.write2mem(address=0x1234, offsets=[0x1, 0x2, 0x3], end_offset=0x4, value=float|int|bool|str|...])
```

You can use the frida version too by identifying the pid with `tasklist | findstr "Among Us.exe"` cmd under Windows.
Then run with `frida -p <pid> -l amogus.js`
```js
let client = new AmongClient();
client.getPlayerSpeed();
```
