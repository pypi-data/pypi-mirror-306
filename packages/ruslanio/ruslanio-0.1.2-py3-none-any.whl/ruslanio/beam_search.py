import typing as tp
from abc import ABC, abstractmethod
import numpy as np

from .sorting import argtopk
from .arrays import flatten_list


class Sequence(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def updated_copy(self, item: tp.Any):
        pass

    @abstractmethod
    def get_candidates(self) -> list[tuple[tp.Any, float]]:
        pass

    @abstractmethod
    def ended(self) -> bool:
        pass


class NoItemClass:
    pass


NoItem = NoItemClass()


class BeamSearch:
    def __init__(self, beam_size: int):
        self.beam_size = beam_size

    def search(
        self,
        initial_sequences: list[Sequence],
        max_iters: int,
        initial_scores: list[float] | None = None,
        tqdm=None,
    ) -> Sequence:
        # Initialize beam
        sequences = initial_sequences
        if initial_scores is not None:
            scores = initial_scores
        else:
            scores = [0 for _ in sequences]

        pbar = range(max_iters)
        if tqdm is not None:
            pbar = tqdm(range(max_iters))
        for _ in pbar:
            # Generate new points
            candidates = [
                [(seq_i, item, delta_score) for (item, delta_score) in seq.get_candidates()]
                for (seq_i, seq) in enumerate(sequences) if not seq.ended()
            ]  # [n_candidates * current_beam_size]

            # Add stopped sequences
            candidates.extend([
                [(seq_i, NoItem, 0)]
                for (seq_i, seq) in enumerate(sequences) if seq.ended()
            ])

            # Find top scoring candidates
            candidates = flatten_list(candidates, 1)
            candidate_scores = np.array([
                scores[seq_i] + delta_score
                for (seq_i, _, delta_score) in candidates
            ])
            top_i = argtopk(candidate_scores, self.beam_size)

            # Update beam
            new_sequences = []
            for i in top_i:
                seq_i, item, _ = candidates[i]
                if item is not NoItem:
                    new_seq = sequences[seq_i].updated_copy(item)
                else:
                    new_seq = sequences[seq_i]
                new_sequences.append(new_seq)
            sequences = new_sequences

            # Update scores
            scores = candidate_scores[top_i]

            pbar.set_postfix(best_score=scores[0])
            
            if all([seq.ended() for seq in sequences]):
                break

        return sequences, scores
