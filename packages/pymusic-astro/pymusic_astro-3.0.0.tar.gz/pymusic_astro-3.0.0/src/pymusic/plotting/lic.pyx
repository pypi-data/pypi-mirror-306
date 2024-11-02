"""Line integral convolution routine.

This is taken from the scipy cookbook:

https://scipy-cookbook.readthedocs.io/items/LineIntegralConvolution.html)

Copyright (c) 2001, 2002 Enthought, Inc.
All rights reserved.

Copyright (c) 2003-2017 SciPy Developers.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  a. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  b. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  c. Neither the name of Enthought nor the names of the SciPy Developers
     may be used to endorse or promote products derived from this software
     without specific prior written permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""

import numpy as np

cimport numpy as np


cdef void _advance(
        float vx, float vy,
        int * p0, int * p1,
        float * f0, float * f1,
        int n0, int n1):

    cdef float tx, ty
    if vx>=0:
        tx = (1-f0[0])/vx
    else:
        tx = -f0[0]/vx

    if vy>=0:
        ty = (1-f1[0])/vy
    else:
        ty = -f1[0]/vy

    if tx < ty:
        if vx >= 0:
            p0[0] += 1
            f0[0] = 0
        else:
            p0[0] -= 1
            f0[0] = 1
        f1[0] += tx*vy
    else:
        if vy >= 0:
            p1[0] += 1
            f1[0] = 0
        else:
            p1[0] -= 1
            f1[0] = 1
        f0[0] += ty*vx

    if p0[0] >= n0:
        p0[0] = n0-1 # FIXME: other boundary conditions?
    if p0[0] < 0:
        p0[0] = 0 # FIXME: other boundary conditions?

    if p1[0] >= n1:
        p1[0] = n1-1 # FIXME: other boundary conditions?
    if p1[0] < 0:
        p1[0] = 0 # FIXME: other boundary conditions?


def line_integral_convolution(
        np.ndarray[float, ndim=2] vx,
        np.ndarray[float, ndim=2] vy,
        np.ndarray[float, ndim=2] texture,
        np.ndarray[float, ndim=1] kernel):

    cdef int i0, i1, k, p1, p0
    cdef int n0, n1, kernellen
    cdef int ndim
    cdef float f0, f1, tx, ty
    cdef np.ndarray[float, ndim=2] result

    n0 = vx.shape[0]
    n1 = vx.shape[1]
    kernellen = kernel.shape[0]

    result = np.zeros((n0,n1), dtype=np.float32)

    for i0 in range(n0):
        for i1 in range(n1):
            p0 = i0
            p1 = i1
            f0 = 0.5
            f1 = 0.5

            k = kernellen // 2
            result[i0, i1] += kernel[k] * texture[p0, p1]
            while k < kernellen-1:
                _advance(vx[p0,p1], vy[p0,p1], &p0, &p1, &f0, &f1, n0, n1)
                k+=1
                result[i0,i1] += kernel[k] * texture[p0, p1]

            p0 = i0
            p1 = i1
            f0 = 0.5
            f1 = 0.5
            while k > 0:
                _advance(-vx[p0,p1],-vy[p0,p1], &p0, &p1, &f0, &f1, n0, n1)
                k-=1
                result[i0,i1] += kernel[k] * texture[p0, p1]

    return result
