# 🚀 PythonAnywhere Deployment Checklist

## ✅ Pre-Deployment Steps

1. **Update PythonAnywhere Code**
   ```bash
   cd meme-quiz-apps
   git pull
   ```

2. **Reload Web App**
   - Go to "Web" tab
   - Click green "Reload" button
   - Wait for reload to complete

## 🐛 Known Issues & Status

### Issue 1: Logout Button ✅ FIXED
**Status**: Fixed with inline onclick handler
**Test**: Click logout button, should redirect to homepage

### Issue 2: All Hearts Turn Red ⚠️ INVESTIGATING
**Symptoms**: After favoriting one meme, all memes show red hearts
**Debug Steps**:
1. Open browser console (F12)
2. Load viral feed
3. Look for: `"Fetched favorites: Set(...)"`
4. Check what IDs are in the Set
5. Favorite one meme
6. Reload feed
7. Check console again

**Possible Causes**:
- IDs mismatch between viral feed and favorites
- userFavorites Set being populated incorrectly

### Issue 3: Videos Not Rendering ⚠️ INVESTIGATING  
**Symptoms**: Videos don't show or play on PythonAnywhere
**Works on**: Localhost ✅

**Possible Causes**:
1. CORS blocking external video URLs
2. Reddit video URLs invalid/expired
3. PythonAnywhere blocking external media

**Debug Steps**:
1. Right-click where video should be
2. Inspect Element
3. Look for `<video>` tag
4. Check `src` attribute
5. Copy URL and try opening in new tab
6. Check browser console for errors

## 🔧 Quick Fixes to Try

### For Heart Issue:
Add this to browser console after loading feed:
```javascript
console.log('All meme IDs:', allMemes.map(m => m.id));
console.log('Favorite IDs:', Array.from(userFavorites));
```

### For Video Issue:
Check if videos load by opening this in browser:
```
https://v.redd.it/[video-id]/DASH_720.mp4
```

## 📞 Next Steps

1. Update PythonAnywhere with latest code
2. Test logout button
3. Share console output for heart/video issues
4. We'll fix remaining issues based on console logs

## 🎯 Expected Behavior

- **Logout**: Should redirect to homepage and clear session
- **Hearts**: Only favorited memes should show ❤️, others show 🤍
- **Videos**: Should display and play with controls
