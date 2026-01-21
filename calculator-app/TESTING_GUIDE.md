# MathHub Calculator - Testing Guide

## 🚀 Quick Start

### Step 1: Start Backend Server

```bash
cd "C:\Users\koman\OneDrive\Desktop\0. KULIAH\2. SEMESTER 3\8. Pengembangan Sistem Backend\TUGAS\calculator-app\calculator-app"
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Expected Output:**

```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 2: Start Frontend Server (New Terminal)

```bash
cd "C:\Users\koman\OneDrive\Desktop\0. KULIAH\2. SEMESTER 3\8. Pengembangan Sistem Backend\TUGAS\calculator-app\calculator-app"
python -m http.server 8080 --directory ./frontend
```

**Expected Output:**

```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...)
```

### Step 3: Access Application

- **Frontend**: http://localhost:8080/index.html
- **History**: http://localhost:8080/history.html
- **API Docs**: http://127.0.0.1:8000/docs

---

## 🧪 Test Cases

### TEST 1: Authentication & Login

**Purpose**: Verify user authentication works

**Steps:**

1. Go to http://localhost:8080/auth.html
2. Register new user: username="testuser", password="test123"
3. Verify success message
4. Login with same credentials
5. Should redirect to index.html
6. Verify username displayed in header

**Expected Result**: ✅ User authenticated and logged in

---

### TEST 2: Basic Calculator Auto-Save

**Purpose**: Verify basic calculations are saved to database

**Steps:**

1. In Basic Calculator tab, perform calculation: 5 + 3
2. Click equals button
3. Open browser console (F12)
4. Look for message: `✓ [BASIC] Calculation saved:`
5. Go to History page
6. Verify "5 + 3" appears in history with result "8"

**Expected Result**: ✅ Calculation saved with correct expression and result

---

### TEST 3: Advanced Calculator Auto-Save

**Purpose**: Verify advanced calculations are saved

**Steps:**

1. Click "Advanced Calculator" tab
2. Select operation: "Square (x²)"
3. Enter value: 7
4. Click Calculate
5. Open console (F12)
6. Look for message: `✓ [ADVANCED] Calculation saved:`
7. Go to History page
8. Verify calculation appears with type "advanced"

**Expected Result**: ✅ Advanced calculation saved

---

### TEST 4: Unit Converter Auto-Save

**Purpose**: Verify unit conversions are saved

**Steps:**

1. Click "Unit Converter" tab
2. Select category: "Length"
3. Select from unit: "Meter" and to unit: "Kilometer"
4. Enter value: 1000
5. Click Convert
6. Open console (F12)
7. Look for message: `✓ [CONVERSION] Calculation saved:`
8. Go to History page
9. Verify conversion appears with type "conversion"

**Expected Result**: ✅ Unit conversion saved

---

### TEST 5: Financial Calculator Auto-Save

**Purpose**: Verify financial calculations are saved

**Steps:**

1. Click "Financial Calculator" tab
2. Select operation: "Simple Interest"
3. Enter: Principal=1000, Rate=5, Time=2
4. Click Calculate
5. Open console (F12)
6. Look for message: `✓ [FINANCE] Calculation saved:`
7. Go to History page
8. Verify calculation appears with type "finance"

**Expected Result**: ✅ Financial calculation saved

---

### TEST 6: History Filtering

**Purpose**: Verify filtering works correctly

**Steps:**

1. Go to History page
2. Create several calculations of different types (Basic, Advanced, Conversion, Finance)
3. Use "All Types" dropdown to select "Basic"
4. Verify only basic calculations are shown
5. Change to "Advanced" - verify only advanced shown
6. Change to "All Types" - verify all calculations shown
7. Use search box to search for expression (e.g., search "5")
8. Verify only calculations matching search appear

**Expected Result**: ✅ Filtering and search work correctly

---

### TEST 7: Delete Single Calculation

**Purpose**: Verify deleting individual calculations

**Steps:**

1. Go to History page
2. Find a calculation
3. Click the "Delete" button next to it
4. Confirm deletion when prompted
5. Verify calculation is removed from history

**Expected Result**: ✅ Calculation deleted successfully

---

### TEST 8: Clear All History

**Purpose**: Verify clearing all calculations

**Steps:**

1. Go to History page
2. Create at least 2 calculations
3. Click "Clear All" button
4. Confirm deletion when prompted
5. Verify all calculations are removed
6. Verify history list shows "No calculations yet"

**Expected Result**: ✅ All calculations cleared

---

### TEST 9: CSV Export

**Purpose**: Verify CSV export functionality

**Steps:**

1. Create at least 3 calculations of different types
2. Go to History page
3. Click "📥 Export CSV" button
4. File should download automatically
5. Open downloaded CSV file in text editor or Excel
6. Verify:
   - Header row: No, Expression, Result, Type, Date/Time
   - All calculations are present
   - Data is correctly formatted
   - Timestamp is recent

**Expected Result**: ✅ CSV file exports correctly with all data

**CSV Format Example:**

