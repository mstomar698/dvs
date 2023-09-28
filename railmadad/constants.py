from django.db import OperationalError



train_types = (
    ("RNCC", "RNCC"),
    ("RGD", "RGD"),
    ("DNR", "DNR"),
    ("PNBE", "PNBE"),
    ("PPTA", "PPTA"),
    ("IPR", "IPR"),
    ("KEU", "KEU"),
    ("MKA", "MKA"),
    ("ARA", "ARA"),
)


department = (
    ("OBHS", "OBHS"),
    ("Electrical", "Electrical")
)

POSTS = (
    ("Moderator", "Moderator"),
    ("Railway Admin", "Railway Admin"),
    ("Normal User", "Normal User"),
    ("Superuser", "Superuser"),
)

TRAIN_CATS = ["all", "rncc", "rgd", "dnr",
              "pnbe", "ppta", "ipr", "keu", "mka", "ara"]
TRAIN_CATS.sort()             


SUB_TYPE_FOR_DISPOSAL_TIME = [
    'Lights', 'Air Conditioner', 'Fans', 'Charging Points']


COMPLAINS_TYPE = [
    "Coach - Cleanliness",
    "Water Availability",
    "Coach - Maintenance",
    "Bed Roll",
    "Electrical Equipment",
    "Security",
    "Staff Behaviour",
    "Miscellaneous",
    "Corruption Bribery",
    "Catering and Vending Services",
    "Punctuality",
    "Divyangjan Facilities",
    "Medical Assistance",
    "Facilities for Women with Special needs",
]
SUB_TYPES_DICT = {
    "Coach - Cleanliness": [
        "Toilets",
        "Others",
        "Coach Interior",
        "Washbasins",
        "Cockroach / Rodents",
        "Coach Exterior",
    ],
    "Water Availability": [
        "Others",
        "Packaged Drinking Water / Rail Neer",
        "Washbasin",
        "Toilet",
    ],
    "Coach - Maintenance": [
        "Broken/Missing Toilet Fittings",
        "Tap leaking/Tap not working",
        "Others",
        "Jerks/Abnormal Sound",
        "Window/Door locking problem",
        "Window/Seat Broken",
    ],
    "Bed Roll": [
        "Non Availability",
        "Others",
        "E-Bed Roll",
        "Dirty / Torn",
        "Over Charging",
    ],
    "Electrical Equipment": [
        "Lights",
        "Air Conditioner",
        "Fans",
        "Others",
        "Charging Points",
    ],
    "Security": [
        "Others",
        "Nuisance by Hawkers/Beggar/Eunuch/Passenger",
        "Harassment/Extortion by Security Personnel/Railway personnel",
        "Unauthorized person in Ladies/Disabled Coach/SLR/Reserve Coach",
    ],
    "Staff Behaviour": ["Staff Behaviour"],
    "Miscellaneous": ["Miscellaneous"],
    "Corruption Bribery": ["Corruption / Bribery"],
    "Catering and Vending Services": [
        "Others",
        "Food & Water Not Available",
        "Food Quality & Quantity",
        "Service Quality & Hygiene",
    ],
    "Punctuality": ["NTES APP", "Late Running"],
    "Divyangjan Facilities": [
        "Braille signage in coach",
        "Divyangjan coach unavailability",
        "Divyangjan toilet /washbasin",
    ],
    "Medical Assistance": ["Medical Assistance"],
    "Facilities for Women with Special needs": ["Baby Food"],
}


ALL_TYPES = [
    "Coach - Cleanliness",
    "Bed Roll",
    "Security",
    "Medical Assistance",
    "Punctuality",
    "Water Availability",
    "Electrical Equipment",
    "Coach - Maintenance",
    "Miscellaneous",
    "Staff Behaviour",
    "Corruption Bribery",
    "Catering and Vending Services",
    "Divyangjan Facilities",
    "Facilities for Women with Special needs",
]
CRITICAL_TYPES = [
    "Coach - Cleanliness",
    "Bed Roll",
    "Water Availability",
    "Electrical Equipment",
    "Coach - Maintenance",
]

IMPORTANT_SUBTYPE_CATS = [
    "Coach - Cleanliness",
    "Electrical Equipment",
    "Coach - Maintenance",
]

SUB_TYPES_COACH_CLEANLINESS = [
    "Toilets",
    "Others",
    "Coach Interior",
    "Washbasins",
    "Cockroach / Rodents",
    "Coach Exterior",
]

SUB_TYPES_COACH_MAINTAINANCE = [
    "Broken/Missing Toilet Fittings",
    "Tap leaking/Tap not working",
    "Others",
    "Jerks/Abnormal Sound",
    "Window/Door locking problem",
    "Window/Seat Broken",
]

SUB_TYPES_ELECTRICAL_EQUIPMENT = [
    "Lights",
    "Air Conditioner",
    "Fans",
    "Others",
    "Charging Points",
]


