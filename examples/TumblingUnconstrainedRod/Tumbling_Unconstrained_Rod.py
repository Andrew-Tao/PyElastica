import elastica as ea

import numpy as np
from elastica.timestepper.symplectic_steppers import PositionVerlet
from elastica.timestepper import integrate
from elastica.external_forces import (
    EndPointTorque,
    EndpointForces_with_time_factor,
    EndPointTorque_with_time_factor,
)
from elastica.external_forces import UniformTorques
from Tumbling_Unconstrained_Rod_postprocessing import (
    plot_video_with_surface,
    adjust_parameter,
    lamda_t_function,
)
from matplotlib import pyplot as plt

n_elem = 256
start = np.array([0.0, 0.0, 8.0])
end = np.array([6.0, 0.0, 0.0])
direction = np.array([0.6, 0.0, -0.8])
normal = np.array([0.0, 1.0, 0.0])
base_length = 10

side_length = 0.01


base_radius = side_length / (np.pi ** (1 / 2))


density = 1e4
youngs_modulus = 1e7
poisson_ratio = 0
shear_modulus = youngs_modulus / (poisson_ratio + 1.0)


class NonConstrainRodSimulator(
    ea.BaseSystemCollection, ea.Constraints, ea.Forcing, ea.Damping, ea.CallBacks
):
    pass


sim = NonConstrainRodSimulator()

rod = ea.CosseratRod.straight_rod(
    n_elem,
    start,
    direction,
    normal,
    base_length,
    base_radius,
    density,
    youngs_modulus=youngs_modulus,
)

adjust_section = adjust_parameter(
    n_elem,
    direction,
    normal,
    base_length,
    side_length,
    base_radius,
    density,
    youngs_modulus=youngs_modulus,
    rod_origin_position=start,
    ring_rod_flag=False,
)

rod.mass_second_moment_of_inertia = adjust_section[0]
rod.inv_mass_second_moment_of_inertia = adjust_section[1]
rod.bend_matrix = adjust_section[2]

print("mass_second_moment_of_inertia=", rod.mass_second_moment_of_inertia)
print("bend_matrix=", rod.bend_matrix)

sim.append(rod)

dl = base_length / n_elem
dt = 0.01 * dl / 1

origin_force = np.array([0.0, 0.0, 0.0])
end_force = np.array([20.0, 0.0, 0.0])

sim.add_forcing_to(rod).using(
    EndpointForces_with_time_factor, origin_force, end_force, lamda_t_function
)


sim.add_forcing_to(rod).using(
    EndPointTorque_with_time_factor,
    1,
    lamda_t_function,
    direction=np.array([0.0, 200.0, -100.0]),
)

sim.dampen(rod).using(
    ea.AnalyticalLinearDamper,
    damping_constant=0.0,
    time_step=dt,
)

print("Forces added to the rod")

final_time = 20
total_steps = int(final_time / dt)

print("Total steps to take", total_steps)

rendering_fps = 30
step_skip = int(1.0 / (rendering_fps * dt))


class AxialStretchingCallBack(ea.CallBackBaseClass):
    def __init__(self, step_skip: int, callback_params: dict):
        ea.CallBackBaseClass.__init__(self)
        self.every = step_skip
        self.callback_params = callback_params

    def make_callback(self, system, time, current_step: int):
        if current_step % self.every == 0:
            self.callback_params["time"].append(time)
            self.callback_params["step"].append(current_step)
            self.callback_params["position"].append(system.position_collection.copy())
            self.callback_params["radius"].append(system.radius.copy())
            self.callback_params["velocity"].append(system.velocity_collection.copy())
            self.callback_params["avg_velocity"].append(
                system.compute_velocity_center_of_mass()
            )
            self.callback_params["center_of_mass"].append(
                system.compute_position_center_of_mass()
            )


recorded_history = ea.defaultdict(list)
sim.collect_diagnostics(rod).using(
    AxialStretchingCallBack, step_skip=step_skip, callback_params=recorded_history
)

sim.finalize()
print("System finalized")


timestepper = PositionVerlet()
integrate(timestepper, sim, final_time, total_steps)

time_analytic = [0.0, 2.0, 3.0, 3.8, 4.4, 5.0, 5.5, 5.8, 6.1, 6.5, 7.0]
mass_center_analytic = [
    [
        3.0,
        4.0667,
        6.5667,
        9.7304,
        12.5288,
        15.500,
        18.000,
        19.500,
        21.00,
        23.00,
        25.500,
    ],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
plt.plot(
    time_analytic,
    mass_center_analytic[0],
    marker="*",
    color="black",
    label="x_analytic",
)
plt.plot(
    time_analytic,
    mass_center_analytic[1],
    marker="*",
    color="black",
    label="y_analytic",
)
plt.plot(
    time_analytic,
    mass_center_analytic[2],
    marker="*",
    color="black",
    label="z_analytic",
)


mass_center = np.array(recorded_history["center_of_mass"])

plt.plot(recorded_history["time"][0:240], mass_center[:, 0][0:240], label="x")
plt.plot(recorded_history["time"][0:240], mass_center[:, 1][0:240], label="y")
plt.plot(recorded_history["time"][0:240], mass_center[:, 2][0:240], label="z")

plt.xlabel("Time/(second)")  # X-axis label
plt.ylabel("Center of mass")  # Y-axis label
plt.grid()
plt.legend()  # Optional: Add a grid
plt.show()


plot_video_with_surface(
    [recorded_history],
    video_name="Tumbling_Unconstrained_Rod.mp4",
    fps=rendering_fps,
    step=1,
    # The following parameters are optional
    x_limits=(0, 200),  # Set bounds on x-axis
    y_limits=(-4, 4),  # Set bounds on y-axis
    z_limits=(0.0, 8),  # Set bounds on z-axis
    dpi=100,  # Set the quality of the image
    vis3D=True,  # Turn on 3D visualization
    vis2D=False,  # Turn on projected (2D) visualization
)