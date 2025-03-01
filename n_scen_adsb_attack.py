import os
import subprocess

# Function to execute the stat.py file
def execute_stat():
    print("Executing stat.py...")
    subprocess.run(["python", "n_scen_stat.py"])

# Function to execute different jammer files
def execute_jammer(jammer_file, attack_file):
    print(f"Executing {jammer_file}...")
    subprocess.run(["python", jammer_file])  # Running the jammer file
    print(f"Executing {attack_file}...")
    subprocess.run(["python", attack_file])  # Running the attack file
    execute_stat()  # Run the common stat.py file

# Function to execute the spoofer file and its respective attack file
def execute_spoofer(spoofer_file, attack_file):
    print(f"Executing {spoofer_file}...")
    subprocess.run(["python", spoofer_file])  # Running the spoofer file
    print(f"Executing {attack_file}...")
    subprocess.run(["python", attack_file])  # Running the attack file
    execute_stat()  # Run the common stat.py file

def main():
    print("Select the type of attack to execute:")
    print("1. Continuous Wave Jamming")
    print("2. Sweeping Jamming")
    print("3. Pulsed Noise Jamming")
    print("4. Directional Jamming")
    print("5. Spoofing Attack")

    choice = input("Enter your choice (1-5): ").strip()

    if choice == '1':
        execute_jammer("jammer_continuous_wave.py", "n_scen_adsb_attack_continuous_wave.py")
    elif choice == '2':
        execute_jammer("jammer_directional.py", "n_scen_adsb_attack_directional.py")
    elif choice == '3':
        execute_jammer("jammer_pulsed_noise.py", "n_scen_adsb_attack_pulsed_noise.py")
    elif choice == '4':
        execute_jammer("jammer_sweeping.py", "n_scen_adsb_attack_sweeping.py")
    elif choice == '5':
        execute_spoofer("spoofer.py", "n_scen_adsb_attack_spoofer.py")
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
