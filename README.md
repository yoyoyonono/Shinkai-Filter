# Shinkai-Filter

This repository originally used OMPC (a MATLAB-like Python bridge). The codebase has been rewritten to run on modern Python with NumPy + OpenCV.

## Requirements

- Python 3.10+
- pip

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Nix (optional)

If you use Nix, a dev shell is provided:

```bash
nix develop
```

## Run the pipeline

```bash
python final.py \
  --src input/input5.jpg \
  --target input/input1.jpg \
  --sky sky.jpg \
  --out-dir output
```

Outputs are written to `output/` as step-by-step images.

Optional light source position:

```bash
python final.py \
  --src input/input5.jpg \
  --target input/input1.jpg \
  --sky sky.jpg \
  --light-x 300 --light-y 120 \
  --out-dir output
```

## Batch mode

```bash
python batch.py \
  --input-dir input \
  --target input/input1.jpg \
  --sky sky.jpg \
  --out-dir batch_output
```

This writes one final image per input file.
