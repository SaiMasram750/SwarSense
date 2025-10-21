"""Emotion detection backend stub.

For the Streamlit app, the primary emotion classifier runs client-side in
`backend/model.html` via Teachable Machine. This module exposes a minimal
server-side hook that could be wired to aggregate signals or accept
client-posted results in the future.
"""

from __future__ import annotations

from typing import Optional


def detect_emotion() -> Optional[str]:
    """
    Placeholder: returns None. In a production app, this could:
    - Ingest recent client-side predictions via websocket/REST
    - Fuse audio/video features for a more robust signal
    - Provide debounced summary labels and confidence
    """
    return None
