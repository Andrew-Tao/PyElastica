import numpy as np
from elastica.boundary_conditions import OneEndFixedRod
from elastica.external_forces import EndpointForces
from elastica.timestepper.symplectic_steppers import PositionVerlet
from elastica.timestepper import integrate
import elastica as ea
from fontTools.misc.cython import returns

from TimoshenkoBeamCase.convergence_functions import calculate_error_norm
from cantilever_transversal_load_postprocessing import adjust_square_cross_section
from matplotlib import pyplot as plt
from matplotlib.colors import to_rgb


def analytical_results(index):
    analytical_results = [
        0.00000000e00,
        1.22204628e-07,
        1.35200810e-05,
        4.01513712e-05,
        7.99730376e-05,
        1.32941281e-04,
        1.99011559e-04,
        2.78138600e-04,
        3.70276423e-04,
        4.75378357e-04,
        5.93397051e-04,
        7.24284499e-04,
        8.67992049e-04,
        1.02447043e-03,
        1.19366975e-03,
        1.37553953e-03,
        1.57002873e-03,
        1.77708572e-03,
        1.99665834e-03,
        2.22869391e-03,
        2.47313923e-03,
        2.72994059e-03,
        2.99904381e-03,
        3.28039424e-03,
        3.57393679e-03,
        3.87961590e-03,
        4.19737562e-03,
        4.52715957e-03,
        4.86891100e-03,
        5.22257275e-03,
        5.58808731e-03,
        5.96539683e-03,
        6.35444310e-03,
        6.75516760e-03,
        7.16751149e-03,
        7.59141563e-03,
        8.02682062e-03,
        8.47366675e-03,
        8.93189407e-03,
        9.40144239e-03,
        9.88225128e-03,
        1.03742601e-02,
        1.08774079e-02,
        1.13916338e-02,
        1.19168763e-02,
        1.24530742e-02,
        1.30001658e-02,
        1.35580893e-02,
        1.41267830e-02,
        1.47061848e-02,
        1.52962324e-02,
        1.58968638e-02,
        1.65080166e-02,
        1.71296282e-02,
        1.77616363e-02,
        1.84039782e-02,
        1.90565913e-02,
        1.97194129e-02,
        2.03923802e-02,
        2.10754305e-02,
        2.17685010e-02,
        2.24715289e-02,
        2.31844514e-02,
        2.39072057e-02,
        2.46397290e-02,
        2.53819584e-02,
        2.61338313e-02,
        2.68952850e-02,
        2.76662567e-02,
        2.84466838e-02,
        2.92365039e-02,
        3.00356543e-02,
        3.08440727e-02,
        3.16616967e-02,
        3.24884640e-02,
        3.33243125e-02,
        3.41691802e-02,
        3.50230049e-02,
        3.58857250e-02,
        3.67572786e-02,
        3.76376041e-02,
        3.85266402e-02,
        3.94243253e-02,
        4.03305983e-02,
        4.12453981e-02,
        4.21686639e-02,
        4.31003348e-02,
        4.40403504e-02,
        4.49886500e-02,
        4.59451736e-02,
        4.69098609e-02,
        4.78826522e-02,
        4.88634876e-02,
        4.98523077e-02,
        5.08490530e-02,
        5.18536646e-02,
        5.28660834e-02,
        5.38862507e-02,
        5.49141079e-02,
        5.59495968e-02,
        5.69926592e-02,
        5.80432372e-02,
        5.91012732e-02,
        6.01667098e-02,
        6.12394897e-02,
        6.23195560e-02,
        6.34068518e-02,
        6.45013207e-02,
        6.56029064e-02,
        6.67115529e-02,
        6.78272044e-02,
        6.89498053e-02,
        7.00793003e-02,
        7.12156343e-02,
        7.23587527e-02,
        7.35086008e-02,
        7.46651243e-02,
        7.58282693e-02,
        7.69979819e-02,
        7.81742086e-02,
        7.93568962e-02,
        8.05459917e-02,
        8.17414424e-02,
        8.29431959e-02,
        8.41511998e-02,
        8.53654024e-02,
        8.65857520e-02,
        8.78121972e-02,
        8.90446868e-02,
        9.02831702e-02,
        9.15275966e-02,
        9.27779159e-02,
        9.40340781e-02,
        9.52960333e-02,
        9.65637321e-02,
        9.78371254e-02,
        9.91161643e-02,
        1.00400800e-01,
        1.01690984e-01,
        1.02986669e-01,
        1.04287807e-01,
        1.05594350e-01,
        1.06906251e-01,
        1.08223463e-01,
        1.09545939e-01,
        1.10873633e-01,
        1.12206499e-01,
        1.13544491e-01,
        1.14887564e-01,
        1.16235671e-01,
        1.17588769e-01,
        1.18946812e-01,
        1.20309756e-01,
        1.21677557e-01,
        1.23050171e-01,
        1.24427554e-01,
        1.25809663e-01,
        1.27196455e-01,
        1.28587887e-01,
        1.29983916e-01,
        1.31384501e-01,
        1.32789599e-01,
        1.34199168e-01,
        1.35613168e-01,
        1.37031556e-01,
        1.38454293e-01,
        1.39881337e-01,
        1.41312648e-01,
        1.42748186e-01,
        1.44187911e-01,
        1.45631783e-01,
        1.47079764e-01,
        1.48531814e-01,
        1.49987894e-01,
        1.51447966e-01,
        1.52911991e-01,
        1.54379932e-01,
        1.55851751e-01,
        1.57327410e-01,
        1.58806872e-01,
        1.60290100e-01,
        1.61777057e-01,
        1.63267707e-01,
        1.64762014e-01,
        1.66259941e-01,
        1.67761453e-01,
        1.69266514e-01,
        1.70775089e-01,
        1.72287144e-01,
        1.73802642e-01,
        1.75321550e-01,
        1.76843834e-01,
        1.78369458e-01,
        1.79898390e-01,
        1.81430597e-01,
        1.82966043e-01,
        1.84504697e-01,
        1.86046526e-01,
        1.87591496e-01,
        1.89139575e-01,
        1.90690732e-01,
        1.92244934e-01,
        1.93802149e-01,
        1.95362346e-01,
        1.96925493e-01,
        1.98491560e-01,
        2.00060515e-01,
        2.01632328e-01,
        2.03206968e-01,
        2.04784405e-01,
        2.06364609e-01,
        2.07947550e-01,
        2.09533198e-01,
        2.11121524e-01,
        2.12712499e-01,
        2.14306094e-01,
        2.15902280e-01,
        2.17501027e-01,
        2.19102309e-01,
        2.20706096e-01,
        2.22312361e-01,
        2.23921075e-01,
        2.25532211e-01,
        2.27145741e-01,
        2.28761639e-01,
        2.30379877e-01,
        2.32000427e-01,
        2.33623265e-01,
        2.35248361e-01,
        2.36875692e-01,
        2.38505229e-01,
        2.40136948e-01,
        2.41770821e-01,
        2.43406825e-01,
        2.45044932e-01,
        2.46685118e-01,
        2.48327358e-01,
        2.49971626e-01,
        2.51617898e-01,
        2.53266148e-01,
        2.54916353e-01,
        2.56568488e-01,
        2.58222528e-01,
        2.59878451e-01,
        2.61536231e-01,
        2.63195845e-01,
        2.64857269e-01,
        2.66520481e-01,
        2.68185455e-01,
        2.69852171e-01,
        2.71520603e-01,
        2.73190730e-01,
        2.74862529e-01,
        2.76535977e-01,
        2.78211052e-01,
        2.79887730e-01,
        2.81565991e-01,
        2.83245812e-01,
        2.84927171e-01,
        2.86610046e-01,
        2.88294416e-01,
        2.89980258e-01,
        2.91667553e-01,
        2.93356277e-01,
        2.95046410e-01,
        2.96737931e-01,
        2.98430819e-01,
        3.00125053e-01,
        3.01820613e-01,
        3.03517477e-01,
        3.05215625e-01,
        3.06915037e-01,
        3.08615693e-01,
        3.10317572e-01,
        3.12020653e-01,
        3.13724919e-01,
        3.15430347e-01,
        3.17136919e-01,
        3.18844614e-01,
        3.20553414e-01,
        3.22263299e-01,
        3.23974248e-01,
        3.25686244e-01,
        3.27399267e-01,
        3.29113297e-01,
        3.30828315e-01,
        3.32544303e-01,
        3.34261242e-01,
        3.35979112e-01,
        3.37697895e-01,
        3.39417573e-01,
        3.41138127e-01,
        3.42859538e-01,
        3.44581788e-01,
        3.46304859e-01,
        3.48028732e-01,
        3.49753389e-01,
        3.51478811e-01,
        3.53204982e-01,
        3.54931882e-01,
        3.56659495e-01,
        3.58387801e-01,
        3.60116783e-01,
        3.61846424e-01,
        3.63576705e-01,
        3.65307609e-01,
        3.67039118e-01,
        3.68771215e-01,
        3.70503882e-01,
        3.72237102e-01,
        3.73970858e-01,
        3.75705131e-01,
        3.77439905e-01,
        3.79175162e-01,
        3.80910885e-01,
        3.82647057e-01,
        3.84383660e-01,
        3.86120679e-01,
        3.87858094e-01,
        3.89595890e-01,
        3.91334049e-01,
        3.93072555e-01,
        3.94811390e-01,
        3.96550537e-01,
        3.98289980e-01,
        4.00029701e-01,
        4.01769684e-01,
        4.03509911e-01,
        4.05250367e-01,
        4.06991034e-01,
        4.08731895e-01,
        4.10472933e-01,
        4.12214132e-01,
        4.13955475e-01,
        4.15696946e-01,
        4.17438527e-01,
        4.19180201e-01,
        4.20921952e-01,
        4.22663764e-01,
        4.24405619e-01,
        4.26147501e-01,
        4.27889393e-01,
        4.29631278e-01,
        4.31373140e-01,
        4.33114961e-01,
        4.34856726e-01,
        4.36598416e-01,
        4.38340016e-01,
        4.40081509e-01,
        4.41822878e-01,
        4.43564106e-01,
        4.45305176e-01,
        4.47046072e-01,
        4.48786776e-01,
        4.50527272e-01,
        4.52267543e-01,
        4.54007571e-01,
        4.55747340e-01,
        4.57486833e-01,
        4.59226034e-01,
        4.60964923e-01,
        4.62703486e-01,
        4.64441704e-01,
        4.66179561e-01,
        4.67917039e-01,
        4.69654122e-01,
        4.71390791e-01,
        4.73127029e-01,
        4.74862820e-01,
        4.76598146e-01,
        4.78332989e-01,
        4.80067332e-01,
        4.81801158e-01,
        4.83534448e-01,
        4.85267185e-01,
        4.86999352e-01,
        4.88730931e-01,
        4.90461903e-01,
        4.92192252e-01,
        4.93921959e-01,
        4.95651006e-01,
        4.97379375e-01,
        4.99107049e-01,
        5.00834008e-01,
        5.02560235e-01,
        5.04285711e-01,
        5.06010418e-01,
        5.07734338e-01,
        5.09457451e-01,
        5.11179741e-01,
        5.12901186e-01,
        5.14621770e-01,
        5.16341473e-01,
        5.18060276e-01,
        5.19778160e-01,
        5.21495106e-01,
        5.23211094e-01,
        5.24926107e-01,
        5.26640124e-01,
        5.28353125e-01,
        5.30065092e-01,
    ]
    return analytical_results[index]


