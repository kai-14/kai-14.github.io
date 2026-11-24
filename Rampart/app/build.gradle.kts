plugins {
    id("com.android.application")
}

android {
    namespace = "com.kai14.watchface.rampart"
    compileSdk = 35

    defaultConfig {
        // Watch Face Format v2 needs Wear OS 5 (API 34) or newer; the Galaxy Watch Ultra line qualifies.
        applicationId = "com.kai14.watchface.rampart"
        minSdk = 34
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            // Sideload-friendly: sign release with the debug key. Use your own key for Play Store.
            signingConfig = signingConfigs.getByName("debug")
        }
    }
}
