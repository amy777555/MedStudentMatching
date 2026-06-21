#Med Student Matching
# Amy Ward
# Brenden Toussant
# Jordan Reid
# Caleb Mickens


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
    


if __name__ == '__main__':

    file_name = 'sample_input.txt'
    
    hosp_dict, res_dict = parse_matching_data(file_name)
    
    if hosp_dict and res_dict:
        print("--- HOSPITALS ---")
        for h_name, data in hosp_dict.items():
            print(f"{h_name} (Slots: {data['slots']}): {data['preferences']}")
            
        print("\n--- RESIDENTS ---")
        for r_name, prefs in res_dict.items():
            print(f"{r_name}: {prefs}")

#Main method of the program
def main():
    print("Let's get to work.")

