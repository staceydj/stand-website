"""Turn the Canva exports into web-ready assets for the STAND remake.

Usage: python3 -I tools/cutout.py <raw_dir> <out_dir>

- Objects shot on white: background removed by flood fill from the image border,
  so bright areas inside the subject (snow, mist) are kept. Edges are feathered.
- Clouds shot on black: alpha taken from brightness, colour set to white.
- Full scenes: re-encoded only.
Output is WebP (lossy for scenes, with alpha for cutouts).
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def load(name):
    return np.asarray(Image.open(os.path.join(RAW, name + '.png')).convert('RGB')).astype(np.float32)


def save(arr, name, alpha=None, width=None, q=82):
    img = Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGB')
    if alpha is not None:
        img.putalpha(Image.fromarray(alpha.clip(0, 255).astype(np.uint8), 'L'))
    if width and img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=q, method=6)
    return img.size


def cut_white(name, thresh=236, sat_max=18, feather=1.6, crop=True, width=None):
    """Remove an edge-connected near-white background."""
    a = load(name)
    mn, mx = a.min(axis=2), a.max(axis=2)
    whiteish = (mn > thresh) & ((mx - mn) < sat_max)
    labels, _ = ndimage.label(whiteish)
    border = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    border = border[border != 0]
    bg = np.isin(labels, border)
    # close small specks inside the background, then feather the edge
    bg = ndimage.binary_opening(bg, iterations=1)
    alpha = (~bg).astype(np.float32) * 255
    alpha = np.asarray(Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))).astype(np.float32)
    # decontaminate: pull semi-transparent edge pixels away from white
    t = (alpha / 255.0)[..., None]
    a = np.where(t > 0.02, (a - 255 * (1 - t)) / np.maximum(t, 0.02), a)
    if crop:
        ys, xs = np.where(alpha > 8)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        a, alpha = a[y0:y1, x0:x1], alpha[y0:y1, x0:x1]
    return save(a, name, alpha, width)


def cut_black_clouds(name, width=None):
    """Clouds on black -> white clouds with alpha.

    Alpha comes from brightness. Towards the left and right edges a growing penalty is
    subtracted from that density, so thin wisps vanish first and the edge follows the
    puffs instead of a straight line.
    """
    a = load(name)
    lum = a.mean(axis=2)
    dens = np.clip((lum - 40) / 200, 0, 1)
    h, w = dens.shape
    x = np.abs(np.arange(w) / (w - 1) - 0.5) * 2          # 0 centre .. 1 edge
    pen = np.clip((x - 0.45) / 0.55, 0, 1) ** 1.2 * 1.1    # 0 in the middle, >1 at edges
    alpha = np.clip(dens - pen[None, :], 0, 1)
    alpha = np.clip(alpha * 1.35, 0, 1) ** 1.25 * 255
    alpha = np.asarray(Image.fromarray(alpha.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32)
    rgb = np.clip(a / np.maximum(dens[..., None], 0.35), 0, 255)  # lift towards white without glowing thin areas
    ys = np.where(alpha.max(axis=1) > 30)[0]
    xs = np.where(alpha.max(axis=0) > 30)[0]
    rgb, alpha = rgb[ys.min():, xs.min():xs.max() + 1], alpha[ys.min():, xs.min():xs.max() + 1]
    return save(rgb, name, alpha, width)


sizes = {}
for n in ['peak1', 'peak2', 'peak3', 'peak4']:
    sizes[n] = cut_white(n, width=1400)
sizes['rocks'] = cut_white('rocks', width=1600)
sizes['rug'] = cut_white('rug', thresh=200, sat_max=22, width=1400)
sizes['compass'] = cut_white('compass', thresh=195, sat_max=16, width=360)
sizes['torch'] = cut_white('torch', thresh=195, sat_max=16, width=360)
sizes['backpack'] = cut_white('backpack', thresh=195, sat_max=16, width=900)
sizes['hiker'] = cut_white('hiker', thresh=240, sat_max=14, width=1600, crop=False)
sizes['clouds'] = cut_black_clouds('clouds', width=1776)
for n, w in [('hero', 2400), ('about', 1600), ('forest', 1680), ('summit', 1408)]:
    sizes[n] = save(load(n), n, width=w, q=80)
sizes['grass'] = save(load('grass'), 'grass', width=640, q=78)
for k, v in sizes.items():
    print(k, v)
