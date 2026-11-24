plugins {
    id("com.android.application")
}

android {
    namespace = "com.kai14.watchface.tidal"
    compileSdk = 35

    defaultConfig {
        // Watch Face Format v2 needs Wear OS 5 (API 34) or newer; the Galaxy Watch Ultra line qualifies.
        applicationId = "com.kai14.watchface.tidal"
        minSdk = 34
        targetSdk = 34
        versionCode = 7
        versionName = "1.6"
    }

    // The permanent watch face key. CI decodes it from repo secrets and sets these variables;
    // without them (e.g. a quick local build) release falls back to the debug key.
    val keystore = System.getenv("WATCHFACE_KEYSTORE")
    signingConfigs {
        if (keystore != null) {
            create("permanent") {
                storeFile = file(keystore)
                storeType = "pkcs12"
                storePassword = System.getenv("WATCHFACE_KEYSTORE_PASSWORD")
                keyAlias = "watchface"
                keyPassword = System.getenv("WATCHFACE_KEYSTORE_PASSWORD")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = signingConfigs.getByName(if (keystore != null) "permanent" else "debug")
        }
    }
}
