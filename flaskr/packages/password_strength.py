from zxcvbn import zxcvbn

def calculate_strength(password):
    """Function to calcualate the strength of the password submited"""

    # Calcualate
    results = zxcvbn(password)

    # Returm score
    return results['score']
