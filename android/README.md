# 🏥 AI Health Assistant - Android WebView Wrapper

This folder contains the Android WebView wrapper that packages your Streamlit web app as a native Android application.

## 📁 Project Structure

```
android/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/health/assistant/
│   │       │   └── MainActivity.java
│   │       ├── res/
│   │       │   └── layout/
│   │       │       └── activity_main.xml
│   │       └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
└── settings.gradle
```

## 🛠️ Setup & Build Instructions

### Step 1: Install Android Studio
1. Download Android Studio from https://developer.android.com/studio
2. Install Android SDK (API 34)
3. Install Android Emulator or connect a physical device

### Step 2: Open Project in Android Studio
1. Launch Android Studio
2. Click **File → Open**
3. Select the `android/` folder from this project
4. Wait for Gradle sync to complete

### Step 3: Build the APK
1. Click **Build → Build Bundle(s) / APK(s) → Build APK(s)**
2. Wait for the build to complete
3. APK will be generated at: `android/app/build/outputs/apk/debug/app-debug.apk`

### Step 4: Test on Device
1. Connect your Android phone via USB (enable Developer Mode)
2. Click **Run → Run 'app'**
3. Select your device
4. App will install and launch

### Step 5: Generate Release APK (for Play Store)
1. **Create a keystore file** (one-time setup):
   ```bash
   keytool -genkey -v -keystore ~/health-assistant.keystore -keyalg RSA -keysize 2048 -validity 10000 -alias health-assistant
   ```

2. In Android Studio:
   - Click **Build → Generate Signed Bundle / APK**
   - Choose **APK** (or **Bundle** for Play Store)
   - Select your keystore file
   - Enter keystore password
   - Enter key password
   - Click **Build**

3. Signed APK will be at: `android/app/release/app-release.apk`

## 📱 Customization

### Change App Name
Edit `android/app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">AI Health Assistant</string>
```

### Change App Icon
Replace `android/app/src/main/res/mipmap/ic_launcher.png` with your icon (512x512 PNG)

### Change App URL
Edit `MainActivity.java` line 28:
```java
webView.loadUrl("YOUR_STREAMLIT_CLOUD_URL_HERE");
```

### Update Version
Edit `android/app/build.gradle`:
```gradle
versionCode 1
versionName "1.0.0"
```

## 🚀 Upload to Google Play Store

### Prerequisites
- Google Play Developer Account ($25 one-time fee)
- Signed Release APK

### Steps
1. Go to https://play.google.com/console
2. Create a new app
3. Fill in app details (name, description, screenshots, privacy policy)
4. Upload signed APK/AAB
5. Review and publish

**Important Notes:**
- Add privacy policy (required by Google)
- Add screenshots (at least 2)
- Add app description
- Add app icon (512x512 PNG)
- Provide support email

## ⚠️ Important: Permissions

Your app requires internet permission (already in AndroidManifest.xml). For Play Store approval:

- ✅ **Internet permission** — Required for web app
- ✅ **Privacy Policy** — Required by Google (add to Play Store listing)
- ✅ **Disclaimer** — Add medical disclaimer in Play Store description

## 🔗 Useful Links

- [Android Studio Documentation](https://developer.android.com/docs)
- [Google Play Console](https://play.google.com/console)
- [App Signing Guide](https://developer.android.com/studio/publish/app-signing)
- [Play Store Release Checklist](https://developer.android.com/distribute/best-practices/launch)

## 📝 Play Store Description Template

```
🏥 AI Health Assistant

Your personal AI-powered guide for:
• 🩺 Symptom checking and condition analysis
• 🥗 Personalized diet plans based on BMI and age
• ⏰ Health reminders for water, medication, and exercise
• 📊 Daily health tracking dashboard

⚠️ DISCLAIMER: This app is for educational purposes only. 
It is NOT a medical device and should not be used for actual 
medical diagnosis or treatment. Always consult a qualified doctor 
for health concerns.

Features:
- 20+ Medical conditions database
- Personalized diet plans
- Health tracking & reminders
- Daily wellness tips
- Available 24/7

Built with AI | Educational Project
```

## 🎓 For Your Capstone Project

**When presenting to your teacher:**
1. Show the Streamlit web app running online
2. Show this Android wrapper in Android Studio
3. Demonstrate the signed APK build
4. Explain the WebView technology used

This shows complete understanding of:
- Web development (Streamlit)
- Mobile development (Android)
- Deployment & publishing

---

*Last updated: 2026-06-09*
