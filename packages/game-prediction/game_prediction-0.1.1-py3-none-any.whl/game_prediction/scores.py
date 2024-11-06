from typing import Sequence
import math
from editdistance import eval as edit_dist
import lcz
import chess_notation as cn
from ._beam_search import Piece

def ned(w1: str, w2: str):
  return edit_dist(w1, w2) / max(len(w1), len(w2))

def ocr_score(
  word: str, logps_ocr: Sequence[tuple[str, float]],
  *, alpha: float
) -> float:
  return max(
    (-alpha*ned(word, w) + logp
    for w, logp in logps_ocr),
    default=float('-inf')
  )

def ocr_score2(
  word: str, logps_ocr: Sequence[tuple[str, float]],
) -> float:
  return max(
    (math.log(1 - d/len(word)) + logp
    for w, logp in logps_ocr if (d := ned(word, w)) < min(len(word), len(w))),
    default=float('-inf')
  )

def max_ocr_score(
  san: str, logps_ocr: Sequence[tuple[str, float]], *,
  motions: cn.MotionStyles, languages: Sequence[cn.Language],
  alpha: float | None = None, captured_piece: Piece | None = None,
):
  reprs = cn.representations(san, motions=motions, languages=languages, captured_piece=captured_piece)
  score = lambda r: ocr_score(r, logps_ocr, alpha=alpha) if alpha else ocr_score2(r, logps_ocr)
  return max(map(score, reprs), default=float('-inf'))

def uci_baseline(fens: Sequence[str]):
  return [
    { uci: math.log(p) for uci, p in distrib.items() }
    for distrib in lcz.eval(fens)
  ]

def weighted_geo_mean(logp: float, logq: float, a: float, b: float):
  """Weighted geometrical mean (`[p^a * q^b]^(1/(a+b))`) but in log-space"""
  return (a*logp + b*logq) / (a+b)
