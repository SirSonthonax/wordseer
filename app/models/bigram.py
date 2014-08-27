"""Bigrams are collections of two words. They are how WordSeer handles
sequences.
"""

from app import db
from .base import Base
from .association_objects import BigramOffset

class Bigram(db.Model, Base):
    """A bigram consists of two words, one primary word and one secondary word.

    Between them is some distance which is less than or equal to five words;
    the secondary word may be anywhere in relation to the primary word.
    """

    word_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    secondary_word_id = db.Column(db.Integer, db.ForeignKey("word.id"))
    frequency = db.Column(db.Integer)

    word = db.relationship("Word", foreign_keys=word_id)
    secondary_word = db.relationship("Word", foreign_keys=secondary_word_id)

    offsets = db.relationship("BigramOffset", backref="bigram")

    def __init__(self, word, secondary_word):
        """Instantiate a bigram.

        Arguments:
            word (Word): The primary word
            secondary_word (Word): The secondary word
        """
        self.word = word
        self.secondary_word = secondary_word
        self.offsets = [BigramOffset(offset=i, bigram=self)
            for i in range(-5, 0) + range(1, 6)]

    def get_offset(self, offset):
        """Get the BigramOffset object that corresponds to a given offset
        for this Bigram.

        Arguments:
            offset (int): The offset to get.

        Returns:
            BigramOffset: The correct BigramOffset object.
        """
        if offset < 0:
            return self.offsets[offset + 5]
        elif offset > 0:
            return self.offsets[offset + 4]
        else:
            raise ValueError("Offset cannot be 0")

    def add_instance(self, offset, sentence, force=True):
        """Add an occurrence of this bigram.

        Arguments:
            offset (int): The offset of ``secondary_word`` from ``word``.
            sentence (Sentence): The sentence where this instance ocurrs.

        Returns:
            BigramOffset: The modified BigramOffset object.
        """
        bigram_offset = self.get_offset(offset)
        bigram_offset.sentences.append(sentence)
        bigram_offset.save(force)

        return bigram_offset
