from typing_extensions import TypedDict, Unpack, Sequence, Iterable, Literal
from dataclasses import dataclass
import math
from haskellian import iter as I
import chess
from chess_utils import position_idx
from chess_notation import MotionStyles, Language, LANGUAGES
from .scores import max_ocr_score, weighted_geo_mean, uci_baseline
from ._beam_search import beam_search, Node, Child, UciBaseline

class Params(TypedDict, total=False):
  motions: MotionStyles
  languages: Sequence[Language]
  beam_width: int
  alpha: float | None
  beta: float
  logp_uci: UciBaseline
  fen: str

def search(
  ocrpreds: Iterable[Sequence[tuple[str, float]]], *,
  motions: MotionStyles = MotionStyles(),
  languages: Sequence[Language] = LANGUAGES,
  fen: str = chess.STARTING_FEN, beam_width: int = 4,
  logp_uci: UciBaseline = uci_baseline,
  alpha: float | None = 2, beta: float = 0.1,
) -> Iterable[Sequence[Node]]:
  """Beam search, yielding the beam at each step.
  - `ocrpreds`: *all* OCR preds (even if `fen` is not the starting position)
  """
  idx = position_idx(fen)
  logps = (
    lambda san, piece: max_ocr_score(
      san, preds, motions=motions, languages=languages,
      captured_piece=piece, alpha=alpha
    )
    for preds in I.skip(idx, ocrpreds)
  )
  agg_logp = lambda lp1, lp2: weighted_geo_mean(lp1, lp2, 1, beta)
  return beam_search(logps, fen=fen, beam_width=beam_width, agg_logp=agg_logp, logp_uci=logp_uci)

def reconstruct(node: Node, max_depth: int | None = None) -> Iterable[Child]:
  """Reconstruct backwards from `node`
  - `max_depth`: limit of backward steps
  """
  if isinstance(node, Child):
    if max_depth is None or max_depth > 0:
      yield from reconstruct(node.parent, max_depth=max_depth and max_depth-1)
    yield node

@dataclass
class ManualPred:
  san: str
  tag: Literal['manual'] = 'manual'

@dataclass
class AutoPred:
  san: str
  prob: float
  tag: Literal['predicted'] = 'predicted'
  
  @classmethod
  def of(cls, child: Child) -> 'AutoPred':
    return AutoPred(san=child.san, prob=math.exp(child.logp))

Pred = ManualPred | AutoPred

def predict(ocrpreds: Iterable[Sequence[tuple[str, float]]], **params: Unpack[Params]) -> list[AutoPred]:
  """Predict game, returning syncrhonously at the end"""
  beam = []
  for beam in search(ocrpreds, **params):
    ...
  if beam == []:
    return []
  return [
    AutoPred.of(node)
    for node in reconstruct(beam[0])
  ]

