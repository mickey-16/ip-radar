# AlienVault OTX API Key Setup Guide

## Why You Need This (Problem You're Facing)

**Current Issue**: You're getting `429 Too Many Requests` errors from AlienVault OTX
- ❌ Can't detect APT groups (MuddyWater, Earth Vetala, etc.)
- ❌ MITRE intelligence shows "found": false
- ❌ High-risk IPs show LOW risk (like 45.142.212.61)

**Root Cause**: Without an API key, you're limited to ~100 requests per day (shared across all free users)

## Solution: Get FREE API Key (Takes 2 Minutes)

### Step 1: Create Account
1. Go to: **https://otx.alienvault.com/**
2. Click **"Sign Up"** (top right)
3. Fill in:
   - Email
   - Username
   - Password
4. Verify your email

### Step 2: Get Your API Key
1. Log in to OTX
2. Click your **username** (top right corner)
3. Click **"Settings"**
4. Scroll to **"OTX Key"** section
5. **Copy your API key** (looks like: `abc123def456...`)

### Step 3: Add to Your Project

Open your `.env` file (in project root) and add:

```bash
# AlienVault OTX API Key (for MITRE/APT intelligence)
ALIENVAULT_OTX_API_KEY=your_api_key_here
```

**Example:**
```bash
ALIENVAULT_OTX_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

### Step 4: Delete Cache (Important!)

Clear old cached data without MITRE intelligence:

```powershell
cd "d:\TICE hackthaon project"
Remove-Item -Path "cache\*.json"
```

### Step 5: Restart Application

```powershell
python app.py
```

## What You Get

✅ **Higher Rate Limits**: 1000s of requests instead of 100  
✅ **No 429 Errors**: API won't block you  
✅ **APT Detection**: Detects MuddyWater, Earth Vetala, Lazarus, etc.  
✅ **MITRE Intelligence**: Links IPs to nation-state actors  
✅ **Fresh Data Every Time**: No need for caching  
✅ **Accurate Scoring**: High-risk IPs show CRITICAL  

## Verify It's Working

When you start the app, you should see:

```
✅ AlienVault OTX: Using API key (higher rate limits)
```

Instead of:

```
⚠️  AlienVault OTX: No API key (limited rate limits - may get 429 errors)
```

## Test With Known Malicious IP

Try analyzing `45.142.212.61` (known APT-linked IP):

```python
# Should show:
# - Threat Score: 85-90
# - Risk Level: CRITICAL
# - APT Groups: MuddyWater, Earth Vetala
# - MITRE Intelligence: Found = true
```

## Troubleshooting

### Still Getting 429 Errors?
- ✅ Check `.env` file has correct key
- ✅ Restart application
- ✅ Clear cache folder

### Not Seeing "Using API key" Message?
- ✅ Check `.env` file format (no quotes around key)
- ✅ Make sure file is named `.env` (not `.env.txt`)
- ✅ Check for typos in `ALIENVAULT_OTX_API_KEY`

### Key Not Working?
- ✅ Copy key again from OTX website
- ✅ Make sure you're logged in to OTX
- ✅ Check your email for verification

## Benefits Summary

| Feature | Without API Key | With API Key |
|---------|----------------|--------------|
| Rate Limit | ~100/day | ~10,000/day |
| APT Detection | ❌ Fails often | ✅ Always works |
| 429 Errors | ✅ Common | ❌ Rare |
| MITRE Intel | ❌ Unreliable | ✅ Reliable |
| Cost | FREE | FREE |

## Need Help?

- OTX Documentation: https://otx.alienvault.com/api
- OTX Support: https://otx.alienvault.com/faq

---

**Bottom Line**: This 2-minute setup will completely fix your MITRE intelligence issues! 🚀
