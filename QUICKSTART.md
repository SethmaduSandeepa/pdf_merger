# QUICK START GUIDE

## For Windows Users (Easiest)

### Step 1: Run Installer
Double-click: **`install.bat`**

The installer will:
- Check if Python is installed
- Create a virtual environment
- Install all dependencies
- Show success message

### Step 2: Run the App
Double-click: **`gui.py`**

OR use Command Prompt:
```
python gui.py
```

### Step 3: Use the App
1. Click "Browse" to select your **Letterhead PDF**
2. Click "Browse" to select your **Content PDF**
3. Click "🔀 Merge PDFs" button
4. Wait for "✅ Success!" message
5. Click "📂 Open Output Folder" to see result

---

## For macOS/Linux Users

### Step 1: Open Terminal
```
cd /path/to/PDF\ Merger\ App
```

### Step 2: Run Installer
```
bash install.sh
```

### Step 3: Run the App
```
python3 gui.py
```

### Step 4: Use the App
(Same as Windows steps 1-5 above)

---

## Folder Structure

```
Your inputs go here:
📁 input/
   📄 letterhead.pdf
   📄 content.pdf

Your results appear here:
📁 output/
   📄 print_ready_merged.pdf
```

---

## Common Issues

### Issue: "Install.bat doesn't work"
**Solution:** Right-click → "Run as Administrator"

### Issue: "Python not found"
**Solution:** Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH"
- Then restart Command Prompt

### Issue: "Module not found"
**Solution:** Run installer again:
```
install.bat
```

### Issue: "GUI window won't open"
**Solution:** Use command line instead:
```
python app.py
```

---

## Need Help?

1. Read **README.md** for detailed instructions
2. Check **DISTRIBUTION_GUIDE.md** for installation methods
3. Ensure both PDFs are in the `input/` folder
4. Make sure PDFs are not corrupted

---

**That's it! Enjoy merging PDFs! 🎉**
