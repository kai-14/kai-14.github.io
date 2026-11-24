# Notes for Claude

## Watch faces (Galaxy Watch Ultra 2, Wear OS)

The owner makes custom watch faces here and installs them on their watch from a Windows PC.

- Faces use Google's **Watch Face Format v2**. They are resource-only Android apps with no code.
  Each face is a self-contained Gradle project: `WatchFace/` ("Tidal") and `Rampart/`.
- **Never hand-edit `app/src/main/res/raw/watchface.xml`.** It is generated.
  Edit `tools/generate.py`, then run `python tools/generate.py` inside the face folder, which also rewrites
  `strings.xml` and `preview/*.svg`.
- Rampart's brushed-metal texture is an image: `python tools/make_texture.py` (needs `pip install numpy pillow`)
  writes `app/src/main/res/drawable-nodpi/metal_texture.png`, which is committed. `generate.py` doesn't touch it.
- **Validate** against the official schema (needs `pip install xmlschema`). Clone Google's spec once, outside the
  repo. On Windows the clone fails with "Filename too long" unless long paths are on:
  `git -c core.longpaths=true clone --depth 1 https://github.com/google/watchface.git`, then inside the face folder
  `python tools/validate.py <clone>/third_party/wff/specification/documents/2/watchface.xsd`.
- **Preview** with `python tools/render_previews.py <face-dir>` from the repo root (headless Edge). It writes
  `<face-dir>/preview/all-colours.png`; `--only <names> --out <png>` renders a subset, and
  `--thumb <name>` refreshes the watch picker thumbnail (`app/src/main/res/drawable-nodpi/preview.png`).
  Show the owner the PNG. Ask the owner before installing anything.
- **New faces**: copy `WatchFace/` to a new folder and give it its own `applicationId`/`namespace`
  so it can sit on the watch next to the others. Add a matrix entry to `.github/workflows/watchface.yml`
  so it builds in CI too.
- Design rule: faces can be *inspired by* a watch the owner likes. Logos and marks are the
  owner's call; these faces are for personal use on their own watch.

### Watch Face Format gotchas

- Gradients: the enclosing `Fill`/`Stroke` colour must be opaque (e.g. `#FFFFFFFF`). Android multiplies the
  gradient by that colour's alpha, so `#00000000` hides it on the watch while browser previews still show it.
- `PartText` needs whole-number `x`, `y`, `width`, `height`.
- There is no polygon shape: tapered or sword hands are built from many short `Line`s.
- Previews that use `<image>` or `<foreignObject>` must be embedded with `<object>`, not `<img>`, when rendering
  (`render_previews.py` does this).

## Building

- **CI**: pushing changes under a face folder runs `.github/workflows/watchface.yml` (one matrix entry per face).
  It checks the XML is up to date, validates it and uploads one artifact per face (`tidal-watch-face`,
  `rampart-watch-face`) containing `app-release.apk`. Download with `gh run download <run-id> -n <artifact>`.
- CI signs with the permanent key (repo secrets `WATCHFACE_KEYSTORE_B64` / `WATCHFACE_KEYSTORE_PASSWORD`;
  cert SHA-256 `9f52241750b83dcd...`, printed in the "Show signing certificate" step), so `install -r` updates
  in place and the owner's selected face stays selected. The keystore and its password live in
  `%USERPROFILE%\.android-keys\` on the owner's PC; never commit them.
  Local builds without `WATCHFACE_KEYSTORE` use the debug key and won't install over a CI build.
- **Locally** (faster for quick changes): needs JDK 17 and the Android SDK
  (`ANDROID_HOME` set; platform 35 and build-tools installed), then `gradle assembleRelease` inside the
  face folder. The APK lands in `app/build/outputs/apk/release/`. (Not set up on the owner's PC yet; use CI.)
- Windows PowerShell variable names are case-insensitive: `$s` and `$S` are the same variable.

## Installing on the watch (owner's Windows PC)

- adb lives at `%USERPROFILE%\Downloads\platform-tools\adb.exe`. In PowerShell, call it as `.\adb` from that folder.
- The watch is already paired. Each session only needs a connect:
  1. The owner opens Settings → Developer options → Wireless debugging on the watch. The watch must be
     on Wi-Fi, so turning the phone's Bluetooth off helps.
  2. `adb mdns services` usually shows the current connect port. Otherwise try the last one that worked
     (`192.168.86.33:44155`) or ask the owner for the IP:port on that screen; the port can change.
     Then run `adb connect <ip>:<port>`.
  3. The watch often appears twice in `adb devices`. Always target one entry:
     `adb -s <serial> install -r <apk>`.
- The watch drops off Wi-Fi often. Run `adb connect` right before each install. If it shows `offline`, use
  `adb disconnect` and connect again. `adb kill-server`/`start-server` from PowerShell can hang the shell.
- Read watch logs filtered on the device (`adb shell "logcat -d -t 6000 | grep -i ..."`); pulling the whole log
  over Wi-Fi is very slow.
- A brand-new face: the owner long-presses the watch face and taps **+** to pick it. Updates need nothing.
