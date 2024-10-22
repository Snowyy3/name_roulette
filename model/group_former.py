import random as rd

class GroupFormer:
    def __init__(self):
        pass

    def group_formation(self, names: list[str], group_size: int = None, num_groups: int = None):
        # names: list of names; group_size: number of people per group; num_groups: number of groups intended to form
        if not names:
            return [], [] 

        if group_size is None and num_groups is None:
            raise ValueError("Either 'group_size' or 'num_groups' must be provided.")
            # At least one value must be provided
        
        if num_groups is not None:  # If group number is provided
            group_size = len(names) // num_groups
            remaining_members = len(names) % num_groups
        else:  # If group size is provided
            num_groups = len(names) // group_size
            remaining_members = len(names) % group_size
        
        rd.shuffle(names)  # Shuffle the original list in case it is in alphabetical order

        groups = [names[i * group_size:(i + 1) * group_size] for i in range(num_groups)]
        # Create randomized groups. From the shuffled name list, slice it into smaller sublists
        
        remainder_list = names[num_groups * group_size:] if group_size else []
        # If cannot divide evenly -> create remainder list. If divide evenly -> empty list

        groups = [group if isinstance(group, list) else [group] for group in groups]

        if remainder_list:
            return groups, remainder_list
        else:
            return groups
            
    
    def handle_uneven_groups(self, groups, remaining_members, distribute_randomly=True):
        # 2 options: remaining members be in a separate group/distribute them randomly into generated groups
        if distribute_randomly:
            for member in remaining_members:
                rd.choice(groups).append(member)
        else:
            groups.append(remaining_members)
        
        return groups
    
    def manual_assignment(self, groups, assignments):
        for i, names in assignments.items():
            group_index = i-1
            # Check if group index exists
            if group_index < len(groups):
                if not isinstance(groups[group_index], list):
                    groups[group_index] = [groups[group_index]]
                groups[group_index].extend(names) 
            else:
                print(f"Group {i} does not exist")
        
        return groups