def cantilever_subjected_to_a_transversal_load(n_elem=19):
    start = np.zeros((3,))
    direction = np.array([0.0, 1.0, 0.0])
    normal = np.array([0.0, 0.0, 1.0])
    radius = 1
    base_length = 0.25 * radius * np.pi
    base_radius = 0.01 / (
        np.pi ** (1 / 2)
    )  # The Cross-sectional area is 1e-4(we assume its equivalent to a square cross-sectional surface with same area)
    base_area = 1e-4
    density = 1000
    youngs_modulus = 1e9
    poisson_ratio = 0
    shear_modulus = youngs_modulus / (poisson_ratio + 1.0)

    class StretchingBeamSimulator(
        ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks
    ):
        pass

    stretch_sim = StretchingBeamSimulator()

    density = 1000
    t = np.linspace(0, 0.25 * np.pi, n_elem + 1)
    tmp = np.zeros((3, n_elem + 1), dtype=np.float64)
    tmp[0, :] = -radius * np.cos(t) + 1
    tmp[1, :] = radius * np.sin(t)
    tmp[2, :] *= 0.0
    dir = np.zeros((3, 3, n_elem), dtype=np.float64)
    tan = tmp[:, 1:] - tmp[:, :-1]
    tan = tan / np.linalg.norm(tan, axis=0)

    d1 = np.array([0.0, 0.0, 1.0]).reshape((3, 1))
    d2 = np.cross(tan, d1, axis=0)

    dir[0, :, :] = d1
    dir[1, :, :] = d2
    dir[2, :, :] = tan

    rod = ea.CosseratRod.straight_rod(
        n_elem,
        start,
        direction,
        normal,
        base_length,
        base_radius,
        density,
        youngs_modulus=youngs_modulus,
        shear_modulus=shear_modulus,
        position=tmp,
        directors=dir,
    )

    # Adjust the Cross Section
    adjust_section = adjust_square_cross_section(
        n_elem,
        direction,
        normal,
        base_length,
        base_radius,
        density,
        youngs_modulus=youngs_modulus,
        rod_origin_position=start,
        ring_rod_flag=False,
    )

    rod.mass_second_moment_of_inertia = adjust_section[0]
    rod.inv_mass_second_moment_of_inertia = adjust_section[1]
    rod.bend_matrix = adjust_section[2]

    stretch_sim.append(rod)

    # stretch_sim.finalize()
    rod.rest_kappa[...] = rod.kappa

    dl = base_length / n_elem
    dt = 0.01 * dl / 100

    stretch_sim.constrain(rod).using(
        OneEndFixedRod, constrained_position_idx=(0,), constrained_director_idx=(0,)
    )

    print("One end of the rod is now fixed in place")

    stretch_sim.dampen(rod).using(
        ea.AnalyticalLinearDamper,
        damping_constant=0.3,
        time_step=dt,
    )

    ramp_up_time = 1

    origin_force = np.array([0.0, 0.0, 0.0])
    end_force = np.array([0.0, 0.0, 6.0])

    stretch_sim.add_forcing_to(rod).using(
        EndpointForces, origin_force, end_force, ramp_up_time=ramp_up_time
    )
    print("Forces added to the rod")

    # Finalization and Run the Project
    final_time = 5
    total_steps = int(final_time / dt)
    print("Total steps to take", total_steps)

    stretch_sim.finalize()
    print("System finalized")

    # The simulation result from Project3.3.2 with 400 elements/ Tip position Z

    # generate analytical solution array from [400]

    analytical_results_sub = np.zeros(n_elem + 1)

    for i in range(n_elem + 1):
        analytical_results_converge_index = round((i * dl) / (base_length / 400))
        position_left = analytical_results(analytical_results_converge_index)
        analytical_results_sub[i] = position_left

    timestepper = PositionVerlet()

    integrate(timestepper, stretch_sim, final_time, total_steps)
    print(rod.position_collection[2, ...])

    error, l1, l2, linf = calculate_error_norm(
        analytical_results_sub,
        rod.position_collection[2, ...],
        n_elem,
    )

    return {"rod": rod, "error": error, "l1": l1, "l2": l2, "linf": linf}


