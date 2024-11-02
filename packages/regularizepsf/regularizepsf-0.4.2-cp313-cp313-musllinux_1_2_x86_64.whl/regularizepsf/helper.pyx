import numpy as np
cimport numpy as np
from numpy.fft import fft2, ifft2
cimport cython

ctypedef np.float_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef _correct_image(image, source_fft, target_fft, x, y, alpha, epsilon):
    """Core Cython code to actually correct an image"""
    cdef int num_evaluations = x.shape[0]
    cdef int size = source_fft.shape[1]
    cdef int i = 0, j=0, xx = 0, yy = 0
    cdef int this_x, this_y, this_x_prime, this_y_prime
    cdef np.ndarray[np.float_t, ndim=2] img_i = np.empty((size, size), dtype=float)
    cdef np.ndarray[DTYPE_t, ndim=2] psf_i = np.empty((size, size), dtype=float)
    cdef np.ndarray[DTYPE_t, ndim=2] corrected_i = np.empty((size, size), dtype=float)
    cdef np.ndarray[DTYPE_t, ndim=2] padded_img = np.pad(image, ((2 * size, 2* size), (2*size, 2*size)),
                                                         mode="constant")
    cdef np.ndarray[DTYPE_t, ndim=2] result_img = np.zeros_like(padded_img, dtype=float)
    cdef float psf_i_hat_abs
    cdef np.ndarray[np.complex128_t, ndim=2] psf_i_hat_norm = np.empty((size, size), dtype=complex)
    cdef np.ndarray[np.complex128_t, ndim=2] img_i_hat = np.empty((size, size), dtype=complex)
    cdef np.ndarray[np.complex128_t, ndim=2] temp = np.empty((size, size), dtype=complex)
    cdef np.ndarray[np.float_t, ndim=2] apodization_window


    xarr, yarr = np.meshgrid(np.arange(size), np.arange(size))
    apodization_window = np.square(np.sin((xarr + 0.5) * (np.pi / size))) * np.square(np.sin((yarr + 0.5) * (np.pi / size)))
    apodization_window = np.sin((xarr + 0.5) * (np.pi / size)) * np.sin((yarr + 0.5) * (np.pi / size))

    for i in range(num_evaluations):
        # get the x and the y
        this_x = x[i]
        this_y = y[i]
        this_x_prime = this_x + 2 * size
        this_y_prime = this_y + 2 * size

        for xx in range(size):
            for yy in range(size):
                img_i[xx, yy] = apodization_window[xx, yy] * padded_img[this_x_prime + xx, this_y_prime + yy]
        img_i_hat = fft2(img_i)

        for xx in range(size):
            for yy in range(size):
                psf_i_hat_norm[xx, yy] = _regularize_value(
                        source_fft[i, xx, yy], alpha, epsilon, target_fft[i, xx, yy])
                temp[xx, yy] = img_i_hat[xx, yy] * psf_i_hat_norm[xx, yy] * target_fft[i, xx, yy]
        corrected_i = np.real(ifft2(temp))

        # add the corrected_i to the array
        for xx in range(size):
            for yy in range(size):
                result_img[this_x_prime+xx, this_y_prime+yy] = result_img[this_x_prime+xx, this_y_prime+yy] + (corrected_i[xx, yy] * apodization_window[xx, yy])

    return result_img[2 * size:image.shape[0] + 2 * size, 2 * size:image.shape[1] + 2 * size]


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef complex _regularize_value(
        complex A,
        float alpha,
        float epsilon,
        complex P):
    """Implements Eqn (6) of Hughes et al. (2023) for one Fourier-space pixel"""
    cdef float A_abs = abs(A)
    cdef complex R_A = (A.conjugate() / A_abs) * (A_abs**alpha / (A_abs**(alpha+1.0) + (epsilon * abs(P))**(alpha+1.0)))
    return R_A


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef _regularize_array(
        np.ndarray[np.complex128_t, ndim=2] A,
        float alpha,
        float epsilon,
        np.ndarray[np.complex128_t, ndim=2] P):
    """Loops _regularize_value across a 2D array"""
    cdef int size = A.shape[1]
    cdef np.ndarray[np.complex128_t, ndim=2] output = np.empty((size, size), dtype=complex)

    for xx in range(size):
        for yy in range(size):
            output[xx, yy] = _regularize_value(A[xx, yy], alpha, epsilon, P[xx, yy])
    return output


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef _precalculate_ffts(np.ndarray[DTYPE_t, ndim=3] values):
    cdef int size = values.shape[1]
    cdef int num_patches = values.shape[0]
    cdef np.ndarray[np.float_t, ndim=2] holder = np.empty((size, size), dtype=float)
    cdef np.ndarray[np.complex128_t, ndim=3] psf_i_hat = np.empty((num_patches, size, size), dtype=complex)
    for patch_i in range(num_patches):
        for xx in range(size):
            for yy in range(size):
                holder[xx, yy] = values[patch_i, xx, yy]
        result = fft2(holder)
        for xx in range(size):
            for yy in range(size):
                psf_i_hat[patch_i, xx, yy] = result[xx, yy]
    return psf_i_hat
