"""Sentence models.
"""
from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from .base import Base
from .association_objects import DependencyInSentence
from .association_objects import SequenceInSentence
from .association_objects import WordInSentence

class Sentence(db.Model, Base):
    """A model representing a sentence.

    The sentence model is treated like "leaf" units. It has a link to its
    parent unit as well as the top-level document. Sentences contain words
    (the model), and also stores its own raw text, for use in search results.

    Attributes:
        unit (Unit): The ``Unit`` containing this sentence.
        document (Document): the ``Document`` (top-level unit) to which this
            sentence belongs to.
        text (str): The raw text of the sentence.
        sequences (list of Sequences): ``Sequence``\s present in this sentence.
            This relationship is described with ``SequenceInSentence``.
        dependencies (list of Dependencies): ``Dependency``\s present in this
            sentence. This relationship is described with
            ``DependencyInSentence``.

    Relationships:
        belongs to: unit, document
        has many: words, sequences, dependencies
    """

    # Attributes

    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    document_id = db.Column(db.Integer, db.ForeignKey("document.id"))
    text = db.Column(db.Text, index=True)

    # Relationships

    words = association_proxy("word_in_sentence", "word",
        creator=lambda word: WordInSentence(word=word)
    )

    sequences = association_proxy("sequence_in_sentence", "sequence",
        creator=lambda sequence: SequenceInSentence(sequence=sequence)
    )
    dependencies = association_proxy("dependency_in_sentence", "dependency",
        creator=lambda dependency: DependencyInSentence(dependency=dependency)
    )

    document = db.relationship("Document", foreign_keys=[document_id],
        backref="all_sentences")

    def __repr__(self):
        """Representation of the sentence, showing its text.

        NOTE: could be trucated to save print space
        """

        return "<Sentence: " + self.text + ">"

    @property
    def tagged(self):
        """Temporary compatibility method
        """

        return self.words

    def add_word(self, word, position=None, space_before="", tag=""):
        """Add a word to the sentence by explicitly creating the association
        object.

        Arguments:
            word (Word): The ``Word`` that should be added to this ``Sentence``.

        Keyword Arguments:
            position (int): The position (0-indexed) of ``word`` in this
                ``Sentence``.
            space_before (str): The space before ``word``, if any.
            tage (str): The part of speech of ``word``.

        Returns:
            WordInSentence: The association object that associates this
                ``Sentence`` and ``word``.
        """

        word_in_sentence = WordInSentence(
            word=word,
            sentence=self,
            position=position,
            space_before=space_before,
            tag=tag
        )
        word_in_sentence.save()

        return word_in_sentence

    def add_dependency(self, dependency, governor_index=None,
        dependent_index=None):
        """Add a dependency to the sentence by explicitly creating the
        association object.

        Arguments:
            dependency (Dependency): The ``Dependency`` in this relationship.

        Keyword Arguments:
            governor_index (int): Position (0-indexed) of the governor in this
                ``Sentence``. Default is ``None``.
            dependent_index (int): Position (0-indexed) of the dependent in this
                ``Sentence``. Default is ``None``.

        Returns:
            DependencyInSentence: The association object that associates this
                ``Sentence`` and ``dependency``.
        """

        dependency_in_sentence = DependencyInSentence(
            dependency=dependency,
            sentence=self,
            governor_index=governor_index,
            dependent_index=dependent_index
        )

        dependency_in_sentence.save()

        return dependency_in_sentence

    def add_sequence(self, sequence, position=None):
        """Add a ``Sequence`` to the ``Sentence`` by explicitly creating the
        association object.

        Arguments:
            sequence (Sequence): The ``Sequence`` to associate with this
                ``Sentence``.

        Keyword Arguments:
            position (int): The position (0-indexed) of this ``Sequence`` in
                this ``Sentence``. Default is ``None``.

        Returns:
            SequenceInSentence: The association object that associates this
            ``Sentence`` and ``sequence``.
        """

        sequence_in_sentence = SequenceInSentence(
            sequence=sequence,
            sentence=self,
            position=position
        )

        sequence_in_sentence.save()

        return sequence_in_sentence