# cantilever_subjected_to_a_transversal_load(630)


results = []
results.append(cantilever_subjected_to_a_transversal_load(25))

results.append(cantilever_subjected_to_a_transversal_load(26))


results.append(cantilever_subjected_to_a_transversal_load(27))


results.append(cantilever_subjected_to_a_transversal_load(28))
results.append(cantilever_subjected_to_a_transversal_load(29))

results.append(cantilever_subjected_to_a_transversal_load(30))
results.append(cantilever_subjected_to_a_transversal_load(40))

results.append(cantilever_subjected_to_a_transversal_load(50))
results.append(cantilever_subjected_to_a_transversal_load(60))
results.append(cantilever_subjected_to_a_transversal_load(70))
results.append(cantilever_subjected_to_a_transversal_load(80))
results.append(cantilever_subjected_to_a_transversal_load(90))

results.append(cantilever_subjected_to_a_transversal_load(100))
results.append(cantilever_subjected_to_a_transversal_load(200))
results.append(cantilever_subjected_to_a_transversal_load(420))

convergence_elements = [25, 26, 27, 28, 29, 30, 40, 50, 60, 70, 80, 90, 100, 200]

l1 = []
l2 = []
linf = []

for result in results:
    l1.append(result["l1"])
    l2.append(result["l2"])
    linf.append(result["linf"])


fig = plt.figure(figsize=(10, 8), frameon=True, dpi=150)
ax = fig.add_subplot(111)
ax.grid(which="minor", color="k", linestyle="--")
ax.grid(which="major", color="k", linestyle="-")
ax.set_xlabel("N_element")  # X-axis label
ax.set_ylabel("Error")  # Y-axis label
ax.set_title("Error Convergence Analysis")

ax.loglog(
    convergence_elements,
    l1,
    marker="o",
    ms=10,
    c=to_rgb("xkcd:bluish"),
    lw=2,
    label="l1",
)
ax.loglog(
    convergence_elements,
    l2,
    marker="o",
    ms=10,
    c=to_rgb("xkcd:reddish"),
    lw=2,
    label="l2",
)
ax.loglog(convergence_elements, linf, marker="o", ms=10, c="k", lw=2, label="linf")
fig.legend(prop={"size": 20})

fig.show()