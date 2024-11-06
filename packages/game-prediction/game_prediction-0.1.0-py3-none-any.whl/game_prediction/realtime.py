from typing_extensions import Sequence, Iterable, Unpack
from functools import partial
from haskellian import iter as I, Iter
import chess
from chess_notation import MotionStyles, Language, LANGUAGES
from chess_utils import position_idx
from ._beam_search import Node, Child
from .decoding import Params, search, AutoPred, ManualPred, Pred
from game_prediction.scores import uci_baseline
from game_prediction._beam_search import Node, Child, UciBaseline

def reconstruct(node: Node, max_depth: int | None = None) -> list[Child]:
  """Reconstruct backwards from `node`
  - `max_depth`: limit of backward steps
  """
  if isinstance(node, Child):
    if max_depth is None or max_depth > 0:
      return reconstruct(node.parent, max_depth=max_depth and max_depth-1) + [node]
    else:
      return [node]
  else:
    return []

def convergence(beam: Sequence[Node], max_depth: int | None = None) -> int:
  """Convergence point: ply back to which all lines of the `beam` agree on the best move
  - `max_depth`: limit of backward steps (from the current beam's ply)
  """
  paths = map(partial(reconstruct, max_depth=max_depth), beam)
  preds: map[list[str]] = map(lambda path: [node.san for node in path], paths)
  plymajor_preds = I.transpose(preds)
  ply_uniq_preds = map(set, plymajor_preds)
  uniq_plys = I.take_while(lambda uniq_preds: len(uniq_preds) == 1, ply_uniq_preds)
  return uniq_plys.len()

@I.lift
def realtime_decode(beams: Iterable[Sequence[Node]]) -> Iterable[list[Child]]:
  last_converged = ply = 0
  beam = None
  for ply, beam in enumerate(beams):
    converged = convergence(beam, max_depth=ply-last_converged)
    if converged > 0:
      yield reconstruct(beam[0], max_depth=ply-last_converged)[:converged]
      last_converged += converged
  if beam is not None:
    yield reconstruct(beam[0], max_depth=max(ply-last_converged, 0))

@I.lift
def realtime_predict(ocrpreds: Iterable[Sequence[tuple[str, float]]], **params: Unpack[Params]) -> Iterable[list[AutoPred]]:
  """Predict game, yielding results as converged"""
  beams = search(ocrpreds, **params)
  for path in realtime_decode(beams):
    yield [AutoPred.of(child) for child in path]

@I.lift
def guided_predict(
  ocrpreds: Iterable[Sequence[tuple[str, float]]],
  manual_ucis: dict[int, str] = {}, *,
  motions: MotionStyles = MotionStyles(),
  languages: Sequence[Language] = LANGUAGES,
  fen: str = chess.STARTING_FEN, beam_width: int = 4,
  logp_uci: UciBaseline = uci_baseline,
  alpha: float | None = None, beta: float = 0.1,
) -> Iterable[Sequence[Pred]]:
  """Predict game, yielding results as converged
  - Passes by `manual_ucis[idx]` at every `idx`, or stops if not legal"""

  idx = position_idx(fen)
  next_manual = Iter(manual_ucis).filter(lambda i: i >= idx).min()
  if next_manual is None:
    yield from realtime_predict(ocrpreds, motions=motions, languages=languages, fen=fen, beam_width=beam_width, logp_uci=logp_uci, alpha=alpha, beta=beta)

  elif next_manual == idx:
    board = chess.Board(fen)
    try:
      move = board.push_uci(manual_ucis[idx])
      fen = board.fen()
      board.pop()
      yield [ManualPred(san=board.san(move))]
      yield from guided_predict(ocrpreds, manual_ucis, motions=motions, languages=languages, fen=fen, beam_width=beam_width, logp_uci=logp_uci, alpha=alpha, beta=beta)
    except chess.IllegalMoveError:
      ...

  else: # next_manual > idx
    child = None
    children = realtime_decode(search(ocrpreds, fen=fen, beam_width=beam_width, logp_uci=logp_uci, alpha=alpha, beta=beta)) \
      .flatmap().take(next_manual-idx)
    for child in children:
      yield [AutoPred.of(child)]

    if child and position_idx(child.fen) == next_manual:
      yield from guided_predict(ocrpreds, manual_ucis, motions=motions, languages=languages, fen=child.fen, beam_width=beam_width, logp_uci=logp_uci, alpha=alpha, beta=beta)