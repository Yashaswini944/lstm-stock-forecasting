# Bug Reports – LSTM Forecasting API

## BUG_LSTM_01 – Wrong status code for invalid data type
**Severity:** High  
**Steps:**  
1. POST /predict with {"series": ["a","b","c"]}  
**Expected:** 400 Bad Request  
**Actual:** 500 Internal Server Error  
**Status:** Open  

---

## BUG_LSTM_02 – Prediction chart not updating
**Severity:** Medium  
**Steps:**  
1. Submit new prediction  
2. Observe chart  
**Expected:** Chart updates  
**Actual:** Old chart remains  
**Status:** Open  