all_type = [
    "Coach - Cleanliness",
    "Bed Roll",
    "Security",
    "Punctuality",
    "Water Availability",
    "Electrical Equipment",
    "Medical Assistance",
    "Coach - Maintenance",
    "Miscellaneous",
    "Staff Behaviour",
    "Corruption Bribery",
    "Catering and Vending Services",
    "Divyangjan Facilities",
    "Facilities for Women with Special needs",
]

critical_type = [
    "Coach - Cleanliness",
    "Bed Roll",
    "Water Availability",
    "Electrical Equipment",
    "Coach - Maintenance",
]

color_code = [
    "#FF3838",
    "#FFB3B3",
    "#006441",
    "#FF8300",
    "#EEFF70",
    "#00FF83",
    "#00E8FF",
    "#4200FF",
    "#BD00FF",
    "#747474",
    "#1D0249",
    "#5F0037",
    "#D33737",
    "#00766B",
]


# Global variables
coach_clean = []
bed_roll = []
security = []
medical_assis = []
punctuality = []
water_avail = []
electrical_equip = []
coach_maintain = []
miscellaneous = []

# Global variables for new complaint types
Corruption_Bribery = []
Catering_and_Vending_Services = []
Divyangjan_Facilities = []
Facilities_for_Women_with_Special_needs = []

staff_behave = []
checked = []
check_type = []
complain_category = []
complain_type = []

# Global variables for train checkbox status
rncc = []
rgd = []
dnr = []
pnbe = []
ppta = []
ipr = []
keu = []
mka = []
ara = []
other = []

def update_global_variables():
    global coach_clean, bed_roll, security, medical_assis, punctuality, water_avail, electrical_equip, coach_maintain, miscellaneous
    global Corruption_Bribery, Catering_and_Vending_Services, Divyangjan_Facilities, Facilities_for_Women_with_Special_needs
    global staff_behave, checked, check_type, complain_category, complain_type
    global rncc, rgd, dnr, pnbe, ppta, ipr, keu, mka, ara, other

    # Clear the existing data in the variables
    coach_clean.clear()
    bed_roll.clear()
    security.clear()
    medical_assis.clear()
    punctuality.clear()
    water_avail.clear()
    electrical_equip.clear()
    coach_maintain.clear()
    miscellaneous.clear()

    Corruption_Bribery.clear()
    Catering_and_Vending_Services.clear()
    Divyangjan_Facilities.clear()
    Facilities_for_Women_with_Special_needs.clear()

    staff_behave.clear()
    checked.clear()
    check_type.clear()
    complain_category.clear()
    complain_type.clear()

    rncc.clear()
    rgd.clear()
    dnr.clear()
    pnbe.clear()
    ppta.clear()
    ipr.clear()
    keu.clear()
    mka.clear()
    ara.clear()
    other.clear()

    # Update the variables based on the new data
    try:
        from railmadad.models import Train_Type
        from railmadad.models import Main_Data_Upload

        train_type_rncc = Train_Type.objects.filter(Type="RNCC")
        train_type_rgd = Train_Type.objects.filter(Type="RGD")
        train_type_dnr = Train_Type.objects.filter(Type="DNR")
        train_type_pnbe = Train_Type.objects.filter(Type="PNBE")
        train_type_ppta = Train_Type.objects.filter(Type="PPTA")
        train_type_ipr = Train_Type.objects.filter(Type="IPR")
        train_type_keu = Train_Type.objects.filter(Type="KEU")
        train_type_mka = Train_Type.objects.filter(Type="MKA")
        train_type_ara = Train_Type.objects.filter(Type="ARA")

        assigned_trains = Train_Type.objects.all()
        trainsss = Main_Data_Upload.objects.all()
        main_trains = []
        for ttt in trainsss:
            main_trains.append(float(ttt.train_station))
        set_train = set(main_trains)
        main_train = list(set_train)

        # Update train checkbox status arrays
        for rncc_train in train_type_rncc:
            rncc.append(rncc_train.train_number)
        for rgd_train in train_type_rgd:
            rgd.append(rgd_train.train_number)

        for dnr_train in train_type_dnr:
            dnr.append(dnr_train.train_number)

        for pnbe_train in train_type_pnbe:
            pnbe.append(pnbe_train.train_number)

        for ppta_train in train_type_ppta:
            ppta.append(ppta_train.train_number)

        for ipr_train in train_type_ipr:
            ipr.append(ipr_train.train_number)

        for keu_train in train_type_keu:
            keu.append(keu_train.train_number)

        for mka_train in train_type_mka:
            mka.append(mka_train.train_number)

        for ara_train in train_type_ara:
            ara.append(ara_train.train_number)

        assigned_train_array = []
        for assigned_train_each in assigned_trains:
            assigned_train_array.append(assigned_train_each.train_number)

        for train in main_train:
            if train not in assigned_train_array:
                other.append(train)

        print("global variables updated")
        

    except OperationalError:
        pass
