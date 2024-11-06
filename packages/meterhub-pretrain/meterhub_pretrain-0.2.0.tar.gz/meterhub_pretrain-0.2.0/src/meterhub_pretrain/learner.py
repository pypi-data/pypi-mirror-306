import typing as t


class Learner(t.Protocol):
    def validate(self, model, dataset):
        """validate the model"""
        pass

    def trainner(model, dataset):
        """train the model"""
        pass
