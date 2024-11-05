class SFNSessionManager:
    _instance = None  # Private class variable to store the singleton instance
    
    def __new__(cls):
        # If instance doesn't exist, create it
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize the data dictionary only once
            cls._instance.data = {
                "suggestion_history": [],
                "current_suggestion_index": 0,
                "df": None,
                "suggestions": None,
                "category": None,
                "operation_stage": 'start',
                "category_identified": False,
                "category_confirmed": False,
                "applied_suggestions": set(),
                "identified_category": None,
                "show_category_selection": False
            }
        return cls._instance

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def clear(self):
        self.data.clear()