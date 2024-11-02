from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any

import h5py
import numpy as np
from numpy.fft import fft2, ifft2, ifftshift

from regularizepsf.exceptions import EvaluatedModelInconsistentSizeError, InvalidSizeError, UnevaluatedPointError
from regularizepsf.helper import _correct_image, _precalculate_ffts
from regularizepsf.psf import PointSpreadFunctionABC, SimplePSF, VariedPSF

if TYPE_CHECKING:
    from pathlib import Path


class CorrectorABC(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, path: str | Path) -> None:
        """Save the model to a file.

        Parameters
        ----------
        path : str or `pathlib.Path`
            where to save the model, suggested extension is ".psf"

        Returns
        -------
        None

        """

    @classmethod
    @abc.abstractmethod
    def load(cls, path: str | Path) -> CorrectorABC:
        """Loads a model from the path.

        Parameters
        ----------
        path : str or `pathlib.Path`
            where to load the model from, suggested extension is ".psf"

        Returns
        -------

        """

    @abc.abstractmethod
    def correct_image(self, image: np.ndarray, size: int,
                      alpha: float = 0.5, epsilon: float = 0.05) -> np.ndarray:
        """PSF correct an image according to the model.

        Parameters
        ----------
        image : 2D float np.ndarray
            image to be corrected
        size : int
            how big to make the patches when correcting an image,
            only used for FunctionalCorrector
        alpha : float
            controls the “hardness” of the transition from amplification
            to attenuation, see notes
        epsilon : float
            controls the maximum of the amplification, see notes

        Returns
        -------
        np.ndarray
            a image that has been PSF corrected

        """

    @abc.abstractmethod
    def simulate_observation(self, image: np.ndarray) -> np.ndarray:
        """Simulates on a star field what an observation using this PSF looks like.

        Parameters
        ----------
        image : 2D float np.ndarray
            image of point source stars to simluate PSF for

        Returns
        -------
        np.ndarray
            an image with the PSF applied

        """


class FunctionalCorrector(CorrectorABC):
    """A version of the PSF corrector that stores the model as a set of functions.
    For the actual correction, the functions must first
    be evaluated to an ArrayCorrector.
    """

    def __init__(self, psf: PointSpreadFunctionABC,
                 target_model: PointSpreadFunctionABC | None) -> None:
        """Initialize a FunctionalCorrector.

        Parameters
        ----------
        psf : SimplePSF or VariedPSF
            the model describing the psf for each patch of the image
        target_model : SimplePSF or None
            the target PSF to use to establish uniformity across the image

        """
        self._psf: PointSpreadFunctionABC = psf
        self._variable: bool = isinstance(self._psf, VariedPSF)
        self._target_model: SimplePSF = target_model

    @property
    def is_variable(self) -> bool:
        """Returns
        -------
        bool
            True if the PSF model is varied (changes across the field-of-view)
            and False otherwise

        """
        return self._variable

    def evaluate_to_array_form(self,
                               x: np.ndarray,
                               y: np.ndarray,
                               size: int) -> ArrayCorrector:
        """Evaluates a FunctionalCorrector to an ArrayCorrector.

        Parameters
        ----------
        x : np.ndarray
            the first dimension coordinates to evaluate over
        y : np.ndarray
            the second dimension coordinates to evaluate over
        size : int
            how large the patches in the PSF correction model shouuld be

        Returns
        -------
        ArrayCorrector
            an array evaluated form of this PSF corrector

        """
        if size % 2 != 0:
            msg = f"size must be even. Found size={size}."
            raise InvalidSizeError(msg)

        psf_x, psf_y = np.meshgrid(np.arange(size), np.arange(size))
        source_evaluations = {}
        for xx in x:
            for yy in y:
                source_evaluations[(xx, yy)] = self._psf.evaluate_at(xx, yy)(psf_x, psf_y)

        target_evaluations = {}
        for xx in x:
            for yy in y:
                target_evaluations[(xx, yy)] = self._target_model.evaluate_at(xx, yy)(psf_x, psf_y) \
                   if self._target_model else np.ones((size, size))

        return ArrayCorrector(source_evaluations, target_evaluations)

    def correct_image(self, image: np.ndarray, size: int,
                      alpha: float = 0.5, epsilon: float = 0.05) -> np.ndarray:
        corners = calculate_covering(image.shape, size)
        array_corrector = self.evaluate_to_array_form(corners[:, 0],
                                                      corners[:, 1], size)
        return array_corrector.correct_image(image.astype(float),
                                             size=size,
                                             alpha=alpha,
                                             epsilon=epsilon)

    def save(self, path: str) -> None:
        msg = "You cannot save a FunctionalCorrector."
        raise NotImplementedError(msg)

    @classmethod
    def load(cls, path: str) -> FunctionalCorrector:
        msg = "You cannot load a FunctionalCorrector."
        raise NotImplementedError(msg)

    def simulate_observation(self, image: np.ndarray, size: int) -> np.ndarray:
        """Simulates on a star field what an observation using this PSF looks like.

        Parameters
        ----------
        image : 2D float np.ndarray
            image of point source stars to simluate PSF for
        size : int
            the PSF will be evaluated to size x size pixels box

        Returns
        -------
        np.ndarray
            an image with the PSF applied

        """
        corners = calculate_covering(image.shape, size)
        array_corrector = self.evaluate_to_array_form(corners[:, 0],
                                                      corners[:, 1],
                                                      size)
        return array_corrector.simulate_observation(image)



