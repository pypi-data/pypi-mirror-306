import typing as t

from meterhub_pretrain import learner, metric


class Resourcer(t.Protocol):
    def get_dataset(self) -> tuple[t.Any, t.Any]:
        """get new-train and valid dataset"""
        ...

    def get_models(self) -> tuple[t.Any, t.Any]:
        """get pretrain model and direct train model"""
        ...


def pretrain_process(
    resourcer: Resourcer,
    learner: learner.Learner,
    collect_metric: t.Type[metric.collect_metric],
    save_metric: t.Type[metric.save_metric],
):
    """to validate if the pretrain worked for meter reading task"""
    pretrain_model, direct_train_model = resourcer.get_models()
    train_dataset, valid_dataset = resourcer.get_dataset()

    # perform validate on pretrain model
    res1 = learner.validate(pretrain_model, valid_dataset)
    res2 = learner.validate(direct_train_model, valid_dataset)

    collect_metric("before_train", "pretrain_model", res1)
    collect_metric("before_train", "direct_train_model", res2)

    trained_model = learner.trainner(direct_train_model, train_dataset)
    trained_model_from_pretrain = learner.trainner(pretrain_model, train_dataset)

    res3 = learner.validate(trained_model, valid_dataset)
    res4 = learner.validate(trained_model_from_pretrain, valid_dataset)
    collect_metric("after_train", "direct_train_model", res3)
    collect_metric("after_train", "pretrain_model", res4)
    save_metric()
