# EasyADB  
**Control your phone from your PC via USB debugging.**

### Installation:  
Before using EasyADB, you need to install [ADB](https://developer.android.com/tools/releases/platform-tools?hl=ru).  

### Setup:  
You can specify the path to your ADB files. For example:  

```python
import easyADB  

easyADB.Phone(adb_path=r"C:\Users\ijidishurka\platform-tools")
``` 

You can also specify the device ID that will accept requests:  

```python
import easyADB  

easyADB.Phone(device='67e345rf')
To view the list of available devices, run adb devices in your terminal.
```

### Code examples can be found in the `examples` folder.