class ArrayCorrector(CorrectorABC):
    """A PSF corrector that is evaluated as array patches."""

    def __init__(self, evaluations: dict[Any, np.ndarray],
                 target_evaluations: np.ndarray | dict[Any, np.ndarray]) -> None:
        """Initialize an ArrayCorrector.

        Parameters
        ----------
        evaluations : dict
            evaluated version of the PSF as they vary over the image,
                keys should be (x, y) of the lower left
                pixel of each patch. values should be the `np.ndarray`
                that corresponds to that patch
        target_evaluations : np.ndarray
            evaluated version of the target PSF

        """
        self._evaluation_points: list[Any] = list(evaluations.keys())
        if isinstance(target_evaluations, np.ndarray):
            target_evaluations = {point: target_evaluations for point in self._evaluation_points}

        if not isinstance(evaluations[self._evaluation_points[0]], np.ndarray):
            msg = (
                f"Individual evaluations must be numpy arrays. "
                             f"Found {type(evaluations[self._evaluation_points[0]])}."
            )
            raise TypeError(msg)
        if len(evaluations[self._evaluation_points[0]].shape) != 2:
            msg = "PSF evaluations must be 2-D numpy arrays."
            raise InvalidSizeError(msg)
        self._size = evaluations[self._evaluation_points[0]].shape[0]
        if self._size % 2 != 0:
            msg = f"Size must be even. Found {self._size}"
            raise InvalidSizeError(msg)

        self._evaluations: dict[Any, np.ndarray] = evaluations
        for (x, y), evaluation in self._evaluations.items():
            if evaluation.shape != (self._size, self._size):
                msg = ("Expected evaluated model to have shapes of "
                       f"{(self._size, self._size)}."
                       f"Found {evaluation.shape} at {(x, y)}.")
                raise EvaluatedModelInconsistentSizeError(msg)

        self._target_evaluations = target_evaluations
        for (x, y), evaluation in self._target_evaluations.items():
            if evaluation.shape != (self._size, self._size):
                msg = ("Expected target model to have shapes of "
                       f"{(self._size, self._size)}."
                       f"Found {evaluation.shape} at {(x, y)}.")
                raise EvaluatedModelInconsistentSizeError(msg)


        normalized_values = np.array(
                [v / v.sum() for v in self._evaluations.values()], dtype=float)
        normalized_target = np.array(
                [v / v.sum() for v in self._target_evaluations.values()], dtype=float)
        self.psf_i_fft = _precalculate_ffts(normalized_values)
        self.target_fft = _precalculate_ffts(normalized_target)

    @property
    def evaluations(self) -> dict[Any, np.ndarray]:
        return self._evaluations

    @property
    def evaluation_points(self) -> list:
        return self._evaluation_points

    def correct_image(self, image: np.ndarray, size: int | None = None,  # noqa: ARG002
                      alpha: float = 0.5, epsilon: float = 0.05) -> np.ndarray:
        if not all(img_dim_i >= psf_dim_i for img_dim_i, psf_dim_i in zip(image.shape,
                                                                          (self._size,
                                                                           self._size), strict=False)):
            msg = "The image must be at least as large as the PSFs in all dimensions"
            raise InvalidSizeError(msg)

        x = np.array([x for x, _ in self._evaluations], dtype=int)
        y = np.array([y for _, y in self._evaluations], dtype=int)

        return _correct_image(image.astype(float), self.psf_i_fft, self.target_fft, x, y, alpha, epsilon)

    def __getitem__(self, xy: tuple[int, int]) -> np.ndarray:
        if xy in self._evaluation_points:
            return self._evaluations[xy]
        else:
            msg = f"Model not evaluated at {xy}."
            raise UnevaluatedPointError(msg)

    def save(self, path: str) -> None:
        with h5py.File(path, "w") as f:
            eval_grp = f.create_group("evaluations")
            for key, val in self._evaluations.items():
                eval_grp.create_dataset(f"{key}", data=val)
            eval_grp = f.create_group("target")
            for key, val in self._target_evaluations.items():
                eval_grp.create_dataset(f"{key}", data=val)

    @classmethod
    def load(cls, path: str) -> ArrayCorrector:
        with h5py.File(path, "r") as f:
            target_evaluations = {}
            for key, val in f["target"].items():
                parsed_key = tuple(int(val) for val in key.replace("(", "").replace(")", "").split(","))
                target_evaluations[parsed_key] = val[:].copy()


            evaluations = {}
            for key, val in f["evaluations"].items():
                parsed_key = tuple(int(val) for val in key.replace("(", "").replace(")", "").split(","))
                evaluations[parsed_key] = val[:].copy()
        return cls(evaluations, target_evaluations)

    def simulate_observation(self, image: np.ndarray) -> np.ndarray:
        psf_shape = (self._size, self._size)
        pad_shape = psf_shape
        img_shape = image.shape

        xarr, yarr = np.meshgrid(np.arange(psf_shape[0]), np.arange(psf_shape[1]))
        apodization_window = np.sin((xarr + 0.5) * (np.pi / psf_shape[0])) * np.sin(
            (yarr + 0.5) * (np.pi / psf_shape[1]))

        img_p = np.pad(image, psf_shape, mode="constant")

        observation_synthetic = np.zeros(img_shape)
        observation_synthetic_p = np.pad(observation_synthetic, pad_shape)

        def get_img_i(x: int, y: int) -> np.ndarray:
            xs, xe = x + psf_shape[0], x + 2 * psf_shape[0]
            ys, ye = y + psf_shape[1], y + 2 * psf_shape[1]
            return img_p[xs:xe, ys:ye]

        def set_synthetic_p(x: int, y: int, image: np.ndarray) -> None:
            xs, xe = x + psf_shape[0], x + 2 * psf_shape[0]
            ys, ye = y + psf_shape[1], y + 2 * psf_shape[1]
            observation_synthetic_p[xs:xe, ys:ye] = np.nansum(
                [image, observation_synthetic_p[xs:xe, ys:ye]], axis=0)

        for (x, y), psf_i in self._evaluations.items():
            img_i = get_img_i(x, y)
            out_i = np.real(ifftshift(ifft2(fft2(img_i * apodization_window)
                                            * fft2(psf_i)))) * apodization_window
            set_synthetic_p(x, y, out_i)

        return observation_synthetic_p[psf_shape[0]:img_shape[0] + psf_shape[0],
                      psf_shape[1]:img_shape[1] + psf_shape[1]]


