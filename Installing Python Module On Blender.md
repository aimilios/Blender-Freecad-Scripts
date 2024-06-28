# Blender: Installing a Python Module in Blender

This guide provides a fast μπακαλικο way to install a Python module in Blender.

## Steps

### 1. Identify System Python Paths

First, open your command prompt (cmd) or terminal and run the following Python commands to print the paths where Python modules are installed on your system:

```python
import sys
for i in sys.path:print(i)
```

This is where your Python modules are installed.
```
C:\Users\USER\AppData\Local\Programs\Python\Python310\python310.zip
C:\Users\USER\AppData\Local\Programs\Python\Python310\DLLs
C:\Users\USER\AppData\Local\Programs\Python\Python310\lib
C:\Users\USER\AppData\Local\Programs\Python\Python310
C:\Users\USER\AppData\Local\Programs\Python\Python310\lib\site-packages
C:\Users\USER\AppData\Local\Programs\Python\Python310\lib\site-packages\win32
C:\Users\USER\AppData\Local\Programs\Python\Python310\lib\site-packages\win32\lib
C:\Users\USER\AppData\Local\Programs\Python\Python310\lib\site-packages\Pythonwin
```

Look for a path similar to:
```
C:\Users\USER\AppData\Local\Programs\Python\Python310\Lib\site-packages
```




### 2. Identify Blender Python Paths

Next, open Blender and go to the Blender Python Console. Run the same commands to print the paths where Blender looks for its Python modules:

```python
import sys
for i in sys.path:print(i)
```

You should see paths similar to:

```
/home/user/.config/blender/4.0/scripts/addons/modules
C:\Program Files\Blender Foundation\Blender 4.0\4.0\scripts\addons
```


### 3. Copy the Module

Locate the module in the system Python path identified in step 1 and copy the entire module folder to one of the Blender paths identified in step 2. For example:

- From: `C:\Users\USER\AppData\Local\Programs\Python\Python310\Lib\site-packages\your_module`
- To: `C:\Program Files\Blender Foundation\Blender 4.0\4.0\scripts\addons\modules`

### 4. Verify Installation

In Blender's Python Console, try importing the module to verify that it has been installed correctly:

```python
import your_module
```

If the module has dependencies, you will need to copy those as well from the system Python path to the Blender Python path.

---
