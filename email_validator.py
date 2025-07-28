import re
import dns.resolver
from typing import Tuple, Dict

def validate_email(email: str) -> Tuple[bool, Dict[str, str]]:
    """
    Comprehensive email validation function
    
    Args:
        email (str): Email address to validate
        
    Returns:
        Tuple[bool, Dict[str, str]]: (is_valid, validation_details)
    """
    validation_results = {
        'format_valid': False,
        'domain_valid': False,
        'length_valid': False,
        'special_chars_valid': False,
        'errors': []
    }
    
    # Check if email is not empty
    if not email or not isinstance(email, str):
        validation_results['errors'].append("Email cannot be empty")
        return False, validation_results
    
    # Check length
    if len(email) > 254:  # RFC 5321 limit
        validation_results['errors'].append("Email too long (max 254 characters)")
    elif len(email) < 5:  # Minimum reasonable length
        validation_results['errors'].append("Email too short (min 5 characters)")
    else:
        validation_results['length_valid'] = True
    
    # Basic format validation using regex
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        validation_results['errors'].append("Invalid email format")
    else:
        validation_results['format_valid'] = True
    
    # Check for valid special characters
    invalid_chars = ['<', '>', '"', "'", '\\', '|', ';', ':', '/', '*', '?', '=']
    if any(char in email for char in invalid_chars):
        validation_results['errors'].append("Email contains invalid characters")
    else:
        validation_results['special_chars_valid'] = True
    
    # Extract domain for additional validation
    if '@' in email:
        domain = email.split('@')[1]
        
        # Check domain format
        domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(domain_pattern, domain):
            validation_results['domain_valid'] = True
        else:
            validation_results['errors'].append("Invalid domain format")
    
    # Determine overall validity
    is_valid = all([
        validation_results['format_valid'],
        validation_results['domain_valid'],
        validation_results['length_valid'],
        validation_results['special_chars_valid']
    ])
    
    return is_valid, validation_results

def validate_email_dns(email: str) -> bool:
    """
    Validate email domain using DNS lookup (optional advanced validation)
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if domain has valid MX records
    """
    try:
        domain = email.split('@')[1]
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
        return False
    except Exception:
        return False

# Example usage and testing
if __name__ == "__main__":
    test_emails = [
        "user@example.com",
        "invalid-email",
        "user@domain",
        "user@.com",
        "user@domain..com",
        "user name@domain.com",
        "user@domain.com",
        "very.long.email.address.that.exceeds.the.maximum.length.allowed.by.rfc.5321@very.long.domain.name.that.also.exceeds.the.maximum.length.allowed.by.rfc.5321.com",
        "user@domain.co.uk",
        "user+tag@domain.com",
        "user.name@domain.com"
    ]
    
    print("Email Validation Results:")
    print("=" * 50)
    
    for email in test_emails:
        is_valid, details = validate_email(email)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{email:<40} {status}")
        
        if not is_valid and details['errors']:
            for error in details['errors']:
                print(f"  └─ {error}")
        print() 