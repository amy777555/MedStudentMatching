# Med Student Matching
# Amy Ward
# Brenden Toussant
# Jordan Reid
# Caleb Mickens

from StabilityChecker import check_stability

def parse_matching_data(file_path):
    """
    Reads the (n + 1 + m) lines of input and returns two dictionaries:
    - hospitals: { 'Name': {'slots': int, 'preferences': [list]} }
    - residents: { 'Name': [list of preferred hospitals] }
    """
    hospitals = {}
    residents = {}
    
    # Flag to track whether we are currently reading hospitals or residents
    parsing_hospitals = True

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Remove leading/trailing whitespace and hidden newline characters
                line = line.strip()
                
                # The blank line signifies the switch from hospitals to residents
                if not line:
                    parsing_hospitals = False
                    continue
                
                # Split by comma and clean up any extra spaces around the names
                parts = [part.strip() for part in line.split(',')]
                
                if parsing_hospitals:
                    # Format: HOSPITAL_1, SLOTS, RESIDENT_a, ...
                    hospital_name = parts[0]
                    slots = int(parts[1])  # Must cast the slot count to an integer
                    preferences = parts[2:]
                    
                    hospitals[hospital_name] = {
                        'slots': slots,
                        'preferences': preferences
                    }
                else:
                    # Format: RESIDENT_1, HOSPITAL_x, HOSPITAL_y, ...
                    resident_name = parts[0]
                    preferences = parts[1:]
                    
                    residents[resident_name] = preferences

        return hospitals, residents

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return None, None

def modified_gale_shapley(hospitals, residents):
    """
    Modified Gale-Shapley algorithm for assigning residents to hospitals
    when hospitals may have more than one available slot, and when there
    are more residents than available slots.

    PSEUDOCODE:
    Start with all hospitals empty and all residents unmatched.
    While some hospital has an open slot and has not proposed to everyone:
        Have that hospital propose to the next resident on its list.
        If the resident does not rank that hospital, reject.
        If the resident is unmatched, assign them to the hospital.
        Otherwise, the resident keeps the hospital they prefer.
    Return the hospital assignments.
    """

    matches = {}
    resident_matches = {}
    next_proposal_index = {}

    # Initialize hospital matches and proposal positions
    for hospital in hospitals:
        matches[hospital] = []
        next_proposal_index[hospital] = 0

    # Initialize all residents as unmatched
    for resident in residents:
        resident_matches[resident] = None

    # Build resident ranking dictionaries
    resident_rankings = {}

    for resident, preference_list in residents.items():
        ranking = {}

        for index, hospital in enumerate(preference_list):
            ranking[hospital] = index

        resident_rankings[resident] = ranking

    while True:
        proposing_hospital = None

        # Find a hospital that still has open slots and someone left to propose to
        for hospital in hospitals:
            has_open_slot = len(matches[hospital]) < hospitals[hospital]['slots']
            has_residents_left = next_proposal_index[hospital] < len(hospitals[hospital]['preferences'])

            if has_open_slot and has_residents_left:
                proposing_hospital = hospital
                break

        # Stop when no hospital can make any more proposals
        if proposing_hospital is None:
            break

        hospital = proposing_hospital
        hospital_preferences = hospitals[hospital]["preferences"]

        resident = hospital_preferences[next_proposal_index[hospital]]
        next_proposal_index[hospital] += 1

        # Reject if this resident was listed by a hospital but not defined as a resident
        if resident not in residents:
            continue

        # Skip if the resident did not rank this hospital
        if hospital not in resident_rankings[resident]:
            continue

        current_hospital = resident_matches[resident]

        # Case 1: resident is unmatched
        if current_hospital is None:
            matches[hospital].append(resident)
            resident_matches[resident] = hospital

        # Case 2: resident is already matched, but may prefer another hospital
        else:
            current_rank = resident_rankings[resident][current_hospital]
            new_rank = resident_rankings[resident][hospital]

            if new_rank < current_rank:
                matches[current_hospital].remove(resident)
                matches[hospital].append(resident)
                resident_matches[resident] = hospital

    return matches

if __name__ == '__main__':

    file_name = 'sample_input.txt'

    hosp_dict, res_dict = parse_matching_data(file_name)

    if hosp_dict and res_dict:
        matches = modified_gale_shapley(hosp_dict, res_dict)

        hospital_prefs = {}
        for hospital, data in hosp_dict.items():
            hospital_prefs[hospital] = data["preferences"]

        is_stable = check_stability(hospital_prefs, res_dict, matches)

        if is_stable:
            print("\n--- FINAL MATCHES ---")
            for hospital, assigned_residents in matches.items():
                if assigned_residents:
                    print(hospital + ", " + ", ".join(assigned_residents))
                else:
                    print(hospital + ",")
        else:
            print("Matching is not stable.")
