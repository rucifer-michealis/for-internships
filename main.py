import json
import os
from datetime import datetime


# ============================================================
# CONSTANTS
# ============================================================

DATA_FILE = "food_donation_data.json"

AVAILABLE = "Available"
CLAIMED = "Claimed"
PICKED_UP = "Picked Up"
DELIVERED = "Delivered"


# ============================================================
# USER CLASS
# ============================================================

class User:

    def __init__(self, user_id, name, phone, location, role):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.location = location
        self.role = role

    def display(self):
        print(f"ID       : {self.user_id}")
        print(f"Name     : {self.name}")
        print(f"Phone    : {self.phone}")
        print(f"Location : {self.location}")
        print(f"Role     : {self.role}")


# ============================================================
# DONOR CLASS
# ============================================================

class Donor(User):

    def __init__(self, user_id, name, phone, location):
        super().__init__(
            user_id,
            name,
            phone,
            location,
            "Donor"
        )


# ============================================================
# VOLUNTEER CLASS
# ============================================================

class Volunteer(User):

    def __init__(self, user_id, name, phone, location):
        super().__init__(
            user_id,
            name,
            phone,
            location,
            "Volunteer"
        )


# ============================================================
# DONATION CLASS
# ============================================================

class Donation:

    def __init__(
        self,
        donation_id,
        donor_id,
        food_name,
        quantity,
        location,
        available_until,
        contact,
        status=AVAILABLE,
        volunteer_id=None
    ):

        self.donation_id = donation_id
        self.donor_id = donor_id
        self.food_name = food_name
        self.quantity = quantity
        self.location = location
        self.available_until = available_until
        self.contact = contact
        self.status = status
        self.volunteer_id = volunteer_id

    # --------------------------------------------------------
    # Display donation
    # --------------------------------------------------------

    def display(self):

        print("\n---------------------------")

        print("Donation ID :", self.donation_id)
        print("Food        :", self.food_name)
        print("Quantity    :", self.quantity)
        print("Location    :", self.location)
        print("Available   :", self.available_until)
        print("Contact     :", self.contact)
        print("Status      :", self.status)

        if self.volunteer_id:
            print(
                "Volunteer   :",
                self.volunteer_id
            )

    # --------------------------------------------------------
    # Claim donation
    # --------------------------------------------------------

    def claim(self, volunteer_id):

        if self.status != AVAILABLE:
            raise ValueError(
                "Only available donations "
                "can be claimed."
            )

        self.status = CLAIMED
        self.volunteer_id = volunteer_id

    # --------------------------------------------------------
    # Mark as picked up
    # --------------------------------------------------------

    def pickup(self, volunteer_id):

        if self.status != CLAIMED:
            raise ValueError(
                "Donation must be claimed "
                "before pickup."
            )

        if self.volunteer_id != volunteer_id:
            raise ValueError(
                "This donation is assigned "
                "to another volunteer."
            )

        self.status = PICKED_UP

    # --------------------------------------------------------
    # Mark as delivered
    # --------------------------------------------------------

    def deliver(self, volunteer_id):

        if self.status != PICKED_UP:
            raise ValueError(
                "Donation must be picked up "
                "before delivery."
            )

        if self.volunteer_id != volunteer_id:
            raise ValueError(
                "This donation is assigned "
                "to another volunteer."
            )

        self.status = DELIVERED


# ============================================================
# DONATION MANAGER
# ============================================================

class DonationManager:

    def __init__(self):
        self.donations = {}

    # --------------------------------------------------------
    # Generate donation ID
    # --------------------------------------------------------

    def generate_id(self):

        number = len(self.donations) + 1

        while True:

            donation_id = f"DON{number:03d}"

            if donation_id not in self.donations:
                return donation_id

            number += 1

    # --------------------------------------------------------
    # Create donation
    # --------------------------------------------------------

    def create_donation(
        self,
        donor,
        food_name,
        quantity,
        location,
        available_until,
        contact
    ):

        donation_id = self.generate_id()

        donation = Donation(
            donation_id,
            donor.user_id,
            food_name,
            quantity,
            location,
            available_until,
            contact
        )

        self.donations[donation_id] = donation

        return donation

    # --------------------------------------------------------
    # Get donation
    # --------------------------------------------------------

    def get_donation(self, donation_id):

        return self.donations.get(
            donation_id
        )

    # --------------------------------------------------------
    # View available donations
    # --------------------------------------------------------

    def get_available_donations(self):

        return [
            donation
            for donation in self.donations.values()
            if donation.status == AVAILABLE
        ]

    # --------------------------------------------------------
    # Display available donations
    # --------------------------------------------------------

    def display_available(self):

        donations = self.get_available_donations()

        print("\n================================")
        print("       AVAILABLE DONATIONS")
        print("================================")

        if not donations:

            print("No available donations.")
            return

        for donation in donations:
            donation.display()

    # --------------------------------------------------------
    # Display all donations
    # --------------------------------------------------------

    def display_all(self):

        if not self.donations:

            print("No donation records found.")
            return

        print("\n================================")
        print("         ALL DONATIONS")
        print("================================")

        for donation in self.donations.values():
            donation.display()


