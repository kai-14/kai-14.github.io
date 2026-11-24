# Notes for Claude

## Watch faces (Galaxy Watch Ultra 2, Wear OS)

The owner makes custom watch faces here and installs them on their watch from a Windows PC.

- Faces use Google's **Watch Face Format v2**. They are resource-only Android apps with no code.
  Each face is a self-contained Gradle project: `WatchFace/` ("Tidal") and `Rampart/`.
- **Never hand-edit `app/src/main/res/raw/watchface.xml`.** It is generated.
  Edit `tools/generate.py`, then run `python tools/generate.py`, which also rewrites
  `strings.xml` and `preview/*.svg`.
- **Validate** against the official schema:
  `git clone --depth 1 https://github.com/google/watchface.git` once, then
  `python tools/validate.py <clone>/third_party/wff/specification/documents/2/watchface.xsd`
  (needs `pip install xmlschema`).
- **Preview** by rendering `preview/*.svg` and showing the owner. Ask the owner before installing anything.
- **New faces**: copy `WatchFace/` to a new folder and give it its own `applicationId`/`namespace`
  so it can sit on the watch next to the others. Add its path to `.github/workflows/watchface.yml`
  if it should build in CI too.
- Design rule: faces can be *inspired by* a watch the owner likes. Logos and marks are the
  owner's call; these faces are for personal use on their own watch.

## Building

- **CI**: pushing changes under a face folder runs `.github/workflows/watchface.yml` (one matrix entry per face).
  It checks the XML is up to date, validates it and uploads one artifact per face (`tidal-watch-face`,
  `rampart-watch-face`) containing `app-release.apk`. Download with `gh run download <run-id> -n <artifact>`.
- CI signs with a throwaway debug key that changes every run, so updating an installed face fails with
  `INSTALL_FAILED_UPDATE_INCOMPATIBLE`. Uninstall the old package first (the owner then re-picks the face).
- Windows PowerShell variable names are case-insensitive: `$s` and `$S` are the same variable.
- **Locally** (faster for quick changes): needs JDK 17 and the Android SDK
  (`ANDROID_HOME` set; platform 35 and build-tools installed), then `gradle assembleRelease` inside the
  face folder. The APK lands in `app/build/outputs/apk/release/`.

## Installing on the watch (owner's Windows PC)

- adb lives at `%USERPROFILE%\Downloads\platform-tools\adb.exe`. In PowerShell, call it as `.\adb` from that folder.
- The watch is already paired. Each session only needs a connect:
  1. The owner opens Settings → Developer options → Wireless debugging on the watch. The watch must be
     on Wi-Fi, so turning the phone's Bluetooth off helps.
  2. `adb mdns services` usually shows the current connect port. Otherwise ask the owner for the
     IP:port on that screen; the port changes often. Then run `adb connect <ip>:<port>`.
  3. The watch often appears twice in `adb devices`. Always target one entry:
     `adb -s <serial> install -r <apk>`.
- After installing, the owner long-presses the watch face and taps **+** to pick the new face.
