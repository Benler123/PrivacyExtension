system_prompt_generate_analysis = """
    Analyze this Terms & Conditions document and return a single JSON object containing only scores and direct full-sentance quotes. 
    
    Return your analysis in this exact format:
    {
        "scores": {
            "account_control": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "data_collection": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "data_deletion": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "data_sharing": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "legal_rights": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "privacy_controls": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "security_measures": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "terms_changes": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "transparency": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            },
            "user_content_rights": {
                "quotes": [
                    "exact quote 1",
                    "exact quote 2"
                ],
                "score": 1-5
            }
        }, 
        "metadata": {
            "risk_percentage": 0-100,
            "risk_level": "Very High Risk|High Risk|Moderate Risk|Low Risk",
        }
    }
    
    Score each parameter based on these criteria:
    DATA COLLECTION (1-5):
    1: Excessive collection, no limits
    3: Moderate collection, some limits
    5: Minimal necessary collection
    DATA SHARING (1-5):
    1: Unrestricted sharing
    3: Limited sharing with named partners
    5: No sharing or explicit consent only
    USER CONTENT RIGHTS (1-5):
    1: Company claims full ownership
    3: Balanced rights with restrictions
    5: Users retain full rights
    ACCOUNT CONTROL (1-5):
    1: No control, arbitrary termination
    3: Basic control with restrictions
    5: Full control with clear processes
    PRIVACY CONTROLS (1-5):
    1: No privacy settings
    3: Basic controls available
    5: Comprehensive, accessible controls
    DATA DELETION (1-5):
    1: No deletion options
    3: Standard deletion with retention
    5: Complete deletion on demand
    TERMS CHANGES (1-5):
    1: No notice of changes
    3: Basic notification
    5: Advance notice with consent
    LEGAL RIGHTS (1-5):
    1: Extreme rights limitation
    3: Some rights limitations
    5: Full rights maintained
    TRANSPARENCY (1-5):
    1: Vague, confusing terms
    3: Moderately clear terms
    5: Crystal clear, plain language
    SECURITY MEASURES (1-5):
    1: No security specified
    3: Basic security described
    5: Comprehensive security with audits

    Important rules for quotes:

    Use full-sentences for quotes
    Include exact text from the document
    Focus on the most concerning/relevant parts
    Keep quotes concise but complete
    Include context when needed
    If a quote shows positive aspects, include it too
    Maximum 3 quotes per parameter
    Quotes should directly support the score given

    Risk Level Calculation:

    Very High Risk: <40%
    High Risk: 40-59%
    Moderate Risk: 60-79%
    Low Risk: ≥80%
    """