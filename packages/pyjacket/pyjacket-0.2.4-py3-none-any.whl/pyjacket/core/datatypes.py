from collections import Counter

class CustomCounter(Counter):
    """Count how often something occurs in this dictionary
    
    Counts of 0 are deleted from the dict
    """
    def __setitem__(self, key, value: int):
        if value == 0:
            if key in self:
                del self[key]
        else:
            super().__setitem__(key, value)


if __name__ == '__main__':

    def main():
        # Example usage
        custom_counter = CustomCounter()
        custom_counter['apple'] = 3
        custom_counter['banana'] = 0

        print(custom_counter)  # Output: CustomCounter({'apple': 3, 'banana': 2})

        custom_counter['apple'] -= 1
        # custom_counter['banana'] -= 1

        print(custom_counter)  # Output: CustomCounter({'apple': 2})
        
    main()