def build_hospital_rankings(hospital_prefs):
    """
    convert whatever is in the prefernce list
    so something like...
    ['DARRIUS', 'JOSEPH', 'ARTHUR']

    turns into something like this...
    Hospital: {
        'DARRIUS': 0,
        'JOSEPH': 1,
        'ARTHUR': 2
    }
    """
    rankings = {} #empty dictionary

    for hospital, prefs in hospital_prefs.items():
        rankings[hospital] = {} #add to dictionary

        for rank, resident in enumerate(prefs):
            rankings[hospital][resident] = rank #assign rank to resident for each hospital

    return rankings


def build_resident_rankings(resident_prefs):
    rankings = {}

    for resident, prefs in resident_prefs.items():
        rankings[resident] = {}

        for rank, hospital in enumerate(prefs):
            rankings[resident][hospital] = rank

    return rankings


def get_resident_assignments(matching):

    #create matching dicitonary for hospital to residient for easier lookup, makes stability checking easier

    assignments = {}

    for hospital, residents in matching.items():
        for resident in residents:
            assignments[resident] = hospital

    return assignments


def check_stability(hospital_prefs, resident_prefs, matching):

    hospital_rank = build_hospital_rankings(hospital_prefs)
    resident_rank = build_resident_rankings(resident_prefs)

    resident_assignment = get_resident_assignments(matching)

    all_residents = set(resident_prefs.keys())

    assigned_residents = set(resident_assignment.keys())

    unassigned_residents = all_residents - assigned_residents

    print("Checking stability...\n")


    #TYPE 1 INSTABILITY
        #s -> h
        #s' -> null
        #h PREFERS s'>s

    for hospital, assigned_list in matching.items():

        for assigned_resident in assigned_list:

            for unassigned_resident in unassigned_residents:

                if unassigned_resident not in hospital_rank[hospital]:
                    continue

                if assigned_resident not in hospital_rank[hospital]:
                    continue

                if (
                    hospital_rank[hospital][unassigned_resident]
                    <
                    hospital_rank[hospital][assigned_resident]
                ):

                    print("TYPE 1 INSTABILITY FOUND") #print out if type 1 found and details of it below
                    print(f"Hospital: {hospital}")
                    print(f"Assigned Resident: {assigned_resident}")
                    print(f"Unassigned Resident: {unassigned_resident}")

                    return False


    #TYPE 2 INSTABILITY
        #s -> h
        #s' -> h'
        #BUT
        #h PREFERS s'> s
        #s' PREFERS h > h'


    for hospital in matching:

        assigned_here = matching[hospital]

        for resident_current in assigned_here:

            for resident_other, current_hospital in resident_assignment.items():

                if current_hospital == hospital:
                    continue

                if resident_other not in hospital_rank[hospital]:
                    continue

                if resident_current not in hospital_rank[hospital]:
                    continue

                hospital_prefers_other = (
                    hospital_rank[hospital][resident_other]
                    <
                    hospital_rank[hospital][resident_current]
                )

                if not hospital_prefers_other:
                    continue

                if hospital not in resident_rank[resident_other]:
                    continue

                if current_hospital not in resident_rank[resident_other]:
                    continue

                resident_prefers_hospital = (
                    resident_rank[resident_other][hospital]
                    <
                    resident_rank[resident_other][current_hospital]
                )

                if resident_prefers_hospital:

                    print("TYPE 2 INSTABILITY FOUND") #print out if type 2 found, with details of it below
                    print(f"Hospital: {hospital}")
                    print(f"Current Resident: {resident_current}")

                    print(
                        f"Resident: {resident_other}"
                    )

                    print(
                        f"Current Hospital: {current_hospital}"
                    )

                    return False
#if nothing returned false, the following prints
    print("No instabilities have been detected.")
    print("THE MATCHING IS STABLE")

    return True