```
No,Expression,Result,Type,Date/Time
1,5 + 3,8,basic,2026-01-20 23:15:45
2,7^2,49,advanced,2026-01-20 23:16:12
3,1000 m → km,1,conversion,2026-01-20 23:17:03
```

---

### TEST 10: PDF Export

**Purpose**: Verify PDF export functionality

**Steps:**

1. Create at least 3 calculations of different types
2. Go to History page
3. Click "📥 Export PDF" button
4. File should download automatically
5. Open downloaded PDF file
6. Verify:
   - Title: "📊 Calculation History Report"
   - Generation date/time is current
   - All calculations appear in table
   - Summary shows correct counts:
     - Total Calculations
     - Basic count
     - Advanced count
     - Conversion count
     - Finance count
   - Professional formatting with colors

**Expected Result**: ✅ PDF file exports correctly with all data and summary

---

### TEST 11: User Isolation - Different Users

**Purpose**: Verify users cannot see each other's calculations

**Steps:**

1. Login as "User A" (e.g., john/pass123)
2. Create 3 calculations
3. Go to History - verify 3 calculations shown
4. Logout
5. Login as "User B" (e.g., jane/pass456)
6. Go to History - verify NO calculations shown (empty)
7. Create 2 calculations as User B
8. Verify only 2 calculations shown
9. Logout and login as User A again
10. Go to History - verify original 3 calculations still there
11. Statistics should show correct User A counts

**Expected Result**: ✅ Users completely isolated - cannot see other users' data

---

### TEST 12: Statistics Display

**Purpose**: Verify statistics display correctly

**Steps:**

1. Create 2 basic calculations
2. Create 1 advanced calculation
3. Create 1 unit conversion
4. Create 1 financial calculation
5. Go to History page
6. Verify statistics cards show:
   - Total Calculations: 5
   - Basic Calculations: 2
   - Advanced Calculations: 1
   - (Other types: 2)

**Expected Result**: ✅ Statistics calculated and displayed correctly

---

### TEST 13: Calculation Expression Display

**Purpose**: Verify expressions display correctly in history

**Steps:**

1. Perform Basic: 12 ÷ 4 = 3
2. Perform Advanced: Square of 5 = 25
3. Perform Conversion: 5 km to m = 5000
4. Go to History
5. Verify each expression displays clearly
6. Verify results are correct
7. Perform CSV export and verify expressions in CSV
8. Perform PDF export and verify expressions in PDF

**Expected Result**: ✅ All expressions display correctly in history and exports

---

### TEST 14: Timestamp Accuracy

**Purpose**: Verify calculation timestamps are accurate

**Steps:**

1. Note current time
2. Perform calculation
3. Go to History page
4. Check timestamp of calculation
5. Verify timestamp matches or is very close to current time (within ~1 second)
6. Export to CSV and verify timestamp format
7. Export to PDF and verify timestamp in summary

**Expected Result**: ✅ Timestamps are accurate and properly formatted

---

### TEST 15: Console Logging

**Purpose**: Verify debug logging works

**Steps:**

1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Perform any calculation
4. Look for console message indicating calculation was saved
5. Export to CSV - look for "CSV exported" message
6. Export to PDF - look for "PDF exported" message
7. Verify no error messages in console

**Expected Result**: ✅ Debug logging shows all operations

---

## 📋 Test Summary Checklist

- [ ] Authentication & Login works
- [ ] Basic Calculator auto-saves
- [ ] Advanced Calculator auto-saves
- [ ] Unit Converter auto-saves
- [ ] Financial Calculator auto-saves
- [ ] History filtering works
- [ ] Delete single calculation works
- [ ] Clear all history works
- [ ] CSV export works correctly
- [ ] PDF export works correctly
- [ ] User isolation works (different users)
- [ ] Statistics display correctly
- [ ] Expressions display correctly
- [ ] Timestamps are accurate
- [ ] Console logging works

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'reportlab'"

**Solution**:

```bash
pip install reportlab==4.0.9
```

### Issue: Backend returns 500 error on export

**Check**:

1. Backend server is running
2. You are logged in (valid token)
3. You have at least one calculation in history
4. Check backend console for error details

### Issue: CSV/PDF doesn't download

**Check**:

1. Browser allows downloads from localhost
2. Browser console (F12) for JavaScript errors
3. Network tab to see HTTP response
4. Verify file is being generated (check browser download folder)

### Issue: Calculations not appearing in history

**Check**:

1. Browser console for errors
2. Network tab - verify API calls are succeeding (200 response)
3. User is authenticated (token exists)
4. Backend is saving data (check database)
5. Refresh history page

### Issue: Wrong calculations shown for current user

**Solution**:

1. Clear browser cookies/localStorage for localhost
2. Logout completely
3. Login again
4. History should now show correct user's data

---

## 📞 Support

For issues or questions:

1. Check console errors (F12)
2. Check network tab for failed requests
3. Review backend logs
4. Verify all dependencies are installed
5. Ensure both servers are running on correct ports