# ============================================================
# USER MANAGER
# ============================================================

class UserManager:

    def __init__(self):

        self.users = {}

    # --------------------------------------------------------
    # Add user
    # --------------------------------------------------------

    def add_user(self, user):

        if user.user_id in self.users:

            raise ValueError(
                "User ID already exists."
            )

        self.users[user.user_id] = user

    # --------------------------------------------------------
    # Get user
    # --------------------------------------------------------

    def get_user(self, user_id):

        return self.users.get(user_id)

    # --------------------------------------------------------
    # Get donor
    # --------------------------------------------------------

    def get_donor(self, user_id):

        user = self.get_user(user_id)

        if user and user.role == "Donor":
            return user

        return None

    # --------------------------------------------------------
    # Get volunteer
    # --------------------------------------------------------

    def get_volunteer(self, user_id):

        user = self.get_user(user_id)

        if user and user.role == "Volunteer":
            return user

        return None


# ============================================================
# FILE MANAGER
# ============================================================

class FileManager:

    @staticmethod
    def save(user_manager, donation_manager):

        data = {
            "users": [],
            "donations": []
        }

        # Save users
        for user in user_manager.users.values():

            data["users"].append({
                "user_id": user.user_id,
                "name": user.name,
                "phone": user.phone,
                "location": user.location,
                "role": user.role
            })

        # Save donations
        for donation in donation_manager.donations.values():

            data["donations"].append({
                "donation_id": donation.donation_id,
                "donor_id": donation.donor_id,
                "food_name": donation.food_name,
                "quantity": donation.quantity,
                "location": donation.location,
                "available_until": donation.available_until,
                "contact": donation.contact,
                "status": donation.status,
                "volunteer_id": donation.volunteer_id
            })

        try:

            with open(
                DATA_FILE,
                "w"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

            print("\nData saved successfully.")

        except IOError:

            print(
                "\nError: Could not save data."
            )

    @staticmethod
    def load(user_manager, donation_manager):

        if not os.path.exists(DATA_FILE):
            return

        try:

            with open(
                DATA_FILE,
                "r"
            ) as file:

                data = json.load(file)

            # Load users
            for item in data.get(
                "users",
                []
            ):

                if item["role"] == "Donor":

                    user = Donor(
                        item["user_id"],
                        item["name"],
                        item["phone"],
                        item["location"]
                    )

                else:

                    user = Volunteer(
                        item["user_id"],
                        item["name"],
                        item["phone"],
                        item["location"]
                    )

                user_manager.users[
                    user.user_id
                ] = user

            # Load donations
            for item in data.get(
                "donations",
                []
            ):

                donation = Donation(
                    item["donation_id"],
                    item["donor_id"],
                    item["food_name"],
                    item["quantity"],
                    item["location"],
                    item["available_until"],
                    item["contact"],
                    item["status"],
                    item["volunteer_id"]
                )

                donation_manager.donations[
                    donation.donation_id
                ] = donation

            print("Existing data loaded.")

        except (
            IOError,
            json.JSONDecodeError,
            KeyError
        ):

            print(
                "Error: Invalid or corrupted data file."
            )


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def get_required_input(message):

    while True:

        value = input(message).strip()

        if value:
            return value

        print(
            "Input cannot be empty. "
            "Please try again."
        )


def get_phone():

    while True:

        phone = input(
            "Phone: "
        ).strip()

        if phone.isdigit() and len(phone) >= 10:
            return phone

        print(
            "Invalid phone number."
        )


# ============================================================
# CREATE DONOR
# ============================================================

def create_donor(user_manager):

    print("\n========== CREATE DONOR ==========")

    user_id = get_required_input(
        "Donor ID: "
    )

    if user_manager.get_user(user_id):

        print(
            "Error: User ID already exists."
        )

        return

    name = get_required_input(
        "Name: "
    )

    phone = get_phone()

    location = get_required_input(
        "Location: "
    )

    donor = Donor(
        user_id,
        name,
        phone,
        location
    )

    try:

        user_manager.add_user(donor)

        print(
            "Donor created successfully."
        )

    except ValueError as error:

        print("Error:", error)


# ============================================================
# CREATE VOLUNTEER
# ============================================================

def create_volunteer(user_manager):

    print("\n========== CREATE VOLUNTEER ==========")

    user_id = get_required_input(
        "Volunteer ID: "
    )

    if user_manager.get_user(user_id):

        print(
            "Error: User ID already exists."
        )

        return

    name = get_required_input(
        "Name: "
    )

    phone = get_phone()

    location = get_required_input(
        "Location: "
    )

    volunteer = Volunteer(
        user_id,
        name,
        phone,
        location
    )

    try:

        user_manager.add_user(volunteer)

        print(
            "Volunteer created successfully."
        )

    except ValueError as error:

        print("Error:", error)


# ============================================================
# CREATE DONATION
# ============================================================

def create_donation(
    user_manager,
    donation_manager
):

    print("\n========== CREATE DONATION ==========")

    donor_id = get_required_input(
        "Donor ID: "
    )

    donor = user_manager.get_donor(
        donor_id
    )

    if donor is None:

        print(
            "Invalid donor ID."
        )

        return

    food_name = get_required_input(
        "Food Name: "
    )

    quantity = get_required_input(
        "Quantity: "
    )

    location = get_required_input(
        "Location: "
    )

    available_until = get_required_input(
        "Available Until: "
    )

    contact = get_required_input(
        "Contact Information: "
    )

    donation = donation_manager.create_donation(
        donor,
        food_name,
        quantity,
        location,
        available_until,
        contact
    )

    print(
        "\nDonation Created Successfully."
    )

    print(
        "Donation ID:",
        donation.donation_id
    )

    print(
        "Status:",
        donation.status
    )


# ============================================================
# CLAIM DONATION
# ============================================================

def claim_donation(
    user_manager,
    donation_manager
):

    print("\n========== CLAIM DONATION ==========")

    volunteer_id = get_required_input(
        "Volunteer ID: "
    )

    volunteer = user_manager.get_volunteer(
        volunteer_id
    )

    if volunteer is None:

        print(
            "Invalid volunteer ID."
        )

        return

    donation_id = get_required_input(
        "Donation ID: "
    )

    donation = donation_manager.get_donation(
        donation_id
    )

    if donation is None:

        print(
            "Donation not found."
        )

        return

    try:

        donation.claim(
            volunteer.user_id
        )

        print(
            f"\nDonation {donation_id}"
        )

        print(
            "Status:",
            donation.status
        )

        print(
            "Volunteer:",
            volunteer.user_id
        )

    except ValueError as error:

        print(
            "Error:",
            error
        )


# ============================================================
# PICK UP DONATION
# ============================================================

def pickup_donation(
    user_manager,
    donation_manager
):

    print("\n========== PICK UP DONATION ==========")

    volunteer_id = get_required_input(
        "Volunteer ID: "
    )

    volunteer = user_manager.get_volunteer(
        volunteer_id
    )

    if volunteer is None:

        print(
            "Invalid volunteer ID."
        )

        return

    donation_id = get_required_input(
        "Donation ID: "
    )

    donation = donation_manager.get_donation(
        donation_id
    )

    if donation is None:

        print(
            "Donation not found."
        )

        return

    try:

        donation.pickup(
            volunteer.user_id
        )

        print(
            f"Donation {donation_id}"
        )

        print(
            "Status:",
            donation.status
        )

    except ValueError as error:

        print(
            "Error:",
            error
        )


# ============================================================
# DELIVER DONATION
# ============================================================

def deliver_donation(
    user_manager,
    donation_manager
):

    print("\n========== DELIVER DONATION ==========")

    volunteer_id = get_required_input(
        "Volunteer ID: "
    )

    volunteer = user_manager.get_volunteer(
        volunteer_id
    )

    if volunteer is None:

        print(
            "Invalid volunteer ID."
        )

        return

    donation_id = get_required_input(
        "Donation ID: "
    )

    donation = donation_manager.get_donation(
        donation_id
    )

    if donation is None:

        print(
            "Donation not found."
        )

        return

    try:

        donation.deliver(
            volunteer.user_id
        )

        print(
            f"Donation {donation_id}"
        )

        print(
            "Status:",
            donation.status
        )

    except ValueError as error:

        print(
            "Error:",
            error
        )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    user_manager = UserManager()
    donation_manager = DonationManager()

    # Load previous records
    FileManager.load(
        user_manager,
        donation_manager
    )

    while True:

        print("\n")
        print("========================================")
        print("     FOOD DONATION MANAGEMENT SYSTEM")
        print("========================================")

        print("1. Create Donor")
        print("2. Create Volunteer")
        print("3. Create Donation")
        print("4. View Available Donations")
        print("5. View All Donations")
        print("6. Claim Donation")
        print("7. Mark Donation as Picked Up")
        print("8. Mark Donation as Delivered")
        print("9. Save Data")
        print("10. Exit")

        print("========================================")

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            create_donor(
                user_manager
            )

        elif choice == "2":

            create_volunteer(
                user_manager
            )

        elif choice == "3":

            create_donation(
                user_manager,
                donation_manager
            )

        elif choice == "4":

            donation_manager.display_available()

        elif choice == "5":

            donation_manager.display_all()

        elif choice == "6":

            claim_donation(
                user_manager,
                donation_manager
            )

        elif choice == "7":

            pickup_donation(
                user_manager,
                donation_manager
            )

        elif choice == "8":

            deliver_donation(
                user_manager,
                donation_manager
            )

        elif choice == "9":

            FileManager.save(
                user_manager,
                donation_manager
            )

        elif choice == "10":

            FileManager.save(
                user_manager,
                donation_manager
            )

            print(
                "Data saved successfully."
            )

            print(
                "Thank you. Goodbye!"
            )

            break

        else:

            print(
                "Invalid option. "
                "Please choose 1-10."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
