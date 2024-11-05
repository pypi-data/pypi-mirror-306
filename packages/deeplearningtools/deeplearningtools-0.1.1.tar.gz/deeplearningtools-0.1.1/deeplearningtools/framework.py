import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
from torch.utils.data import Dataset, DataLoader

import inspect
import collections
from IPython import display


def plot_learning_curve(
    loss_record, title="", xlabel="Training step", ylabel="MSE loss"
):
    """Plot learning curve of your DNN (train & dev loss)"""
    total_steps = len(loss_record["train"])
    x_1 = range(total_steps)
    x_2 = x_1[:: len(loss_record["train"]) // len(loss_record["dev"])]
    figure(figsize=(6, 4))
    plt.plot(x_1, loss_record["train"], c="tab:red", label="train")
    plt.plot(x_2, loss_record["dev"], c="tab:cyan", label="dev")
    plt.ylim(0.0, 5.0)
    plt.xlabel("Training step")
    plt.ylabel("MSE loss")
    plt.title("Learning curve of {}".format(title))
    plt.legend()
    plt.show()


def plot_pred(dv_set, model, device, lim=35.0, preds=None, targets=None):
    """Plot prediction of your DNN"""
    if preds is None or targets is None:
        model.eval()
        preds, targets = [], []
        for x, y in dv_set:
            x, y = x.to(device), y.to(device)
            with torch.no_grad():
                pred = model(x)
                preds.append(pred.detach().cpu())
                targets.append(y.detach().cpu())
        preds = torch.cat(preds, dim=0).numpy()
        targets = torch.cat(targets, dim=0).numpy()

    figure(figsize=(5, 5))
    plt.scatter(targets, preds, c="r", alpha=0.5)
    plt.plot([-0.2, lim], [-0.2, lim], c="b")
    plt.xlim(-0.2, lim)
    plt.ylim(-0.2, lim)
    plt.xlabel("ground truth value")
    plt.ylabel("predicted value")
    plt.title("Ground Truth v.s. Prediction")
    plt.show()


class HyperParameters:
    def save_hyperparameters(self, ignore=[]):
        frame = inspect.currentframe().f_back
        _, _, _, local_vars = inspect.getargvalues(frame)
        self.hparams = {
            k: v
            for k, v in local_vars.items()
            if k not in set(ignore + ["self"]) and not k.startswith("_")
        }
        for k, v in self.hparams.items():
            setattr(self, k, v)


class ProgressBoard(HyperParameters):
    def __init__(
        self,
        xlabel=None,
        ylabel=None,
        xlim=None,
        ylim=None,
        xscale="linear",
        yscale="linear",
        ls=["-", "--", "-.", ":"],
        colors=["C0", "C1", "C2", "C3"],
        fig=None,
        axes=None,
        figsize=(3.5, 2.5),
        display=True,
    ):
        self.save_hyperparameters()

    def draw(self, x, y, label, every_n=1):
        """Defined in :numref:`sec_utils`"""
        Point = collections.namedtuple("Point", ["x", "y"])
        if not hasattr(self, "raw_points"):
            self.raw_points = collections.OrderedDict()
            self.data = collections.OrderedDict()
        if label not in self.raw_points:
            self.raw_points[label] = []
            self.data[label] = []
        points = self.raw_points[label]
        line = self.data[label]
        points.append(Point(x, y))
        if len(points) != every_n:
            return
        mean = lambda x: sum(x) / len(x)
        line.append(Point(mean([p.x for p in points]), mean([p.y for p in points])))
        points.clear()
        if not self.display:
            return
        if self.fig is None:
            self.fig = plt.figure(figsize=self.figsize)
        plt_lines, labels = [], []
        axes = self.axes if self.axes else plt.gca()
        for (k, v), ls, color in zip(self.data.items(), self.ls, self.colors):
            plt_lines.append(
                axes.plot(
                    [p.x for p in v], [p.y for p in v], linestyle=ls, color=color
                )[0]
            )
            labels.append(k)
        if self.xlim:
            axes.set_xlim(self.xlim)
        if self.ylim:
            axes.set_ylim(self.ylim)
        if not self.xlabel:
            self.xlabel = self.x
        axes.set_xlabel(self.xlabel)
        axes.set_ylabel(self.ylabel)
        axes.set_xscale(self.xscale)
        axes.set_yscale(self.yscale)
        axes.legend(plt_lines, labels)
        display.display(self.fig)
        display.clear_output(wait=True)


class DataModule(HyperParameters):
    """The base class of data.

    Defined in :numref:`subsec_oo-design-models`"""

    def __init__(self, root="../data", num_workers=4):
        self.save_hyperparameters()

    def get_dataloader(self, train):
        raise NotImplementedError

    def train_dataloader(self):
        return self.get_dataloader(train=True)

    def val_dataloader(self):
        return self.get_dataloader(train=False)

    def get_tensorloader(self, tensors, train, indices=slice(0, None)):
        """Defined in :numref:`sec_synthetic-regression-data`"""
        tensors = tuple(a[indices] for a in tensors)
        dataset = torch.utils.data.TensorDataset(*tensors)
        return torch.utils.data.DataLoader(dataset, self.batch_size, shuffle=train)


class Module(nn.Module, HyperParameters):
    def __init__(self, plot_train_per_epoch=2, plot_valid_per_epoch=1):
        super().__init__()
        self.save_hyperparameters()
        self.board = ProgressBoard()

    def forward(self, X):
        assert hasattr(self, "net"), "Neural network is defined"
        return self.net(X)

    def plot(self, key, value, train, board=None):
        """Plot a point in animation."""
        assert hasattr(self, "trainer"), "Trainer is not inited"
        if board is None:
            board = self.board
        board.xlabel = "epoch"
        if train:
            x = self.trainer.train_batch_idx / self.trainer.num_train_batches
            n = self.trainer.num_train_batches / self.plot_train_per_epoch
        else:
            x = self.trainer.epoch + 1
            n = self.trainer.num_val_batches / self.plot_valid_per_epoch
        board.draw(
            x,
            torch.detach(value).to("cpu"),
            ("train_" if train else "val_") + key,
            every_n=int(n),
        )

    def loss(self, y_hat, y):
        return self.loss_fn(y_hat, y)

    def training_step(self, batch):
        l = self.loss(self(*batch[:-1]), batch[-1])
        self.plot("loss", l, train=True)
        return l

    def validation_step(self, batch):
        l = self.loss(self(*batch[:-1]), batch[-1])
        self.plot("loss", l, train=False)

    def configure_optimizers(self):
        """Defined in :numref:`sec_classification`"""
        return torch.optim.SGD(self.parameters(), lr=self.lr)

    def apply_init(self, inputs, init=None):
        """Defined in :numref:`sec_lazy_init`"""
        self.forward(*inputs)
        if init is not None:
            self.net.apply(init)


class Classifier(Module):
    """This module will plot accuracy during training"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        acc_fig, axes = plt.subplots(
            ncols=2, nrows=1, figsize=(10, 6), layout="constrained"
        )
        acc_ax = axes[1]
        loss_ax = axes[0]
        self.acc_board = ProgressBoard(fig=acc_fig, axes=acc_ax, xlabel="Accuracy")
        self.board = ProgressBoard(fig=acc_fig, axes=loss_ax, xlabel="Loss")

    def training_step(self, batch):
        pred = self(*batch[:-1])
        pred_class = pred.argmax(axis=1)
        y = batch[-1]
        acc = (pred_class == y).sum() / pred.shape[0]
        l = self.loss(pred, y)
        self.plot("loss", l, train=True, board=self.board)
        self.plot("accuracy", acc, train=True, board=self.acc_board)
        return l

    def validation_step(self, batch):
        pred = self(*batch[:-1])
        pred_class = pred.argmax(axis=1)
        y = batch[-1]
        acc = (pred_class == y).sum() / pred.shape[0]
        l = self.loss(pred, y)
        self.plot("loss", l, train=False, board=self.board)
        self.plot("accuracy", acc, train=False, board=self.acc_board)
        return l


class Trainer(HyperParameters):
    def __init__(self, max_epochs, device="cpu", gradient_clip_val=0):
        """Defined in :numref:`sec_use_gpu`"""
        self.save_hyperparameters()
        self.loss_record = {
            "train": [],
            "dev": [],
        }

    def prepare_data(self, data: DataModule):
        self.train_dataloader = data.train_dataloader()
        self.val_dataloader = data.val_dataloader()
        self.num_train_batches = len(self.train_dataloader)
        self.num_val_batches = (
            len(self.val_dataloader) if self.val_dataloader is not None else 0
        )

    def fit(self, model: Module, data: DataModule):
        self.prepare_data(data)
        self.prepare_model(model)
        self.optim = model.configure_optimizers()
        self.epoch = 0
        self.train_batch_idx = 0
        self.val_batch_idx = 0
        for self.epoch in range(self.max_epochs):
            self.fit_epoch()

    def fit_epoch(self):
        self.model.train()
        for batch in self.train_dataloader:
            loss = self.model.training_step(self.prepare_batch(batch))
            self.loss_record["train"].append(torch.detach(loss))
            self.optim.zero_grad()
            with torch.no_grad():
                loss.backward()
                if self.gradient_clip_val > 0:  # To be discussed later
                    self.clip_gradients(self.gradient_clip_val, self.model)
                self.optim.step()
            self.train_batch_idx += 1
        if self.val_dataloader is None:
            return
        self.model.eval()
        for batch in self.val_dataloader:
            with torch.no_grad():
                val_loss = self.model.validation_step(self.prepare_batch(batch))
                self.loss_record["dev"].append(torch.detach(val_loss))
            self.val_batch_idx += 1

    def prepare_batch(self, batch):
        batch = [a.to(self.device) for a in batch]
        return batch

    def prepare_model(self, model):
        model.trainer = self
        model.board.xlim = [0, self.max_epochs]
        model.to(self.device)
        self.model = model

    def clip_gradients(self, grad_clip_val, model):
        params = [p for p in model.parameters() if p.requires_grad]
        norm = torch.sqrt(sum(torch.sum((p.grad**2)) for p in params))
        if norm > grad_clip_val:
            for param in params:
                param.grad[:] *= grad_clip_val / norm

    def plot_loss_record(self):
        plot_learning_curve(self.loss_record)

    def predict(self, model, data) -> list[torch.Tensor]:
        self.prepare_model(model)
        self.test_dataloader = data.test_dataloader()
        model.eval()
        preds = []
        for batch in self.test_dataloader:
            batch = batch.to(self.device)
            with torch.no_grad():
                pred = model(batch)
                preds.append(torch.detach(pred))
        return preds


if __name__ == "__main__":
    import torchvision
    from torchvision import transforms

    class FashionMNIST(DataModule):
        """The Fashion-MNIST dataset."""

        def __init__(self, batch_size=64, resize=(28, 28)):
            super().__init__()
            self.save_hyperparameters()
            trans = transforms.Compose(
                [transforms.Resize(resize), transforms.ToTensor()]
            )
            self.train = torchvision.datasets.FashionMNIST(
                root=self.root, train=True, transform=trans, download=True
            )
            self.val = torchvision.datasets.FashionMNIST(
                root=self.root, train=False, transform=trans, download=True
            )

        def text_labels(self, indices):
            """Return text labels."""
            labels = [
                "t-shirt",
                "trouser",
                "pullover",
                "dress",
                "coat",
                "sandal",
                "shirt",
                "sneaker",
                "bag",
                "ankle boot",
            ]
            return [labels[int(i)] for i in indices]

        def get_dataloader(self, train):
            data = self.train if train else self.val
            return torch.utils.data.DataLoader(
                data, self.batch_size, shuffle=train, num_workers=self.num_workers
            )

    class SoftmaxRegression(Classifier):  #
        """The softmax regression model."""

        def __init__(self, num_outputs, lr):
            super().__init__()
            self.save_hyperparameters()
            self.net = nn.Sequential(nn.Flatten(), nn.LazyLinear(num_outputs))

        def forward(self, X):
            return self.net(X)

        def loss(self, Y_hat, Y, averaged=True):
            Y_hat = Y_hat.reshape((-1, Y_hat.shape[-1]))
            Y = Y.reshape((-1,))
            return nn.functional.cross_entropy(  # softmax + log
                Y_hat, Y, reduction="mean" if averaged else "none"
            )

    data = FashionMNIST(batch_size=256)
    model = SoftmaxRegression(num_outputs=10, lr=0.1)
    trainer = Trainer(max_epochs=10)
    trainer.fit(model, data)
