from typing import Protocol, Literal, Mapping, Sequence, Iterable
from dataclasses import dataclass
import itertools
import chess
import chess_notation as cn

Piece = Literal['P', 'N', 'B', 'R', 'Q']
class Logprob(Protocol):
  def __call__(self, san: str, captured: Piece | None, /) -> float:
    ...

class AggregateLogps(Protocol):
  def __call__(self, logp_ocr: float, logp_base: float, /) -> float:
    ...

@dataclass
class Node:
  fen: str
  sum_logp: float

@dataclass
class Child(Node):
  logp: float
  san: str
  parent: Node

def captured_piece(board: chess.Board, move: chess.Move) -> Piece | None:
  """The piece captured by `move` on `board` (or `None`)"""
  type = board.piece_type_at(move.to_square)
  if type is not None:
    return chess.piece_symbol(type).upper() # type: ignore

def successors(
  node: Node, uci_base_logps: Mapping[str, float],
  *, logp_ocr: Logprob, agg_logp: AggregateLogps
):
  board = chess.Board(node.fen)
  for uci, lp_base in uci_base_logps.items():
    move = chess.Move.from_uci(uci)
    san = board.san(move)
    captured = captured_piece(board, move)
    lp_ocr = logp_ocr(san, captured)
    logp = agg_logp(lp_ocr, lp_base)
    board.push(move)
    yield Child(fen=board.fen(), sum_logp=node.sum_logp + logp, logp=logp, san=san, parent=node)
    board.pop()


class UciBaseline(Protocol):
  """Evaluates a batch of `fens` into `UCI -> Logprob` mappings"""
  def __call__(self, fens: Sequence[str], /) -> list[dict[str, float]]:
    ...

def step(
  beam: Sequence[Node], *,
  logp_ocr: Logprob, logp_uci: UciBaseline,
  agg_logp: AggregateLogps
) -> Sequence[Node]:
  baselines = logp_uci([node.fen for node in beam])
  succs = [
    successors(node, uci_base, logp_ocr=logp_ocr, agg_logp=agg_logp)
    for node, uci_base in zip(beam, baselines)
  ]
  succs = itertools.chain.from_iterable(succs)
  return sorted(succs, key=lambda child: child.sum_logp, reverse=True)

def beam_search(
  logps_ocr: Iterable[Logprob], *,
  fen: str, beam_width: int,
  logp_uci: UciBaseline, agg_logp: AggregateLogps,
  **_, # to simplify kwargs passing
) -> Iterable[Sequence[Node]]:
  """Semi-general beam search, yielding the beam at each step"""
  beam: Sequence[Node] = [Node(fen=fen, sum_logp=0)]
  for logp in logps_ocr:
    beam = step(beam, logp_ocr=logp, logp_uci=logp_uci, agg_logp=agg_logp)[:beam_width]
    if beam == []:
      break
    yield beam