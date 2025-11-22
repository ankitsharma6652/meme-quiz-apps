# Debug Steps for Current Issues

## Issue 1: All hearts turning red
**Symptom**: After favoriting one meme, all memes show red hearts when returning to feed

**Likely cause**: The `userFavorites` Set is being populated with wrong IDs

**Fix**: Check that we're using consistent IDs (meme.id vs meme.meme_id)

## Issue 2: Videos not rendering
**Symptom**: Videos don't show up or play

**Possible causes**:
1. Video URLs are invalid
2. CORS issues
3. Video format not supported

**Debug**: Check browser console for errors

## Issue 3: Logout not working
**Symptom**: Clicking logout button does nothing

**Possible causes**:
1. JavaScript error preventing function execution
2. Button not properly wired to logout function
3. Event listener not attached

**Fix**: Check browser console and verify button onclick handler

## Quick Test Steps:
1. Open browser console (F12)
2. Click "Load Viral Feed"
3. Check for any JavaScript errors
4. Try to favorite a meme
5. Check console.log output
6. Try logout button
7. Check for errors
