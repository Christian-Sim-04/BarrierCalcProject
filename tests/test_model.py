from barrier_calc import barrier_inputs, sliding_check

inputs = barrier_inputs(
    water_depth=0.6,
    mu_membrane_ground=0.33,  # cast concrete surface 
    mu_barrier_ground=0.72,  # cast concrete surface
    mu_kentledge_ground=0.40,  # cast concrete kentledge and surface
)

barrier_outputs = sliding_check(inputs)

print(f"Driving Force: {barrier_outputs.total_driving_force_kN:.3f} kN")
print(f"Total Resistance: {barrier_outputs.resisting_force_kN:.3f} kN")
print(f"Sliding Factor of Safety: {barrier_outputs.actual_fos:.3f}")
print(f"Sliding Check Passed: {barrier_outputs.passes}")
print(f"Required Kentledge Mass for Required FoS: {barrier_outputs.required_kentledge_mass_kg:.0f} kg")