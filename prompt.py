system_prompt_generate_analysis = """
    Please analyze the following Terms & Conditions document and return a single JSON object with scores and references. For each parameter, analyze the document and provide:

    A score from 1-5
    A brief explanation (max 150 characters)
    Specific clause references from the document
    Any concerning quotes from the text

    Return only a valid JSON object in this exact format:
    {
        "scores": {
            "data_collection": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "data_sharing": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "user_content_rights": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "account_control": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "privacy_controls": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "data_deletion": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "terms_changes": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "legal_rights": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "transparency": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            },
            "security_measures": {
                "score": 1-5,
                "explanation": "Brief explanation of the score",
                "clause_references": ["Section X.X", "Section Y.Y"],
                "concerning_quotes": ["Exact quote from document"]
            }
        },
        "metadata": {
            "total_score": 0-50,
            "percentage": 0-100,
            "risk_level": "Very High Risk|High Risk|Moderate Risk|Low Risk",
            "major_concerns": [
                "Brief description of major concern"
            ],
            "positive_aspects": [
                "Brief description of positive aspect"
            ]
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
    Risk Level Calculation:

    Very High Risk: <40%
    High Risk: 40-59%
    Moderate Risk: 60-79%
    Low Risk: ≥80%"""