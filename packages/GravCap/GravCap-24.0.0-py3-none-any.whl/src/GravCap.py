import mendeleev

def get_atomic_weight(element):
    try:
        return mendeleev.element(element).atomic_weight
    except Exception as e:
        print(f"Error: {element} not recognized. {e}")
        exit()

def main():
    num_H2_molecules = int(input("Enter the number of H2 molecules on the substrate : "))
    num_elements = int(input("Enter the total number atomic species in your substrate (if your substrate include BO then total no. of species should be 2. please exclude H2 molecule here) : "))
    substrate_molar_mass = 0

    for i in range(num_elements):
        element = input(f"Enter atomic symbol for element {i+1}: ").capitalize()
        count = int(input(f"Enter number of atoms for {element}: "))
        atomic_weight = get_atomic_weight(element)
        element_molar_mass = count * atomic_weight
#        print(f"Molar mass contribution of {count} {element} atoms: {element_molar_mass:.2f} g/mol")
        substrate_molar_mass += element_molar_mass
    molar_mass_H2 = num_H2_molecules * (2 * get_atomic_weight('H'))
    molar_mass_total = substrate_molar_mass + molar_mass_H2
    wt_percent_H2 = (molar_mass_H2 / molar_mass_total) * 100
    print(f"\\nWeight percent of {num_H2_molecules} H2 molecules: {wt_percent_H2:.2f}%")

if __name__ == "__main__":
    main()
