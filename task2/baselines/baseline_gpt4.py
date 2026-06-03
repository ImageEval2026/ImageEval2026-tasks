"""
CRAI-Bench GPT-4 Baseline (LLM-as-a-Judge) via OpenRouter
===========================================================
Scores image-caption pairs using GPT-4 with the CRAI rubric.
This is the organizer baseline — teams are expected to beat it,
particularly on cultural specificity.

Requirements:
    pip install openai pillow

Usage:
    python baseline_gpt4.py \
        --captions dev/captions.tsv \
        --ref_dir  dev/imgs/ref \
        --gen_dir  dev/imgs/generated \
        --output   predictions.tsv \
        --api_key  YOUR_OPENROUTER_API_KEY
"""

import argparse
import base64
import csv
import json
import os
import time
from openai import OpenAI

DIMENSIONS = ['CRAI_CEA', 'CRAI_CC', 'CRAI_CS', 'CRAI_CI', 'CRAI_HP', 'CRAI_composite']

CRAI_PROMPT = """You are a cultural accuracy evaluator for AI-generated images.

You will be given:
1. A reference image showing an authentic Qatari/Arab cultural scene
2. A caption that was used to generate an image
3. An AI-generated image produced from that caption

Score the generated image on the following five dimensions. Return ONLY a JSON object with no explanation.

Scoring dimensions:

CEA (Cultural Element Accuracy) [0.0-1.0]:
  Are the expected cultural elements present and correctly depicted?
  1.0 = all elements accurate, 0.5 = partially accurate, 0.0 = absent or wrong

CC (Contextual Coherence) [0.0-1.0]:
  Are elements placed in culturally appropriate settings and contexts?
  1.0 = fully coherent, 0.5 = partially coherent, 0.0 = incoherent

CS (Cultural Specificity) [0.0, 0.25, 0.50, 0.75, or 1.0]:
  How culturally specific is the depiction?
  1.0 = uniquely Qatari/target culture
  0.75 = strongly associated with target culture
  0.50 = regionally common across Arab world
  0.25 = generic Middle Eastern or vague
  0.0 = no cultural specificity

CI (Cultural Integrity) [0.0-1.0]:
  Is the representation truthful and free of distortion or disrespect?
  1.0 = fully respectful and accurate, 0.5 = minor issues, 0.0 = distorted or disrespectful

HP (Hallucination Penalty) [0.0-1.0]:
  Are there culturally incorrect or fabricated elements NOT mentioned in the caption?
  0.0 = no hallucinations (good), 0.5 = some, 1.0 = many hallucinations

Composite CRAI score:
  CRAI = 0.30 * CEA + 0.20 * CC + 0.20 * CS + 0.20 * CI - 0.10 * HP

Return ONLY this JSON with the five dimension scores. Do not include a composite score:
{
  "CRAI_CEA": <float>,
  "CRAI_CC": <float>,
  "CRAI_CS": <float>,
  "CRAI_CI": <float>,
  "CRAI_HP": <float>
}
"""


def encode_image(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def find_image(directory, image_id):
    for ext in ['.png', '.jpg', '.jpeg']:
        path = os.path.join(directory, f"{image_id}{ext}")
        if os.path.exists(path):
            return path
    return None


def score_instance(client, ref_path, gen_path, caption):
    ref_b64 = encode_image(ref_path)
    gen_b64 = encode_image(gen_path)

    ref_ext  = os.path.splitext(ref_path)[1].lower().replace('.', '')
    gen_ext  = os.path.splitext(gen_path)[1].lower().replace('.', '')
    ref_mime = f"image/{'jpeg' if ref_ext == 'jpg' else ref_ext}"
    gen_mime = f"image/{'jpeg' if gen_ext == 'jpg' else gen_ext}"

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=[
            {"role": "system", "content": CRAI_PROMPT},
            {"role": "user", "content": [
                {"type": "text",      "text": "Reference image (authentic cultural scene):"},
                {"type": "image_url", "image_url": {"url": f"data:{ref_mime};base64,{ref_b64}"}},
                {"type": "text",      "text": f"Caption used for generation:\n{caption}"},
                {"type": "text",      "text": "AI-generated image:"},
                {"type": "image_url", "image_url": {"url": f"data:{gen_mime};base64,{gen_b64}"}},
                {"type": "text",      "text": "Return your CRAI scores as JSON only."},
            ]}
        ],
        max_tokens=256,
        temperature=0.0,
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)


def main(captions_path, ref_dir, gen_dir, output_path, api_key, delay=1.0):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://crai-bench.github.io",
            "X-Title": "CRAI-Bench"
        }
    )

    captions = {}
    with open(captions_path, encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            captions[row['id']] = row['caption']

    out_cols = ['id'] + DIMENSIONS
    results  = []
    errors   = []

    print(f"Scoring {len(captions)} instances with GPT-4 via OpenRouter...\n")

    for idx, (id_, caption) in enumerate(sorted(captions.items()), 1):
        parts    = id_.rsplit('_', 1)
        image_id = parts[0]
        ver      = parts[1]

        ref_path = find_image(ref_dir, image_id)
        gen_path = find_image(gen_dir, f"{image_id}_{ver}")

        if not ref_path:
            errors.append(f"Reference image not found for {image_id}")
            continue
        if not gen_path:
            errors.append(f"Generated image not found for {id_}")
            continue

        try:
            scores = score_instance(client, ref_path, gen_path, caption)
            # Always recompute composite from dimensions — never trust GPT-4's own calculation
            scores['CRAI_composite'] = round(
                0.30 * scores['CRAI_CEA'] +
                0.20 * scores['CRAI_CC']  +
                0.20 * scores['CRAI_CS']  +
                0.20 * scores['CRAI_CI']  -
                0.10 * scores['CRAI_HP'],
                4
            )
            scores['id'] = id_
            results.append(scores)
            print(f"  [{idx}/{len(captions)}] {id_}  CRAI={scores.get('CRAI_composite', '?'):.3f}")
        except Exception as e:
            errors.append(f"Error on {id_}: {e}")
            print(f"  [{idx}/{len(captions)}] {id_}  ERROR: {e}")

        time.sleep(delay)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_cols, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. {len(results)} scored, {len(errors)} errors.")
    print(f"Predictions saved to {output_path}")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CRAI-Bench GPT-4 baseline via OpenRouter')
    parser.add_argument('--captions', required=True, help='Path to captions.tsv')
    parser.add_argument('--ref_dir',  required=True, help='Path to reference images folder')
    parser.add_argument('--gen_dir',  required=True, help='Path to generated images folder')
    parser.add_argument('--output',   default='predictions.tsv', help='Output predictions file')
    parser.add_argument('--api_key',  required=True, help='OpenRouter API key (https://openrouter.ai/keys)')
    parser.add_argument('--delay',    type=float, default=1.0, help='Seconds between API calls')
    args = parser.parse_args()
    main(args.captions, args.ref_dir, args.gen_dir, args.output, args.api_key, args.delay)