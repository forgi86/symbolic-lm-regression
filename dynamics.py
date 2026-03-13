import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# ==================== PARAMETERS ====================
# Physical parameters - easily adjustable
m1 = 1.0      # mass of first pendulum (kg)
m2 = 1.0      # mass of second pendulum (kg)
l1 = 1.0      # length of first pendulum (m)
l2 = 1.0      # length of second pendulum (m)
g = 9.81      # gravitational acceleration (m/s^2)

# Simulation parameters
t_span = (0, 20)          # time span for simulation (s)
t_eval = np.linspace(0, 20, 1000)  # time points for output
initial_state = [np.pi/4, -np.pi/4, 0.5, -0.5]  # [theta1, theta2, omega1, omega2]


# ==================== STATE-SPACE MODEL ====================

def double_pendulum(t, x):
    """
    State-space model for non-linear double pendulum: dx/dt = f(x)
    
    State vector x = [theta1, theta2, omega1, omega2]
    where:
        theta1 = angle of first pendulum (rad)
        theta2 = angle of second pendulum (rad)
        omega1 = angular velocity of first pendulum (rad/s)
        omega2 = angular velocity of second pendulum (rad/s)
    
    Returns derivatives [dtheta1/dt, dtheta2/dt, domega1/dt, domega2/dt]
    """
    theta1, theta2, omega1, omega2 = x
    
    # Denominator term (common to both angular acceleration equations)
    denom = m2 * l2**2 + m1 * (l1**2 + l2**2 + 2 * l1 * l2 * np.cos(theta1 - theta2))
    
    # Numerator for first pendulum angular acceleration
    num1 = -m2 * g * l2 * np.sin(theta2) - m1 * g * (l1 * np.sin(theta1) 
             + l2 * np.sin(theta2) * np.cos(theta1 - theta2))
    
    # Numerator for second pendulum angular acceleration  
    num2 = (m1 + m2) * g * l1 * np.sin(theta1) - m2 * g * l2 * np.sin(theta2)
    
    # Angular accelerations
    alpha1 = num1 / denom
    alpha2 = num2 / denom
    
    # State derivatives
    dxdt = [omega1, omega2, alpha1, alpha2]
    
    return dxdt


# ==================== SIMULATION FUNCTION ====================

def simulate_double_pendulum():
    """
    Simulate the double pendulum system and plot results.
    """
    # Solve the differential equation
    sol = solve_ivp(double_pendulum, t_span, initial_state, 
                    t_eval=t_eval, method='RK45')
    
    # Extract state variables
    theta1 = sol.y[0]
    theta2 = sol.y[1]
    omega1 = sol.y[2]
    omega2 = sol.y[3]
    time = sol.t
    
    # Plot results
    plt.figure(figsize=(12, 8))
    
    # Plot angles vs time
    plt.subplot(2, 2, 1)
    plt.plot(time, theta1, label='theta1', linewidth=2)
    plt.plot(time, theta2, label='theta2', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (rad)')
    plt.title('Double Pendulum Angles vs Time')
    plt.legend()
    plt.grid(True)
    
    # Plot angular velocities vs time
    plt.subplot(2, 2, 2)
    plt.plot(time, omega1, label='omega1', linewidth=2)
    plt.plot(time, omega2, label='omega2', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (rad/s)')
    plt.title('Double Pendulum Angular Velocities vs Time')
    plt.legend()
    plt.grid(True)
    
    # Plot positions in phase space
    plt.subplot(2, 2, 3)
    plt.plot(theta1, theta2, linewidth=2)
    plt.xlabel('theta1 (rad)')
    plt.ylabel('theta2 (rad)')
    plt.title('Phase Space: theta2 vs theta1')
    plt.grid(True)
    
    # Plot energy (kinetic + potential)
    kinetic_energy = 0.5 * m1 * l1**2 * omega1**2 + 0.5 * m2 * (l1**2 * omega1**2 
                         + l2**2 * omega2**2 + 2 * l1 * l2 * omega1 * omega2 * np.cos(theta1 - theta2))
    potential_energy = -m1 * g * l1 * np.cos(theta1) - m2 * g * (l1 * np.cos(theta1) 
                         + l2 * np.cos(theta2))
    total_energy = kinetic_energy + potential_energy
    
    plt.subplot(2, 2, 4)
    plt.plot(time, total_energy, label='Total Energy', linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Energy (J)')
    plt.title('Total Energy vs Time')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return sol


# ==================== MAIN EXECUTION ====================

if __name__ == '__main__':
    print(f"Double Pendulum Simulation")
    print(f"Parameters:")
    print(f"  m1 = {m1} kg, m2 = {m2} kg")
    print(f"  l1 = {l1} m, l2 = {l2} m")
    print(f"  g = {g} m/s^2")
    print(f"Initial state: theta1={initial_state[0]:.3f}, "
          f"theta2={initial_state[1]:.3f}, "
          f"omega1={initial_state[2]:.3f}, omega2={initial_state[3]:.3f}")
    print(f"\nRunning simulation...")
    
    sol = simulate_double_pendulum()
    
    print(f"\nSimulation completed.")
    print(f"Final state: theta1={sol.y[0][-1]:.4f}, "
          f"theta2={sol.y[1][-1]:.4f}, "
          f"omega1={sol.y[2][-1]:.4f}, omega2={sol.y[3][-1]:.4f}")
