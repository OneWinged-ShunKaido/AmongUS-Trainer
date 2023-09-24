const gameOffsets = {
    "speed": {
        "address": 0x0282F5D8,
        "offsets": [0xB8, 0x0, 0xB8, 0x50],
        "default_value": 1.0
    },
    "vision": {
        "address": 0x0,
        "offsets": [0x0],
        "default_value": 0.0
    }
}

/*function readFileContent(filePath) {
  try {
    const file = new File(filePath, "r"); // Open the file for reading
    const fileContent = [];

    let line;
    while ((line = file.readLine()) !== null) {
      fileContent.push(line);
    }

    file.close(); // Close the file when you're done

    return fileContent;
  } catch (err) {
    console.error("Error:", err);
    return null;
  }
}

class AmongClient {
    constructor() {
        /*this.offsetPath = "frida.text"
        this.gameOffsets = readFileContent(this.offsetPath);
        console.log(this.gameOffsets)*/
        this.gameOffsets = gameOffsets;
        this.moduleName = "GameAssembly.dll";
        this.gameAssembly = this.getAssembly(this.moduleName);
        if (!this.gameAssembly) {
            console.error(`Module '${this.moduleName}' not found.`);
            return;
        }
        this.base = this.gameAssembly.base;
    }

    getAssembly(moduleName) {
        try {
            return Process.getModuleByName(moduleName);
        } catch (e) {
            return null;
        }
    }

    memoryAccess(address, offsets) {
        let base = this.base || this.gameAssembly.base;
        let addrPtr = ptr(base.add(address));
        let addr = Memory.readS64(addrPtr);

        for (let i = 0; i < offsets.length - 1; i++) {
            try {
                addrPtr = ptr(addr.add(offsets[i]));
                addr = Memory.readS64(addrPtr);
            } catch (e) {
                console.error(e);
                return null;
            }
        }

        return ptr(addr.add(offsets[offsets.length - 1]));
    }

    readMemory(address, offsets, vType) {
        let method;
        if (vType === 'int') {
            method = Memory.readS64;
        } else if (vType === 'float') {
            method = Memory.readFloat;
        } else if (vType === 'str') {
            method = Memory.readUtf8String;
        } else if (vType === 'bool') {
            method = Memory.readBool;
        } else {
            console.error('Invalid vType:', vType);
            return null;
        }
        return method(this.memoryAccess(address, offsets));
    }

    getPlayerSpeed() {
        let speedAddr = gameOffsets.speed.address;
        let speedOffsets = gameOffsets.speed.offsets;
        var speedVal = this.readMemory(speedAddr, speedOffsets, 'float');
        console.log(`Player speed ${speedVal}`);
    }
}

// Example usage:
/*let client = new GameLauncher();
if (client.gameAssembly) {
    client.getPlayerSpeed();
}*/
