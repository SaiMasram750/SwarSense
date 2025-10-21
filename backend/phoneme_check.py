"""
Utilities for pronunciation analysis using ARPABET phonemes.

This module provides:
- Phoneme extraction from words using CMUdict via `pronouncing`
- Lightweight similarity scoring between two phoneme sequences
- Server-side TTS synthesis using gTTS, returned as bytes for UI playback

All functions are side-effect free and do not depend on Streamlit directly,
to keep presentation and logic concerns separated.
"""

from __future__ import annotations

import io
from functools import lru_cache
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

import pronouncing
from gtts import gTTS


@lru_cache(maxsize=4096)
def get_phonemes(word: str) -> Optional[List[str]]:
    """
    Return the first ARPABET phoneme sequence for a word as a list of tokens.

    If no pronunciation is available in CMUdict, returns None.
    The result is cached to avoid repeated CMUdict lookups.
    """
    if not word:
        return None
    phones: List[str]
    try:
        phones = pronouncing.phones_for_word(word.lower())
    except Exception:
        return None
    if not phones:
        return None
    # CMUdict phones are space-delimited, e.g., "HH AW1 S"
    return phones[0].split()


def synthesize_pronunciation(text: str, lang: str = "en") -> bytes:
    """
    Synthesize speech for `text` using gTTS and return MP3 bytes.
    Intended for UI playback via `st.audio` on the frontend.
    """
    tts = gTTS(text=text, lang=lang)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer.read()


def _similarity_score(target: List[str], spoken: List[str]) -> Tuple[int, float]:
    """
    Compute a similarity score between two phoneme sequences.

    Returns a tuple of (score_percent [0-100], ratio [0-1]).
    Uses SequenceMatcher ratio on token sequences for a fast, interpretable metric.
    """
    if not target or not spoken:
        return 0, 0.0
    # Token-level distance via SequenceMatcher is fast and sufficient for demo.
    ratio = SequenceMatcher(None, target, spoken).ratio()
    score = int(round(ratio * 100))
    return score, ratio


def _diff_ops(target: List[str], spoken: List[str]) -> List[Dict[str, str]]:
    """
    Produce a compact list of edit operations between target and spoken phonemes.

    Each entry is a dict with fields: op (equal/replace/insert/delete),
    target (phoneme or ""), spoken (phoneme or ""). Intended to power UI tips.
    """
    ops: List[Dict[str, str]] = []
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, target, spoken).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                ops.append({"op": "equal", "target": target[i1 + k], "spoken": spoken[j1 + k]})
        elif tag == "replace":
            # Pair up items when possible, then emit remaining as inserts/deletes
            length = min(i2 - i1, j2 - j1)
            for k in range(length):
                ops.append({
                    "op": "replace",
                    "target": target[i1 + k],
                    "spoken": spoken[j1 + k],
                })
            for k in range(length, i2 - i1):
                ops.append({"op": "delete", "target": target[i1 + k], "spoken": ""})
            for k in range(length, j2 - j1):
                ops.append({"op": "insert", "target": "", "spoken": spoken[j1 + k]})
        elif tag == "delete":
            for k in range(i1, i2):
                ops.append({"op": "delete", "target": target[k], "spoken": ""})
        elif tag == "insert":
            for k in range(j1, j2):
                ops.append({"op": "insert", "target": "", "spoken": spoken[k]})
    return ops


def compare_pronunciation(
    user_word: str,
    target_word: str,
    play_only: bool = False,
) -> Dict[str, object]:
    """
    Compare `user_word` and `target_word` at the phoneme level.

    If `play_only` is True, returns a dict with just {"audio_mp3": bytes} for
    UI playback of the target word. Otherwise, returns a rich result dict:

    {
      "target_phonemes": List[str] | None,
      "user_phonemes": List[str] | None,
      "score": int,  # 0..100 similarity
      "ratio": float, # 0..1 similarity
      "ops": List[Dict[str, str]],
      "error": Optional[str]
    }
    """
    if play_only:
        try:
            audio_bytes = synthesize_pronunciation(target_word)
            return {"audio_mp3": audio_bytes, "error": None}
        except Exception as exc:
            return {"audio_mp3": b"", "error": f"TTS failed: {exc}"}

    target_phonemes = get_phonemes(target_word)
    user_phonemes = get_phonemes(user_word)

    if target_phonemes is None:
        return {
            "target_phonemes": None,
            "user_phonemes": user_phonemes,
            "score": 0,
            "ratio": 0.0,
            "ops": [],
            "error": "Target word not found in CMU Pronouncing Dictionary.",
        }

    if user_phonemes is None:
        return {
            "target_phonemes": target_phonemes,
            "user_phonemes": None,
            "score": 0,
            "ratio": 0.0,
            "ops": [],
            "error": "Spoken/transcribed word not found in CMU Pronouncing Dictionary.",
        }

    score, ratio = _similarity_score(target_phonemes, user_phonemes)
    ops = _diff_ops(target_phonemes, user_phonemes)
    return {
        "target_phonemes": target_phonemes,
        "user_phonemes": user_phonemes,
        "score": score,
        "ratio": ratio,
        "ops": ops,
        "error": None,
    }