def calculate_covering(image_shape: tuple[int, int], size: int) -> np.ndarray:
    """Determines the grid of overlapping neighborhood patches.

    Parameters
    ----------
    image_shape : tuple of 2 ints
        shape of the image we plan to correct
    size : int
        size of the square patches we want to create

    Returns
    -------
    np.ndarray
        an array of shape Nx2 where return[:, 0]
        are the x coordinate and return[:, 1] are the y coordinates

    """
    half_size = np.ceil(size / 2).astype(int)

    x1 = np.arange(0, image_shape[0], size)
    y1 = np.arange(0, image_shape[1], size)

    x2 = np.arange(-half_size, image_shape[0], size)
    y2 = np.arange(-half_size, image_shape[1], size)

    x3 = np.arange(-half_size, image_shape[0], size)
    y3 = np.arange(0, image_shape[1], size)

    x4 = np.arange(0, image_shape[0], size)
    y4 = np.arange(-half_size, image_shape[1], size)

    x1, y1 = np.meshgrid(x1, y1)
    x2, y2 = np.meshgrid(x2, y2)
    x3, y3 = np.meshgrid(x3, y3)
    x4, y4 = np.meshgrid(x4, y4)

    x1, y1 = x1.flatten(), y1.flatten()
    x2, y2 = x2.flatten(), y2.flatten()
    x3, y3 = x3.flatten(), y3.flatten()
    x4, y4 = x4.flatten(), y4.flatten()

    x = np.concatenate([x1, x2, x3, x4])
    y = np.concatenate([y1, y2, y3, y4])
    return np.stack([x, y], -1)
