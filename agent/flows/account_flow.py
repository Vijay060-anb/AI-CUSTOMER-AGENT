from typing import Dict, Any


# ============================================================
# MOCK CUSTOMER DATABASE
# ============================================================

CUSTOMERS = {
    "C001": {
        "customer_id": "C001",
        "name": "Alex",
        "email": "alex@example.com",
        "password": "hashed_password",
        "active": True,
    },

    "C002": {
        "customer_id": "C002",
        "name": "Maria",
        "email": "maria@example.com",
        "password": "hashed_password",
        "active": True,
    },

    "C003": {
        "customer_id": "C003",
        "name": "John",
        "email": "john@example.com",
        "password": "hashed_password",
        "active": False,
    },
}


# ============================================================
# CREATE ACCOUNT
# ============================================================

def create_account(
    customer_id: str,
    name: str,
    email: str,
) -> Dict[str, Any]:
    """
    Create a new customer account.
    """

    if customer_id in CUSTOMERS:
        return {
            "success": False,
            "message": (
                f"Customer {customer_id} "
                "already exists."
            ),
        }

    CUSTOMERS[customer_id] = {
        "customer_id": customer_id,
        "name": name,
        "email": email,
        "password": "temporary_password",
        "active": True,
    }

    return {
        "success": True,
        "message": (
            f"Account for {name} "
            "has been created successfully."
        ),
        "customer_id": customer_id,
        "email": email,
    }


# ============================================================
# DELETE ACCOUNT
# ============================================================

def delete_account(
    customer_id: str,
) -> Dict[str, Any]:
    """
    Deactivate a customer account.
    """

    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "success": False,
            "message": (
                f"Customer {customer_id} "
                "was not found."
            ),
        }

    if not customer["active"]:
        return {
            "success": False,
            "message": (
                f"Account {customer_id} "
                "is already inactive."
            ),
        }

    customer["active"] = False

    return {
        "success": True,
        "message": (
            f"Account {customer_id} "
            "has been deleted successfully."
        ),
        "customer_id": customer_id,
    }


# ============================================================
# EDIT ACCOUNT
# ============================================================

def edit_account(
    customer_id: str,
    name: str = "",
    email: str = "",
) -> Dict[str, Any]:
    """
    Update customer account information.
    """

    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "success": False,
            "message": (
                f"Customer {customer_id} "
                "was not found."
            ),
        }

    if not customer["active"]:
        return {
            "success": False,
            "message": (
                f"Account {customer_id} "
                "is inactive."
            ),
        }

    if name:
        customer["name"] = name

    if email:
        customer["email"] = email

    return {
        "success": True,
        "message": (
            f"Account {customer_id} "
            "has been updated successfully."
        ),
        "customer": customer.copy(),
    }


# ============================================================
# RECOVER PASSWORD
# ============================================================

def recover_password(
    customer_id: str,
) -> Dict[str, Any]:
    """
    Start the password recovery process.
    """

    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "success": False,
            "message": (
                f"Customer {customer_id} "
                "was not found."
            ),
        }

    if not customer["active"]:
        return {
            "success": False,
            "message": (
                f"Account {customer_id} "
                "is inactive."
            ),
        }

    return {
        "success": True,
        "message": (
            f"Password recovery instructions "
            f"have been sent to {customer['email']}."
        ),
        "customer_id": customer_id,
    }


# ============================================================
# REGISTRATION PROBLEMS
# ============================================================

def registration_problems(
    email: str,
) -> Dict[str, Any]:
    """
    Diagnose a basic registration problem.
    """

    for customer in CUSTOMERS.values():

        if customer["email"].lower() == email.lower():

            return {
                "success": False,
                "message": (
                    "An account with this email "
                    "already exists. Please try "
                    "logging in instead."
                ),
            }

    return {
        "success": True,
        "message": (
            "No existing account was found with "
            "this email. You can proceed with "
            "registration."
        ),
    }


# ============================================================
# SWITCH ACCOUNT
# ============================================================

def switch_account(
    customer_id: str,
) -> Dict[str, Any]:
    """
    Simulate switching to another customer account.
    """

    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "success": False,
            "message": (
                f"Customer {customer_id} "
                "was not found."
            ),
        }

    if not customer["active"]:
        return {
            "success": False,
            "message": (
                f"Account {customer_id} "
                "is inactive."
            ),
        }

    return {
        "success": True,
        "message": (
            f"Successfully switched to "
            f"{customer['name']}'s account."
        ),
        "customer_id": customer_id,
    }


# ============================================================
# TEST ACCOUNT FLOW
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("ACCOUNT BUSINESS FLOW")
    print("========================================\n")

    # --------------------------------------------------------
    # TEST 1: CREATE ACCOUNT
    # --------------------------------------------------------

    print("TEST 1: Create account")

    result = create_account(
        customer_id="C004",
        name="Emma",
        email="emma@example.com",
    )

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 2: CREATE DUPLICATE ACCOUNT
    # --------------------------------------------------------

    print("TEST 2: Create duplicate account")

    result = create_account(
        customer_id="C001",
        name="Alex",
        email="alex@example.com",
    )

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 3: EDIT ACCOUNT
    # --------------------------------------------------------

    print("TEST 3: Edit account")

    result = edit_account(
        customer_id="C001",
        name="Alex Updated",
        email="alex.updated@example.com",
    )

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 4: PASSWORD RECOVERY
    # --------------------------------------------------------

    print("TEST 4: Recover password")

    result = recover_password(
        customer_id="C001"
    )

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 5: REGISTRATION PROBLEM
    # --------------------------------------------------------

    print("TEST 5: Registration problem")

    result = registration_problems(
        email="alex.updated@example.com"
    )

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 6: SWITCH ACCOUNT
    # --------------------------------------------------------

    print("TEST 6: Switch account")

    result = switch_account(
        customer_id="C002"
    )

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 7: DELETE ACCOUNT
    # --------------------------------------------------------

    print("TEST 7: Delete account")

    result = delete_account(
        customer_id="C004"
    )

    print(result["message"])

    print("-" * 60)

    # --------------------------------------------------------
    # TEST 8: DELETE UNKNOWN ACCOUNT
    # --------------------------------------------------------

    print("TEST 8: Delete unknown account")

    result = delete_account(
        customer_id="C999"
    )

    print(result["message"])

    print("-" * 60)