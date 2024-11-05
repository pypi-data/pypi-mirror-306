import numpy as np
import numpy.typing as npt

from cvxopt import matrix
from cvxopt.solvers import qp
from numpy.linalg import inv, norm
from scipy.linalg import solve_triangular
from typing import Iterable


class CL_SPC:
    """This class implements the closed-loop subspace predictive control algorithm.
    """

    def __init__(self,
                 past_window: int,
                 future_window: int,
                 forgetting_factor: float,
                 error_cost: npt.NDArray[np.float64],
                 input_cost: npt.NDArray[np.float64],
                 input_delta_cost: npt.NDArray[np.float64],
                 directional_forgetting:bool=True):
        """
        :param past_window: Length of past data window.
        :type past_window: int
        :param future_window: Length of future data window.
        :type future_window: int
        :param forgetting_factor: Forgetting factor.
        :type forgetting_factor: float
        :param error_cost: Weighting of the reference error term in the cost function.
        :type error_cost: npt.NDArray[np.float64]
        :param input_cost: Weighting of the input magnitude term in the cost function.
        :type input_cost: npt.NDArray[np.float64]
        :param input_delta_cost: Weighting of the input change term in the cost function.
        :type input_delta_cost: npt.NDArray[np.float64]
        :param directional_forgetting: Enable/disable directional forgetting when calculating the Markov parameters. Defaults to True.
        :type directional_forgetting: bool
        """
        self.past_window = past_window
        """Length of past data window."""
        self.future_window = future_window
        """Length of future data window."""

        self.forgetting_factor = forgetting_factor
        """Forgetting factor."""

        self.q = error_cost
        """Weighting of the reference error term."""
        self.r = input_cost
        """Weighting of the input magnitude term."""
        self.r_delta = input_delta_cost
        """Weighting of the input change term."""

        self.directional_forgetting = directional_forgetting
        """Enable/disable directional forgetting in the update of the Markov parameters."""

        self.s_delta = self.calculate_s_delta(future_window)
        """:math:`S_\Delta`. Constant matrix used to calculate input change."""
        self.s_v = self.calculate_s_v(past_window, future_window)
        """:math:`S_v`. Constant matrix used to calculate input change."""

        self.phi = np.zeros((2*(past_window + 1), 1))
        """:math:`\\varphi_k = \\begin{bmatrix} u_{k-p} & y_{k-p} & u_{k-p+1} & y_{k-p+1} & \dots & u_{k-1} & y_{k-1} & \\vert & u_{k} & y_{k} \\end{bmatrix}^T`

        .. note::
            :code:`self.phi` includes :math:`y_{k}` for convenience in the code. :math:`y_{k}` is not included in :math:`\\varphi_k` for calculations.
        """
        self.markov_parameters = np.zeros(2*past_window+1)
        """:math:`\hat{\Theta} = \\begin{bmatrix} \Xi^{(u_{k-p})} & \Xi^{(y_{k-p})} & \Xi^{(u_{k-p+1})} & \Xi^{(y_{k-p+1})} & \dots & \Xi^{(u_{k-1})} & \Xi^{(y_{k-1})} & \\vert & \Xi^{(u_{k})} \\end{bmatrix}^T`"""

        self.cholesky_factor = np.eye(2*self.past_window+1)
        """Cholesky factorisation of the covariance matrix."""

        self.steps = 0
        """Step counter."""

    def calculate_s_delta(self, f: int) -> npt.NDArray[np.float64]:
        """Calculate constant matrix :math:`S_\Delta`.

        .. math::
            S_\Delta \in \mathbb{R}^{f\\times f} = \\begin{bmatrix}
            1 & 0 & 0 & \dots & 0 \\\\
            -1 & 1 & 0 & \dots & 0 \\\\
            0 & -1 & 1 & & \\vdots \\\\
            \\vdots & & \ddots & \ddots & 0 \\\\
            0 & \dots & 0 & -1 & 1
            \\end{bmatrix}


        :param f: Length of future window.
        :type f: int
        :return: Matrix :math:`S_\Delta`.
        :rtype: npt.NDArray[np.float64]
        """
        s = np.zeros((f, f))

        for i in range(f):
            s[i, i] = 1
            if i > 0:
                s[i, i-1] = -1

        return s

    def calculate_s_v(self, p: int, f: int) -> npt.NDArray[np.float64]:
        """Calculate constant matrix :math:`S_v`.

        .. math::
            S_v \in \mathbb{R}^{f\\times p} = \\begin{bmatrix}
            0 & \dots & 0 & 1 \\\\
            0 & \dots & 0 & 0 \\\\
            \\vdots & & \\vdots & \\vdots \\\\
            0 & \dots & 0 & 0
            \\end{bmatrix}

        :param p: Length of past window.
        :type p: int
        :param f: Length of future window.
        :type f: int
        :return: Matrix :math:`S_v`.
        :rtype: npt.NDArray[np.float64]
        """
        s = np.zeros((f, p))
        s[0, -1] = 1

        return s

    def step(self, uk: float, yk: float, rf: npt.NDArray[np.float64]) -> float:
        """Perform one control step:

        1. Update :code:`self.phi` with :math:`u_k`, :math:`y_k`
        2. Increase step counter

        If the step counter is bigger than the past window size:

        3. Update Markov parameters
        4. Construct :math:`\\tilde{\mathcal{H}}`
        5. Calculate :math:`\mathcal{G}`, :math:`\Gamma \\tilde{\mathcal{K}}`, :math:`\Gamma \\tilde{\mathcal{L}}`
        6. Solve quadratic program
        7. Return :math:`u_{k+1}`.

        :param uk: :math:`u_k`, most recent input.
        :type uk: float
        :param yk: :math:`y_k`, most recent output.
        :type yk: float
        :param rf: :math:`r_f`, future reference array of size :py:attr:`CL_SPC.future_window`.
        :type rf: npt.NDArray[np.float64]
        :return: :math:`u_{k+1}`, new input.
        :rtype: float
        """
        self.phi = np.roll(self.phi, -2, axis=0)
        self.phi[-2:, 0] = uk, yk

        self.steps += 1

        if self.steps > self.past_window:
            markov = self.update_markov_parameters(self.phi[:-1, :], self.phi[-1, 0])
            markov_u, markov_y = markov[0::2], markov[1::2]

            h_tilde = self.calculate_h_tilde(markov_y)
            g = self.calculate_g(markov_u, h_tilde)
            gamma_l = self.calculate_gamma_l(markov_u, h_tilde)
            gamma_k = self.calculate_gamma_k(markov_y, h_tilde)

            return self.solve_qp(self.phi[2::2, :], self.phi[3::2, :], rf, g, gamma_l, gamma_k)

    def update_markov_parameters(self, phi: npt.NDArray[np.float64], yk: float) -> npt.NDArray[np.float64]:
        """Update Markov parameters:

        1. Create pre-array
        2. Perform directional forgetting step using Givens rotations
        3. Perform covariance update using Givens rotations
        4. Update Markov parameters

        :param phi: :code:`self.phi`, not including :math:`y_k`.
        :type phi: npt.NDArray[np.float64]
        :param yk: System output :math:`y_k`.
        :type yk: float
        :return: Updated Markov parameters :math:`\hat{\Theta}_k`
        :rtype: npt.NDArray[np.float64]
        """

        # build pre-array
        s = self.cholesky_factor.shape[0] + 1
        array = np.zeros((s, s))

        # directional forgetting step
        if self.directional_forgetting:
            # set up array for directional forgetting
            array[1:, 1:] = self.cholesky_factor
            sqrt_alpha = np.sqrt((1 - self.forgetting_factor)/self.forgetting_factor) * 1 / norm(inv(self.cholesky_factor)@phi)
            array[1:, 0:1] = sqrt_alpha * phi

            array = self.perform_givens_rotations(array, row_range=np.arange(1, s), r_col_range=np.arange(1, s), zero_col_range=np.zeros(s-1, dtype=np.int32))

            # set up array for covariance update after directional forgetting
            array[0, 0] = 1

        else:
            # set up array for covariance update without directional forgetting
            array[0, 0] = np.sqrt(self.forgetting_factor)
            array[1:, 1:] = 1/np.sqrt(self.forgetting_factor)*self.cholesky_factor

        # covariance update step
        array[0, 1:] = phi.T @ array[1:, 1:]

        array = self.perform_givens_rotations(array, row_range=np.zeros(s-1, dtype=np.int32), r_col_range=np.zeros(s-1, dtype=np.int32), zero_col_range=np.arange(s-1, 0, -1))

        # save cholesky factor for next step
        self.cholesky_factor = array[1:, 1:]

        # update Markov parameters
        self.markov_parameters = self.markov_parameters + np.sqrt(self.forgetting_factor)/array[0, 0]*array[1:, 0] * (yk - phi.T @ self.markov_parameters)

        return self.markov_parameters

    @staticmethod
    def perform_givens_rotations(pre_array: npt.NDArray[np.float64], row_range: Iterable[int], r_col_range: Iterable[int], zero_col_range: Iterable[int]) -> npt.NDArray[np.float64]:
        """Perform a set of givens rotations to zero each element :code:`bi = pre_array[row_range[i], zero_col_range[i]]` \
            by rotating it to onto the corresponding :code:`ai = pre_array[row_range[i], r_col_range[i]]`.

        .. math:: \\begin{bmatrix} a & b \\end{bmatrix} \\begin{bmatrix} c & -s \\\\ s & c \\end{bmatrix} = \\begin{bmatrix} r & 0 \\end{bmatrix}

        .. math:: r = \\sqrt{a^2 + b^2}

        .. math:: c = \\frac{a}{r}

        .. math:: s = \\frac{b}{r}

        :param pre_array: Input array containing elements to be zeroed.
        :type pre_array: npt.NDArray[np.float64]
        :param row_range: _description_
        :type row_range: Iterable[int]
        :param r_col_range: _description_
        :type r_col_range: Iterable[int]
        :param zero_col_range: _description_
        :type zero_col_range: Iterable[int]
        :return: _description_
        :rtype: npt.NDArray[np.float64]
        """
        g = np.empty((2, 2))

        for i, jr, j0 in zip(row_range, r_col_range, zero_col_range):
            r_inv = 1/np.hypot(pre_array[i, jr], pre_array[i, j0])
            c = pre_array[i, jr]*r_inv
            s = pre_array[i, j0]*r_inv

            g[0, 0] = c
            g[0, 1] = -s
            g[1, 0] = s
            g[1, 1] = c

            pre_array[:, (jr, j0)] = pre_array[:, (jr, j0)] @ g
            pre_array[i, j0] = 0

        return pre_array

    def calculate_h_tilde(self, markov_y: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Construct :math:`\\tilde{\\mathcal{H}}` from Markov parameters.

        .. math::
            \\tilde{\mathcal{H}} = \\begin{bmatrix}
            I & 0 & \dots & 0 \\\\
            -CK & I & & \\vdots \\\\
            \\vdots & \\vdots & \ddots & 0 \\\\
            - C\\tilde{A}^{f-2}K & -C\\tilde{A}^{f-3}K & \dots & I
            \\end{bmatrix}

        with

        .. math::
            \\tilde{\Xi}^{(y_{k-i})} = C\\tilde{A}^{i-1}K

        :param markov_y: :math:`\\tilde{\Xi}^{(y)}`, Markov parameters pertaining to the outputs.
        :type markov_y: npt.NDArray[np.float64]
        :return: :math:`\\tilde{\\mathcal{H}}`.
        :rtype: npt.NDArray[np.float64]
        """
        h_tilde = np.zeros((self.future_window, self.future_window))
        h_tilde[0, 0] = 1
        for i in range(1, len(h_tilde)):
            h_tilde[i, i] = 1
            h_tilde[i, 0:i] = -1 * markov_y[-i::]

        return h_tilde

    def calculate_g(self, markov_u: npt.NDArray[np.float64], h_tilde: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Calculate :math:`\\mathcal{G}`. First, construct :math:`\\tilde{\\mathcal{G}}` from Markov parameters, \
            then calculate :math:`\\mathcal{G}` using :math:`\\tilde{\\mathcal{H}}` taking advantage of the fact that \
            the latter is lower triangular.

        .. math::
            \\tilde{\mathcal{G}} = \\begin{bmatrix}
            D & 0 & \dots & 0 \\\\
            C\\tilde{B} & D & \dots & 0 \\\\
            \\vdots & \\vdots & \ddots & \\vdots \\\\
            C\\tilde{A}^{f-2}\\tilde{B} & C\\tilde{A}^{f-3}\\tilde{B} & \dots & D
            \\end{bmatrix}

        with

        .. math::
            \\tilde{\Xi}^{(u_{k-i})} = \\begin{cases}
            D, &\\text{if } i = 0 \\\\
            C\\tilde{A}^{i-1}\\tilde{B}, &\\text{if } i > 0
            \\end{cases}

        Then

        .. math::
            \\mathcal{G} = \\tilde{\\mathcal{H}}^{-1} \\tilde{\\mathcal{G}}

        :param markov_u: :math:`\\tilde{\Xi}^{(u)}`, Markov parameters pertaining to the inputs.
        :type markov_u: npt.NDArray[np.float64]
        :param h_tilde: :math:`\\tilde{\\mathcal{H}}`.
        :type h_tilde: npt.NDArray[np.float64]
        :return: :math:`\\mathcal{G}`.
        :rtype: npt.NDArray[np.float64]
        """
        g_tilde = np.zeros((self.future_window, self.future_window))
        for i in range(len(g_tilde)):
            g_tilde[i, 0:i+1] = markov_u[-i-1::]

        return solve_triangular(h_tilde, g_tilde, lower=True, unit_diagonal=True)

    def calculate_gamma_l(self, markov_u: npt.NDArray[np.float64], h_tilde: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Calculate :math:`\Gamma \\tilde{\\mathcal{L}}`. First, construct :math:`\\tilde{\Gamma}\\tilde{\\mathcal{L}}` from Markov parameters, \
            then calculate :math:`\Gamma \\tilde{\\mathcal{L}}` using :math:`\\tilde{\\mathcal{H}}` taking advantage of the fact that \
            the latter is lower triangular.

        .. math::
            \\tilde{\Gamma}\\tilde{\\mathcal{L}} = \\begin{bmatrix}
            \\tilde{\Xi}^{(u_{k-p})} & \\tilde{\Xi}^{(u_{k-p+1})} & \dots & \\tilde{\Xi}^{(u_{k-p+f-1})} & \dots & \\tilde{\Xi}^{(u_{k-1})} \\\\
            0 & \\tilde{\Xi}^{(u_{k-p})} & \dots & \\tilde{\Xi}^{(u_{k-p+f-2})} & \dots & \\tilde{\Xi}^{(u_{k-2})} \\\\
            \\vdots & & & \\vdots & \ddots & \\vdots \\\\
            0 & & \dots & \\tilde{\Xi}^{(u_{k-p})} & \dots & \\tilde{\Xi}^{(u_{k-f})}
            \end{bmatrix}

        Then

        .. math::
            \Gamma \\tilde{\\mathcal{L}} = \\tilde{\\mathcal{H}}^{-1} \\tilde{\Gamma} \\tilde{\\mathcal{L}}

        :param markov_u: :math:`\\tilde{\Xi}^{(u)}`, Markov parameters pertaining to the inputs.
        :type markov_u: npt.NDArray[np.float64]
        :param h_tilde: :math:`\\tilde{\\mathcal{H}}`.
        :type h_tilde: npt.NDArray[np.float64]
        :return: :math:`\Gamma \\tilde{\\mathcal{L}}`.
        :rtype: npt.NDArray[np.float64]
        """
        return self._calculate_gamma_kl(markov_u, h_tilde)

    def calculate_gamma_k(self, markov_y: npt.NDArray[np.float64], h_tilde: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Calculate :math:`\Gamma \\tilde{\\mathcal{K}}`. First, construct :math:`\\tilde{\Gamma}\\tilde{\\mathcal{K}}` from Markov parameters, \
            then calculate :math:`\Gamma \\tilde{\\mathcal{K}}` using :math:`\\tilde{\\mathcal{H}}` taking advantage of the fact that \
            the latter is lower triangular.

        .. math::
            \\tilde{\Gamma}\\tilde{\mathcal{K}} = \\begin{bmatrix}
            \\tilde{\Xi}^{(y_{k-p})} & \\tilde{\Xi}^{(y_{k-p+1})} & \dots & \\tilde{\Xi}^{(y_{k-p+f-1})} & \dots & \\tilde{\Xi}^{(y_{k-1})} \\\\
            0 & \\tilde{\Xi}^{(y_{k-p})} & \dots & \\tilde{\Xi}^{(y_{k-p+f-2})} & \dots & \\tilde{\Xi}^{(y_{k-2})} \\\\
            \\vdots & & & \\vdots & \ddots & \\vdots \\\\
            0 & & \dots & \\tilde{\Xi}^{(y_{k-p})} & \dots & \\tilde{\Xi}^{(y_{k-f})}
            \end{bmatrix}

        Then

        .. math::
            \Gamma \\tilde{\\mathcal{K}} = \\tilde{\\mathcal{H}}^{-1} \\tilde{\Gamma} \\tilde{\\mathcal{K}}

        :param markov_y: :math:`\\tilde{\Xi}^{(y)}`, Markov parameters pertaining to the outputs.
        :type markov_y: npt.NDArray[np.float64]
        :param h_tilde: :math:`\\tilde{\\mathcal{H}}`.
        :type h_tilde: npt.NDArray[np.float64]
        :return: :math:`\Gamma \\tilde{\\mathcal{K}}`.
        :rtype: npt.NDArray[np.float64]
        """
        return self._calculate_gamma_kl(markov_y, h_tilde)

    def _calculate_gamma_kl(self, markov: npt.NDArray[np.float64], h_tilde: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        """Implements common functionality of :py:meth:`CL_SPC.calculate_gamma_k` and :py:meth:`CL_SPC.calculate_gamma_l`, \
            since array structure is identical and only differs in which Markov parameters are used.

        :param markov: :math:`\\tilde{\Xi}^{(u)}` or :math:`\\tilde{\Xi}^{(y)}`, Markov parameters.
        :type markov: npt.NDArray[np.float64]
        :param h_tilde: :math:`\\tilde{\\mathcal{H}}`.
        :type h_tilde: npt.NDArray[np.float64]
        :return: :math:`\Gamma \\tilde{\\mathcal{K}}` or :math:`\Gamma \\tilde{\\mathcal{L}}`, depending on provided Markov parameters.
        :rtype: npt.NDArray[np.float64]
        """
        gamma_kl_tilde = np.zeros((self.future_window, self.past_window))
        for i in range(len(gamma_kl_tilde)):
            gamma_kl_tilde[i, i::] = markov[:self.past_window-i]

        return solve_triangular(h_tilde, gamma_kl_tilde, lower=True, unit_diagonal=True)

    def solve_qp(self, up: npt.NDArray[np.float64], yp: npt.NDArray[np.float64], rf: npt.NDArray[np.float64], g: npt.NDArray[np.float64], gamma_l: npt.NDArray[np.float64], gamma_k: npt.NDArray[np.float64]) -> float:
        """Solve quadratic program

        .. math::
            J = u^T_f P u_f + q^T u_f

        with

        .. math::
            P = \\mathcal{G}^T Q_a \\mathcal{G} + S^T_\Delta R^\Delta_a S_\Delta + R_a

        .. math::
            q^T = 2\\left(u^T_p \Gamma \\tilde{\\mathcal{L}} Q_a \\mathcal{G} + u^T_p \Gamma \\tilde{\\mathcal{K}} Q_a \\mathcal{G} - r^T_f Q \\mathcal{G} - u^T_p S^T_v R^\Delta_a S_\Delta \\right)

        :param up: :math:`u_p`, array of past inputs of length :py:attr:`CL_SPC.past_window`.
        :type up: npt.NDArray[np.float64]
        :param yp: :math:`y_p`, array of past outputs of length :py:attr:`CL_SPC.past_window`.
        :type yp: npt.NDArray[np.float64]
        :param rf: :math:`r_f`, array of future references of length :py:attr:`CL_SPC.future_window`.
        :type rf: npt.NDArray[np.float64]
        :param g: :math:`\\mathcal{G}`.
        :type g: npt.NDArray[np.float64]
        :param gamma_l: :math:`\Gamma \\tilde{\\mathcal{L}}`.
        :type gamma_l: npt.NDArray[np.float64]
        :param gamma_k: :math:`\Gamma \\tilde{\\mathcal{K}}`.
        :type gamma_k: npt.NDArray[np.float64]
        :return: :math:`u_{k+1}`, next input.
        :rtype: float
        """
        p = g.T @ self.q @ g \
            + self.s_delta.T @ self.r_delta @ self.s_delta \
            + self.r

        q = 2 * (
            up.T @ gamma_l.T @ self.q @ g
            + yp.T @ gamma_k.T @ self.q @ g
            - rf.T @ self.q @ g
            - up.T @ self.s_v.T @ self.r_delta @ self.s_delta
        )

        sol = qp(matrix(2*p), matrix(q.T))
        return sol['x'][0, 0]
