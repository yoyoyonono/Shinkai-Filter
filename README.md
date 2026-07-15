# Shinkai-Filter

Shinkai-Filter applies a Makoto Shinkai–style look to photos.

This project originally used OMPC. It now runs on modern Python (NumPy + OpenCV) while keeping the same pipeline idea.

## Pipeline (same style as original)

## Step1: median filtering
![step1_median_filtering](https://user-images.githubusercontent.com/29944979/31849912-a7b4c452-b674-11e7-83cf-60095229b113.jpg)

## Step2: color transform
![step2_color_transfer](https://user-images.githubusercontent.com/29944979/31849913-a7efc412-b674-11e7-967b-cac5860c39f7.jpg)

## Step3: adjust
![step3_adjust](https://user-images.githubusercontent.com/29944979/31849914-a82cbd72-b674-11e7-8edd-2ee8dbaef171.jpg)

## Step4: paste sky
![step4_paste_sky](https://user-images.githubusercontent.com/29944979/31849915-a878d87e-b674-11e7-80c1-d7aa2690d004.jpg)

### Step4-1: threshold
![step4-1_threshold](https://user-images.githubusercontent.com/29944979/31849916-a8b12fb2-b674-11e7-957a-ac50de358437.jpg)

### Step4-2: dilation
![step4-2_dilation](https://user-images.githubusercontent.com/29944979/31849918-a9135016-b674-11e7-817d-d7c33943b2a9.jpg)

### Step4-3: erosion
![step4-3_erosion](https://user-images.githubusercontent.com/29944979/31849919-a94bbcd0-b674-11e7-824c-7c7789ba9554.jpg)

## Step5: add light
![step5_add_light](https://user-images.githubusercontent.com/29944979/31849920-a99f2f50-b674-11e7-9735-88f4347022d9.jpg)

### Step5-1: light filter
![step5-1_light_filter](https://user-images.githubusercontent.com/29944979/31849921-aa00da34-b674-11e7-8f92-4e48897eed0c.jpg)

## Step6: sharpening
![step6_sharpening](https://user-images.githubusercontent.com/29944979/31849922-aa3f7b22-b674-11e7-8302-1bf593c25e3e.jpg)

---

## Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Optional: Nix

```bash
nix develop
```

---

## How to use

### 1) Single image run (`final.py`)

```bash
python final.py \
  --src input/input5.jpg \
  --target input/input1.jpg \
  --sky sky.jpg \
  --out-dir output
```

This writes all intermediate and final step images to `output/`.

Example output files include:

- `step1_median_filtering.jpg`
- `step2_color_transfer.jpg`
- `step3_adjust.jpg`
- `step4_paste_sky.jpg`
- `step5_add_light.jpg`
- `step6_sharpening.jpg`

### 2) Batch run (`batch.py`)

```bash
python batch.py \
  --input-dir input \
  --target input/input1.jpg \
  --sky sky.jpg \
  --out-dir batch_output
```

This processes all `*.jpg`, `*.jpeg`, and `*.png` images in `--input-dir` and writes one final image per input.

---

## CLI switches

### `final.py`

Run help:

```bash
python final.py --help
```

| Switch | Required | Default | Meaning |
|---|---|---|---|
| `--src` | Yes | none | Input/source image path to stylize. |
| `--target` | Yes | none | Guide image path used for color transfer. |
| `--sky` | Yes | none | Sky texture image path used in sky replacement/blending. |
| `--out-dir` | No | `output` | Directory where all step images are saved. |
| `--light-x` | No | auto | X coordinate for light source. If omitted, brightest point is used automatically. |
| `--light-y` | No | auto | Y coordinate for light source. If omitted, brightest point is used automatically. |

Manual light position example:

```bash
python final.py \
  --src input/input5.jpg \
  --target input/input1.jpg \
  --sky sky.jpg \
  --light-x 300 \
  --light-y 120 \
  --out-dir output
```

### `batch.py`

Run help:

```bash
python batch.py --help
```

| Switch | Required | Default | Meaning |
|---|---|---|---|
| `--input-dir` | No | `input` | Directory containing source images to process in batch. |
| `--target` | Yes | none | Guide image path used for color transfer. |
| `--sky` | Yes | none | Sky texture image path used in sky replacement/blending. |
| `--out-dir` | No | `batch_output` | Directory where batch final outputs are saved. |

---

## Notes

- Paths can be relative or absolute.
- If an image cannot be read, the program raises `FileNotFoundError`.
- `final.py` saves full pipeline outputs; `batch.py` saves only final sharpened images.
